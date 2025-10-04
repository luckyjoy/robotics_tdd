🤖 Robotics Test-Driven Development (TDD) Framework
A robust, test-driven framework for verifying the functionality, path planning, and critical safety protocols of a simulated mobile manipulator robot.

👤 Author & Contact
Author: Bang Thien Nguyen | Contact: ontario1998@gmail.com

🛠️ Core Technologies
💡 Project Overview
This framework implements Test-Driven Development (TDD) principles, focusing on writing precise, repeatable Python tests before implementing the corresponding robot simulation logic. It uses the Pytest framework for execution and Allure for professional reporting.

Component

Technology

Role

Test Runner

pytest

The primary engine for test discovery and execution.

Test Logic

Python Modules (test_*.py)

Contains all executable TDD tests (unit, integration, and end-to-end).

Reporting

Allure & pytest-html

Generates professional, interactive HTML dashboards for traceability and analysis.

Isolation

Docker

Ensures a consistent, portable testing environment matching the CI/CD pipeline.

🚀 Getting Started
Prerequisites
Docker Desktop (Required for the containerized test runner)

Windows Command Prompt (or compatible shell, to execute run_docker.bat)

(Optional) Python 3.10+ (If running tests locally without Docker)

(Optional) Allure command-line tool

Installation
Clone the Repository:

git clone <your-repository-url>
cd robotics_tdd

Install Dependencies:
(Only necessary if running tests locally outside of Docker)

pip install -r requirements.txt

🐳 Dockerized Execution (Recommended)
The entire test suite can be run using a single batch script, which automates the build, execution, and reporting steps within an isolated Docker environment.

1. The Execution Script (run_docker.bat)
This is the primary entry point for testing on a local Windows machine. It handles the entire lifecycle using the image tagged robotics-tdd-local:latest.

Step

Action Performed by Script

Setup

Verifies Docker is running and cleans up previous allure-results and reports folders.

Build/Check

Ensures the robotics-tdd-local:latest image is available, building it if necessary.

Execute Tests

Runs the container, mounting the local allure-results folder to collect test output.

Generate & Serve Report

Launches a containerized web server to display the interactive Allure Report in your browser at http://localhost:8080.

Execution Command:

run_docker.bat

2. Build Optimization (.dockerignore)
A .dockerignore file is used to exclude large, irrelevant files (like local virtual environments, OS cache, and reports) from the Docker build context, which significantly speeds up build times and reduces the final image size.

🌳 Framework Architecture
The framework adheres to standard TDD and clean architecture principles, maintaining a clear separation between the simulation logic and the test validation code.

robotics_tdd/
├─ README.md
├─ run_docker.bat                   # Windows batch script for Docker build/run/report
├─ Dockerfile                       # Defines the isolated testing environment
├─ .dockerignore                    # Excludes files from Docker build context
├─ Jenkinsfile                      # CI/CD pipeline definition
├─ pytest.ini                       # pytest configuration (markers)
├─ requirements.txt
├─ src/                             # Source code for robot simulation (robot_sim.py, sensors.py)
├─ supports/                        # Configuration files (e.g., allure metadata)
├─ tests/                           # All pytest TDD modules (test_*.py)

🏷️ Test Tags and Execution
Tests are logically grouped using pytest markers (tags) defined in pytest.ini. This allows for highly selective execution of specific test suites.

Tag

Focus Area

Description

navigation

Path Planning

Safe movement, obstacle avoidance, and waypoint following.

pick_and_place

Manipulation

Object handling, arm kinematics, and dynamic manipulation sequences.

safety

System Integrity

Collision prevention, boundary limits, and critical error handling.

walking

Gait Control

Posture, speed, stability, and movement transitions during locomotion.

sensors

Data Fusion

Accuracy and stability of sensor-based state estimation (e.g., Kalman Filter).

Running Test Suites (Local Python Environment Only)
Execution Mode

Command

Run All Tests

pytest --verbose

Run Specific Tag

pytest -m sensors --verbose

Sequential Execution (OR)

pytest -m "navigation or pick_and_place"

Parallel Execution

pytest -m "navigation or safety" -n auto

📊 Professional Test Reporting
1. Interactive Allure Report (Recommended for Analysis)
Allure provides a customizable, interactive HTML dashboard suitable for detailed analysis, trend monitoring, and CI/CD integration.

Generate Raw Results:

pytest -m "pick_and_place or safety" --alluredir=allure-results

Serve Interactive Report:

allure serve allure-results

This opens the report in your default web browser.

2. Static HTML Report (pytest-html)
Generates a single, self-contained HTML file, ideal for archiving or sharing via email.

pytest --html=reports/report.html --self-contained-html

📝 Test Coverage Summary
Feature Area

Objective

Value Proposition

Navigation

Validate robust, collision-free movement across the environment.

Ensures the robot reliably reaches targets while adhering to safety clearances.

Pick and Place

Confirm reliable object interaction and arm dexterity within reach limits.

Guarantees consistent success rates for manipulation tasks.

Safety

Enforce non-negotiable operational limits and error handling.

Prevents equipment damage and maintains system integrity (e.g., boundary limits).

Sensor Fusion

Ensure the accuracy and stability of sensor-based state estimation.

Validates the integrity of the robot's perception system (Kalman Filter convergence).

Walking

Verify stable and safe locomotion dynamics.

Prevents tripping/falling and maintains optimal posture during movement.

