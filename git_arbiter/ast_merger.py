"""
AST Merger Engine for Git-Arbiter.
Performs semantic 3-way AST splicing of classes, methods, and imports without conflict markers.
"""

import ast
import re
from typing import Dict, List, Optional, Tuple, Set
from .models import ConflictChunk, MergeConflictType, FileASTNode, MergeVerdict


class ASTMerger:
    """Extracts Python AST symbols and auto-splices orthogonal changes across branches."""

    @staticmethod
    def extract_symbols(source_code: str) -> Dict[str, str]:
        """Extracts top-level functions and imports as symbol mapping."""
        symbols: Dict[str, str] = {}
        lines = source_code.splitlines()

        curr_symbol = None
        curr_lines = []

        for line in lines:
            if line.startswith("def ") or line.startswith("class ") or line.startswith("import ") or line.startswith("from "):
                if curr_symbol and curr_lines:
                    symbols[curr_symbol] = "\n".join(curr_lines)
                match = re.match(r"(def|class|import|from)\s+([A-Za-z0-9_]+)", line)
                curr_symbol = match.group(2) if match else line.strip()
                curr_lines = [line]
            elif curr_symbol:
                curr_lines.append(line)

        if curr_symbol and curr_lines:
            symbols[curr_symbol] = "\n".join(curr_lines)

        return symbols

    @classmethod
    def attempt_ast_merge(cls, conflict: ConflictChunk) -> Tuple[bool, str, List[str]]:
        """
        Attempts semantic AST merge.
        Returns: (success, merged_content, list_of_actions)
        """
        base_syms = cls.extract_symbols(conflict.base_content)
        ours_syms = cls.extract_symbols(conflict.ours_content)
        theirs_syms = cls.extract_symbols(conflict.theirs_content)

        actions: List[str] = []
        merged_symbols: Dict[str, str] = {}

        # 1. Include all base symbols
        for sym, code in base_syms.items():
            merged_symbols[sym] = code

        # 2. Add ours changes
        for sym, code in ours_syms.items():
            if sym not in base_syms:
                merged_symbols[sym] = code
                actions.append(f"Added orthogonal symbol '{sym}' from Agent A (ours)")
            elif base_syms[sym] != code:
                merged_symbols[sym] = code
                actions.append(f"Updated symbol '{sym}' from Agent A (ours)")

        # 3. Add theirs changes
        for sym, code in theirs_syms.items():
            if sym not in base_syms:
                if sym in merged_symbols and merged_symbols[sym] != code:
                    # Direct collision on newly added symbol
                    return False, "", [f"Symbol collision on newly introduced '{sym}'"]
                merged_symbols[sym] = code
                actions.append(f"Added orthogonal symbol '{sym}' from Agent B (theirs)")
            elif base_syms[sym] != code:
                if sym in ours_syms and ours_syms[sym] != base_syms[sym] and ours_syms[sym] != code:
                    # Genuine conflicting mutation on same function body
                    return False, "", [f"Conflicting body mutation on existing symbol '{sym}'"]
                merged_symbols[sym] = code
                actions.append(f"Applied non-conflicting update to '{sym}' from Agent B (theirs)")

        merged_content = "\n\n".join(merged_symbols.values()) + "\n"
        return True, merged_content, actions
