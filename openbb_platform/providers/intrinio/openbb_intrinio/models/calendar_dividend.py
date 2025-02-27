"""Intrinio Dividend Calendar Model."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from dateutil.relativedelta import relativedelta
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.calendar_dividend import (
    CalendarDividendData,
    CalendarDividendQueryParams,
)
from openbb_core.provider.utils.descriptions import QUERY_DESCRIPTIONS
from openbb_core.provider.utils.helpers import get_querystring
from openbb_intrinio.utils.helpers import get_data_many
from pydantic import Field


class IntrinioCalendarDividendQueryParams(CalendarDividendQueryParams):
    """Intrinio Dividend Calendar Query.

    Source: https://docs.intrinio.com/documentation/web_api/get_security_stock_price_adjustments_v2
    """

    symbol: str = Field(description=QUERY_DESCRIPTIONS.get("symbol", ""))
    limit: Optional[int] = Field(
        default=100,
        description=QUERY_DESCRIPTIONS.get("limit", ""),
        alias="page_size",
    )


class IntrinioCalendarDividendData(CalendarDividendData):
    """Intrinio Dividend Calendar Data."""

    __alias_dict__ = {
        "amount": "dividend",
    }

    factor: float = Field(
        description=(
            "factor by which to multiply stock prices before this date, "
            "in order to calculate historically-adjusted stock prices."
        ),
    )
    dividend_currency: Optional[str] = Field(
        default=None, description="The currency of the dividend."
    )
    split_ratio: float = Field(
        description="The ratio of the stock split, if a stock split occurred.",
    )


class IntrinioCalendarDividendFetcher(
    Fetcher[
        IntrinioCalendarDividendQueryParams,
        List[IntrinioCalendarDividendData],
    ]
):
    """Transform the query, extract and transform the data from the Intrinio endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> IntrinioCalendarDividendQueryParams:
        """Transform the query params."""
        transformed_params = params

        now = datetime.now().date()
        if params.get("start_date") is None:
            transformed_params["start_date"] = now - relativedelta(year=1)
        if params.get("end_date") is None:
            transformed_params["end_date"] = now

        return IntrinioCalendarDividendQueryParams(**transformed_params)

    @staticmethod
    def extract_data(
        query: IntrinioCalendarDividendQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the Intrinio endpoint."""
        api_key = credentials.get("intrinio_api_key") if credentials else ""

        base_url = "https://api-v2.intrinio.com/securities"
        query_str = get_querystring(query.model_dump(), ["symbol"])
        url = f"{base_url}/{query.symbol}/prices/adjustments?{query_str}&api_key={api_key}"

        return get_data_many(url, "stock_price_adjustments", **kwargs)

    @staticmethod
    def transform_data(
        query: IntrinioCalendarDividendQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[IntrinioCalendarDividendData]:
        """Return the transformed data."""
        transformed_data: List[Dict] = [
            {"symbol": query.symbol, **item} for item in data
        ]
        return [
            IntrinioCalendarDividendData.model_validate(d) for d in transformed_data
        ]
