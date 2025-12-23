"""Compatibility shim exposing scikit-learn modules under treeple._lib.sklearn.

The original project vendors a fork of scikit-learn under ``treeple._lib``.
In environments where the fork is unavailable, we fall back to the installed
``sklearn`` package while preserving the expected module layout so imports
continue to function.
"""
import importlib
import sys

from sklearn.base import BaseEstimator
from sklearn.utils._tags import Tags

_SKLEARN_TREE = importlib.import_module("sklearn.tree")
_SKLEARN_TREE_CLASSES = importlib.import_module("sklearn.tree._classes")
_SKLEARN_TREE_TREE = importlib.import_module("sklearn.tree._tree")
_SKLEARN_TREE_CRITERION = importlib.import_module("sklearn.tree._criterion")
_SKLEARN_TREE_UTILS = importlib.import_module("sklearn.tree._utils")
_SKLEARN_ENSEMBLE = importlib.import_module("sklearn.ensemble")
_SKLEARN_ENSEMBLE_FOREST = importlib.import_module("sklearn.ensemble._forest")

# Modern scikit-learn removed the legacy ``_xfail_checks`` tag attribute that the
# vendored fork still tries to populate. Allow the attribute to be set on the
# slotted ``Tags`` object and ensure the base implementation always provides it
# so downstream ``__sklearn_tags__`` overrides remain compatible.
if "_xfail_checks" not in Tags.__slots__:
    Tags.__slots__ = (*Tags.__slots__, "_xfail_checks")

_ORIGINAL_BASE_TAGS = BaseEstimator.__sklearn_tags__


def _compat_tags(self):
    tags = _ORIGINAL_BASE_TAGS(self)
    if not hasattr(tags, "_xfail_checks"):
        tags._xfail_checks = {}
    return tags


BaseEstimator.__sklearn_tags__ = _compat_tags

# Provide legacy attribute aliases expected by the vendored fork.
if not hasattr(_SKLEARN_TREE_CRITERION, "BaseCriterion"):
    _SKLEARN_TREE_CRITERION.BaseCriterion = _SKLEARN_TREE_CRITERION.Criterion

_PREFIX = __name__

# Register aliases for tree submodules.
sys.modules[f"{_PREFIX}.tree"] = _SKLEARN_TREE
sys.modules[f"{_PREFIX}.tree._classes"] = _SKLEARN_TREE_CLASSES
sys.modules[f"{_PREFIX}.tree._tree"] = _SKLEARN_TREE_TREE
sys.modules[f"{_PREFIX}.tree._criterion"] = _SKLEARN_TREE_CRITERION
sys.modules[f"{_PREFIX}.tree._utils"] = _SKLEARN_TREE_UTILS

# Register aliases for ensemble submodules.
sys.modules[f"{_PREFIX}.ensemble"] = _SKLEARN_ENSEMBLE
sys.modules[f"{_PREFIX}.ensemble._forest"] = _SKLEARN_ENSEMBLE_FOREST

# Re-export common classes for convenience.
from sklearn.ensemble import *  # noqa: F401,F403,E402
from sklearn.tree import *  # noqa: F401,F403,E402
