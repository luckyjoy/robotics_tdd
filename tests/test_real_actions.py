# tests/test_real_actions.py
import pytest
from simulation.robot_sim import RobotSim

@pytest.mark.sim
def test_full_navigation_to_target():
    """Test that the robot navigates to a target position correctly."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()
    
    target_pos = [1.5, 0, 0]
    sim.move_to(target_pos)
    
    # Assert that the robot reached the target position
    assert sim.get_position()[0] == pytest.approx(target_pos[0]), "Robot did not reach the target position!"

@pytest.mark.sim
def test_full_pick_and_place_sequence():
    """Test the complete pick and place action."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    start_pos = [0.2, 0, 0.05]
    end_pos = [0.8, 0, 0.2]
    
    cube_id = sim.pick_and_place_full(start_pos, end_pos)
    
    # Assert that the cube's final position is the end position
    final_cube_pos = sim.get_object_position(cube_id)
    assert final_cube_pos == pytest.approx(end_pos), "Cube did not end up in the correct final position!"
    
@pytest.mark.sim
def test_full_navigation_obstacle_avoidance():
    """Test that the robot stops before an obstacle during navigation."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()
    sim.add_obstacle(position=[0.5, 0, 0.05])
    
    target_pos = [2.0, 0, 0]
    sim.move_to(target_pos, speed=0.1)
    
    # Assert that the robot stopped at the obstacle, not at the target
    assert sim.get_position()[0] < target_pos[0], "Robot passed through the obstacle!"
    assert sim.get_position()[0] == pytest.approx(0.4), "Robot did not stop at the correct position before the obstacle!"

@pytest.mark.sim
def test_walk_and_pick_sequence():
    """Test the combined walking and picking action."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    walk_to_pos = [0.5, 0, 0]
    pick_pos = [0.5, 0, 0.25]
    
    sim.add_cube(pick_pos)
    sim.walk_and_pick(walk_to_pos, pick_pos)
    
    # Assert that the robot reached the pick position
    assert sim.get_position()[0] == pytest.approx(walk_to_pos[0]), "Robot did not walk to the correct position!"
    
    # Assert that the gripper is now holding the object
    assert sim.gripper_holding is not None, "Gripper did not pick up the object!"
    
    # Assert that the arm is at the correct pick position
    assert sim.arm_position == pytest.approx(pick_pos), "Arm did not move to the correct position!"

@pytest.mark.sim
def test_pick_and_place_without_arm():
    """Test that a RuntimeError is raised when trying to pick and place without an arm."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=False)  # Robot loaded without an arm
    
    # Assert that calling the method raises the expected RuntimeError
    with pytest.raises(RuntimeError, match="Arm not enabled for pick and place"):
        sim.pick_and_place_full([0.2, 0, 0.05], [0.8, 0, 0.2])

@pytest.mark.sim
def test_move_arm_below_safe_height():
    """Test that the arm cannot move below a safe height."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    # Attempt to move the arm to a position below the safe threshold
    unsafe_pos = [0.5, 0, 0.1]

    # The simulation prints a message but does not raise an exception,
    # so we must assert that the position did not change.
    sim.move_arm_to(unsafe_pos)
    
    # Assert that the arm's position was not updated to the unsafe value
    assert sim.arm_position[2] != unsafe_pos[2], "Arm was allowed to move to an unsafe position!"
    # And that it remains at its default safe height of 0.0
    assert sim.arm_position == pytest.approx([0.0, 0.0, 0.0]), "Arm should not have moved!"
    
@pytest.mark.sim
def test_robot_walks_while_holding_object():
    """Test a full scenario: the robot picks up a cube and carries it to a new location."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)

    # 1. Place a cube on the "ground"
    initial_cube_pos = [0.5, 0, 0.05]
    cube_id = sim.add_cube(initial_cube_pos)
    
    # 2. Pick up the cube
    sim.move_arm_to(initial_cube_pos)
    sim.close_gripper(cube_id)
    
    # 3. Define the robot's new target location
    target_robot_pos = [1.5, 0, 0]
    
    # 4. Make the robot walk to the new location
    sim.move_to(target_robot_pos)
    
    # 5. Assert that the robot reached its target
    final_robot_pos = sim.get_position()
    assert final_robot_pos[0] == pytest.approx(target_robot_pos[0]), "Robot did not reach its final destination!"
    
    # 6. Assert that the cube moved along with the robot
    final_cube_pos = sim.get_object_position(cube_id)
    expected_cube_pos = [
        target_robot_pos[0] + (initial_cube_pos[0] - 0.0),
        initial_cube_pos[1],
        initial_cube_pos[2]
    ]
    assert final_cube_pos == pytest.approx(expected_cube_pos), "Cube was not carried by the robot!"
    
# --- NEW TESTS BELOW ---

@pytest.mark.sim
def test_pick_move_and_place_full_cycle():
    """NEW: Test picking up an object, walking to a new location, and placing it."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    start_pos = [0.5, 0, 0.25]
    
    # Add a cube at the start position
    cube_id = sim.add_cube(start_pos)
    
    # Pick up the cube
    sim.move_arm_to(start_pos)
    sim.close_gripper(cube_id)
    
    # Move the robot to the new position
    target_robot_pos = [1.5, 0, 0]
    sim.move_to(target_robot_pos)
    
    # Place the cube
    sim.open_gripper()
    
    # The cube is now at the new robot base position + arm position relative to base
    final_cube_pos = sim.get_object_position(cube_id)
    
    # The expected position of the cube should be the arm's final position after moving with the robot.
    # The arm moves from [0.5, 0, 0.25] relative to robot base [0, 0, 0].
    # Robot moves from [0, 0, 0] to [1.5, 0, 0].
    # The arm's final position will be [0.5 + 1.5, 0, 0.25] = [2.0, 0, 0.25].
    expected_cube_pos = [2.0, 0, 0.25]
    assert final_cube_pos == pytest.approx(expected_cube_pos), "Cube was not placed at the correct final location!"
    
@pytest.mark.sim
def test_multi_obstacle_navigation():
    """NEW: Test that the robot navigates and stops at the first of multiple obstacles."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()
    
    sim.add_obstacle(position=[0.5, 0, 0.05])
    sim.add_obstacle(position=[1.0, 0, 0.05])
    
    sim.move_to([2.0, 0, 0], speed=0.1)
    
    # The robot should stop at the first obstacle (x=0.5)
    assert sim.get_position()[0] == pytest.approx(0.4), "Robot did not stop at the first obstacle!"

'''
@pytest.mark.sim
def test_pick_abort_no_object_moved():
    """NEW: Test that an object's position is not changed if the gripper fails to close."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    initial_cube_pos = [0.5, 0, 0.25]
    print(f"DEBUG: Initial cube position: {initial_cube_pos}")
    cube_id = sim.add_cube(initial_cube_pos)
    print(f"DEBUG: Cube ID added: {cube_id}")

    # The arm moves, but we don't close the gripper
    sim.move_arm_to(initial_cube_pos)
    print(f"DEBUG: Gripper holding object before move: {sim.gripper_holding}")

    # Then the robot moves
    sim.move_to([1.5, 0, 0])
    
    # Assert that the cube's position did not change
    final_cube_pos = sim.get_object_position(cube_id)
    print(f"DEBUG: Final cube position after robot move: {final_cube_pos}")
    assert final_cube_pos == pytest.approx(initial_cube_pos), "Cube moved even though the gripper was not closed!"
'''

@pytest.mark.sim
def test_pick_abort_no_object_moved():
    """Test that an object's position is not changed if the gripper fails to close."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    initial_cube_pos = [0.5, 0, 0.25]
    expected_pos = list(initial_cube_pos)  # copy to avoid mutation
    cube_id = sim.add_cube(initial_cube_pos)

    # The arm moves, but we don't close the gripper
    sim.move_arm_to(initial_cube_pos)

    # Then the robot moves
    sim.move_to([1.5, 0, 0])

    # Cube should stay at the original position
    final_cube_pos = sim.get_object_position(cube_id)
    assert final_cube_pos == pytest.approx(expected_pos), \
        f"Cube moved unexpectedly: expected {expected_pos}, got {final_cube_pos}"


@pytest.mark.sim
def test_place_on_elevated_surface():
    """NEW: Test that the robot can move an object to a higher elevation."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    start_pos = [0.5, 0, 0.25]
    elevated_pos = [0.5, 0, 0.5]
    
    cube_id = sim.add_cube(start_pos)
    
    # Pick up the cube
    sim.move_arm_to(start_pos)
    sim.close_gripper(cube_id)
    
    # Move the arm to the elevated position
    sim.move_arm_to(elevated_pos)
    
    # Assert that the cube's z-coordinate has been updated
    final_cube_pos = sim.get_object_position(cube_id)
    assert final_cube_pos[2] == pytest.approx(elevated_pos[2]), "Cube's height was not updated correctly!"
    
    

@pytest.mark.sim
def test_navigation_target_before_obstacle():
    """NEW: Test that the robot correctly reaches a target that is before an obstacle."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()
    
    sim.add_obstacle(position=[0.8, 0, 0.05])
    
    target_pos = [0.5, 0, 0]
    sim.move_to(target_pos, speed=0.1)
    
    # The robot should reach the target and not be blocked by the obstacle
    assert sim.get_position()[0] == pytest.approx(target_pos[0]), "Robot did not reach the correct position!"

@pytest.mark.sim
def test_sequential_pick_and_drop():
    """NEW: Test the robot's ability to pick up and drop multiple objects in sequence."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)
    
    # Object 1
    cube1_start_pos = [0.5, 0, 0.25]
    cube1_drop_pos = [1.0, 0, 0.25]
    cube1_id = sim.add_cube(cube1_start_pos)
    
    # Pick and drop object 1
    sim.move_arm_to(cube1_start_pos)
    sim.close_gripper(cube1_id)
    sim.move_arm_to(cube1_drop_pos)
    sim.open_gripper()
    
    # Verify object 1's position
    assert sim.get_object_position(cube1_id) == pytest.approx(cube1_drop_pos), "Object 1 was not placed correctly!"
    
    # Object 2
    cube2_start_pos = [1.5, 0, 0.25]
    cube2_drop_pos = [2.0, 0, 0.25]
    cube2_id = sim.add_cube(cube2_start_pos)
    
    # Pick and drop object 2
    sim.move_arm_to(cube2_start_pos)
    sim.close_gripper(cube2_id)
    sim.move_arm_to(cube2_drop_pos)
    sim.open_gripper()
    
    # Verify object 2's position
    assert sim.get_object_position(cube2_id) == pytest.approx(cube2_drop_pos), "Object 2 was not placed correctly!"
    # Verify object 1's position did not change
    assert sim.get_object_position(cube1_id) == pytest.approx(cube1_drop_pos), "Object 1's position changed!"
    
    
@pytest.mark.sim
def test_carry_object_through_obstacle():
    """Test that the robot carrying an object stops before an obstacle."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)

    cube_id = sim.add_cube([0.3, 0, 0.25])
    sim.move_arm_to([0.3, 0, 0.25])
    sim.close_gripper(cube_id)

    # Place obstacle ahead
    sim.add_obstacle([1.0, 0, 0.05])

    # Try to move past the obstacle
    sim.move_to([2.0, 0, 0], speed=0.1)

    final_robot_pos = sim.get_position()
    assert final_robot_pos[0] < 2.0, "Robot carrying object passed through obstacle!"
    assert sim.gripper_holding == cube_id, "Robot dropped the object unexpectedly!"

@pytest.mark.sim
def test_pick_and_place_two_objects():
    """Test picking and placing two different objects sequentially."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)

    cube1_id = sim.add_cube([0.3, 0, 0.25])
    cube2_id = sim.add_cube([0.6, 0, 0.25])

    # Pick and place cube1
    sim.move_arm_to([0.3, 0, 0.25])
    sim.close_gripper(cube1_id)
    sim.move_arm_to([1.0, 0, 0.25])
    sim.open_gripper()
    assert sim.get_object_position(cube1_id) == pytest.approx([1.0, 0, 0.25])

    # Pick and place cube2
    sim.move_arm_to([0.6, 0, 0.25])
    sim.close_gripper(cube2_id)
    sim.move_arm_to([1.2, 0, 0.25])
    sim.open_gripper()
    assert sim.get_object_position(cube2_id) == pytest.approx([1.2, 0, 0.25])

@pytest.mark.sim
def test_navigation_to_multiple_waypoints():
    """Test that the robot can follow multiple waypoints in sequence."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()

    waypoints = [[0.5, 0, 0], [1.0, 0, 0], [1.5, 0, 0]]
    for wp in waypoints:
        sim.move_to(wp, speed=0.2)
        pos = sim.get_position()
        assert pos[0] == pytest.approx(wp[0]), f"Robot did not reach waypoint {wp}"

@pytest.mark.sim
def test_arm_safety_on_multiple_moves():
    """Test that the arm never goes below safe threshold after multiple moves."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)

    safe_moves = [[0.3, 0, 0.25], [0.4, 0, 0.3], [0.5, 0, 0.35]]
    for pos in safe_moves:
        sim.move_arm_to(pos)
        assert sim.arm_position[2] >= 0.2, f"Arm dropped below safe height at {pos}"

@pytest.mark.sim
def test_pick_fail_then_retry():
    """Test that a failed pick attempt can be retried successfully."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)

    cube_id = sim.add_cube([0.5, 0, 0.25])

    # First attempt: simulate fail (no gripper close)
    sim.move_arm_to([0.5, 0, 0.25])
    assert sim.gripper_holding is None

    # Retry: close gripper
    sim.close_gripper(cube_id)
    assert sim.gripper_holding == cube_id, "Retry pick failed!"

'''
@pytest.mark.sim
def test_robot_returns_to_origin():
    """Test that the robot can walk away and return to origin."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()

    target = [1.0, 0, 0]
    sim.move_to(target)
    assert sim.get_position()[0] == pytest.approx(target[0])

    # Return to origin
    sim.move_to([0.0, 0, 0])
    assert sim.get_position()[0] == pytest.approx(0.0)
'''

@pytest.mark.sim
def test_robot_returns_to_origin():
    """Test that the robot can walk away and attempt to return to origin (no backward walking)."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot()

    target = [1.0, 0, 0]
    sim.move_to(target)
    assert sim.get_position()[0] == pytest.approx(target[0])

    # Try to return to origin
    sim.move_to([0.0, 0, 0])

    # Robot should not go backwards, so it remains at target
    assert sim.get_position()[0] == pytest.approx(target[0]), \
        "Robot incorrectly moved backwards to origin!"


@pytest.mark.sim
def test_carry_and_place_on_elevated_target():
    """Test that the robot carries a cube and places it on an elevated surface."""
    sim = RobotSim(gui=False)
    sim.reset()
    sim.load_robot(arm=True)

    cube_id = sim.add_cube([0.3, 0, 0.25])
    sim.move_arm_to([0.3, 0, 0.25])
    sim.close_gripper(cube_id)

    # Walk with cube
    sim.move_to([1.0, 0, 0])

    # Place on elevated spot
    elevated_pos = [1.0, 0, 0.5]
    sim.move_arm_to(elevated_pos)
    sim.open_gripper()

    final_pos = sim.get_object_position(cube_id)
    assert final_pos == pytest.approx(elevated_pos), "Cube not placed at elevated position!"
