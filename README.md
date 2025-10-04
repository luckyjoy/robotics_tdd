🤖 Robotics Test-Driven Development (TDD) Framework
A robust, test-driven framework for verifying the functionality and safety protocols of a simulated mobile manipulator robot.

Author: Bang Thien Nguyen | Contact: ontario1998@gmail.com

💡 Project Overview
This framework implements Test-Driven Development (TDD) principles using the industry-standard Pytest runner. The goal is to enforce a test-first approach, ensuring that all complex functional and safety requirements are validated through clear, organized, and repeatable Python test cases.

Core Component

Technology

Description

Test Execution

Pytest

Industry-standard Python testing tool for discovering and running tests.

Test Logic

Python Modules (test_*.py)

Contains all executable TDD tests for unit and integration validation.

Reporting

allure-pytest

Plugin used to generate rich, interactive reports with detailed status and logging.

🚀 Getting Started
Prerequisites
Docker Desktop (Essential for the automated test runner)

Windows Command Prompt (or compatible shell, to execute the batch file)

Python 3.8+ (Required only if running tests without Docker)

Allure command-line tool (Required only if running tests without Docker)

Installation
Clone the Repository:

git clone <your-repository-url>
cd robotics_tdd

Install Dependencies:

pip install -r requirements.txt

🐳 Dockerized Execution (Recommended)
The entire test environment is containerized to ensure consistent results, regardless of the host machine's configuration. The image is built and run automatically using the provided batch script.

1. The Docker Image (Dockerfile)
The image, tagged robotics-tdd-local:latest, is a complete, self-contained environment built on python:3.10-slim. Key components include:

Java JRE 21 and the Allure Command Line tool (v2.29.0), which are necessary for generating the interactive HTML reports.

The project code and Python dependencies (requirements.txt) are copied and installed into the /app working directory.

2. The Execution Script (run_docker.bat)
The Windows batch script automates the entire TDD testing workflow, from environment setup to report viewing. It automatically uses the local directory C:\my_work\robotics_tdd for artifact storage.

Step

Action Performed by Script

Purpose

Setup

Checks Docker status and cleans previous allure-results / reports directories.

Ensures a fresh, clean test run every time.

Build

Checks for robotics-tdd-local:latest. If missing, it runs docker build --no-cache.

Guarantees the necessary test environment is ready.

Test Run

Runs the container using docker run --rm, mounting the local allure-results folder.

Executes tests in an isolated environment and collects results locally.

Report Generation

Runs a containerized allure generate to create static HTML files in the local reports folder.

Converts raw results into a shareable, interactive report.

Serve Report

Launches a final container running a fast Python HTTP server (python -m http.server 8080) and opens the report in the default browser at http://localhost:8080 in a new window.

Provides immediate, interactive access to the test results.

Execution Command:

run_docker.bat

3. Build Optimization (.dockerignore)
It is highly recommended to include a .dockerignore file. This prevents irrelevant files (like local virtual environments, OS cache, and report folders) from being copied into the Docker build context, which drastically speeds up the build process and reduces final image size.

🌳 Framework Architecture
The structure adheres to standard TDD practices, separating the source code (src/) from the test code (tests/).

🏷️ Test Tags and Execution
Tests are grouped using pytest markers (tags) to allow for selective execution.

Tag

Focus Area

Description

navigation

Path Planning

Safe movement, obstacle avoidance, and waypoint following.

pick_and_place

Manipulation

Object handling, arm kinematics, and dynamic pick-and-carry tasks.

safety

System Integrity

Collision prevention, boundary limits, and critical error handling.

sensors

Data Fusion

Accuracy and stability of sensor-based state estimation.

Running Test Suites (Local Python Environment Only)
If you need to run tests without the Docker container, these commands apply:

Command

Description

Run All Tests

pytest --verbose

Run Specific Suite

pytest -m sensors --verbose

Run Multiple Suites (Sequential)

pytest -m "navigation or safety"

Run Multiple Suites (Parallel)

pytest -m "pick_and_place or safety" -n auto

📊 Professional Test Reporting
1. Interactive Allure Report (Recommended for Analysis)
Allure generates a rich, interactive HTML dashboard ideal for deep analysis of test results, including trends, defect categorization, and test history.

Generate Raw Results:

pytest --alluredir=allure-results -m "navigation or safety"

Serve Interactive Report:

allure serve allure-results

This opens the report in your default web browser.

2. Static HTML Report (pytest-html)
Generates a single, self-contained HTML file for simple archiving and sharing.

pytest --html=reports/report.html --self-contained-html

📝 Key Feature Validation Areas
Feature Area

Objective

Sample Scenarios

Navigation

Validate robust movement control.

Robot moves to a target safely, The robot stops before an obstacle.

Pick and Place

Confirm reliable object interaction.

A full pick and place sequence, Robot can not pick from beyond its reach.

Safety

Enforce non-negotiable operational limits.

Robot does not cross boundary, Robot must halt when an emergency stop is triggered.

Sensor Fusion

Ensure the accuracy and stability of sensor-based state estimation.

Filter output converges within 10 iterations, State estimate error remains below 5%.

Walking

Verify stable and safe locomotion dynamics.

Robot maintains balance on a 10-degree slope, Footfall pattern is within tolerance.

