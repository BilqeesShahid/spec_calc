<!--
Sync Impact Report:
- Version change: 0.0.0 -> 1.0.0
- Modified principles:
  - Principle 1: New -> Test-Driven Development
  - Principle 2: New -> Modern Python with Type Hints
  - Principle 3: New -> Clean and Readable Code
  - Principle 4: New -> Architectural Decision Records
  - Principle 5: New -> SOLID, DRY, KISS Principles
- Added sections:
  - Technical Stack
  - Quality Requirements
- Removed sections:
  - Principle 6
- Templates requiring updates: None
- Follow-up TODOs: None
-->
# spec_calc Constitution

## Core Principles

### I. Test-Driven Development
Write tests first (TDD approach). TDD is mandatory: Tests are written, user-approved, and failing before implementation. The Red-Green-Refactor cycle is strictly enforced.

### II. Modern Python with Type Hints
Use Python 3.12+ with type hints everywhere. This improves code clarity, reduces bugs, and enables static analysis.

### III. Clean and Readable Code
Keep code clean and easy to read. This facilitates maintenance and collaboration.

### IV. Architectural Decision Records
Document important decisions with ADRs. This provides context and history for architectural choices.

### V. SOLID, DRY, KISS Principles
Follow essential OOP principles: SOLID, DRY, KISS. This leads to robust, maintainable, and simple object-oriented design.

## Technical Stack

- Python 3.12+ with UV package manager
- pytest for testing
- Keep all project files in git

## Quality Requirements

- All tests must pass
- At least 80% code coverage
- Use dataclasses for data structures
- All functions must include type hints on parameters and return types (e.g., `def add(a: float, b: float) -> float:`)
- All functions must include docstrings explaining what they do (e.g., `"""Add two numbers and return the sum."""`)
- Follow PEP 8 naming conventions (lowercase_with_underscores for functions)
- Lines must be under 100 characters
- No magic numbers; use named constants (e.g., `if x > MAX_POWER_EXPONENT:`)

## Governance

This Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan. All PRs/reviews must verify compliance. Complexity must be justified.

**Version**: 1.0.0 | **Ratified**: 2025-11-14 | **Last Amended**: 2025-11-14