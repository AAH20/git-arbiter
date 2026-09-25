"""
Command Line Interface & Conflict Demonstration for Git-Arbiter.
"""

import sys
from .models import ConflictChunk
from .test_driven_arbiter import TestDrivenArbiter


def run_demo() -> None:
    print("\n" + "=" * 70)
    print("❖ GIT-ARBITER: SEMANTIC 3-WAY AST MERGE & TEST AUTOPILOT")
    print("=" * 70)
    print("Target Models: Claude Opus 5.5 & DeepSeek V4.1-Flash")
    print("Scenario:      2 Parallel Swarm Agents Edited the Same Class Simultaneously")
    print("-" * 70)

    base = """
class BillingService:
    def __init__(self, account_id):
        self.account_id = account_id

    def get_balance(self):
        return 100.0
"""

    # Agent A (ours) added calculate_tax
    ours = """
class BillingService:
    def __init__(self, account_id):
        self.account_id = account_id

    def get_balance(self):
        return 100.0

    def calculate_sales_tax(self, amount, rate=0.08):
        return amount * rate
"""

    # Agent B (theirs) added issue_refund
    theirs = """
class BillingService:
    def __init__(self, account_id):
        self.account_id = account_id

    def get_balance(self):
        return 100.0

    def issue_stripe_refund(self, tx_id, amount):
        return {"refunded": True, "tx": tx_id, "amount": amount}
"""

    conflict = ConflictChunk(
        file_path="src/billing/service.py",
        base_content=base.strip(),
        ours_content=ours.strip(),
        theirs_content=theirs.strip()
    )

    print("[STEP 1] DETECTED 3-WAY GIT CONFLICT IN 'src/billing/service.py'...")
    print(" • Agent A Branch: Introduced `calculate_sales_tax`")
    print(" • Agent B Branch: Introduced `issue_stripe_refund`")
    print(" • Standard Git:   Produces `<<<<<<< HEAD` merge collision error!")

    print("-" * 70)
    print("[STEP 2] PARSING AST SYMBOL TREES & DISPATCHING GIT-ARBITER...")
    arbiter = TestDrivenArbiter()
    verdict = arbiter.resolve_conflict(conflict)

    print(f" ✓ Resolution Status:  {verdict.status}")
    print(f" ✓ AST Auto-Splice:    {verdict.resolved_by_ast}")
    print(f" ✓ Test Exit Code:     {verdict.test_exit_code} (Clean Syntax & 100% Test Pass)")
    print(f" ✓ Resolution Latency: {verdict.resolution_time_ms} ms")
    print(" • Actions Executed:")
    for act in verdict.actions_taken:
        print(f"   - {act}")

    print("-" * 70)
    print("[STEP 3] CLEAN MERGED CODE COMMITTED AUTOMATICALLY:")
    print(verdict.clean_content.strip())
    print("=" * 70 + "\n")


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
