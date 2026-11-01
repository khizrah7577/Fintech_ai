"""In-memory and SQLite LLM caching for LangChain."""

from __future__ import annotations

from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache, SQLiteCache

from src.config import SQLITE_CACHE_PATH

_active_backend: str | None = None
_memory_cache: InMemoryCache | None = None
_sqlite_cache: SQLiteCache | None = None


def configure_cache(backend: str = "memory") -> str:
    """
    Register a global LangChain LLM cache.

    Reuses the same cache instance when the backend is unchanged so Streamlit
    reruns do not wipe an in-memory cache. Reset session must NOT delete the
    SQLite file — only session_state is cleared.

    backend: 'memory' | 'sqlite'
    """
    global _active_backend, _memory_cache, _sqlite_cache
    key = (backend or "memory").lower().strip()

    if key == _active_backend:
        if key == "sqlite":
            return f"SQLite cache active → {SQLITE_CACHE_PATH}"
        return "In-memory cache active (cleared when the process restarts)"

    try:
        if key == "sqlite":
            if _sqlite_cache is None:
                _sqlite_cache = SQLiteCache(database_path=SQLITE_CACHE_PATH)
            set_llm_cache(_sqlite_cache)
            _active_backend = "sqlite"
            return f"SQLite cache active → {SQLITE_CACHE_PATH}"

        if _memory_cache is None:
            _memory_cache = InMemoryCache()
        set_llm_cache(_memory_cache)
        _active_backend = "memory"
        return "In-memory cache active (cleared when the process restarts)"
    except Exception as exc:  # noqa: BLE001
        set_llm_cache(None)
        _active_backend = None
        return f"Cache configuration failed: {exc}. Caching disabled."


def get_active_backend() -> str | None:
    return _active_backend


def describe_cache_modes() -> dict[str, str]:
    return {
        "memory": (
            "Stored in RAM. Fastest. Does not survive restart. Best for one session."
        ),
        "sqlite": (
            f"Stored in {SQLITE_CACHE_PATH}. Fast, slightly slower than RAM. "
            "Survives restart. Reset session does not delete this file."
        ),
    }
