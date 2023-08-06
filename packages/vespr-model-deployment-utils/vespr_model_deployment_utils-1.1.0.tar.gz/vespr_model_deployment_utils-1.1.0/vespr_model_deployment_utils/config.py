"""Enums and constants used to integrate with VESPR."""
from enum import Enum


class SupportedDatetimeOutput:
    """Class to hold supported datetime formats."""

    CATEGORICAL_REFERENCE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    class Categorical(Enum):
        """Supported Categorical Datetime formats."""

        DAY_OF_WEEK = "day_of_week"
        DAY_OF_MONTH = "day_of_month"
        DAY_OF_YEAR = "day_of_year"
        SEASON_OF_YEAR = "season_of_year"
        QUARTER_OF_YEAR = "quarter_of_year"
        MONTH_OF_YEAR = "month_of_year"
        YEAR = "year"

    class Continuous(Enum):
        """Supported Continuous Datetime formats."""

        SECONDS = (1,)
        MINUTES = (60,)
        HOURS = (3600,)
        DAYS = (86400,)
        WEEKS = (604800,)
        YEARS = (31449600,)


class RowModification(Enum):
    """Supported row modifications for pre-processing."""

    DROP = "DROP_ROW"


class VarType(Enum):
    """Supported variable types."""

    CATEGORICAL = "categorical"
    CONTINUOUS = "continuous"
