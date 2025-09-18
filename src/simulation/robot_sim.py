# src/simulation/robot_sim.py
import math

class RobotSim:
    def __init__(self, gui=True):
        self.gui = gui
        self.reset()
        self.chest_height = 0.5

    def reset(self):
        """Resets the simulator state to its initial values."""
        self.position = [0.0, 0.0, 0.0]
        self.arm_position = [0.0, 0.0, 0.0]
        self.arm_enabled = False
        self.obstacles = []
        self.objects = {}
        self.next_object_id = 1
        self.gripper_holding = None
        self.chest_height = 0.5
        print("Simulator state has been reset.")

    def load_robot(self, arm=False):
        self.arm_enabled = arm
        print(f"Robot loaded with arm={arm}")

    # --- Base movement ---
    def step_forward(self, speed=0.1):
        new_x = self.position[0] + speed
        for obs in self.obstacles:
            if new_x >= obs[0]:
                print(f"Obstacle detected at {obs}, stopping")
                return
        self.position[0] = new_x
        print(f"Robot stepped forward to {self.position}")

    def step_backward(self, speed=0.1):
        self.position[0] -= speed
        print(f"Robot stepped backward to {self.position}")
    
    def move_to(self, target_position, speed=0.1):
        """Moves robot to a target position, handling steps and obstacles."""
        print(f"Moving robot to target {target_position}...")
        while self.position[0] < target_position[0]:
            old_position = self.position[0]
            self.step_forward(speed=speed)
            
            if self.position[0] == old_position:
                print("Robot's position did not change. Assuming an obstacle blocked the path. Exiting navigation.")
                break
            
            delta_x = self.position[0] - old_position
            
            self.arm_position[0] += delta_x
            if self.gripper_holding and self.gripper_holding in self.objects:
                self.objects[self.gripper_holding]["position"][0] += delta_x
                
            if self.position[0] >= target_position[0]:
                self.position[0] = target_position[0]
                break
            
    def get_position(self):
        return self.position

    def get_chest_height(self):
        return self.chest_height
        
    def add_obstacle(self, position):
        self.obstacles.append(position)
        print(f"Added obstacle {len(self.obstacles)} at {position}")

    # --- Arm functions ---
    def move_arm_to(self, position):
        if not self.arm_enabled:
            raise RuntimeError("Arm not enabled")
        if position[2] < 0.2:
            print("Arm movement blocked: arm cannot go below z=0.2")
            return
        
        self.arm_position = position
        print(f"Arm moved to {self.arm_position}")
        if self.gripper_holding:
            self.objects[self.gripper_holding]["position"] = position

    def close_gripper(self, object_id):
        if object_id in self.objects:
            self.gripper_holding = object_id
            print(f"Gripper closed and attached object {object_id}")

    def open_gripper(self):
        if self.gripper_holding:
            print(f"Gripper released object {self.gripper_holding}")
            self.gripper_holding = None

    def pick_and_place_full(self, start_pos, end_pos):
        """Orchestrates a full pick-and-place sequence."""
        if not self.arm_enabled:
            raise RuntimeError("Arm not enabled for pick and place")
            
        print("Starting full pick and place sequence...")
        cube_id = self.add_cube(start_pos)
        self.move_arm_to(start_pos)
        self.close_gripper(cube_id)
        self.move_arm_to(end_pos)
        self.open_gripper()
        print("Pick and place sequence completed.")
        return cube_id

    def walk_and_pick(self, walk_to_pos, pick_pos):
        """Combines walking and picking an object."""
        self.move_to(walk_to_pos)
        self.move_arm_to(pick_pos)
        self.close_gripper(1)
        print("Walk and pick sequence completed.")

    # --- Objects ---
    def add_cube(self, position):
        obj_id = self.next_object_id
        self.objects[obj_id] = {"type": "cube", "position": position.copy()}
        self.next_object_id += 1
        print(f"Added cube {obj_id} at {position}")
        return obj_id

    def get_object_position(self, object_id):
        if object_id in self.objects:
            return self.objects[object_id]["position"]
        return None

    def disconnect(self):
        print("Simulator disconnected.")