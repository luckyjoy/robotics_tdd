# src/simulation/sensors.py

class KalmanFilter:
    def __init__(self, initial_state=0, process_noise=1e-5, measurement_noise=1e-2):
        self.state_estimate = initial_state
        self.P = 1.0
        self.Q = process_noise
        self.R = measurement_noise

    def update(self, measurement):
        # Predict
        self.P += self.Q
        # Update
        K = self.P / (self.P + self.R)
        self.state_estimate += K * (measurement - self.state_estimate)
        self.P = (1 - K) * self.P
        return self.state_estimate
