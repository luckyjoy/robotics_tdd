# tests/test_real_actions.py
import pytest
from simulation.robot_sim import RobotSim

# -------------------------
# Navigation Suite
# -------------------------
@pytest.mark.sim
@pytest.mark.actions  # High-level suite marker
@pytest.mark.navigation
class TestNavigationSuite:

    def test_full_navigation_to_target(self):
        """Test that the robot navigates to a target position correctly."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot()
        
        target_pos = [1.5, 0, 0]
        sim.move_to(target_pos)
        assert sim.get_position()[0] == pytest.approx(target_pos[0]), \
            "Robot did not reach the target position!"

    def test_full_navigation_obstacle_avoidance(self):
        """Test that the robot stops before an obstacle during navigation."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot()
        sim.add_obstacle(position=[0.5, 0, 0.05])
        
        target_pos = [2.0, 0, 0]
        sim.move_to(target_pos, speed=0.1)
        assert sim.get_position()[0] < target_pos[0], "Robot passed through the obstacle!"
        assert sim.get_position()[0] == pytest.approx(0.4), "Robot did not stop at the correct position!"

    def test_multi_obstacle_navigation(self):
        """Test that the robot navigates and stops at the first of multiple obstacles."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot()
        sim.add_obstacle(position=[0.5, 0, 0.05])
        sim.add_obstacle(position=[1.0, 0, 0.05])
        sim.move_to([2.0, 0, 0], speed=0.1)
        assert sim.get_position()[0] == pytest.approx(0.4), "Robot did not stop at the first obstacle!"

    def test_navigation_target_before_obstacle(self):
        """Test that the robot correctly reaches a target that is before an obstacle."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot()
        sim.add_obstacle(position=[0.8, 0, 0.05])
        target_pos = [0.5, 0, 0]
        sim.move_to(target_pos, speed=0.1)
        assert sim.get_position()[0] == pytest.approx(target_pos[0]), "Robot did not reach the correct position!"

    def test_navigation_to_multiple_waypoints(self):
        """Test that the robot can follow multiple waypoints in sequence."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot()
        waypoints = [[0.5, 0, 0], [1.0, 0, 0], [1.5, 0, 0]]
        for wp in waypoints:
            sim.move_to(wp, speed=0.2)
            pos = sim.get_position()
            assert pos[0] == pytest.approx(wp[0]), f"Robot did not reach waypoint {wp}"

    def test_robot_returns_to_origin(self):
        """Test that the robot can walk away and attempt to return to origin (no backward walking)."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot()
        target = [1.0, 0, 0]
        sim.move_to(target)
        assert sim.get_position()[0] == pytest.approx(target[0])
        sim.move_to([0.0, 0, 0])
        assert sim.get_position()[0] == pytest.approx(target[0]), "Robot incorrectly moved backwards to origin!"

# -------------------------
# Pick & Place Suite
# -------------------------
@pytest.mark.sim
@pytest.mark.actions  # High-level suite marker
@pytest.mark.pick
class TestPickPlaceSuite:

    def test_full_pick_and_place_sequence(self):
        """Test the complete pick and place action."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot(arm=True)
        start_pos = [0.2, 0, 0.05]
        end_pos = [0.8, 0, 0.2]
        cube_id = sim.pick_and_place_full(start_pos, end_pos)
        final_cube_pos = sim.get_object_position(cube_id)
        assert final_cube_pos == pytest.approx(end_pos), "Cube did not end up in the correct final position!"

    def test_walk_and_pick_sequence(self):
        """Test combined walking and picking action."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot(arm=True)
        walk_to_pos = [0.5, 0, 0]
        pick_pos = [0.5, 0, 0.25]
        sim.add_cube(pick_pos)
        sim.walk_and_pick(walk_to_pos, pick_pos)
        assert sim.get_position()[0] == pytest.approx(walk_to_pos[0]), "Robot did not walk to correct position!"
        assert sim.gripper_holding is not None, "Gripper did not pick up the object!"
        assert sim.arm_position == pytest.approx(pick_pos), "Arm did not move to correct position!"

    def test_pick_and_place_without_arm(self):
        """Test that a RuntimeError is raised when trying to pick/place without arm."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot(arm=False)
        with pytest.raises(RuntimeError, match="Arm not enabled for pick and place"):
            sim.pick_and_place_full([0.2, 0, 0.05], [0.8, 0, 0.2])

    def test_move_arm_below_safe_height(self):
        """Test that the arm cannot move below safe height."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot(arm=True)
        unsafe_pos = [0.5, 0, 0.1]
        sim.move_arm_to(unsafe_pos)
        assert sim.arm_position[2] != unsafe_pos[2], "Arm was allowed to move to unsafe position!"
        assert sim.arm_position == pytest.approx([0.0, 0.0, 0.0]), "Arm should not have moved!"

    def test_carry_object_through_obstacle(self):
        """Test that the robot carrying an object stops before an obstacle."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot(arm=True)
        cube_id = sim.add_cube([0.3, 0, 0.25])
        sim.move_arm_to([0.3, 0, 0.25])
        sim.close_gripper(cube_id)
        sim.add_obstacle([1.0, 0, 0.05])
        sim.move_to([2.0, 0, 0], speed=0.1)
        final_robot_pos = sim.get_position()
        assert final_robot_pos[0] < 2.0, "Robot carrying object passed through obstacle!"
        assert sim.gripper_holding == cube_id, "Robot dropped the object unexpectedly!"

    def test_sequential_pick_and_drop(self):
        """Test picking and dropping multiple objects in sequence."""
        sim = RobotSim(gui=False)
        sim.reset()
        sim.load_robot(arm=True)
        cube1_id = sim.add_cube([0.5, 0, 0.25])
        cube1_drop_pos = [1.0, 0, 0.25]
        sim.move_arm_to([0.5, 0, 0.25])
        sim.close_gripper(cube1_id)
        sim.move_arm_to(cube1_drop_pos)
        sim.open_gripper()
        assert sim.get_object_position(cube1_id) == pytest.approx(cube1_drop_pos)
        cube2_id = sim.add_cube([1.5, 0, 0.25])
        cube2_drop_pos = [2.0, 0, 0.25]
        sim.move_arm_to([1.5, 0, 0.25])
        sim.close_gripper(cube2_id)
        sim.move_arm_to(cube2_drop_pos)
        sim.open_gripper()
        assert sim.get_object_position(cube2_id) == pytest.approx(cube2_drop_pos)
        assert sim.get_object_position(cube1_id) == pytest.approx(cube1_drop_pos)

# -------------------------
# Additional Robot Actions Tests
# -------------------------
@pytest.mark.sim
@pytest.mark.actions
@pytest.mark.navigation
def test_robot_walk_with_variable_speeds():
    """Test that the robot can move to a target with variable speeds without falling."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()
    
    speeds = [0.1, 0.3, 0.2, 0.4]
    target_x = 0.0
    for speed in speeds:
        target_x += speed * 0.5  # Assume 0.5s per step
        sim.step_forward(speed)
        assert sim.get_chest_height() > 0.2, "Robot chest touched the ground!"
    assert sim.get_position()[0] == pytest.approx(target_x), "Robot did not move correctly with variable speeds!"

@pytest.mark.sim
@pytest.mark.actions
@pytest.mark.pick
def test_pick_and_place_multiple_cubes_in_sequence():
    """Test picking and placing multiple cubes sequentially without collisions."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    cubes = [
        ([0.3, 0, 0.25], [1.0, 0, 0.25]),
        ([0.5, 0, 0.25], [1.2, 0, 0.25]),
        ([0.7, 0, 0.25], [1.4, 0, 0.25]),
    ]
    
    for start, end in cubes:
        cube_id = sim.add_cube(start)
        sim.move_arm_to(start)
        sim.close_gripper(cube_id)
        sim.move_arm_to(end)
        sim.open_gripper()
        assert sim.get_object_position(cube_id) == pytest.approx(end), f"Cube {cube_id} not placed correctly!"

@pytest.mark.sim
@pytest.mark.actions
@pytest.mark.pick
def test_robot_pick_abort_and_retry():
    """Test that a failed pick attempt can be retried successfully."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    cube_id = sim.add_cube([0.5, 0, 0.25])
    
    # First attempt: fail (do not close gripper)
    sim.move_arm_to([0.5, 0, 0.25])
    assert sim.gripper_holding is None
    
    # Retry: close gripper
    sim.close_gripper(cube_id)
    assert sim.gripper_holding == cube_id, "Retry pick failed!"

@pytest.mark.sim
@pytest.mark.actions
@pytest.mark.navigation
def test_robot_turn_and_navigate_corner():
    """Test robot turns and navigates a corner without hitting walls."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()
    
    # Simulate a corner path
    path = [[0.5, 0, 0], [0.5, 0.5, 0], [1.0, 0.5, 0]]
    for pos in path:
        sim.move_to(pos, speed=0.1)
        assert sim.get_position()[0] == pytest.approx(pos[0]), f"Robot X did not match for {pos}"
        assert sim.get_position()[1] == pytest.approx(pos[1]), f"Robot Y did not match for {pos}"

@pytest.mark.sim
@pytest.mark.actions
@pytest.mark.pick
def test_robot_pick_and_place_on_elevated_platform():
    """Test robot lifts a cube to an elevated platform safely."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    start_pos = [0.4, 0, 0.25]
    elevated_pos = [0.8, 0, 0.5]
    
    cube_id = sim.add_cube(start_pos)
    sim.move_arm_to(start_pos)
    sim.close_gripper(cube_id)
    sim.move_to([0.8, 0, 0])
    sim.move_arm_to(elevated_pos)
    sim.open_gripper()
    
    final_pos = sim.get_object_position(cube_id)
    assert final_pos == pytest.approx(elevated_pos), "Cube not placed at elevated platform!"

@pytest.mark.sim
@pytest.mark.actions
@pytest.mark.pick
def test_robot_pick_and_place_with_obstacle_interference():
    """Test pick and place sequence with an obstacle along the path."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    cube_id = sim.add_cube([0.3, 0, 0.25])
    sim.move_arm_to([0.3, 0, 0.25])
    sim.close_gripper(cube_id)
    
    sim.add_obstacle([0.5, 0, 0.05])
    sim.move_to([1.0, 0, 0], speed=0.1)
    
    final_robot_pos = sim.get_position()
    assert final_robot_pos[0] < 1.0, "Robot passed through obstacle while carrying cube!"
    assert sim.gripper_holding == cube_id, "Cube dropped unexpectedly!"

@pytest.mark.sim
@pytest.mark.actions
@pytest.mark.pick
def test_robot_pick_place_sequential_multi_object():
    """Test pick-and-place for multiple objects sequentially ensuring positions are correct."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    positions = [
        ([0.3, 0, 0.25], [1.0, 0, 0.25]),
        ([0.5, 0, 0.25], [1.2, 0, 0.25]),
        ([0.7, 0, 0.25], [1.4, 0, 0.25])
    ]
    
    cube_ids = []
    for start, end in positions:
        cube_id = sim.add_cube(start)
        sim.move_arm_to(start)
        sim.close_gripper(cube_id)
        sim.move_arm_to(end)
        sim.open_gripper()
        cube_ids.append(cube_id)
    
    for cube_id, (_, end) in zip(cube_ids, positions):
        assert sim.get_object_position(cube_id) == pytest.approx(end), f"Cube {cube_id} not at correct final position!"

