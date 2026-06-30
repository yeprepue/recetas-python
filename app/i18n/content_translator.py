import threading
from typing import Optional
from deep_translator import GoogleTranslator

_cache = {}
_cache_lock = threading.Lock()

LANG_CODE_MAP = {
    "es": "es",
    "en": "en",
    "fr": "fr",
    "zh": "zh-CN",
}


class ContentTranslator:
    def __init__(self, target_language: str = "es"):
        self.target_language = target_language if target_language != "en" else None
        mapped_lang = LANG_CODE_MAP.get(target_language, target_language)
        self.translator = GoogleTranslator(source="en", target=mapped_lang) if self.target_language else None

    def translate(self, text: Optional[str]) -> Optional[str]:
        if not text or not self.translator:
            return text
        if text in _cache:
            return _cache[text]
        try:
            translated = self.translator.translate(text)
            if translated:
                with _cache_lock:
                    _cache[text] = translated
                return translated
        except Exception:
            pass
        return text

    def translate_batch(self, texts: list) -> list:
        if not self.translator:
            return texts
        return [self.translate(text) for text in texts]
