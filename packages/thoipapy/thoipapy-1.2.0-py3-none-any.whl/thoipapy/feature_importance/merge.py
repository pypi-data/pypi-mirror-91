from ast import literal_eval
from pathlib import Path
from typing import List, Set

import pandas as pd

from thoipapy.utils import reorder_dataframe_columns, make_sure_path_exists


def merge_top_features_anova_ensemble(s, logging):
    logging.info('starting merge_top_features_anova_ensemble')
    # inputs
    train_data_excl_duplicates_csv = Path(s["data_dir"]) / f"results/{s['setname']}/train_data/02_train_data_excl_duplicates.csv"
    top_features_anova_csv = Path(s["data_dir"]) / f"results/{s['setname']}/feat_imp/top_features_anova.csv"
    top_features_rfe_csv = Path(s["data_dir"]) / f"results/{s['setname']}/feat_imp/top_features_rfe.csv"
    # outputs
    train_data_after_first_feature_seln_csv = Path(s["data_dir"]) / f"results/{s['setname']}/train_data/03_train_data_after_first_feature_seln.csv"

    make_sure_path_exists(train_data_after_first_feature_seln_csv, isfile=True)

    anova_ser = pd.read_csv(top_features_anova_csv, index_col=0).iloc[:, 0]
    df_rfe = pd.read_csv(top_features_rfe_csv, index_col=0)
    features_to_be_retained_during_selection = s['features_to_be_retained_during_selection'].split(",")

    anova_top_features: List[str] = literal_eval(anova_ser["top_features"])
    rfe_top_features: List[str] = df_rfe.loc[df_rfe["ranking"] == 1]["features"].to_list()

    combined_top_features: List[str] = list(set(anova_top_features + rfe_top_features + features_to_be_retained_during_selection))
    n_combined_top_features: int = len(combined_top_features)
    features_in_anova_but_not_ensemble_rfe: Set[str] = set(anova_top_features) - set(rfe_top_features)
    features_in_ensemble_rfe_but_not_anova: Set[str] = set(rfe_top_features) - set(anova_top_features)

    df_train_data_excl_duplicates = pd.read_csv(train_data_excl_duplicates_csv, index_col=0)
    combined_top_features_incl_y: List[str] = [s["bind_column"]] + combined_top_features
    n_dropped_features: int = df_train_data_excl_duplicates.shape[1] - n_combined_top_features

    logging.info(f"n_combined_top_features : {n_combined_top_features}")
    logging.info(f"combined_top_features : {combined_top_features}")
    logging.info(f"features_in_anova_but_not_ensemble_rfe : {features_in_anova_but_not_ensemble_rfe}")
    logging.info(f"features_in_ensemble_rfe_but_not_anova : {features_in_ensemble_rfe_but_not_anova}")
    logging.info(f"n_dropped_features : {n_dropped_features}")
    logging.info(f"total number of retained features : {len(combined_top_features)}")

    for column_name in combined_top_features_incl_y:
        if column_name not in df_train_data_excl_duplicates.columns:
            raise Exception(f"df_train_data_excl_duplicates does not contain {column_name}")

    df_train_data_excl_dup_top_feat = df_train_data_excl_duplicates.reindex(columns=combined_top_features_incl_y, index=df_train_data_excl_duplicates.index)
    df_train_data_excl_dup_top_feat.to_csv(train_data_after_first_feature_seln_csv)

    logging.info('finished merge_top_features_anova_ensemble')
