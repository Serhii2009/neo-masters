# 🎓 Neoversity — Master's Degree in AI/ML Engineering

This repository serves as a centralized hub for practical assignments, engineering tasks, and implementation work completed during my Master of Science (M.S.) program in Artificial Intelligence and Machine Learning Engineering at Neoversity.

The primary objective of this repository is to maintain a structured, clean, and production-grade codebase for academic deliverables, _separating curriculum-driven tasks from my primary open-source projects_.

## Repository Architecture

The codebase is organized modularly by discipline. Ongoing and completed courses are partitioned into dedicated root directories:

```text
neo-masters/
├── .gitignore
├── requirements.txt
├── README.md
│
├── python-core/                        # ✅ Core Python engineering and automation
├── mathematics/                        # ✅ Mathematics for AI/ML
├── basic-dsa/                          # ✅ Data structures and algorithms
└── numerical-python/                   # ✅ Numerical programming for AI/ML
```

Every discipline follows the same layout: one directory per assignment, plus `paper-review-*` directories for the reviewed scientific publications.

## Tracked Disciplines

### ✅ `python-core/` — Completed

Focused on foundational software design, data structures, algorithm optimization, and automation script workflows essential for building data pipelines and preprocessing utilities in AI/ML workflows. Includes 8 homework sprints and 2 paper reviews.

**Final Team Project:** [smart-assistant-cli](https://github.com/Serhii2009/smart-assistant-cli) — a command-line personal assistant built collaboratively, integrating contact management, notes, and scheduling with a clean CLI interface.

---

### ✅ `mathematics/` — Completed

Covers the mathematical foundations required for modern AI/ML engineering: **linear algebra** (vector spaces, matrix decompositions, eigenvalues), **calculus** (differentiation, gradients, optimization), and **fundamentals of probability & statistics** (distributions, inference, Bayes' theorem). Each homework is submitted as a Google Colab notebook (`.ipynb`). Two peer-reviewed scientific article analyses are included as paper reviews.

---

### ✅ `basic-dsa/` — Completed

Classical data structures and algorithms: **linked lists**, stacks and queues, **trees and heaps**, **graphs** with shortest-path search, sorting, substring search, **greedy methods and dynamic programming**, and Monte Carlo simulation. Solutions are plain Python modules, with the measurements and conclusions for each task documented alongside them. Includes a final project and 2 paper reviews.

---

### ✅ `numerical-python/` — Completed

Applies numerical methods to practical AI/ML problems: **clustering** and **matrix decompositions**, distance metrics and correlation analysis, the **discrete Fourier transform**, probabilistic and discriminant classification, and parameter optimization by **gradient descent**, **reinforcement learning** and **genetic algorithms**. Each assignment is a Google Colab notebook (`.ipynb`). Includes a final project and 2 paper reviews.

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
