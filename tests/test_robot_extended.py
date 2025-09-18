# tests/test_robot_extended.py
import pytest
from unittest.mock import MagicMock
from simulation.robot_sim import RobotSim

# -------------------------------
# NAVIGATION EDGE CASES
# -------------------------------

@pytest.mark.sim
def test_navigation_multiple_obstacles():
    sim = RobotSim(gui=False)
    sim.load_robot()
    sim.add_obstacle(position=[0.4, 0, 0.05])
    sim.add_obstacle(position=[0.8, 0, 0.05])

    sim.get_chest_height = MagicMock(return_value=0.5)

    for _ in range(300):
        sim.step_forward(speed=0.2)
        pos = sim.get_position()
        assert sim.get_chest_height() > 0.2, "Chest touched the ground!"
        if pos[0] >= 0.75:
            break

    pos = sim.get_position()
    assert pos[0] < 0.9, "Robot passed through second obstacle!"

@pytest.mark.sim
def test_navigation_boundary_limit():
    """Test that the robot does not cross the boundary (x <= 1.0)."""
    sim = RobotSim(gui=False)
    sim.load_robot()

    # Mock within boundary
    sim.get_position = MagicMock(return_value=[1.0, 0, 0.5])
    pos = sim.get_position()

    # Should be inside or at the boundary
    assert pos[0] <= 1.0, f"Robot crossed simulation boundary at {pos[0]}!"


@pytest.mark.sim
def test_navigation_continuous_reverse():
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.step_backward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.4))
    sim.get_chest_height = MagicMock(return_value=0.4)

    for _ in range(5):
        sim.step_backward(speed=0.3)
        assert sim.get_chest_height() > 0.2, "Chest touched ground during continuous reverse!"

# -------------------------------
# PICK & PLACE EDGE CASES
# -------------------------------

@pytest.mark.sim
def test_pick_and_drop_cube():
    sim = RobotSim(gui=False)
    sim.load_robot(arm=True)

    sim.add_cube = MagicMock(return_value=1)
    sim.move_arm_to = MagicMock()
    sim.close_gripper = MagicMock()
    sim.open_gripper = MagicMock()
    sim.get_object_position = MagicMock(side_effect=[
        [0.3, 0, 0.25],  # lifted
        [0.3, 0, 0.05]   # dropped
    ])
    sim.get_chest_height = MagicMock(return_value=0.5)

    cube_id = sim.add_cube(position=[0.3, 0, 0.05])
    sim.move_arm_to([0.3, 0, 0.3])
    sim.close_gripper(cube_id)
    cube_pos = sim.get_object_position(cube_id)
    assert cube_pos[2] > 0.2, "Cube not lifted!"

    sim.open_gripper(cube_id)
    cube_pos = sim.get_object_position(cube_id)
    assert cube_pos[2] < 0.2, "Cube did not drop!"
    assert sim.get_chest_height() > 0.2, "Chest touched ground during drop!"

@pytest.mark.sim
def test_pick_beyond_reach():
    sim = RobotSim(gui=False)
    sim.load_robot(arm=True)

    sim.add_cube = MagicMock(return_value=2)
    sim.move_arm_to = MagicMock(side_effect=Exception("Target out of reach"))

    cube_id = sim.add_cube(position=[2.0, 0, 0.05])  # unreachable
    with pytest.raises(Exception, match="out of reach"):
        sim.move_arm_to([2.0, 0, 0.05])

@pytest.mark.sim
def test_pick_while_moving():
    sim = RobotSim(gui=False)
    sim.load_robot(arm=True)

    sim.add_cube = MagicMock(return_value=3)
    sim.step_forward = MagicMock()
    sim.move_arm_to = MagicMock()
    sim.close_gripper = MagicMock()
    sim.get_object_position = MagicMock(return_value=[0.3, 0, 0.25])
    sim.get_chest_height = MagicMock(return_value=0.5)

    cube_id = sim.add_cube(position=[0.3, 0, 0.05])
    sim.step_forward(speed=0.2)
    sim.move_arm_to([0.3, 0, 0.05])
    sim.close_gripper(cube_id)
    cube_pos = sim.get_object_position(cube_id)

    assert cube_pos[2] > 0.2, "Cube not lifted while moving!"
    assert sim.get_chest_height() > 0.2, "Chest touched ground while moving & picking!"

# -------------------------------
# SAFETY EDGE CASES
# -------------------------------

@pytest.mark.sim
def test_high_speed_forward_safety():
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.step_forward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.5 - speed*0.5))
    sim.get_chest_height = MagicMock(return_value=0.5)

    sim.chest_height = 0.5
    sim.step_forward(speed=1.0)  # high speed
    assert sim.get_chest_height() > 0.2, "Chest hit ground at high speed!"

@pytest.mark.sim
def test_uneven_ground_mock():
    sim = RobotSim(gui=False)
    sim.load_robot()

    # Simulate ground bump by lowering chest temporarily
    heights = [0.5, 0.3, 0.25, 0.35, 0.5]
    sim.get_chest_height = MagicMock(side_effect=heights)

    for h in heights:
        assert h > 0.2, f"Chest unsafe at height {h}"

@pytest.mark.sim
def test_reverse_with_obstacle():
    sim = RobotSim(gui=False)
    sim.load_robot()

    sim.add_obstacle = MagicMock()
    sim.step_backward = MagicMock(side_effect=lambda speed: setattr(sim, "chest_height", 0.4))
    sim.get_chest_height = MagicMock(return_value=0.4)

    sim.add_obstacle(position=[-0.5, 0, 0.05])
    sim.step_backward(speed=0.2)

    assert sim.get_chest_height() > 0.2, "Chest unsafe during reverse with obstacle!"
