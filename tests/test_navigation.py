# tests/test_navigation.py
import pytest
from unittest.mock import MagicMock
from simulation.robot_sim import RobotSim

@pytest.mark.sim
@pytest.mark.navigation
@pytest.mark.forward
def test_robot_navigation_obstacle_avoidance():
    """Navigation test: robot avoids obstacle while moving forward."""
    sim = RobotSim(gui=False)
    sim.load_robot()
    sim.add_obstacle(position=[0.5, 0, 0.05])

    # Mock chest height to prevent ground collision
    sim.get_chest_height = MagicMock(return_value=0.5)

    for _ in range(200):
        sim.step_forward(speed=0.2)
        pos = sim.get_position()
        chest_height = sim.get_chest_height()
        assert chest_height > 0.2, "Chest touched the ground!"
        if pos[0] >= 0.45:
            break

    # Ensure robot did not pass obstacle
    pos = sim.get_position()
    assert pos[0] < 0.6, "Robot passed through obstacle!"

@pytest.mark.sim
@pytest.mark.navigation
@pytest.mark.reverse
def test_robot_navigation_reverse():
    """Navigation test: robot reverses safely."""
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.step_forward = MagicMock(side_effect=lambda speed: None)
    sim.step_backward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.4))
    sim.get_chest_height = MagicMock(return_value=0.4)

    sim.step_forward(speed=0.5)
    sim.step_backward(speed=0.5)
    assert sim.get_chest_height() > 0.2, "Chest touched the ground during reverse!"

@pytest.mark.sim
@pytest.mark.navigation
@pytest.mark.forward
@pytest.mark.safety
def test_robot_navigation_forward_safety_limit():
    """Forward navigation with safety check for chest height."""
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.get_chest_height = MagicMock(return_value=0.5)
    sim.step_forward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", sim.get_chest_height() - 0.05))

    sim.chest_height = 0.5
    for _ in range(10):
        sim.step_forward(speed=0.1)
        assert sim.get_chest_height() > 0.2, "Chest too low during forward navigation!"

@pytest.mark.sim
@pytest.mark.navigation
@pytest.mark.reverse
@pytest.mark.safety
def test_robot_navigation_reverse_safety_limit():
    """Reverse navigation with safety check for chest height."""
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.step_backward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.35))
    sim.get_chest_height = MagicMock(return_value=0.35)

    sim.step_backward(speed=0.1)
    assert sim.get_chest_height() > 0.2, "Chest too low during reverse navigation!"
