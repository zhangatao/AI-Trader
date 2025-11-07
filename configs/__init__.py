"""
Configuration Package

This package provides centralized configuration management for the AI-Trader application.
It supports:
- Default configuration with environment variable overrides (default_config.py)
- Configuration loading from JSON files
- Dynamic configuration updates
- Configuration validation
"""

from .default_config import (
    DEFAULT_CONFIG,
    get_config as get_default_config,
    get_enabled_models as get_default_enabled_models,
    get_model_config as get_default_model_config,
    validate_config,
)

from .config_manager import (
    initialize_config,
    load_config_from_json,
    get_config,
    set_config,
    get_value,
    set_value,
    get_model_config,
    get_enabled_models,
    validate,
    reload,
    get_config_file_path,
)

__all__ = [
    # From default_config.py
    "DEFAULT_CONFIG",
    "get_default_config",
    "get_default_enabled_models",
    "get_default_model_config",
    "validate_config",
    
    # From config_manager.py
    "initialize_config",
    "load_config_from_json",
    "get_config",
    "set_config",
    "get_value",
    "set_value",
    "get_model_config",
    "get_enabled_models",
    "validate",
    "reload",
    "get_config_file_path",
]
