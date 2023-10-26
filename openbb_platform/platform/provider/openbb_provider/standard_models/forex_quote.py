"""Forex Quote Data Model."""

from datetime import datetime
from typing import List, Set, Union

from pydantic import Field, field_validator

from openbb_provider.abstract.data import Data
from openbb_provider.abstract.query_params import QueryParams
from openbb_provider.utils.descriptions import DATA_DESCRIPTIONS, QUERY_DESCRIPTIONS


class ForexQuoteQueryParams(QueryParams):
    """Forex Quote Query Model."""

    symbol: str = Field(
        description=QUERY_DESCRIPTIONS.get("symbol", "")
        + " Accepted formats are CURR1CURR2 and CURR1/CURR2."
    )

    @field_validator("symbol", mode="before", check_fields=False)
    @classmethod
    def upper_symbol(cls, v: Union[str, List[str], Set[str]]):
        """Convert symbol to uppercase."""
        if isinstance(v, str):
            return v.upper()
        return ",".join([symbol.upper() for symbol in list(v)])


class ForexQuoteData(Data):
    """Forex Quote Data."""

    symbol: str = Field(description=DATA_DESCRIPTIONS.get("symbol", ""))
    ask_price: float = Field(description="Latest ask price for the currency pair.")
    bid_price: float = Field(description="Latest bid price for the currency pair.")
    date: datetime = Field(description=DATA_DESCRIPTIONS.get("date", ""))
