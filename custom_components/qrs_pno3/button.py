"""Button entities for QRS PNO3."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import PnoConfigEntry
from .api import PnoError
from .coordinator import PnoCoordinator
from .entity import PnoEntity


@dataclass(frozen=True, kw_only=True)
class PnoButtonDescription(ButtonEntityDescription):
    press_fn: Callable[[PnoCoordinator], Coroutine[Any, Any, Any]]


BUTTONS: tuple[PnoButtonDescription, ...] = (
    PnoButtonDescription(
        key="clear_faults",
        translation_key="clear_faults",
        entity_category=EntityCategory.CONFIG,
        press_fn=lambda c: c.api.async_clear_faults(),
    ),
    PnoButtonDescription(
        key="panic_stop",
        translation_key="panic_stop",
        device_class=ButtonDeviceClass.IDENTIFY,
        press_fn=lambda c: c.api.async_stop(),
    ),
    PnoButtonDescription(
        key="refresh_library",
        translation_key="refresh_library",
        entity_category=EntityCategory.CONFIG,
        press_fn=lambda c: c.async_refresh_library(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PnoConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(PnoButton(coordinator, desc) for desc in BUTTONS)


class PnoButton(PnoEntity, ButtonEntity):
    entity_description: PnoButtonDescription

    def __init__(self, coordinator, description: PnoButtonDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{description.key}"

    async def async_press(self) -> None:
        try:
            await self.entity_description.press_fn(self.coordinator)
        except PnoError as err:
            raise HomeAssistantError(str(err)) from err
        await self.coordinator.async_request_refresh()
