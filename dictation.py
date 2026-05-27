"""
Dictation with embedded cache-pad substitutions.

In command mode (VSCode), a spoken phrase is processed as follows:
  1. Scan for embedded (cache|recent) N tokens.
  2. Replace each with the corresponding cache item.
  3. Insert the resulting text (and cache items) in sequence.

Example: "my variable equals recent 1 plus 35"
  → inserts "my variable equals " + cache[0] + " plus 35"
"""

import re

from talon import Module, actions

mod = Module()

# Matches "cache 3", "recent 3", "cache three", etc.
# Numbers are already resolved to ints by Talon before we see them,
# so we work with the raw spoken words and resolve manually.
_WORD_TO_INT = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
}

_CACHE_PATTERN = re.compile(
    r"\b(cache|recent)\s+(\d+|"
    + "|".join(_WORD_TO_INT.keys())
    + r")\b",
    re.IGNORECASE,
)


def _resolve_index(token: str) -> int:
    try:
        return int(token)
    except ValueError:
        return _WORD_TO_INT.get(token.lower(), 0)


@mod.action_class
class Actions:
    def voicecoder_dictate(phrase: list) -> None:
        """Insert phrase, substituting embedded (cache|recent) N references"""
        text = " ".join(phrase)
        _insert_with_substitutions(text)


def _insert_with_substitutions(text: str) -> None:
    """Split text on cache/recent tokens, inserting each segment then each cache item."""
    last = 0
    for m in _CACHE_PATTERN.finditer(text):
        prefix = text[last:m.start()]
        if prefix:
            actions.insert(prefix)
        index = _resolve_index(m.group(2))
        item = actions.user.voicecoder_cache_get(index)
        if item:
            actions.insert(item)
        last = m.end()
    tail = text[last:]
    if tail:
        actions.insert(tail)
