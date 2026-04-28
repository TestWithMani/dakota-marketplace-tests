"""URL access helpers backed by ``config.json``."""

import json
import os
from typing import Dict, List, Optional, Set

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
DEFAULT_ENV = "uat"


def _load_config() -> Dict[str, dict]:
    with open(CONFIG_PATH, encoding="utf-8") as config_file:
        return json.load(config_file)


_config = _load_config()


def _get_all_environment_names() -> List[str]:
    names = []
    for key, value in _config.items():
        if isinstance(value, dict) and "url" in value and "urls" in value:
            names.append(key)
    return sorted(names)


def _normalize_environment_name(environment: Optional[str]) -> str:
    env = (environment or os.environ.get("ENV") or DEFAULT_ENV).strip().lower()
    return env.replace("-", "_").replace(" ", "_")


def _resolve_environment(environment: Optional[str]) -> str:
    normalized = _normalize_environment_name(environment)
    if normalized in _config:
        return normalized

    available = _get_all_environment_names()
    message = (
        f"Environment '{normalized}' not found in config.json. "
        f"Available: {', '.join(available)}"
    )
    raise ValueError(message)


def _normalize_url_path(raw_path: str) -> str:
    path = (raw_path or "").strip().lstrip("/")
    # Defensive normalization for accidental trailing separators in config values.
    return path.rstrip("-")


class URLs:
    """Centralized URL keys and helpers."""

    ACCOUNTS_DEFAULT = "accounts_default"
    CONTACT_DEFAULT = "contact_default"
    INVESTMENT_ALLOCATOR_ACCOUNTS_DEFAULT = "investment_allocator_accounts_default"
    INVESTMENT_FIRM_ACCOUNTS_DEFAULT = "investment_firm_accounts_default"
    DAKOTA_SEARCHES_TAB = "dakota_searches_tab"
    MY_ACCOUNTS_DEFAULT = "my_accounts_default"
    INVESTMENT_ALLOCATOR_CONTACTS_DEFAULT = "investment_allocator_contacts_default"
    INVESTMENT_FIRM_CONTACTS_DEFAULT = "investment_firm_contacts_default"
    PORTFOLIO_COMPANIES_CONTACTS_DEFAULT = "portfolio_companies_contacts_default"
    UNIVERSITY_ALUMNI_CONTACTS_DEFAULT = "university_alumni_contacts_default"
    ALL_DOCUMENTS = "all_documents"
    MANAGER_PRESENTATION_DASHBOARD = "manager_presentation_dashboard"
    CONSULTANT_REVIEWS = "consultant_reviews"
    PENSION_DOCUMENTS = "pension_documents"
    PUBLIC_PLAN_MINUTES_SEARCH_TAB = "public_plan_minutes_search_tab"
    FEE_SCHEDULES_DASHBOARD = "fee_schedules_dashboard"
    FUND_FAMILY_MEMOS = "fund_family_memos"
    DAKOTA_CITY_GUIDES = "dakota_city_guides"
    PUBLIC_INVESTMENTS_SEARCH_TAB = "public_investments_search_tab"
    FILINGS_13F_INVESTMENTS_SEARCH_TAB = "13f_filings_investments_search_tab"
    PRIVATE_FUND_SEARCH_TAB = "private_fund_search_tab"
    FUND_LAUNCHES = "fund_launches"
    CONTINUATION_VEHICLE = "continuation_vehicle"
    PORTFOLIO_COMPANIES = "portfolio_companies"
    RECENT_TRANSACTIONS = "recent_transactions"
    CONFERENCE_SEARCH_TAB = "conference_search_tab"
    DAKOTA_VIDEO_SEARCH_TAB = "dakota_video_search_tab"
    PUBLIC_COMPANY_SEARCH_TAB = "public_company_search_tab"

    ALL_KEYS = (
        ACCOUNTS_DEFAULT,
        CONTACT_DEFAULT,
        INVESTMENT_ALLOCATOR_ACCOUNTS_DEFAULT,
        INVESTMENT_FIRM_ACCOUNTS_DEFAULT,
        DAKOTA_SEARCHES_TAB,
        MY_ACCOUNTS_DEFAULT,
        INVESTMENT_ALLOCATOR_CONTACTS_DEFAULT,
        INVESTMENT_FIRM_CONTACTS_DEFAULT,
        PORTFOLIO_COMPANIES_CONTACTS_DEFAULT,
        UNIVERSITY_ALUMNI_CONTACTS_DEFAULT,
        ALL_DOCUMENTS,
        MANAGER_PRESENTATION_DASHBOARD,
        CONSULTANT_REVIEWS,
        PENSION_DOCUMENTS,
        PUBLIC_PLAN_MINUTES_SEARCH_TAB,
        FEE_SCHEDULES_DASHBOARD,
        FUND_FAMILY_MEMOS,
        DAKOTA_CITY_GUIDES,
        PUBLIC_INVESTMENTS_SEARCH_TAB,
        FILINGS_13F_INVESTMENTS_SEARCH_TAB,
        PRIVATE_FUND_SEARCH_TAB,
        FUND_LAUNCHES,
        CONTINUATION_VEHICLE,
        PORTFOLIO_COMPANIES,
        RECENT_TRANSACTIONS,
        CONFERENCE_SEARCH_TAB,
        DAKOTA_VIDEO_SEARCH_TAB,
        PUBLIC_COMPANY_SEARCH_TAB,
    )

    @staticmethod
    def get_url_path(url_key: str, environment: Optional[str] = None) -> str:
        resolved_env = _resolve_environment(environment)
        env_config = _config.get(resolved_env, {})
        urls = env_config.get("urls")

        if not isinstance(urls, dict):
            raise ValueError(
                f"No valid 'urls' section found for environment '{resolved_env}' in config.json"
            )

        if url_key not in urls:
            raise ValueError(
                f"URL key '{url_key}' not found for environment '{resolved_env}' in config.json"
            )

        return _normalize_url_path(urls[url_key])

    @staticmethod
    def get_full_url(base_url: str, url_key: str, environment: Optional[str] = None) -> str:
        if not (base_url or "").strip():
            raise ValueError("base_url cannot be empty")

        normalized_base = base_url.rstrip("/") + "/"
        return f"{normalized_base}{URLs.get_url_path(url_key, environment)}"

    @staticmethod
    def available_environments() -> List[str]:
        return _get_all_environment_names()

    @staticmethod
    def validate_config() -> Dict[str, List[str]]:
        """Validate env/url integrity and return issues grouped by environment."""
        issues: Dict[str, List[str]] = {}
        required: Set[str] = set(URLs.ALL_KEYS)

        for env_name in URLs.available_environments():
            env_issues: List[str] = []
            env_config = _config.get(env_name, {})
            urls = env_config.get("urls", {})
            missing = sorted(required - set(urls.keys()))
            extra = sorted(set(urls.keys()) - required)

            if missing:
                env_issues.append(f"Missing url keys: {', '.join(missing)}")
            if extra:
                env_issues.append(f"Extra url keys: {', '.join(extra)}")

            trailing = [k for k, v in urls.items() if isinstance(v, str) and v.strip().endswith("-")]
            if trailing:
                env_issues.append(f"Paths with trailing '-': {', '.join(sorted(trailing))}")

            if env_issues:
                issues[env_name] = env_issues

        return issues


def get_url(base_url: str, url_key: str, environment: Optional[str] = None) -> str:
    """Backward-compatible wrapper around ``URLs.get_full_url``."""
    return URLs.get_full_url(base_url, url_key, environment)

