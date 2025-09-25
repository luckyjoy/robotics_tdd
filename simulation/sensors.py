# simulation/sensors.py

import random

class Sensor:
    """Simple sensor model with Gaussian noise."""
    def __init__(self, noise=0.0):
        self.noise = noise

    def read(self, true_value: float) -> float:
        """Return sensor reading with noise applied."""
        return true_value + random.gauss(0, self.noise)


class KalmanFilter:
    """Basic 1D Kalman filter."""
    def __init__(self, process_variance=1e-5, measurement_variance=1e-2, initial_estimate=0.0, initial_error=1.0):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimate = initial_estimate
        self.error_estimate = initial_error

    def update(self, measurement: float) -> float:
        # Prediction step
        self.error_estimate += self.process_variance

        # Kalman gain
        kalman_gain = self.error_estimate / (self.error_estimate + self.measurement_variance)

        # Correction step
        self.estimate = self.estimate + kalman_gain * (measurement - self.estimate)

        # Update error estimate
        self.error_estimate = (1 - kalman_gain) * self.error_estimate

        return self.estimate
