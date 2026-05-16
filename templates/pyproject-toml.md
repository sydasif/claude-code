---
name: pyproject-toml
description: Python project configuration template with ruff, mypy pytest, coverage, and security tooling
---

# pyproject.toml Template

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.0.0",
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "bandit>=1.7.0",
    "safety>=3.0.0",
]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM"]
ignore = ["E501"]

[tool.mypy]
python-version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
exclude = ["tests/*", "**/__pycache__/*"]
```

## Usage

1. `uv init my-project`
2. Copy this content into pyproject.toml
3. `uv sync --all-extras --dev`
