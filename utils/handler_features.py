def get_view (fs):

    trans_fg = fs.get_feature_group(name='transactions_fraud_batch_fg', version=1)
    window_aggs_fg = fs.get_feature_group(name='transactions_4h_aggs_fraud_batch_fg', version=1)

    query = trans_fg.select([
        "fraud_label",
        "category",
        "amount",
        "age_at_transaction",
        "days_until_card_expires",
        "loc_delta"
    ]).join(window_aggs_fg.select_except(["cc_num"]))

    # show few lines for quality control
    print(query.show(5))

    # load transformation functions
    label_encoder = fs.get_transformation_function(name="label_encoder")

    # map features to transformations.
    transformation_functions = {
        "category": label_encoder,
    }

    feature_view = fs.get_or_create_feature_view(
        name='transactions_view_fraud_batch_fv',
        version=1,
        query=query,
        labels=["fraud_label"],
        transformation_functions=transformation_functions,
    )

    return feature_view

def get_splits(feature_view, TEST_SIZE = 0.2):

    X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size = TEST_SIZE)

    X_train = X_train.sort_values("datetime")
    y_train = y_train.reindex(X_train.index)

    X_test = X_test.sort_values("datetime")
    y_test = y_test.reindex(X_test.index)

    X_train.drop(["datetime"], axis=1, inplace=True)
    X_test.drop(["datetime"], axis=1, inplace=True)

    y_train.value_counts(normalize=True)

    return X_train, X_test, y_train, y_test
