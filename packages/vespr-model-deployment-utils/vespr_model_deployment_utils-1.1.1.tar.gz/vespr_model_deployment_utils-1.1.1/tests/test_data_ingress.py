from itertools import combinations

import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer

from vespr_model_deployment_utils.config import RowModification, SupportedDatetimeOutput, VarType
from vespr_model_deployment_utils.data_ingress import (
    categorical_frequency_imputer,
    categorical_string_encoding,
    clip_values,
    construct_datetime_features,
    drop_rows,
    group_small,
    group_values,
    transformed_ndarray_to_df,
)


def all_len_combinations(a):
    """
    Construct a list of combinations for each subsequent slice of a list.

    :param a: list
    :return: list
    """
    b = []
    for i in range(1, len(a) + 1):
        b += [list(c) for c in combinations(a, i)]
    return b


datetime_categorical_combinations = [
    c for c in all_len_combinations([i.value for i in list(SupportedDatetimeOutput.Categorical)])
]


@pytest.mark.parametrize("convert_to", datetime_categorical_combinations)
def test_datetime_feature_construction_categorical(convert_to):
    df = {"test": pd.date_range(start="01/01/1970", end="01/01/1980", freq="M").astype(str).tolist()}
    df["test"][10] = "hello_world"
    df = pd.DataFrame(df)
    datetime_format = "%Y-%m-%d"
    column_info = pd.DataFrame(
        {
            "name": ["test"],
            "is_datetime": [True],
            "datetime_schema_info": [{"datetime_format": datetime_format, "convert_to": convert_to}],
            "data_type": [VarType.CATEGORICAL.value],
        }
    )

    solutions = dict()
    solutions["test_day_of_week"] = [
        6,
        6,
        2,
        4,
        7,
        2,
        5,
        1,
        3,
        6,
        1,
        4,
        7,
        7,
        3,
        5,
        1,
        3,
        6,
        2,
        4,
        7,
        2,
        5,
        1,
        2,
        5,
        7,
        3,
        5,
        1,
        4,
        6,
        2,
        4,
        7,
        3,
        3,
        6,
        1,
        4,
        6,
        2,
        5,
        7,
        3,
        5,
        1,
        4,
        4,
        7,
        2,
        5,
        7,
        3,
        6,
        1,
        4,
        6,
        2,
        5,
        5,
        1,
        3,
        6,
        1,
        4,
        7,
        2,
        5,
        7,
        3,
        6,
        7,
        3,
        5,
        1,
        3,
        6,
        2,
        4,
        7,
        2,
        5,
        1,
        1,
        4,
        6,
        2,
        4,
        7,
        3,
        5,
        1,
        3,
        6,
        2,
        2,
        5,
        7,
        3,
        5,
        1,
        4,
        6,
        2,
        4,
        7,
        3,
        3,
        6,
        1,
        4,
        6,
        2,
        5,
        7,
        3,
        5,
        1,
    ]

    solutions["test_day_of_month"] = (
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] * 2
        + [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        + [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] * 3
        + [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        + [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] * 3
    )

    solutions["test_day_of_year"] = [
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        60,
        91,
        121,
        152,
        182,
        213,
        244,
        274,
        305,
        335,
        366,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        60,
        91,
        121,
        152,
        182,
        213,
        244,
        274,
        305,
        335,
        366,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
        31,
        59,
        90,
        120,
        151,
        181,
        212,
        243,
        273,
        304,
        334,
        365,
    ]

    solutions["test_month_of_year"] = list(range(1, 13)) * 10
    solutions["test_season_of_year"] = ([1] * 2 + [2] * 3 + [3] * 3 + [4] * 3 + [1]) * 10
    solutions["test_quarter_of_year"] = ([1] * 2 + [2] * 3 + [3] * 3 + [4] * 3 + [1]) * 10
    solutions["test_year"] = []
    for i in range(10):
        solutions["test_year"] += [1970 + i] * 12

    for column in solutions:
        solutions[column][10] = None

    solutions = pd.DataFrame(solutions)
    df_dt = construct_datetime_features(df, column_info)

    assert "test" not in df_dt.columns, "test column was not dropped"
    for ct in convert_to:
        assert f"test_{ct}" in df_dt.columns.to_list(), f"test_{ct} was not constructed"
        assert np.all(
            np.equal(
                df_dt.loc[~df_dt[f"test_{ct}"].isna(), f"test_{ct}"].to_list(),
                solutions.loc[~df_dt[f"test_{ct}"].isna(), f"test_{ct}"].to_list(),
            )
        ), f"test_{ct} failed"
        assert (df_dt[f"test_{ct}"].isna() == solutions[f"test_{ct}"].isna()).all()


@pytest.mark.parametrize(
    "convert_to",
    {c.name: c.value for c in list(SupportedDatetimeOutput.Continuous)},
)
def test_datetime_feature_construction_continuous(convert_to):
    df = {
        "test": pd.date_range(
            start="01/01/1970",
            end="01/01/1980",
            freq="M",
        )
        .astype(str)
        .tolist()
    }
    df["test"][10] = "hello_world"
    df = pd.DataFrame(df)
    reference_point = "1970-01-01T00:00:00"
    datetime_format = "%Y-%m-%d"
    column_info = pd.DataFrame(
        {
            "name": ["test"],
            "is_datetime": [True],
            "datetime_schema_info": [
                {
                    "datetime_format": datetime_format,
                    "convert_to": convert_to,
                    "reference_point": reference_point,
                }
            ],
            "data_type": [VarType.CONTINUOUS.value],
        }
    )

    solutions = dict()

    solutions["seconds"] = np.array(
        [
            2592000,
            5011200,
            7689600,
            10281600,
            12960000,
            15552000,
            18230400,
            20908800,
            23500800,
            26179200,
            np.nan,
            31449600,
            34128000,
            36547200,
            39225600,
            41817600,
            44496000,
            47088000,
            49766400,
            52444800,
            55036800,
            57715200,
            60307200,
            62985600,
            65664000,
            68169600,
            70848000,
            73440000,
            76118400,
            78710400,
            81388800,
            84067200,
            86659200,
            89337600,
            91929600,
            94608000,
            97286400,
            99705600,
            102384000,
            104976000,
            107654400,
            110246400,
            112924800,
            115603200,
            118195200,
            120873600,
            123465600,
            126144000,
            128822400,
            131241600,
            133920000,
            136512000,
            139190400,
            141782400,
            144460800,
            147139200,
            149731200,
            152409600,
            155001600,
            157680000,
            160358400,
            162777600,
            165456000,
            168048000,
            170726400,
            173318400,
            175996800,
            178675200,
            181267200,
            183945600,
            186537600,
            189216000,
            191894400,
            194400000,
            197078400,
            199670400,
            202348800,
            204940800,
            207619200,
            210297600,
            212889600,
            215568000,
            218160000,
            220838400,
            223516800,
            225936000,
            228614400,
            231206400,
            233884800,
            236476800,
            239155200,
            241833600,
            244425600,
            247104000,
            249696000,
            252374400,
            255052800,
            257472000,
            260150400,
            262742400,
            265420800,
            268012800,
            270691200,
            273369600,
            275961600,
            278640000,
            281232000,
            283910400,
            286588800,
            289008000,
            291686400,
            294278400,
            296956800,
            299548800,
            302227200,
            304905600,
            307497600,
            310176000,
            312768000,
            315446400,
        ]
    )

    solutions["minutes"] = solutions["seconds"] / 60
    solutions["hours"] = solutions["minutes"] / 60
    solutions["days"] = solutions["hours"] / 24
    solutions["weeks"] = solutions["days"] / 7
    solutions["years"] = solutions["weeks"] / 52

    df_dt = construct_datetime_features(df, column_info)

    assert "test" not in df_dt.columns, "test column was not dropped"
    assert (
        f"test_{convert_to}_to_{reference_point}" in df_dt.columns.to_list()
    ), f"test_{convert_to}_to_{reference_point} was not constructed"
    assert np.all(
        np.abs(np.nan_to_num(df_dt[f"test_{convert_to}_to_{reference_point}"] - solutions[convert_to.lower()])) < 1e-8
    )


def test_drop_row_clipping():
    df = dict()
    df["feature_cont_drop_clip"] = list(range(-50, 50))
    df = pd.DataFrame(df)

    column_info = dict()
    column_info["name"] = ["feature_cont_drop_clip"]
    column_info["data_type"] = [VarType.CONTINUOUS.value]

    column_info["is_feature"] = [True]
    column_info["is_target"] = [False]
    column_info["is_protected"] = [False]
    column_info["drop"] = [False]
    column_info["add_schema"] = [True]
    column_info["schema_info"] = [
        {
            "min_value": -25,
            "max_value": 24,
            "failure_action": RowModification.DROP.value,
        }
    ]
    column_info["missing_value_action"] = ["FILL_MEAN"]
    column_info = pd.DataFrame(column_info)
    df = drop_rows(df, column_info)

    assert not any(np.isnan(df.to_numpy()))
    solutions = dict()
    solutions["feature_cont_drop_clip"] = list(range(-25, 25))
    assert all(df["feature_cont_drop_clip"] == solutions["feature_cont_drop_clip"])


def test_drop_row_missing():
    df = dict()

    df["feature_cat_fill_missing"] = ["a"] + (["b"] * 10) + ([np.nan] * 39) + (["d"] * 50)

    df["feature_cont_fill_missing"] = [np.nan] * 26 + list(range(-24, 25)) + [np.nan] * 25
    df = pd.DataFrame(df)

    column_info = dict()
    column_info["name"] = [
        "feature_cat_fill_missing",
        "feature_cont_fill_missing",
    ]
    column_info["data_type"] = [VarType.CATEGORICAL.value, VarType.CONTINUOUS.value]

    column_info["is_feature"] = [True, True]
    column_info["is_target"] = [False, False]
    column_info["is_protected"] = [False, False]
    column_info["drop"] = [False, False]
    column_info["add_schema"] = [False, False]
    column_info["schema_info"] = [
        {
            "min_samples": 1,
            "apply_groupings": True,
            "grouping_info": {"other": ["a", "b"]},
        },
        {"min_value": np.nan, "max_value": np.nan, "failure_action": None},
    ]
    column_info["missing_value_action"] = [
        RowModification.DROP.value,
        RowModification.DROP.value,
    ]
    column_info = pd.DataFrame(column_info)
    df = drop_rows(df, column_info)

    assert not df.isna().to_numpy().any()

    solutions = dict()
    solutions["feature_cat_fill_missing"] = ["d"] * 25
    solutions["feature_cont_fill_missing"] = list(range(25))

    assert all(df["feature_cat_fill_missing"] == solutions["feature_cat_fill_missing"])
    assert all(df["feature_cont_fill_missing"] == solutions["feature_cont_fill_missing"])


def test_categorical_string_encoding():
    df = pd.DataFrame(
        [
            {"A": 1, "B": 1.15, "C": "str1"},
            {"A": 2, "B": 12.12, "C": "str2"},
            {"A": 3, "B": 100.1, "C": "str3"},
        ]
    )
    categorical_columns = ["A", "C"]

    encoded_df = categorical_string_encoding(df, categorical_columns)
    for col in categorical_columns:
        for val in encoded_df[col].values:
            assert isinstance(val, str)


def test_categorical_frequency_imputer():
    x = [1, 1, np.nan, 2, 2, 1]
    x_filled = categorical_frequency_imputer(x)
    assert pd.isna(x_filled).sum() == 0

    x = [np.nan, "A", np.nan, "C", "D"]
    x_filled = categorical_frequency_imputer(x)
    assert pd.isna(x_filled).sum() == 0

    x = pd.Series(data=[20.9, np.nan, 1.21, 100.85, np.nan])
    x_filled = categorical_frequency_imputer(x)
    assert pd.isna(x_filled).sum() == 0


def test_group_values():
    x = np.array(["a"] + (["b"] * 10) + (["c"] * 39) + (["d"] * 50), dtype=object)
    x_solved = np.array((["other"] * 11) + (["c"] * 39) + (["d"] * 50), dtype=object)

    x_result = group_values(x, {"other": ["a", "b"]})
    assert all(x_result == x_solved)


@pytest.mark.parametrize("min_samples", [1, 10, 20, 50, 100])
def test_group_small(min_samples):
    x = np.array(["a"] + (["b"] * 10) + (["c"] * 39) + (["d"] * 50), dtype=object)

    solutions = dict()
    solutions[1] = ["a"] + (["b"] * 10) + (["c"] * 39) + (["d"] * 50)
    solutions[10] = ["other"] + (["b"] * 10) + (["c"] * 39) + (["d"] * 50)
    solutions[20] = (["other"] * 11) + (["c"] * 39) + (["d"] * 50)
    solutions[50] = (["other"] * 50) + (["d"] * 50)
    solutions[100] = ["other"] * 100

    x_grouped = group_small(x, min_samples=min_samples, label="other")
    assert all(x_grouped == solutions[min_samples])


@pytest.mark.parametrize("method", ["CLIP", "FILL_MEAN", "FILL_MEDIAN"])
def test_clip_values(method):
    x = np.array([1.0, 1.0, 1.0, 2.0, 3.0, 4.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 9.0, 9.0])

    min_value = 2
    max_value = 7

    solution = dict()
    solution["CLIP"] = np.array([2, 2, 2, 2, 3, 4, 4, 5, 6, 7, 7, 7, 7, 7])
    solution["FILL_MEAN"] = np.array(
        [
            (31 / 7),
            (31 / 7),
            (31 / 7),
            2,
            3,
            4,
            4,
            5,
            6,
            7,
            (31 / 7),
            (31 / 7),
            (31 / 7),
            (31 / 7),
        ]
    )
    solution["FILL_MEDIAN"] = np.array([4, 4, 4, 2, 3, 4, 4, 5, 6, 7, 4, 4, 4, 4])

    x_clipped = clip_values(x, min_value, max_value, method)
    assert all(x_clipped == solution[method])


def test_transformed_ndarray_to_df():
    data = pd.DataFrame(
        [
            {"A": 1, "B": 1.15, "C": "str1"},
            {"A": 2, "B": 12.12, "C": "str2"},
            {"A": 3, "B": 100.1, "C": "str3"},
        ]
    )
    categorical_columns = ["C"]
    continuous_columns = ["B"]

    column_transformer = ColumnTransformer(
        [
            ("drop_transformers", "drop", ["A"]),
            ("transformer1", "passthrough", ["B"]),
            ("transformer2", "passthrough", ["C"]),
        ]
    )
    X = column_transformer.fit_transform(data)

    df = transformed_ndarray_to_df(X, column_transformer, categorical_columns, continuous_columns)
    assert isinstance(df, pd.DataFrame)
    for c in ["B", "C"]:
        assert c in df.columns
