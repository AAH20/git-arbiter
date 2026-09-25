# ❖ Git-Arbiter

> **Semantic 3-Way AST Merge & Test Autopilot for Agent PRs**  
> Resolves multi-agent branch collisions cleanly using Abstract Syntax Tree (AST) symbol splicing and test-driven synthesis. Powered by **Claude Opus 5.5** and **DeepSeek V4.1-Flash** to eliminate `<<<<<<< HEAD` merge conflicts and broken CI builds in autonomous swarms.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Git](https://img.shields.io/badge/Git-AST%20Semantic%20Merge-purple.svg)]()
[![Tests](https://img.shields.io/badge/Tests-3%2F3%20Passing-success.svg)]()

---

## ⚡ The Problem: The Swarm Git Collision Disaster

When enterprise swarms launch 10 parallel subagents against a repository:
1. **Line-Based Blindness**: Two agents add new methods to the bottom of the same file. Standard `git merge` fails with `<<<<<<< HEAD` conflict markers.
2. **Broken Syntax**: Naive text merging drops closing brackets, corrupts imports, and breaks compilation.
3. **Flaky CI Regressions**: Merges that look syntactically clean break runtime tests because internal assumptions conflict.

**Git-Arbiter** implements **AST Semantic Splicing & Test-Driven Merging**:
* **AST Symbol Graph**: Parses the base, ours, and theirs AST syntax trees to extract functions, classes, and imports.
* **Orthogonal Auto-Splicing**: Automatically merges disjoint additions without conflict markers.
* **Test Verification Loop**: When genuine mutations collide, candidates are verified against the local test suite in a sandboxed fork until exit code 0 is achieved.

---

## 📐 Architecture & Merge Flow

```mermaid
flowchart TD
    subgraph DivergentBranches["Colliding Swarm Branches"]
        Base["Base Commit (main)"]
        BranchA["Agent A (Ours)\nAdds Method calculate_tax()"]
        BranchB["Agent B (Theirs)\nAdds Method issue_refund()"]
        
        Base --> BranchA
        Base --> BranchB
    end

    subgraph GitArbiter["Git-Arbiter Semantic Engine"]
        Parser["AST Symbol Extractor\n(Classes, Methods, Imports)"]
        Classifier["Conflict Classifier\n(Orthogonal vs Conflicting Body)"]
        Splicer["AST Semantic Splicer\n(Clean non-overlapping merge)"]
        TestRunner["Sandbox Test Runner\n(pytest / cargo test verify)"]

        BranchA --> Parser
        BranchB --> Parser
        Base --> Parser
        Parser --> Classifier
        Classifier --> Splicer
        Splicer --> TestRunner
    end

    subgraph FinalCommit["Clean Merged Branch"]
        Clean["Atomic Merged Commit (main)\n[Exit Code: 0 | Zero Conflict Markers]"]
        TestRunner -->|Pass| Clean
    end
```

---

## 🚀 Quickstart

### 1. Installation
```bash
cd projects/git_arbiter
pip install -e .
```

### 2. Run the Conflict Resolution Demo
```bash
python3 -m git_arbiter.cli resolve
```

---

## 🧪 Testing

```bash
python3 -m unittest discover -s tests
```
Result: `Ran 3 tests in 0.000s ... OK (100% passing)`

---

## 📜 License
Apache-2.0. Copyright (c) 2026 AAH20.
