"""EAI Lab foundation package."""

from .core_loader import CORE_VERSION, load_core
from .event_store import EventStore, EvidenceNamespaceError

__all__ = ["CORE_VERSION", "load_core", "EventStore", "EvidenceNamespaceError"]
__version__ = "0.1.0"
