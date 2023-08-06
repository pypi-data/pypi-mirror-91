"""Data ingress functions."""
import logging

import numpy as np
from pandas import DataFrame, isna, to_datetime

from vespr_model_deployment_utils.config import RowModification, SupportedDatetimeOutput, VarType

logger = logging.getLogger(__name__)


def transformed_ndarray_to_df(X, column_transformer, categorical_columns, continuous_columns):
    """
    Build dataframe from ndarray output of transformer.

    :param X: ndarray, output of transformer
    :param column_transformer: transformer object
    :param categorical_columns: list of columns
    :param continuous_columns: list of columns
    :return: df
    """
    columns = []
    for transformer in column_transformer.transformers_:
        if not transformer[0] == "drop_transformers":
            columns += transformer[2]
    df = DataFrame(data=X, columns=columns)
    df[categorical_columns] = df[categorical_columns].astype(str)
    df[continuous_columns] = df[continuous_columns].astype(float)
    return df


def drop_rows(df, column_info):
    """
    Drop missing samples.

    :param df: DataFrame: input dataframe - pandas
    :param column_info: DataFrame: column information related to df
    :return: df, DataFrame, input dataframe - pandas
    """
    logger.info("Dropping rows from dataset...")
    logger.info("Finding columns with DROP_ROW for missing data")
    drop_missing = column_info.loc[column_info["missing_value_action"] == RowModification.DROP.value]
    logger.info(f"Columns for processing missing_value_action = {drop_missing['name']}")

    for ft in drop_missing["name"]:
        issues = df[ft].isna()
        df = df.drop(df[issues].index, axis=0)

    logger.info("Finding columns with DROP_ROW for schema failure")
    drop_boundaries = column_info[(column_info["data_type"] == VarType.CONTINUOUS.value) & column_info["add_schema"]]
    logger.info(f"Columns for processing missing_value_action = {drop_boundaries['name']}")
    for i in drop_boundaries.index:
        ft = drop_boundaries["name"][i]
        schema_info = drop_boundaries["schema_info"][i]
        if schema_info["failure_action"] == RowModification.DROP.value:
            logger.info(
                f"Processing column {ft} with boundaries [{schema_info['min_value']}, {schema_info['max_value']}]"
            )
            issues = df.loc[
                ~df[ft].between(
                    schema_info["min_value"],
                    schema_info["max_value"],
                    inclusive=True,
                )
            ]
            df = df.drop(issues.index, axis=0)
    logger.info("Exiting row dropping")
    return df


def categorical_string_encoding(df, categorical_columns):
    """
    Encode strings as categorical features.

    :param df: DataFrame: input dataframe - pandas
    :param categorical_columns: list of categorical samples
    :return: dataframe
    """
    logger.info("Beginning string encoding of categorical features")
    for column in categorical_columns:
        df.loc[~df[column].isna(), column] = df.loc[~df[column].isna(), column].astype(str)
    logger.info("Completed...")
    return df


def construct_datetime_features(df, datetime_column_info):
    """
    Create datetime features.

    :param df: DataFrame: input dataframe - pandas
    :param datetime_column_info: DataFrame: column information related to df (datetime info only)
    :return: DataFrame
    """
    to_categorical = datetime_column_info[datetime_column_info["data_type"] == VarType.CATEGORICAL.value][
        "name"
    ].to_list()
    logger.info(f"Converting to categorical: {to_categorical}")
    to_continuous = datetime_column_info[datetime_column_info["data_type"] == VarType.CONTINUOUS.value][
        "name"
    ].to_list()
    logger.info(f"Converting to continuous: {to_continuous}")

    for idx, column in datetime_column_info.iterrows():
        datetime_info = column["datetime_schema_info"]
        column_name = column["name"]
        convert_to = datetime_info["convert_to"]
        datetime_format = datetime_info["datetime_format"]
        logger.info(f"Processing {column_name}")

        ts = to_datetime(df[column_name], errors="coerce", format=datetime_format)

        if column_name in to_categorical:
            assert len(convert_to) > 0, f"no output formats found for {column_name}"
            categorical_supported_datetime_output = [i.value for i in list(SupportedDatetimeOutput.Categorical)]
            assert all(
                [output_format in categorical_supported_datetime_output for output_format in convert_to]
            ), f"unsupported output_format found in {convert_to} for column: {column_name}, {[i.value for i in list(SupportedDatetimeOutput.Categorical)]}"

            for ct in convert_to:
                new_column_name = f"{column_name}_{ct}"

                if ct == SupportedDatetimeOutput.Categorical.DAY_OF_WEEK.value:
                    df[new_column_name] = [t.isoweekday() if not isna(t) else t for t in ts]

                if ct == SupportedDatetimeOutput.Categorical.DAY_OF_MONTH.value:
                    df[new_column_name] = [t.day if not isna(t) else t for t in ts]

                if ct == SupportedDatetimeOutput.Categorical.DAY_OF_YEAR.value:
                    df[new_column_name] = [t.timetuple().tm_yday if not isna(t) else t for t in ts]

                if (
                    ct == SupportedDatetimeOutput.Categorical.QUARTER_OF_YEAR.value
                    or ct == SupportedDatetimeOutput.Categorical.SEASON_OF_YEAR.value
                ):
                    quarter_of_year = lambda m: ((m % 12) // 3) + 1
                    df[new_column_name] = [quarter_of_year(t.month) if not isna(t) else t for t in ts]

                if ct == SupportedDatetimeOutput.Categorical.MONTH_OF_YEAR.value:
                    df[new_column_name] = [t.month if not isna(t) else None for t in ts]

                if ct == SupportedDatetimeOutput.Categorical.YEAR.value:
                    df[new_column_name] = [t.year if not isna(t) else None for t in ts]

        elif column_name in to_continuous:
            assert convert_to in [
                i.name for i in list(SupportedDatetimeOutput.Continuous)
            ], f"{convert_to} not supported"
            logger.info(f"Processing {column_name} as continuous")
            reference_point = to_datetime(
                datetime_info["reference_point"],
                errors="coerce",
                format=SupportedDatetimeOutput.CATEGORICAL_REFERENCE_FORMAT,
            )
            logger.info(f"References point:{reference_point}")
            new_column_name = f"{column_name}_{convert_to}_to_{reference_point.isoformat()}"
            df[new_column_name] = [
                (t.total_seconds() / SupportedDatetimeOutput.Continuous[convert_to].value[0])
                for t in (ts - reference_point)
            ]

        df = df.drop(column_name, axis=1)

    return df


def group_small(feat, min_samples, label="other"):
    """
    Group levels with fewer than min_samples.

    :param feat: DataSeries, single feature to be processed
    :param min_samples: int, min samples allowed per level
    :param label: string, new label for all rejected levels
    :return: feat: DataSeries, processed feature
    """
    logger.info(f"Applying groupings min_samples = {min_samples}...")
    elements, elements_counts = np.unique(feat, return_counts=True)
    low_count = np.where(elements_counts < min_samples)[0]
    values_to_replace = elements[low_count]
    idxs_to_replace = np.where(np.isin(feat, values_to_replace))[0]
    feat[idxs_to_replace] = label
    logger.info("Grouping complete...")
    return feat


def group_values(feat, groups):
    """
    Group values according to groups.

    :param feat: DataSeries, single feature to be processed
    :param groups: dict, levels to be grouped
    :return: feat: DataSeries, processed feature
    """
    logger.info("Applying value grouping...")
    for new_value, old_values in groups.items():
        idxs = np.where(np.isin(feat, old_values))[0]
        feat[idxs] = new_value
    logger.info("Grouping complete...")
    return feat


def categorical_frequency_imputer(x):
    """
    Imputes missing values using the most frequent feature in the column.

    designed as a speed up over sklearn's SimpleImputer(strategy="most_frequent")

    :param x: array-like x which needs to imputed
    :return x_copy: numpy.ndarray with missing values imputed
    """
    logger.info("Imputing  categorical feature...")
    x_copy = np.array(x)
    excluded = isna(x)
    logger.info(excluded.any())
    values, frequencies = np.unique(x_copy[~excluded], return_counts=True)
    most_frequent = values[np.argmax(frequencies)]
    x_copy[excluded] = most_frequent
    logger.info("Completed imputing")
    return x_copy


def clip_values(feat, min_value, max_value, method):
    """
    Clip continuous values.

    :param feat: DataSeries, single feature to be processed
    :param min_value: float, min value for clipping
    :param max_value: float, max value for clipping
    :param method: string, how to handle values outside range, [CLIP, FILL_MEAN, FILL_MEDIAN]
    :return: feat: DataSeries, processed feature
    """
    clip_top_idxs = np.where(feat > max_value)
    clip_bottom_idxs = np.where(feat < min_value)

    if method == "CLIP":
        feat[clip_top_idxs] = max_value
        feat[clip_bottom_idxs] = min_value
    else:
        fill_idxs = np.where(np.logical_and(feat >= min_value, feat <= max_value))[0]
        fill_value = np.mean(feat[fill_idxs]) if method == "FILL_MEAN" else np.median(feat[fill_idxs])
        fill_idxs = np.where(np.logical_or(feat < min_value, feat > max_value))[0]
        feat[fill_idxs] = fill_value
    return feat
