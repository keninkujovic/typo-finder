from symspellpy import SymSpell, Verbosity


def findTypos(sym_spell, input_term, max_suggestions=3):
    suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST)

    suggestions.sort(key=lambda x: x.distance)

    top_suggestions = suggestions[:max_suggestions]

    recommended_words = [suggestion.term for suggestion in top_suggestions]

    return recommended_words
