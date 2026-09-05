"""Tempo / transpose number entities (experimental).

The controller accepts these ``setParam`` writes (returns success) but no
runtime effect was observed during live testing - see
``research/06-live-test-results.md``.  They are therefore **disabled by
default**; enable them if a future firmware / code path makes them stick.
The *reported* values (from ``playbackInformation``) are always shown.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import PnoConfigEntry
from .api import PnoError
from .const import (
    PARAM_TEMPO,
    PARAM_TRANSPOSE,
    TEMPO_MAX,
    TEMPO_MIN,
    TRANSPOSE_MAX,
    TRANSPOSE_MIN,
)
from .coordinator import PnoData
from .entity import PnoEntity


@dataclass(frozen=True, kw_only=True)
class PnoNumberDescription(NumberEntityDescription):
    param_id: int
    value_fn: Callable[[PnoData], float | None]


NUMBERS: tuple[PnoNumberDescription, ...] = (
    PnoNumberDescription(
        key="tempo",
        translation_key="tempo",
        param_id=PARAM_TEMPO,
        native_min_value=TEMPO_MIN,
        native_max_value=TEMPO_MAX,
        native_step=1,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda d: d.playback.get("tempo") or d.params.get(PARAM_TEMPO),
    ),
    PnoNumberDescription(
        key="transpose",
        translation_key="transpose",
        param_id=PARAM_TRANSPOSE,
        native_min_value=TRANSPOSE_MIN,
        native_max_value=TRANSPOSE_MAX,
        native_step=1,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda d: d.playback.get("transpose") or d.params.get(PARAM_TRANSPOSE),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PnoConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(PnoNumber(coordinator, desc) for desc in NUMBERS)


class PnoNumber(PnoEntity, NumberEntity):
    entity_description: PnoNumberDescription

    def __init__(self, coordinator, description: PnoNumberDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> float | None:
        val = self.entity_description.value_fn(self.coordinator.data)
        try:
            return float(val) if val is not None else None
        except (TypeError, ValueError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        try:
            await self.coordinator.api.async_set_param(self.entity_description.param_id, int(value))
        except PnoError as err:
            raise HomeAssistantError(str(err)) from err
        await self.coordinator.async_request_refresh()
