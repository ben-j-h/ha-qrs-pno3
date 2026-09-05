"""Switch entities for QRS PNO3."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import PnoConfigEntry
from .api import PnoError
from .entity import PnoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PnoConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    async_add_entities([PnoRailPowerSwitch(entry.runtime_data.coordinator)])


class PnoRailPowerSwitch(PnoEntity, SwitchEntity):
    """Solenoid rail power.

    Note: the controller acknowledges ``powerOn=0`` but only drops the rail
    supply on its own idle timer, so turning this off may lag by minutes.
    Turning it on is immediate (and playback turns it on implicitly).
    """

    _attr_translation_key = "rail_power"
    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_rail_power"

    @property
    def is_on(self) -> bool:
        return bool(self._pb.get("currentPowerOn"))

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._set(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._set(False)

    async def _set(self, on: bool) -> None:
        try:
            await self.coordinator.api.async_set_power(on)
        except PnoError as err:
            raise HomeAssistantError(str(err)) from err
        await self.coordinator.async_request_refresh()
