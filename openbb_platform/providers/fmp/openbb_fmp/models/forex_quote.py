"""FMP Forex Quote fetcher."""


from datetime import datetime
from typing import Any, Dict, Optional

from openbb_fmp.utils.helpers import get_data_one
from openbb_provider.abstract.fetcher import Fetcher
from openbb_provider.standard_models.forex_quote import (
    ForexQuoteData,
    ForexQuoteQueryParams,
)
from pydantic import field_validator


class FMPForexQuoteQueryParams(ForexQuoteQueryParams):
    """FMP Forex Quote Query.

    Source: https://site.financialmodelingprep.com/developer/docs#last-forex-quote
    """

    @field_validator("symbol", mode="before", check_fields=False)
    @classmethod
    def symbol_validate(cls, v):
        return v.replace("/", "") if "/" in v else v


class FMPForexQuoteData(ForexQuoteData):
    """FMP Forex Quote Data."""
    __alias_dict__ = {
        "ask_price": "ask",
        "bid_price": "bid",
        "date": "timestamp"
    }

    @field_validator("timestamp", mode="before", check_fields=False)
    @classmethod
    def date_validate(cls, v):  # pylint: disable=E0213
        """Return the date as a datetime object."""
        return datetime.fromtimestamp(v/1000)


class FMPForexQuoteFetcher(
    Fetcher[
        FMPForexQuoteQueryParams,
        FMPForexQuoteData,
    ]
):
    """Transform the query, extract and transform the data from the FMP endpoints."""
    @staticmethod
    def transform_query(params: Dict[str, Any]) -> FMPForexQuoteQueryParams:
        """Transform the query params."""
        return FMPForexQuoteQueryParams(**params)

    @staticmethod
    def extract_data(
        query: FMPForexQuoteQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> Dict:
        """Return the raw data from the FMP endpoint."""
        api_key = credentials.get("fmp_api_key") if credentials else ""

        base_url = "https://financialmodelingprep.com/api/v4"
        url = f"{base_url}/forex/last/{query.symbol}?apikey={api_key}"

        return get_data_one(url, **kwargs)

    @staticmethod
    def transform_data(
        query: FMPForexQuoteQueryParams, data: Dict, **kwargs: Any
    ) -> FMPForexQuoteData:
        """Return the transformed data."""
        return FMPForexQuoteData.model_validate(data)
