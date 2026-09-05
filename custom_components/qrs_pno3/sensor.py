"""Diagnostic sensors for QRS PNO3."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import PnoConfigEntry
from .coordinator import PnoData
from .entity import PnoEntity


@dataclass(frozen=True, kw_only=True)
class PnoSensorDescription(SensorEntityDescription):
    """Describes a PNO3 sensor."""

    value_fn: Callable[[PnoData], Any]


def _download_pct(data: PnoData) -> float | None:
    pb = data.playback
    total = pb.get("totalToDownload") or 0
    done = pb.get("totalDownloaded") or 0
    if not pb.get("downloadInProgress") or total <= 0:
        return 0.0
    return round(min(100.0, done / total * 100.0), 1)


SENSORS: tuple[PnoSensorDescription, ...] = (
    PnoSensorDescription(
        key="system_faults",
        translation_key="system_faults",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.playback.get("systemFaults"),
    ),
    PnoSensorDescription(
        key="system_warnings",
        translation_key="system_warnings",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.playback.get("systemWarnings"),
    ),
    PnoSensorDescription(
        key="library_songs",
        translation_key="library_songs",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.library_stats.get("songs"),
    ),
    PnoSensorDescription(
        key="library_version",
        translation_key="library_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.playback.get("libraryVersion"),
    ),
    PnoSensorDescription(
        key="tag_version",
        translation_key="tag_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.playback.get("tagVersion"),
    ),
    PnoSensorDescription(
        key="download_progress",
        translation_key="download_progress",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=_download_pct,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PnoConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(PnoSensor(coordinator, desc) for desc in SENSORS)


class PnoSensor(PnoEntity, SensorEntity):
    """A single value pulled from the poll payload."""

    entity_description: PnoSensorDescription

    def __init__(self, coordinator, description: PnoSensorDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> Any:
        return self.entity_description.value_fn(self.coordinator.data)
