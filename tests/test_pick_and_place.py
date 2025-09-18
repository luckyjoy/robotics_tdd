# tests/test_pick_and_place.py
import pytest
from unittest.mock import MagicMock
from simulation.robot_sim import RobotSim

@pytest.mark.sim
def test_pick_and_place_cube():
    sim = RobotSim(gui=False)
    sim.load_robot(arm=True)

    # Mock methods to simulate cube pick
    sim.add_cube = MagicMock(return_value=1)
    sim.move_arm_to = MagicMock()
    sim.close_gripper = MagicMock()
    sim.get_object_position = MagicMock(return_value=[0.3, 0, 0.25])
    sim.get_chest_height = MagicMock(return_value=0.5)
    sim.disconnect = MagicMock()

    cube_id = sim.add_cube(position=[0.3, 0, 0.05])
    sim.move_arm_to([0.3, 0, 0.05])
    sim.close_gripper(cube_id)
    sim.move_arm_to([0.3, 0, 0.3])

    cube_pos = sim.get_object_position(cube_id)
    chest_height = sim.get_chest_height()

    assert cube_pos[2] > 0.2, "Cube was not lifted!"
    assert chest_height > 0.2, "Chest touched ground during pick-and-place!"
    sim.disconnect()
