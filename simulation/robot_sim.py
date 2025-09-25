# simulation/robot_sim.py

class RobotSim:
    def __init__(self, gui=False):
        self.gui = gui
        self.walking = False
        self.crouched = False
        self.object_position = (0, 0, 0)
        self.gripper_blocked = False
        self.holding_object = False

    # Position
    def set_position(self, x, y, z):
        """Explicitly set the robot's position."""
        self.object_position = (x, y, z)

    # Walking
    def start_walking(self):
        self.walking = True

    def crouch_until_chest_touches_ground(self):
        self.crouched = True


    def move_forward(self, distance):
        x, y, z = self.object_position
        # Move along Y-axis for forward
        self.object_position = (x, y + distance, z)

    def move_backward(self, distance):
        x, y, z = self.object_position
        # Move along Y-axis for backward
        self.object_position = (x, y - distance, z)
        
    # Pick and Place
    def pick_object(self):
        if self.gripper_blocked:
            self.holding_object = False
            return False
        self.holding_object = True
        return True

    def move_object_to(self, x, y, z):
        if self.holding_object:
            self.object_position = (x, y, z)
            return True
        return False

    # Gripper state
    def block_gripper(self):
        self.gripper_blocked = True

    def unblock_gripper(self):
        self.gripper_blocked = False
