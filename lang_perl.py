"""
Perl-specific cache pad prefixes.
Active when the editor language mode is set to Perl.
"""

from talon import Context, actions

ctx = Context()
ctx.matches = r"""
code.language: perl
"""

ctx.lists["user.voicecoder_cache_prefix"] = {
    "scalar": "$",
    "array":  "@",
    "hash":   "%",
}
ctx.tags = ["user.voicecoder_has_cache_prefixes"]
