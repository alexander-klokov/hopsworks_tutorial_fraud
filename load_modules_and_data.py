import os

path_to_modules = 'https://raw.githubusercontent.com/logicalclocks/hopsworks-tutorials/master/fraud_batch/features'
path_to_data = 'https://repo.hops.works/master/hopsworks-tutorials/data/card_fraud_data'

# load modules

print("⚙️ Downloading modules...")

if not os.path.isdir('features'):
    os.mkdir('features')
os.system(f'cd features && wget -N {path_to_modules}/transactions_fraud.py')
os.system(f'cd features && wget -N {path_to_modules}/window_aggs.py')

print('✅ done: modules\n')

# load data

print("⚙️ Downloading data...")

if not os.path.isdir('data'):
    os.mkdir('data')
os.system(f'cd data && wget -N {path_to_data}/credit_cards.csv')
os.system(f'cd data && wget -N {path_to_data}/profiles.csv')
os.system(f'cd data && wget -N {path_to_data}/transactions.csv')

print('✅ done: data\n')
