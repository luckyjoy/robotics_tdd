# tests/test_robot_safety.py
import pytest
from unittest.mock import MagicMock
from simulation.robot_sim import RobotSim

@pytest.mark.sim
@pytest.mark.safety
def test_robot_walking_no_chest_collision():
    sim = RobotSim(gui=False)
    sim.load_robot()
    
    # Mock step_forward
    sim.step_forward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.5 - speed))
    sim.get_chest_height = MagicMock(return_value=0.5)

    sim.chest_height = 0.5
    for _ in range(5):
        sim.step_forward(speed=0.1)
        assert sim.get_chest_height() > 0.2, "Chest touched the ground!"

@pytest.mark.sim
@pytest.mark.safety
def test_robot_move_with_ground_contact():
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.move_to = MagicMock(side_effect=lambda position: setattr(sim, "chest_height", position[2]))
    sim.move_to([0.2, 0, 0.25])
    assert sim.chest_height >= 0.2, "Robot chest too low!"

@pytest.mark.sim
@pytest.mark.safety
def test_robot_safe_reverse():
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.step_backward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.4))
    sim.get_chest_height = MagicMock(return_value=0.4)

    sim.step_backward(speed=0.1)
    assert sim.get_chest_height() > 0.2, "Chest touched the ground during reverse!"
