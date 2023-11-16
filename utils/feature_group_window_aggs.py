def hops_feature_group_window_aggs (fs, window_aggs_df, window_len):

    window_aggs_fg = fs.get_or_create_feature_group(
        name=f"transactions_{window_len}_aggs_fraud_batch_fg",
        version=1,
        description=f"Aggregate transaction data over {window_len} windows.",
        primary_key=["cc_num"],
        event_time="datetime",
    )

    window_aggs_fg.insert(window_aggs_df)

    feature_descriptions = [
        {"name": "datetime", "description": "Transaction time"},
        {"name": "cc_num", "description": "Number of the credit card performing the transaction"},
        {"name": "loc_delta_mavg", "description": "Moving average of location difference between consecutive transactions from the same card"},
        {"name": "trans_freq", "description": "Moving average of transaction frequency from the same card"},
        {"name": "trans_volume_mavg", "description": "Moving average of transaction volume from the same card"},
        {"name": "trans_volume_mstd", "description": "Moving standard deviation of transaction volume from the same card"},
    ]

    for desc in feature_descriptions: 
        window_aggs_fg.update_feature_description(desc["name"], desc["description"])

    pass