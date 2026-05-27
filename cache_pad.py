"""
Cache pad — a numbered list of recently-used symbols/identifiers.

Commands (defined in cache_pad.talon):
  remember this        — add selected text (or word at cursor) to top of cache
  cache word           — alias for remember this
  (cache | recent) N   — insert item N from the cache
  forget cache N       — remove item N from the cache
  clear cache          — empty the cache
  show cache           — display the imgui overlay
  hide cache           — hide the overlay
"""

import json
import pathlib
import socket

from talon import Context, Module, actions, app, imgui, settings

mod = Module()
mod.tag("voicecoder_cache_pad", desc="Enables voicecoder cache pad commands")

mod.list(
    "voicecoder_cache_prefix",
    desc="Language-specific prefixes for cache pad retrieval (e.g. scalar→$ in Perl)",
)
mod.tag(
    "voicecoder_has_cache_prefixes",
    desc="Activated by language contexts that populate voicecoder_cache_prefix",
)

mod.setting(
    "voicecoder_cache_pad_size",
    type=int,
    default=20,
    desc="Maximum number of items in the voicecoder cache pad",
)

# Default context: empty prefix list so the grammar rule is simply absent
# when no language-specific context overrides it.
ctx = Context()
ctx.lists["user.voicecoder_cache_prefix"] = {}

_STORE = pathlib.Path.home() / ".talon" / "user" / "voicecoder" / "cache_pad.json"
_cache: list[str] = []
_gui_visible = False


def _push_to_vscode() -> None:
    try:
        msg = json.dumps({"cmd": "syncCacheItems", "items": _cache}) + "\n"
        with socket.create_connection(("127.0.0.1", 7890), timeout=0.5) as s:
            s.sendall(msg.encode())
    except Exception:
        pass


def _save() -> None:
    _STORE.write_text(json.dumps(_cache))
    _push_to_vscode()


def _load() -> None:
    global _cache
    try:
        _cache = json.loads(_STORE.read_text())
    except Exception:
        _cache = []


@imgui.open()
def gui(m):
    m.text("Cache Pad")
    m.line()
    if _cache:
        for i, item in enumerate(_cache, 1):
            display = item if len(item) <= 30 else item[:27] + "…"
            m.text(f"{i:>2}: {display}")
    else:
        m.text("(empty)")


@mod.action_class
class Actions:
    def voicecoder_cache_remember() -> None:
        """Add selected text or word at cursor to top of cache pad"""
        word = actions.edit.selected_text().strip()
        if not word:
            actions.edit.select_word()
            word = actions.edit.selected_text().strip()
            actions.key("right")
        if not word:
            return
        if word in _cache:
            _cache.remove(word)
        _cache.insert(0, word)
        max_size: int = settings.get("user.voicecoder_cache_pad_size")
        del _cache[max_size:]
        _save()

    def voicecoder_cache_insert(index: int) -> None:
        """Insert cache pad item at 1-based index"""
        if 1 <= index <= len(_cache):
            actions.insert(_cache[index - 1])

    def voicecoder_cache_evict(index: int) -> None:
        """Remove cache pad item at 1-based index"""
        if 1 <= index <= len(_cache):
            _cache.pop(index - 1)
            _save()

    def voicecoder_cache_clear() -> None:
        """Clear all items from the cache pad"""
        global _cache
        _cache = []
        _save()

    def voicecoder_cache_show() -> None:
        """Show the cache pad overlay"""
        gui.show()

    def voicecoder_cache_hide() -> None:
        """Hide the cache pad overlay"""
        gui.hide()

    def voicecoder_cache_insert_prefixed(index: int, prefix: str) -> None:
        """Insert cache pad item at 1-based index with a prefix string prepended"""
        if 1 <= index <= len(_cache):
            actions.insert(prefix + _cache[index - 1])

    def voicecoder_cache_get(index: int) -> str:
        """Return cache pad item at 1-based index, or empty string"""
        if 1 <= index <= len(_cache):
            return _cache[index - 1]
        return ""


def _on_ready():
    _load()
    gui.show()

app.register("ready", _on_ready)
