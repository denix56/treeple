"""Compatibility shim exposing scikit-learn modules under treeple._lib.sklearn.

The original project vendors a fork of scikit-learn under ``treeple._lib``.
In environments where the fork is unavailable, we fall back to the installed
``sklearn`` package while preserving the expected module layout so imports
continue to function.
"""
import importlib
import sys

_SKLEARN_TREE = importlib.import_module("sklearn.tree")
_SKLEARN_TREE_CLASSES = importlib.import_module("sklearn.tree._classes")
_SKLEARN_TREE_TREE = importlib.import_module("sklearn.tree._tree")
_SKLEARN_TREE_CRITERION = importlib.import_module("sklearn.tree._criterion")
_SKLEARN_TREE_UTILS = importlib.import_module("sklearn.tree._utils")
_SKLEARN_ENSEMBLE = importlib.import_module("sklearn.ensemble")
_SKLEARN_ENSEMBLE_FOREST = importlib.import_module("sklearn.ensemble._forest")

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
