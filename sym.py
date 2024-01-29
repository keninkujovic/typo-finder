from symspellpy import SymSpell, Verbosity


def findTypos(sym_spell, text, max_suggestions=3):
        unique_words = set(text.split())

        corrected_text = {}

        for word in unique_words:
            suggestions = sym_spell.lookup(word, Verbosity.CLOSEST)
            suggestions = suggestions[:max_suggestions]

            corrected_words = {suggestion.term for suggestion in suggestions}
            corrected_text[word] = list(corrected_words)

        return corrected_text
