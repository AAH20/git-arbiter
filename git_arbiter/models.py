"""
Data models and typed schemas for Git-Arbiter.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import time


class MergeConflictType(str, Enum):
    ORTHOGONAL_ADDITIONS = "orthogonal_additions" # Two agents added different methods to same class
    DISJOINT_IMPORTS = "disjoint_imports"         # Two agents added different imports
    OVERLAPPING_MUTATION = "overlapping_mutation" # Both modified same function body
    SYNTACTIC_COLLISION = "syntactic_collision"   # Overlapping line edits


@dataclass
class FileASTNode:
    symbol_name: str
    node_type: str # "function", "class", "import"
    signature: str
    body: str
    source_branch: str = "base"


@dataclass
class ConflictChunk:
    file_path: str
    base_content: str
    ours_content: str
    theirs_content: str
    conflict_type: MergeConflictType = MergeConflictType.ORTHOGONAL_ADDITIONS


@dataclass
class MergeVerdict:
    status: str # "AUTO_RESOLVED_AST", "TEST_VERIFIED_SYNTHESIS", "MANUAL_ESCALATION"
    clean_content: str
    resolved_by_ast: bool
    test_exit_code: int = 0
    actions_taken: List[str] = field(default_factory=list)
    resolution_time_ms: float = 0.0
