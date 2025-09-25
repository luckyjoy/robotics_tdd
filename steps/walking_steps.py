# steps/walking_steps.py
import pytest

from pytest_bdd import scenarios, given, when, then, parsers
from simulation.robot_sim import RobotSim
scenarios('../features/walking.feature')


# --- Fixture for robot simulation ---
@pytest.fixture
def sim():
    return RobotSim(gui=False)

# --- GIVEN steps ---
@given(parsers.parse("a robot at position [{x:d}, {y:d}, {z:d}]"))
def robot_at_position(sim, x, y, z):
    sim.set_position(x, y, z)
    return sim

# --- WHEN steps ---
@when("the robot starts walking")
def robot_starts_walking(sim):
    sim.start_walking()

@when("the robot crouches so that its chest touches the ground")
def robot_crouch(sim):
    sim.crouch_until_chest_touches_ground()

@when(parsers.parse("the robot walks forward by {distance:d} units"))
def walk_forward(sim, distance):
    # Move along Y axis
    x, y, z = sim.object_position
    sim.object_position = (x, y + distance, z)

# --- THEN steps ---
@then("the robot should be walking")
def check_robot_walking(sim):
    assert sim.walking is True

@then("the robot should be in crouched position")
def check_robot_crouched(sim):
    assert sim.crouched is True

@then(parsers.parse("the robot should be at position [{x:d}, {y:d}, {z:d}]"))
def check_robot_position(sim, x, y, z):
    pos = sim.object_position
    assert pos == (x, y, z)
