def hops_feature_group_trans (fs, trans_df):

    trans_fg = fs.get_or_create_feature_group(
        name="transactions_fraud_batch_fg",
        version=1,
        description="Transaction data",
        primary_key=["cc_num"],
        event_time="datetime",
    )

    trans_fg.insert(trans_df)

    feature_descriptions = [
        {"name": "tid", "description": "Transaction id"},
        {"name": "datetime", "description": "Transaction time"},
        {"name": "cc_num", "description": "Number of the credit card performing the transaction"},
        {"name": "category", "description": "Expense category"},
        {"name": "amount", "description": "Dollar amount of the transaction"},
        {"name": "latitude", "description": "Transaction location latitude"},
        {"name": "longitude", "description": "Transaction location longitude"},
        {"name": "city", "description": "City in which the transaction was made"},
        {"name": "country", "description": "Country in which the transaction was made"},
        {"name": "fraud_label", "description": "Whether the transaction was fraudulent or not"},
        {"name": "age_at_transaction", "description": "Age of the card holder when the transaction was made"},
        {"name": "days_until_card_expires", "description": "Card validity days left when the transaction was made"},
        {"name": "loc_delta", "description": "Haversine distance between this transaction location and the previous transaction location from the same card"},
    ]

    for desc in feature_descriptions: 
        trans_fg.update_feature_description(desc["name"], desc["description"])

    pass
