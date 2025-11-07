import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get project root directory
PROJECT_DIR = Path(__file__).parent.parent.resolve()

DEFAULT_CONFIG = {
    # ==================== Project Settings ====================
    "project_dir": str(PROJECT_DIR),
    "results_dir": os.getenv("RESULTS_DIR", "./results"),
    "data_dir": os.getenv("DATA_DIR", "./data"),
    "data_cache_dir": str(PROJECT_DIR / "data" / "cache"),
    
    # ==================== Agent Settings ====================
    "agent_type": "BaseAgent",  # BaseAgent, BaseAgent_Hour, BaseAgentAStock
    "market": "us",  # us, cn
    "agent_config": {
        "max_steps": 30,
        "max_retries": 3,
        "base_delay": 1.0,
        "initial_cash": 10000.0,
    },
    
    # ==================== Date Range ====================
    "date_range": {
        "init_date": "2025-10-01",
        "end_date": "2025-10-21",
    },
    
    # ==================== LLM Settings ====================
    "llm_provider": os.getenv("LLM_PROVIDER", "deepseek").lower(),  # deepseek, openai, anthropic, google, qwen, minimax
    "deep_think_llm": os.getenv("DEEP_THINK_LLM", "deepseek-chat"),
    "quick_think_llm": os.getenv("QUICK_THINK_LLM", "deepseek-chat"),
    "backend_url": os.getenv("BACKEND_URL", "https://api.deepseek.com/v1"),
    
    # ==================== API Keys ====================
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "openai_base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "deepseek_api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    "deepseek_base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "google_api_key": os.getenv("GOOGLE_API_KEY", ""),
    "qwen_api_key": os.getenv("QWEN_API_KEY", ""),
    "minimax_api_key": os.getenv("MINIMAX_API_KEY", ""),
    
    # ==================== Data Source Settings ====================
    "primary_data_source": os.getenv("PRIMARY_DATA_SOURCE", "yahoo"),  # yahoo, alphavantage, akshare
    "fallback_data_sources": ["yahoo", "alphavantage", "akshare"],
    
    # Alpha Vantage API
    "alphavantage_api_key": os.getenv("ALPHAVANTAGE_API_KEY", ""),
    "alphavantage_rate_limit_wait": 0.25,  # Seconds between API calls
    
    # AKShare settings (for Chinese stocks)
    "akshare_enabled": os.getenv("AKSHARE_ENABLED", "true").lower() == "true",
    "akshare_market": os.getenv("AKSHARE_MARKET", "A"),  # A, HK, US
    
    # Finnhub API
    "finnhub_api_key": os.getenv("FINNHUB_API_KEY", ""),
    
    # Yahoo Finance rate limiting
    "yfinance_rate_limit_wait": float(os.getenv("YFINANCE_RATE_LIMIT_WAIT", "2.0")),
    "yfinance_retry_wait": float(os.getenv("YFINANCE_RETRY_WAIT", "10.0")),
    
    # ==================== Logging Settings ====================
    "log_config": {
        "log_path": os.getenv("LOG_PATH", "./data/agent_data"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    },
    
    # ==================== Model Configuration ====================
    "models": [
        {
            "name": "deepseek-chat",
            "basemodel": "deepseek/deepseek-chat",
            "signature": "deepseek-chat",
            "enabled": True,
        },
        {
            "name": "deepseek-chat-v3.1",
            "basemodel": "deepseek/deepseek-chat-v3.1",
            "signature": "deepseek-chat-v3.1",
            "enabled": False,
        },
        {
            "name": "claude-3.7-sonnet",
            "basemodel": "anthropic/claude-3.7-sonnet",
            "signature": "claude-3.7-sonnet",
            "enabled": False,
            "openai_base_url": None,
            "openai_api_key": None,
        },
        {
            "name": "qwen3-max",
            "basemodel": "qwen/qwen3-max",
            "signature": "qwen3-max",
            "enabled": False,
        },
        {
            "name": "gemini-2.5-flash",
            "basemodel": "google/gemini-2.5-flash",
            "signature": "gemini-2.5-flash",
            "enabled": False,
        },
        {
            "name": "gpt-4-turbo",
            "basemodel": "openai/gpt-4-turbo",
            "signature": "gpt-4-turbo",
            "enabled": False,
        },
    ],
}


def get_config():
    """Get a copy of the default configuration."""
    return DEFAULT_CONFIG.copy()


def update_config(custom_config: dict):
    """Update the default configuration with custom values.
    
    Args:
        custom_config: Dictionary of configuration values to update
    """
    global DEFAULT_CONFIG
    DEFAULT_CONFIG.update(custom_config)


def get_model_config(model_name_or_signature: str):
    """Get configuration for a specific model by name or signature.
    
    Args:
        model_name_or_signature: Model name or signature to look up
        
    Returns:
        Model configuration dictionary or None if not found
    """
    for model in DEFAULT_CONFIG.get("models", []):
        if (model.get("name") == model_name_or_signature or 
            model.get("signature") == model_name_or_signature):
            return model
    return None


def get_enabled_models():
    """Get list of enabled models.
    
    Returns:
        List of enabled model configurations
    """
    return [m for m in DEFAULT_CONFIG.get("models", []) if m.get("enabled", False)]


def validate_config():
    """Validate the current configuration.
    
    Returns:
        Tuple of (is_valid: bool, errors: list)
    """
    errors = []
    
    # Check LLM provider
    valid_providers = ["openai", "deepseek", "anthropic", "google", "qwen", "minimax"]
    if DEFAULT_CONFIG.get("llm_provider", "").lower() not in valid_providers:
        errors.append(f"Invalid LLM provider: {DEFAULT_CONFIG.get('llm_provider')}")
    
    # Check at least one model is enabled
    if not get_enabled_models():
        errors.append("No models are enabled in configuration")
    
    # Check data source
    valid_sources = ["yahoo", "alphavantage", "akshare"]
    if DEFAULT_CONFIG.get("primary_data_source") not in valid_sources:
        errors.append(f"Invalid primary data source: {DEFAULT_CONFIG.get('primary_data_source')}")
    
    # Check market
    if DEFAULT_CONFIG.get("market") not in ["us", "cn"]:
        errors.append(f"Invalid market: {DEFAULT_CONFIG.get('market')}")
    
    return len(errors) == 0, errors
