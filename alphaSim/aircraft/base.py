"""
Base aircraft class
"""

import numpy as np
from typing import Tuple


class Aircraft:
    """
    Base class for aircraft in the simulation.
    """

    def __init__(self, aircraft_id: str, initial_position: Tuple[float, float, float],
                 velocity: Tuple[float, float, float]):
        """
        Initialize an aircraft.

        Args:
            aircraft_id: Unique identifier
            initial_position: (latitude, longitude, altitude) in degrees and meters
            velocity: (lat_velocity, lon_velocity, alt_velocity) in m/s
        """
        self.id = aircraft_id
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.trajectory = [self.position.copy()]

    def update(self, dt: float):
        """
        Update aircraft position based on velocity.

        Args:
            dt: Time step in seconds
        """
        # Simple kinematic update (should use proper geodetic calculations)
        self.position += self.velocity * dt
        self.trajectory.append(self.position.copy())

    def set_velocity(self, velocity: Tuple[float, float, float]):
        """Set new velocity vector"""
        self.velocity = np.array(velocity, dtype=float)

    def get_trajectory(self) -> np.ndarray:
        """Get the aircraft's trajectory history"""
        return np.array(self.trajectory)
