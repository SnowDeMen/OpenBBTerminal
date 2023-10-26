from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import (
    ExtraParams,
    ProviderChoices,
    StandardParams,
)
from openbb_core.app.query import Query
from openbb_core.app.router import Router
from pydantic import BaseModel

router = Router(prefix="")


# pylint: disable=unused-argument
@router.command(model="ForexPairs")
def pairs(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[BaseModel]:
    """Available Forex Pairs."""
    return OBBject(results=Query(**locals()).execute())


# pylint: disable=unused-argument
@router.command(model="ForexHistorical")
def load(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[BaseModel]:
    """Forex Pair Historical Price Data."""
    return OBBject(results=Query(**locals()).execute())


# pylint: disable=unused-argument
@router.command(model="ForexQuote")
def quote(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[BaseModel]:
    """Forex Pair Quote."""
    return OBBject(results=Query(**locals()).execute())


# pylint: disable=unused-argument
@router.command(model="ForexForwardRates")
def fwd(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[BaseModel]:
    """Forex Pair Forward Rate."""
    return OBBject(results=Query(**locals()).execute())