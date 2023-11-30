from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='en')
translated_text = translator.translate("aaj mera din was really bad")
print(translated_text)
