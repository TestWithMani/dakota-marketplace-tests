"""URL access helpers backed by ``config.json``."""

from typing import Dict, List, Optional, Set

from .settings import resolve_runtime_config


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
    BENCHMARKING_TAB = "benchmarking_tab"
    HEDGE_FUND_PERFORMANCE = "hedge_fund_performance"
    EVERGREEN_FUND_PERFORMANCE = "evergreen_fund_performance"
    FORECASTED_TRANSACTIONS = "forecasted_transactions"
    PRIVATE_COMPANIES_TRANSACTIONS = "private_companies_transactions"
    FUNDRAISING_NEWS = "fundraising_news"
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
        BENCHMARKING_TAB,
        HEDGE_FUND_PERFORMANCE,
        EVERGREEN_FUND_PERFORMANCE,
        FORECASTED_TRANSACTIONS,
        PRIVATE_COMPANIES_TRANSACTIONS,
        FUNDRAISING_NEWS,
        CONFERENCE_SEARCH_TAB,
        DAKOTA_VIDEO_SEARCH_TAB,
        PUBLIC_COMPANY_SEARCH_TAB,
    )

    @staticmethod
    def get_url_path(url_key: str, environment: Optional[str] = None) -> str:
        runtime = resolve_runtime_config(environment)
        urls = runtime.get("urls")

        if url_key not in urls:
            raise ValueError(
                f"URL key '{url_key}' not found in config.json urls map"
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
        environments: List[str] = []
        for base_env in ("uat", "prod"):
            environments.append(base_env)
            for portal in (
                "fa_portal",
                "ria_portal",
                "fo_portal",
                "benchmark_portal",
                "recommends_portal",
                "fa_ria_portal",
            ):
                environments.append(f"{base_env}_{portal}")
        return environments

    @staticmethod
    def validate_config() -> Dict[str, List[str]]:
        """Validate top-level URL key integrity and malformed paths."""
        issues: Dict[str, List[str]] = {"config": []}
        required: Set[str] = set(URLs.ALL_KEYS)
        runtime = resolve_runtime_config("uat")
        urls = runtime.get("urls", {})
        missing = sorted(required - set(urls.keys()))
        extra = sorted(set(urls.keys()) - required)
        if missing:
            issues["config"].append(f"Missing url keys: {', '.join(missing)}")
        if extra:
            issues["config"].append(f"Extra url keys: {', '.join(extra)}")

        trailing = [k for k, v in urls.items() if isinstance(v, str) and v.strip().endswith("-")]
        if trailing:
            issues["config"].append(f"Paths with trailing '-': {', '.join(sorted(trailing))}")

        if not issues["config"]:
            return {}
        return issues


def get_url(base_url: str, url_key: str, environment: Optional[str] = None) -> str:
    """Backward-compatible wrapper around ``URLs.get_full_url``."""
    return URLs.get_full_url(base_url, url_key, environment)

