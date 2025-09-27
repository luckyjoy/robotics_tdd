# 🤖 Robotics Behavior-Driven Development (BDD) Framework

A robust, test-driven framework for verifying the functionality and safety protocols of a simulated mobile manipulator robot.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Pytest-BDD](https://img.shields.io/badge/BDD%2FPytest--BDD-FF5733?style=for-the-badge&logo=bdd&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-0077B6?style=for-the-badge&logo=jenkins&logoColor=white)

**Author:** Bang Thien Nguyen | **Contact:** ontario1998@gmail.com

---

## 💡 Project Overview

This framework implements **Behavior-Driven Development (BDD)** principles using `pytest-bdd` to create a living documentation and validation layer for robot simulation logic. All functional and safety requirements are documented as human-readable **Gherkin scenarios** in the `features/` directory, making the test suite accessible to engineers, product managers, and QA specialists.

| Core Component | Technology | Description |
| :--- | :--- | :--- |
| **Test Syntax** | **Gherkin** (`.feature` files) | Defines test cases using **Given-When-Then** steps for clear, unambiguous behavior specification. |
| **Test Runner** | **`pytest`** | Industry-standard Python testing tool. |
| **Test Glue** | **`pytest-bdd`** | Connects Gherkin steps to executable Python code in `steps/`. |
| **Reporting** | **Allure & `pytest-html`** | Generates professional, interactive HTML reports for test traceability. |

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* `pip` package manager
* Allure command-line tool (for full HTML reporting)

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd robotics_bdd
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🌳 Framework Architecture

The project structure enforces separation of concerns between human-readable feature descriptions, executable step definitions, and core simulation logic.

````

robotics\_bdd/
├─ README.md
├─ Jenkinsfile                     \# CI/CD pipeline definition (Jenkins)
├─ pytest.ini                      \# pytest configuration and marker definitions
├─ requirements.txt
├─ simulation/
│  ├─ robot\_sim.py                 \# Core simulated robot model and API
│  └─ sensors.py                   \# Sensor/Kalman filter implementation
├─ features/                       \# Gherkin Scenarios (\*.feature files)
│  ├─ navigation.feature
│  ├─ pick\_and\_place.feature
│  ├─ safety.feature
│  └─ sensors.feature
└─ steps/                          \# Python Step Definitions (Glue Code)
   ├─ navigation\_steps.py
   ├─ pick\_and\_place\_steps.py
   ├─ safety\_steps.py
   └─ sensor\_steps.py

````

---

## 🏷️ Test Tags and Execution

Tests are grouped using `pytest` markers (tags) defined in `pytest.ini`.

| Tag | Focus Area | Description |
| :--- | :--- | :--- |
| **`navigation`** | Path Planning | Safe movement, obstacle avoidance, and waypoint following. |
| **`pick_and_place`** | Manipulation | Object handling, arm kinematics, and dynamic pick-and-carry tasks. |
| **`safety`** | System Integrity | Collision prevention, boundary limits, critical height maintenance, and error handling. |
| **`sensors`** | Data Fusion | Accuracy and convergence of sensor filtering (e.g., Kalman Filter). |

### Running Test Suites

| Command | Description |
| :--- | :--- |
| **Run All Tests** | `pytest --verbose` |
| **Run Specific Suite** | `pytest -m sensors --verbose` |
| **Run Multiple Suites (Sequential)** | `pytest -m "navigation or safety"` | Runs all tests tagged with either `navigation` or `safety`. |
| **Run Multiple Suites (Parallel)** | `pytest -m "pick_and_place or safety" -n auto` | Uses `pytest-xdist` to run tests across available CPU cores. |

---

## 📊 Professional Test Reporting

### 1. Interactive Allure Report (Recommended for Analysis)

Allure generates a rich, interactive HTML dashboard ideal for deep analysis of test results, including trends, defect categorization, and test history.

1.  **Generate Raw Results:**
    ```bash
    pytest --alluredir=allure-results -m "navigation or safety"
    ```
2.  **Serve Interactive Report:**
    ```bash
    allure serve allure-results
    ```
    *This opens the report in your default web browser.*

### 2. Static HTML Report (`pytest-html`)

Generates a single, self-contained HTML file for simple archiving and sharing.

```bash
pytest --html=reports/report.html --self-contained-html
````

-----

## 📝 Key Feature Validation Areas

| Feature Area | Objective | Sample Scenarios |
| :--- | :--- | :--- |
| **Navigation** | Validate robust movement control. | `Robot moves to a target safely`, `The robot stops before an obstacle`. |
| **Pick and Place** | Confirm reliable object interaction. | `A full pick and place sequence`, `Robot can not pick from beyond its reach`. |
| **Safety** | Enforce non-negotiable operational limits. | `Robot does not cross boundary`, `Robot arm stops before obstacle`. |
| **Sensor Fusion** | Ensure data processing accuracy. | `Kalman filter converges to an accurate estimate`. |
