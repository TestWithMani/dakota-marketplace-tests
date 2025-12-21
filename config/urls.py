"""
URL Configuration File
All application URLs are stored here for easy maintenance.
Supports environment-specific URLs (UAT, PROD, etc.)
"""

import os
import json

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH) as f:
    _config = json.load(f)


class URLs:
    """
    Centralized URL paths for the application.
    URLs are loaded from config.json based on the current environment.
    """
    
    # URL key constants for easy reference
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
 
    
    @staticmethod
    def get_url_path(url_key, environment=None):
        """
        Get URL path for a specific key and environment.
        
        Args:
            url_key: The URL key (e.g., URLs.ACCOUNTS_DEFAULT)
            environment: Environment name (uat, prod, etc.). 
                        If None, uses ENV environment variable or defaults to 'uat'
        
        Returns:
            URL path string for the specified environment
        """
        if environment is None:
            environment = os.environ.get("ENV", "uat")
        
        if environment not in _config:
            raise ValueError(f"Environment '{environment}' not found in config.json")
        
        env_config = _config[environment]
        if "urls" not in env_config:
            raise ValueError(f"No 'urls' section found for environment '{environment}' in config.json")
        
        urls = env_config["urls"]
        if url_key not in urls:
            raise ValueError(f"URL key '{url_key}' not found for environment '{environment}' in config.json")
        
        return urls[url_key]
    
    @staticmethod
    def get_full_url(base_url, url_key, environment=None):
        """
        Get complete URL by combining base_url with environment-specific URL path.
        
        Args:
            base_url: The base URL (e.g., from config)
            url_key: The URL key (e.g., URLs.ACCOUNTS_DEFAULT)
            environment: Environment name (uat, prod, etc.). 
                        If None, uses ENV environment variable or defaults to 'uat'
        
        Returns:
            Complete URL string
        """
        url_path = URLs.get_url_path(url_key, environment)
        
        # Ensure base_url ends with / if it doesn't already
        if not base_url.endswith('/'):
            base_url += '/'
        
        # Remove leading / from url_path if present
        url_path = url_path.lstrip('/')
        
        return f"{base_url}{url_path}"


# Backward compatibility function
def get_url(base_url, url_key, environment=None):
    """
    Helper function to construct full URL from base_url and url_key.
    This is a convenience wrapper around URLs.get_full_url().
    
    Args:
        base_url: The base URL (e.g., from config)
        url_key: The URL key (e.g., URLs.ACCOUNTS_DEFAULT)
        environment: Environment name (uat, prod, etc.). 
                    If None, uses ENV environment variable or defaults to 'uat'
    
    Returns:
        Complete URL string
    """
    return URLs.get_full_url(base_url, url_key, environment)

