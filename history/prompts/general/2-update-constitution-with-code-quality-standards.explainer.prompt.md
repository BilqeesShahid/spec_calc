---
ID: 2
TITLE: Update Constitution with Code Quality Standards
STAGE: explainer
DATE_ISO: 2025-11-17
SURFACE: agent
MODEL: gemini-1.5-flash
FEATURE: none
BRANCH: main
USER: user
COMMAND: Update @.specify/memory/constitution.md to improve Code Quality Standards
LABELS: ["constitution", "code-quality"]
LINKS: null
FILES_YAML:
  - .specify/memory/constitution.md
TESTS_YAML: []
PROMPT_TEXT: |
  Update @.specify/memory/constitution.md to improve Code Quality Standards

  - All functions must include type hints on parameters and return types
    - Example: `def add(a: float, b: float) -> float:`
  - All functions must include docstrings explaining what they do
    - Example: `"""Add two numbers and return the sum."""`
  - Follow PEP 8 naming conventions (lowercase_with_underscores for functions)
  - Lines must be under 100 characters
  - No magic numbers; use named constants
    - Bad: `if x > 10:`
    - Good: `if x > MAX_POWER_EXPONENT:`
RESPONSE_TEXT: |
  I have updated the `constitution.md` file with the new quality requirements.
  Now I need to create a PHR for this interaction.
---
I have updated the `constitution.md` file with the new quality requirements.
