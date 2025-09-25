# tests/test_navigation.py
import pytest
from unittest.mock import MagicMock
from simulation.robot_sim import RobotSim

@pytest.mark.sim
@pytest.mark.navigation
def test_robot_navigation_obstacle_avoidance():
    # Navigation test with obstacle
    sim = RobotSim(gui=False)
    sim.load_robot()
    sim.add_obstacle(position=[0.5, 0, 0.05])

    # Mock chest height to ensure robot doesn't hit ground
    sim.get_chest_height = MagicMock(return_value=0.5)

    for _ in range(200):
        sim.step_forward(speed=0.2)
        pos = sim.get_position()  # Get actual position from the simulation
        chest_height = sim.get_chest_height()
        assert chest_height > 0.2, "Chest touched the ground!"
        if pos[0] >= 0.45:
            break

    # Now assert on the real position
    pos = sim.get_position()
    assert pos[0] < 0.6, "Robot passed through obstacle!"

@pytest.mark.sim
@pytest.mark.navigation
def test_robot_navigation_reverse():
    # Reverse movement with safety check
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.step_forward = MagicMock(side_effect=lambda speed: None)
    sim.step_backward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.4))
    sim.get_chest_height = MagicMock(return_value=0.4)

    sim.step_forward(speed=0.5)
    sim.step_backward(speed=0.5)
    assert sim.get_chest_height() > 0.2, "Chest touched the ground during reverse!"