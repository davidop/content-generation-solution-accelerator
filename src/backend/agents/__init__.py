"""Agents package for Content Generation Solution Accelerator.

The multi-agent workflow is handled by the orchestrator using Microsoft Agent Framework.
This package provides utility functions used by the orchestrator.
"""

try:
    from .image_content_agent import generate_image
    __all__ = ["generate_image"]
except ImportError:
    # Running as a sub-package (e.g., from tests/); generate_image not available
    __all__ = []
