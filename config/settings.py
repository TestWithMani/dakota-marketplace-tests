"""Shared runtime configuration helpers for tests and URL builders.

Reads ``config/config.json`` for base URLs, credentials (All Marketplace Access
plus per-portal overrides), and tab URL paths. ``ENV`` selects ``uat``/``prod``
optionally with a portal suffix, for example ``uat_fa_data_set``.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

CONFIG_PATH = Path(__file__).with_name("config.json")
DEFAULT_ENV = "uat"
DEFAULT_PORTAL = "all_marketplace_access"

def load_config() -> Dict[str, dict]:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        return json.load(config_file)


_config = load_config()


def _normalize_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _get_meta() -> Dict[str, list]:
    return _config.get("meta", {})


def parse_environment_name(environment: Optional[str] = None) -> Tuple[str, str, str]:
    raw = environment or os.environ.get("ENV") or _get_meta().get("default_env") or DEFAULT_ENV
    normalized = _normalize_token(raw)

    parts = normalized.split("_", 1)
    base_env = parts[0] if parts and parts[0] else DEFAULT_ENV
    portal = parts[1] if len(parts) == 2 and parts[1] else DEFAULT_PORTAL
    return base_env, portal, normalized


def portal_keys_for_compound_env() -> List[str]:
    """Portal keys used as ``ENV`` suffixes (excludes All Marketplace Access / base)."""
    return [p for p in _supported_portals() if p != DEFAULT_PORTAL]


def _supported_base_envs() -> List[str]:
    return _get_meta().get("supported_base_envs", ["uat", "prod"])


def _supported_portals() -> List[str]:
    return _get_meta().get(
        "supported_portals",
        [
            "all_marketplace_access",
            "dakota_ria_portal",
            "dakota_transactions_ceos_access",
            "fa_data_set",
            "is_deal_team",
            "dakota_private_markets_access",
            "dakota_recommends_portal_access",
            "dakota_family_office_portal",
            "dakota_private_wealth_portal",
            "dakota_international_portal",
        ],
    )


def resolve_runtime_config(environment: Optional[str] = None) -> Dict[str, object]:
    base_env, portal, normalized = parse_environment_name(environment)

    if base_env not in _supported_base_envs():
        raise ValueError(
            f"Unsupported base environment '{base_env}'. Supported: {', '.join(_supported_base_envs())}"
        )
    if portal not in _supported_portals():
        raise ValueError(
            f"Unsupported portal '{portal}'. Supported: {', '.join(_supported_portals())}"
        )

    base_urls = _config.get("base_urls", {})
    url = base_urls.get(base_env)
    if not url:
        raise ValueError(f"Missing base URL for environment '{base_env}' in config.json")

    base_credentials = _config.get("credentials", {}).get("base", {})
    default_creds = base_credentials.get(base_env, {})
    portal_creds = (
        _config.get("credentials", {})
        .get("portals", {})
        .get(portal, {})
        .get(base_env, {})
    )
    username = portal_creds.get("username", default_creds.get("username", ""))
    password = portal_creds.get("password", default_creds.get("password", ""))

    if not username or not password:
        raise ValueError(
            f"Missing credentials for environment '{base_env}' and portal '{portal}' in config.json"
        )

    urls = _config.get("urls", {})
    if not isinstance(urls, dict) or not urls:
        raise ValueError("Missing or invalid top-level 'urls' map in config.json")

    effective_env = base_env if portal == DEFAULT_PORTAL else f"{base_env}_{portal}"
    return {
        "environment": effective_env,
        "base_env": base_env,
        "portal": portal,
        "raw_env_input": normalized,
        "url": url,
        "username": username,
        "password": password,
        "urls": urls,
    }


def validate_config_shape(required_url_keys: Optional[List[str]] = None) -> List[str]:
    errors: List[str] = []

    for env in _supported_base_envs():
        if env not in _config.get("base_urls", {}):
            errors.append(f"Missing base_urls.{env}")
        if env not in _config.get("credentials", {}).get("base", {}):
            errors.append(f"Missing credentials.base.{env}")

    if required_url_keys:
        urls = _config.get("urls", {})
        missing = [k for k in required_url_keys if k not in urls]
        if missing:
            errors.append(f"Missing urls keys: {', '.join(sorted(missing))}")

    return errors
