"""
Configuration Manager Module

This module provides a centralized interface for managing application configurations.
It supports loading from default_config.py, JSON files, and environment variables.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Any

from .default_config import DEFAULT_CONFIG as DEFAULT_PYTHON_CONFIG
from .default_config import validate_config as validate_default_config

# Global configuration instance
_config: Optional[Dict[str, Any]] = None
_config_file_path: Optional[str] = None


def initialize_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Initialize the configuration with default values or load from file.
    
    Args:
        config_path: Optional path to JSON configuration file.
                    If None, uses default_config.py
    
    Returns:
        The initialized configuration dictionary
    """
    global _config, _config_file_path
    
    if config_path:
        # Load from JSON file
        _config = load_config_from_json(config_path)
        _config_file_path = config_path
    else:
        # Use default Python configuration
        _config = DEFAULT_PYTHON_CONFIG.copy()
        _config_file_path = None
    
    return _config.copy()


def load_config_from_json(json_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file.
    
    The JSON file will be merged with default configuration values.
    Environment variables can still override values.
    
    Args:
        json_path: Path to JSON configuration file
        
    Returns:
        The merged configuration dictionary
        
    Raises:
        FileNotFoundError: If JSON file doesn't exist
        json.JSONDecodeError: If JSON file is invalid
    """
    json_path = Path(json_path)
    
    if not json_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {json_path}")
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            json_config = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in configuration file: {e.msg}",
            e.doc,
            e.pos
        )
    
    # Start with default configuration
    config = DEFAULT_PYTHON_CONFIG.copy()
    
    # Merge JSON configuration
    _merge_configs(config, json_config)
    
    return config


def _merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    """Recursively merge override config into base config.
    
    Args:
        base: Base configuration dictionary (modified in place)
        override: Configuration values to override
    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _merge_configs(base[key], value)
        else:
            base[key] = value


def get_config() -> Dict[str, Any]:
    """Get a copy of the current configuration.
    
    Returns:
        A copy of the current configuration dictionary
    """
    global _config
    
    if _config is None:
        initialize_config()
    
    return _config.copy()


def set_config(custom_config: Dict[str, Any]) -> None:
    """Update the current configuration with custom values.
    
    Args:
        custom_config: Dictionary of configuration values to update
    """
    global _config
    
    if _config is None:
        initialize_config()
    
    _merge_configs(_config, custom_config)


def get_value(key: str, default: Optional[Any] = None) -> Any:
    """Get a specific configuration value by key.
    
    Supports nested keys using dot notation (e.g., "agent_config.max_steps")
    
    Args:
        key: Configuration key (can use dot notation for nested values)
        default: Default value if key is not found
        
    Returns:
        The configuration value or default if not found
    """
    config = get_config()
    
    if "." not in key:
        return config.get(key, default)
    
    # Handle nested keys with dot notation
    keys = key.split(".")
    value = config
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
            if value is None:
                return default
        else:
            return default
    
    return value if value is not None else default


def set_value(key: str, value: Any) -> None:
    """Set a specific configuration value by key.
    
    Supports nested keys using dot notation (e.g., "agent_config.max_steps")
    
    Args:
        key: Configuration key (can use dot notation for nested values)
        value: Value to set
    """
    config = get_config()
    
    if "." not in key:
        config[key] = value
        set_config(config)
        return
    
    # Handle nested keys with dot notation
    keys = key.split(".")
    current = config
    
    for k in keys[:-1]:
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        current = current[k]
    
    current[keys[-1]] = value
    set_config(config)


def get_model_config(model_name_or_signature: str) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific model by name or signature.
    
    Args:
        model_name_or_signature: Model name or signature to look up
        
    Returns:
        Model configuration dictionary or None if not found
    """
    config = get_config()
    
    for model in config.get("models", []):
        if (model.get("name") == model_name_or_signature or 
            model.get("signature") == model_name_or_signature):
            return model
    
    return None


def get_enabled_models() -> list:
    """Get list of enabled models.
    
    Returns:
        List of enabled model configurations
    """
    config = get_config()
    return [m for m in config.get("models", []) if m.get("enabled", False)]


def validate() -> tuple:
    """Validate the current configuration.
    
    Returns:
        Tuple of (is_valid: bool, errors: list)
    """
    return validate_default_config()


def reload(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Reload the configuration from file or defaults.
    
    Args:
        config_path: Optional path to JSON configuration file
        
    Returns:
        The reloaded configuration dictionary
    """
    global _config, _config_file_path
    
    _config = None
    _config_file_path = None
    
    return initialize_config(config_path)


def get_config_file_path() -> Optional[str]:
    """Get the path to the currently loaded configuration file.
    
    Returns:
        Path to configuration file or None if using default config
    """
    return _config_file_path


# Initialize with default configuration on module import
initialize_config()
