from mtranslate import translate

class TranslatorHandler:
    def __init__(self):
        # Language codes: en (English), si (Sinhala), ta (Tamil)
        self.supported_languages = ['en', 'si', 'ta']

    def translate_to_english(self, text, source_lang):
        if source_lang == 'en':
            return text
        try:
            return translate(text, 'en', source_lang)
        except Exception as e:
            print(f"Translation Error: {e}")
            return text

    def translate_from_english(self, text, target_lang):
        if target_lang == 'en':
            return text
        try:
            return translate(text, target_lang, 'en')
        except Exception as e:
            print(f"Translation Error: {e}")
            return text
