from math import radians

import pandas as pd
import numpy as np

import hopsworks

from features import transactions_fraud, window_aggs
from utils import feature_group_transactions, feature_group_window_aggs

import warnings

# mute warnings
warnings.filterwarnings("ignore")


# read data
path_to_data = './data/'

credit_cards_df = pd.read_csv(path_to_data + "credit_cards.csv")
profiles_df = pd.read_csv(path_to_data + "profiles.csv", parse_dates=["birthdate"])
trans_df = pd.read_csv(path_to_data + "transactions.csv", parse_dates=["datetime"])


# df trans: age at transaction, days until card expires
trans_df = transactions_fraud.get_age_at_transaction(trans_df, profiles_df)
trans_df = transactions_fraud.get_days_until_card_expires(trans_df, credit_cards_df)

trans_df = trans_df.drop_duplicates(["datetime"])
trans_df.sort_values("datetime", inplace=True)
trans_df[["longitude", "latitude"]] = trans_df[["longitude", "latitude"]].applymap(radians)
trans_df["loc_delta"] = trans_df.groupby("cc_num")\
    .apply(lambda x : transactions_fraud.haversine(x["longitude"], x["latitude"]))\
    .reset_index(level=0, drop=True)\
    .fillna(0)

# df aggregate transaction over windows
window_len = "4h"

window_aggs_df = window_aggs.get_window_aggs_df(window_len, trans_df)
window_aggs_df.tail()

trans_df.datetime = trans_df.datetime.values.astype(np.int64) // 10 ** 6
window_aggs_df.datetime = window_aggs_df.datetime.values.astype(np.int64) // 10 ** 6

# Make and upload the features
project = hopsworks.login()

fs = project.get_feature_store()

feature_group_transactions.hops_feature_group_trans(fs, trans_df)
feature_group_window_aggs.hops_feature_group_window_aggs(fs, window_aggs_df, window_len)
