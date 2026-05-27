# voicecoder — Talon plugin for voice-driven coding in VSCode

A [Talon](https://talonvoice.com) plugin that enables continuous-speech code dictation
with a numbered **cache pad** for rapid identifier reuse. Designed for VSCode on macOS.

## Requirements

| Dependency | Notes |
|---|---|
| Talon v0.4+ | Conformer speech model required |
| [community](https://github.com/talonhub/community) plugin | Standard Talon community plugin, installed alongside this one |
| VSCode | Extension in `../voice-coder/vscode-extension` is optional (adds sidebar panel) |

## Installation

```bash
cd ~/.talon/user
git clone git@github.com:jae-63/voicecoder-talon.git voicecoder
```

Then apply the one manual change to the community plugin (see [Manual setup](#manual-setup) below).

## Files

| File | What it does |
|---|---|
| `cache_pad.py` | Cache pad: stores up to 20 identifiers, imgui overlay, persistence, VSCode sync |
| `cache_pad.talon` | Management commands: remember, forget, clear, show, hide |
| `cache_pad_direct.talon` | Direct insert: say "cache 3" in any context |
| `cache_pad_prefixes.talon` | Language-specific prefixed insert (e.g. Perl `$cache3`) |
| `dictation.py` | Dictation: phrase catch-all + embedded cache substitution |
| `dictation.talon` | Activates `voicecoder_dictate` for VSCode command mode |
| `letters_nato.py` | Overrides `user.letter` with NATO phonetic alphabet |
| `lang_perl.py` | Perl context: populates `voicecoder_cache_prefix` with `$`, `@`, `%` |

## Usage

### Cache pad

| Say | Action |
|---|---|
| `remember this` | Add selected text (or word at cursor) to cache |
| `cache word` | Alias for remember this |
| `show cache` / `hide cache` | Toggle overlay |
| `cache 3` | Insert item #3 from the cache |
| `forget cache 3` | Remove item #3 |
| `clear cache` | Empty the cache |

The overlay appears automatically on Talon startup and can be dragged anywhere on screen.

### Dictation with embedded cache references

Switch to dictation mode (say `"dictation mode"`), then speak naturally with cache
references inline:

> "my variable equals cache one plus thirty five"

inserts: `my variable equals <item1> plus thirty five`

- `cache N` or `cash N` (Conformer sometimes mishears "cache" as "cash") both work.
- Works in VSCode dictation mode via the `user.dictation_insert` override in `dictation.py`.
- Also works in command mode via the `<phrase>` catch-all in `dictation.talon`.

### NATO phonetic alphabet

Letters are spoken using the NATO alphabet: alpha, bravo, charlie, delta, …

This overrides the community default (air, bat, cap, …) globally via `letters_nato.py`.

## Manual setup

These changes live outside this repo and must be applied once on each machine:

**1. `~/.talon/user/community/settings/words_to_replace.csv`** — add this line:
```
cache,cash
```
This ensures Conformer's "cash" mishearing is corrected in dictation mode.

**2. Cursorless** — if installed, disable it or it will litter the editor with letter hats:
```bash
code --disable-extension pokey.cursorless
# then Cmd+Shift+P → Developer: Reload Window
```
Re-enable any time with `code --enable-extension pokey.cursorless`.

## Cache pad persistence

Items are saved to `~/.talon/user/voicecoder/cache_pad.json` (excluded from git).
The cache survives Talon restarts.

## VSCode sidebar sync (optional)

`cache_pad.py` attempts to push cache updates to `localhost:7890` (the VoiceCoder VSCode
extension) whenever the cache changes. This is silent if the extension isn't running.
The extension adds a sidebar panel showing the live cache. See the
[voice-coder](https://github.com/jae-63/voice-coder) repo.
