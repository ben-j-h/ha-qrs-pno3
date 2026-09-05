"""Config + options flow for QRS PNO3."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PnoApiClient, PnoConnectionError
from .const import (
    CONF_HOST,
    DEFAULT_IDLE_INTERVAL,
    DEFAULT_PARAMS_INTERVAL,
    DEFAULT_PLAYING_INTERVAL,
    DEFAULT_TURN_OFF_STOPS,
    DOMAIN,
    OPT_IDLE_INTERVAL,
    OPT_PARAMS_INTERVAL,
    OPT_PLAYING_INTERVAL,
    OPT_TURN_OFF_STOPS,
)

STEP_USER = vol.Schema({vol.Required(CONF_HOST): str})


async def _async_probe(hass, host: str) -> str | None:
    """Confirm we can talk to the controller and return its MAC (for unique_id)."""
    api = PnoApiClient(host, async_get_clientsession(hass))
    await api.async_quick_state()  # raises PnoConnectionError if unreachable
    net = await api.async_network_info()
    mac = net.get("mac") or net.get("wmac")
    return mac.lower() if isinstance(mac, str) and mac else None


class PnoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the initial setup."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            try:
                mac = await _async_probe(self.hass, host)
            except PnoConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(mac or f"host:{host}")
                self._abort_if_unique_id_configured(updates={CONF_HOST: host})
                return self.async_create_entry(title=f"PNO3 ({host})", data={CONF_HOST: host})

        return self.async_show_form(step_id="user", data_schema=STEP_USER, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> OptionsFlow:
        return PnoOptionsFlow()


class PnoOptionsFlow(OptionsFlow):
    """Tune polling cadence + turn-off behaviour."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        opts = self.config_entry.options
        schema = vol.Schema(
            {
                vol.Optional(
                    OPT_PLAYING_INTERVAL,
                    default=opts.get(OPT_PLAYING_INTERVAL, DEFAULT_PLAYING_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=30)),
                vol.Optional(
                    OPT_IDLE_INTERVAL,
                    default=opts.get(OPT_IDLE_INTERVAL, DEFAULT_IDLE_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=600)),
                vol.Optional(
                    OPT_PARAMS_INTERVAL,
                    default=opts.get(OPT_PARAMS_INTERVAL, DEFAULT_PARAMS_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=3600)),
                vol.Optional(
                    OPT_TURN_OFF_STOPS,
                    default=opts.get(OPT_TURN_OFF_STOPS, DEFAULT_TURN_OFF_STOPS),
                ): bool,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
