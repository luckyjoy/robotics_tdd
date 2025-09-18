# Robotics Simulation Testing Framework

This framework provides a **pytest-based solution** for testing robotics applications in a **simulation-only environment** on **Windows 11**. It utilizes the **PyBullet physics engine** to simulate robot behaviors, ensuring that your tests are reproducible and don't require physical hardware.

-----

## ✨ Key Features

  * **Obstacle Avoidance Navigation:** Validate your robot's ability to navigate complex environments and avoid collisions.
  * **Pick-and-Place:** Test robotic arm manipulation for tasks like picking up and placing objects.
  * **Sensor Fusion:** Evaluate the performance of sensor data processing, including Kalman filtering.
  * **Targeted Testing:** Use `pytest -m sim` to run only the simulation-specific tests, allowing for fast, focused feedback.

-----

## 📂 Project Layout

This project follows a clear structure for easy navigation and maintenance.

```
src/
└── simulation/
    ├── robot_sim.py        # PyBullet wrapper for robot control
    └── sensors.py          # Sensor data processing and Kalman filter implementation
tests/
├── test_navigation.py      # Tests for navigation and obstacle avoidance
├── test_pick_and_place.py  # Tests for robotic arm manipulation
└── test_sensor_fusion.py   # Tests for sensor fusion logic
.github/workflows/
└── ci.yml                  # GitHub Actions configuration for CI/CD
Jenkinsfile                 # Jenkins pipeline definition
```

-----

## 🚀 Getting Started

### Prerequisites

  * **Python 3.9+**
  * **PyBullet** (physics simulator)
  * **Pytest** (testing framework)

### Running the Tests

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run all simulation tests:**
    ```bash
    pytest -m sim
    ```
3.  **Generate and view reports (optional):**
    ```bash
    pytest --alluredir=allure-results
    allure serve allure-results --port 8080
    ```
    This command generates a detailed report and launches a local server to view it.

-----

## ⚙️ Continuous Integration (CI)

The project includes pre-configured CI pipelines to automate testing and ensure code quality.

  * **GitHub Actions:** The workflow defined in `.github/workflows/ci.yml` automates linting with `flake8` and runs all simulation tests with code coverage analysis.
  * **Jenkins:** The `Jenkinsfile` provides a pipeline with stages for code checkout, dependency installation, linting, testing, and publishing reports.

-----

## 📝 Important Notes

  * This framework is designed for a **simulation-only** workflow and does **not require physical hardware**.
  * All interactions with hardware are **mocked or simulated** within the PyBullet environment.
  * It is fully functional for **offline use** on Windows 11.
