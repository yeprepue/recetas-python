import json
import os
from typing import Dict, Optional

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")

SUPPORTED_LANGUAGES = ["es", "en", "fr", "zh"]

LANGUAGE_NAMES = {
    "es": "Español",
    "en": "English",
    "fr": "Français",
    "zh": "中文 (Mandarin)",
}


class Translator:
    def __init__(self, language: str = "es"):
        self.language = language if language in SUPPORTED_LANGUAGES else "es"
        self._translations: Dict[str, Dict[str, str]] = {}
        self._load_all()

    def _load_all(self):
        for lang in SUPPORTED_LANGUAGES:
            path = os.path.join(LOCALES_DIR, f"{lang}.json")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._translations[lang] = json.load(f)
            except FileNotFoundError:
                self._translations[lang] = {}

    def set_language(self, language: str):
        if language in SUPPORTED_LANGUAGES:
            self.language = language

    def t(self, key: str, **kwargs) -> str:
        text = self._translations.get(self.language, {}).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass
        return text

    def get_available_languages(self) -> Dict[str, str]:
        return {lang: LANGUAGE_NAMES.get(lang, lang) for lang in SUPPORTED_LANGUAGES}
