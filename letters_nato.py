from talon import Context

# Override user.letter with the NATO phonetic alphabet.
# This replaces the community default (air/bat/cap/...) globally.
# To revert, delete or disable this file.

ctx = Context()
ctx.lists["user.letter"] = {
    "alpha":    "a",
    "bravo":    "b",
    "charlie":  "c",
    "delta":    "d",
    "echo":     "e",
    "foxtrot":  "f",
    "golf":     "g",
    "hotel":    "h",
    "india":    "i",
    "juliet":   "j",
    "kilo":     "k",
    "lima":     "l",
    "mike":     "m",
    "november": "n",
    "oscar":    "o",
    "papa":     "p",
    "quebec":   "q",
    "romeo":    "r",
    "sierra":   "s",
    "tango":    "t",
    "uniform":  "u",
    "victor":   "v",
    "whiskey":  "w",
    "xray":     "x",
    "yankee":   "y",
    "zulu":     "z",
}
