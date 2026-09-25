"""
Git-Arbiter: Semantic 3-Way AST Merge & Test Autopilot for Agent PRs.
Resolves multi-agent branch collisions cleanly using AST syntax tree splicing and test verification.
"""

from .models import (
    MergeConflictType,
    FileASTNode,
    ConflictChunk,
    MergeVerdict,
)
from .ast_merger import ASTMerger
from .test_driven_arbiter import TestDrivenArbiter

__version__ = "1.0.0"
__all__ = [
    "MergeConflictType",
    "FileASTNode",
    "ConflictChunk",
    "MergeVerdict",
    "ASTMerger",
    "TestDrivenArbiter",
]
