import translators

languages = {"nl", "en", "fr"}

def translate(word : str, chosen_language : str):
    if chosen_language.lower() == "en":
        return word
    else:
        translated_word = translate.google(word, 'en', chosen_language.lower())

        return translated_word