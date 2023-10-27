"""Alpha Vantage Forex Quote fetcher."""


from datetime import datetime
from typing import Any, Dict, Optional

from openbb_alpha_vantage.utils.helpers import extract_key_name, get_data_one
from openbb_provider.abstract.fetcher import Fetcher
from openbb_provider.standard_models.forex_quote import (
    ForexQuoteData,
    ForexQuoteQueryParams,
)
from pydantic import (
    Field,
    PrivateAttr,
    model_validator,
)


class AVForexQuoteQueryParams(ForexQuoteQueryParams):
    """Alpha Vantage Forex Quote Query.

    Source: https://www.alphavantage.co/documentation/#currency-exchange
    """

    _from_currency: str = PrivateAttr(default=None)
    _to_currency: str = PrivateAttr(default=None)
    _function: str = PrivateAttr(default="CURRENCY_EXCHANGE_RATE")

    @model_validator(mode="after")
    @classmethod
    def get_input_value(cls, values: "AVForexQuoteQueryParams"):
        """Extract from_currency and to_currency inputs from the symbol for the Alpha Vantage API."""

        if '/' in values.symbol:
            values._from_currency, values._to_currency = values.symbol.split("/")
        else:
            values._from_currency, values._to_currency = values.symbol[:3], values.symbol[3:]

        return values


class AVForexQuoteData(ForexQuoteData):
    """Alpha Vantage Forex Quote Data."""

    __alias_dict__ = {
        "date": "Last Refreshed",
        "ask_price": "Ask Price",
        "bid_price": "Bid Price",
    }

    from_currency_code: str = Field(
        alias="From_Currency Code",
        description="The currency code for the base currency.",
    )
    from_currency_name: str = Field(
        alias="From_Currency Name",
        description="The currency name for the base currency.",
    )
    to_currency_code: str = Field(
        alias="To_Currency Code",
        description="The currency code for the quote currency.",
    )
    to_currency_name: str = Field(
        alias="To_Currency Name",
        description="The currency name for the quote currency.",
    )
    exchange_rate: float = Field(
        alias="Exchange Rate",
        description="The exchange rate between the two currencies.",
    )
    time_zone: str = Field(
        alias="Time Zone",
        description="The time zone of the exchange rate.",
    )


class AVForexQuoteFetcher(
    Fetcher[
        AVForexQuoteQueryParams,
        AVForexQuoteData,
    ]
):
    """Transform the query, extract and transform the data from the Alpha Vantage endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AVForexQuoteQueryParams:
        """Transform the query."""
        return AVForexQuoteQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AVForexQuoteQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> Dict:
        """Return the raw data from the Alpha Vantage endpoint."""
        api_key = credentials.get("alpha_vantage_api_key") if credentials else ""

        query_str = (
            f"function={query._function}"
            f"&from_currency={query._from_currency}"
            f"&to_currency={query._to_currency}"
        )
        url = f"https://www.alphavantage.co/query?{query_str}&apikey={api_key}"

        return get_data_one(url, **kwargs).get("Realtime Currency Exchange Rate", "")

    @staticmethod
    def transform_data(
        query: AVForexQuoteQueryParams, data: Dict, **kwargs: Any
    ) -> AVForexQuoteData:
        """Transform the data to the standard format."""
        data = {
            extract_key_name(field): value
            for field, value in data.items()
        }
        data["symbol"] = query.symbol
        return AVForexQuoteData.model_validate(data)
