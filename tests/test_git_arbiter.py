"""
Unit tests for Git-Arbiter using standard unittest.
"""

import unittest
from git_arbiter.models import ConflictChunk
from git_arbiter.ast_merger import ASTMerger
from git_arbiter.test_driven_arbiter import TestDrivenArbiter


class TestGitArbiter(unittest.TestCase):
    def test_extract_symbols(self):
        code = "def foo():\n    return 1\n\ndef bar():\n    return 2"
        syms = ASTMerger.extract_symbols(code)
        self.assertIn("foo", syms)
        self.assertIn("bar", syms)

    def test_orthogonal_ast_merge_success(self):
        base = "def existing():\n    return 'base'"
        ours = "def existing():\n    return 'base'\n\ndef func_a():\n    return 'A'"
        theirs = "def existing():\n    return 'base'\n\ndef func_b():\n    return 'B'"

        conflict = ConflictChunk("service.py", base, ours, theirs)
        success, merged, actions = ASTMerger.attempt_ast_merge(conflict)

        self.assertTrue(success)
        self.assertIn("func_a", merged)
        self.assertIn("func_b", merged)
        self.assertNotIn("<<<<<<<", merged)

    def test_test_driven_arbiter_resolution(self):
        base = "def ping(): return 'pong'"
        ours = "def ping(): return 'pong'\ndef helper_1(): return 1"
        theirs = "def ping(): return 'pong'\ndef helper_2(): return 2"

        conflict = ConflictChunk("api.py", base, ours, theirs)
        arbiter = TestDrivenArbiter()
        verdict = arbiter.resolve_conflict(conflict)

        self.assertEqual(verdict.status, "AUTO_RESOLVED_AST_CLEAN")
        self.assertEqual(verdict.test_exit_code, 0)
        self.assertTrue(verdict.resolved_by_ast)
        self.assertIn("helper_1", verdict.clean_content)
        self.assertIn("helper_2", verdict.clean_content)


if __name__ == "__main__":
    unittest.main()
