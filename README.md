# 🎓 Neoversity — Master's Degree in AI/ML Engineering

This repository serves as a centralized hub for practical assignments, engineering tasks, and implementation work completed during my Master of Science (M.S.) program in Artificial Intelligence and Machine Learning Engineering at Neoversity.

The primary objective of this repository is to maintain a structured, clean, and production-grade codebase for academic deliverables, _separating curriculum-driven tasks from my primary open-source projects_.

## Repository Architecture

The codebase is organized modularly by discipline. Ongoing and completed courses are partitioned into dedicated root directories:

```text
neo-masters/
├── .gitignore
├── README.md
└── python-core/                      # Core Python engineering and automation tasks
    └── goit-pycore-hw-03/            # Current assignment sprint
        ├── task_1.py                 # Date utility automation
        ├── task_2.py                 # Deterministic lottery generator
        ├── task_3.py                 # E.164 phone string normalizer
        └── task_4.py                 # Rolling 7-day calendar scheduler
```

## Tracked Disciplines

- **`python-core/`**
  Focused on foundational software design, data structures, algorithm optimization, and automation script workflows essential for building data pipelines and preprocessing utilities in AI/ML workflows.

_Future core AI, Machine Learning, Deep Learning, and MLOps engineering modules will be structured into separate top-level directories as the curriculum progresses._

## Getting Started

To clone, set up the environment, and execute any utility locally, use the following standardized workflow:

### 1. Clone the Repository

```bash
git clone https://github.com/Serhii2009/neo-masters.git
cd neo-masters
```

### 2. Environment Setup

Initialize a clean virtual environment to prevent dependency drift:

**On macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Academic Integrity & Disclaimer

This repository is maintained solely for educational tracking, personal reference, and portfolio showcase purposes.

- **To Evaluators:** All solutions presented here are authored independently, reflecting individual engineering implementations of the provided curriculum.
- **To Students:** While referencing architecture patterns or structural concepts is permitted, direct duplication of this codebase violates general Academic Integrity policies and university guidelines.

**_Happy building! 💻_**
