"""Shared base entity for QRS PNO3."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import PnoCoordinator


class PnoEntity(CoordinatorEntity[PnoCoordinator]):
    """Common device wiring."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: PnoCoordinator) -> None:
        super().__init__(coordinator)
        entry = coordinator.entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name=entry.title,
            configuration_url=f"http://{coordinator.api.host}/",
        )

    @property
    def _pb(self) -> dict:
        return self.coordinator.data.playback

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data is not None
