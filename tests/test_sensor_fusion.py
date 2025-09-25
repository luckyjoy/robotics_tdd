# tests/test_sensor_fusion.py
import pytest
from simulation.sensors import KalmanFilter

@pytest.mark.sim
@pytest.mark.sensors
def test_kalman_filter_accuracy():
    kf = KalmanFilter(initial_state=0)

    measurements = [0.1, 0.2, 0.15, 0.3, 0.25]
    estimates = []

    for m in measurements:
        estimates.append(kf.update(m))

    # Kalman filter should converge near measurement mean
    mean_measurement = sum(measurements) / len(measurements)
    assert abs(estimates[-1] - mean_measurement) < 0.05, "Kalman filter did not converge correctly!"
