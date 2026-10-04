from __future__ import annotations

import logging
import os
from typing import Optional

import yaml

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "groups": {
        "premium": {
            "weight": 50,
            "api_keys": ["sk-premium-key-1", "sk-premium-key-2"],
        },
        "standard": {
            "weight": 30,
            "api_keys": ["sk-standard-key-1"],
        },
        "free": {
            "weight": 20,
            "api_keys": ["sk-free-key-1", "sk-free-key-2"],
        },
    },
    "settings": {
        "max_tokens_per_window": 1_000_000,
        "window_seconds": 60,
        "max_queue_depth": 100,
        "max_concurrent": 50,
        "default_group": "free",
    },
}


class WFQConfig:
    def __init__(self, config_path: str | None = None):
        self._raw = self._load(config_path)
        self.groups: dict[str, dict] = self._raw["groups"]
        self.settings: dict = self._raw["settings"]
        self._api_key_to_group: dict[str, str] = {}
        for group_name, group_cfg in self.groups.items():
            for key in group_cfg.get("api_keys", []):
                self._api_key_to_group[key] = group_name

    def _load(self, config_path: str | None) -> dict:
        candidates = [
            config_path,
            os.environ.get("WFQ_CONFIG"),
            os.path.join(os.path.dirname(__file__), "config.yaml"),
            "/etc/wfq/config.yaml",
        ]
        for path in candidates:
            if path and os.path.isfile(path):
                logger.info("Loading config from %s", path)
                with open(path) as f:
                    return yaml.safe_load(f)

        logger.warning("No config file found, using defaults")
        return DEFAULT_CONFIG

    def group_for_api_key(self, api_key: str) -> str:
        return self._api_key_to_group.get(api_key, self.settings.get("default_group", "free"))

    def group_weights(self) -> dict[str, float]:
        return {name: cfg["weight"] for name, cfg in self.groups.items()}
