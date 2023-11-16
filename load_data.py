import os

print("⚙️ Downloading data...")
os.system('mkdir data')
os.system('cd data && wget -N https://repo.hops.works/master/hopsworks-tutorials/data/card_fraud_data/credit_cards.csv')
os.system('cd data && wget -N https://repo.hops.works/master/hopsworks-tutorials/data/card_fraud_data/profiles.csv')
os.system('cd data && wget -N https://repo.hops.works/master/hopsworks-tutorials/data/card_fraud_data/transactions.csv')
print("Done!")
