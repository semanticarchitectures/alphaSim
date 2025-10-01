"""
Main simulation engine for alphaSim
"""

import numpy as np
from typing import List, Dict, Tuple


class Simulation:
    """
    Main simulation class that manages the 3D world, sensors, and aircraft.
    """

    def __init__(self, bounds: Tuple[float, float, float, float] = None):
        """
        Initialize the simulation.

        Args:
            bounds: Geographic bounds (min_lat, max_lat, min_lon, max_lon) for DC area
        """
        # Default to Washington, DC area
        self.bounds = bounds or (38.8, 39.0, -77.2, -76.9)
        self.sensors = []
        self.aircraft = []
        self.terrain_data = None
        self.time = 0.0

    def add_sensor(self, sensor):
        """Add a sensor to the simulation"""
        self.sensors.append(sensor)

    def add_aircraft(self, aircraft):
        """Add an aircraft to the simulation"""
        self.aircraft.append(aircraft)

    def load_terrain(self, terrain_data):
        """Load terrain data for the simulation area"""
        self.terrain_data = terrain_data

    def step(self, dt: float):
        """
        Advance the simulation by one time step.

        Args:
            dt: Time step in seconds
        """
        self.time += dt

        # Update aircraft positions
        for aircraft in self.aircraft:
            aircraft.update(dt)

        # Calculate sensor observations
        observations = self._calculate_observations()

        return observations

    def _calculate_observations(self) -> Dict:
        """
        Calculate what each sensor observes.

        Returns:
            Dictionary mapping sensor IDs to observations
        """
        observations = {}

        for sensor in self.sensors:
            sensor_obs = []
            for aircraft in self.aircraft:
                obs = sensor.observe(aircraft, self.terrain_data)
                if obs is not None:
                    sensor_obs.append(obs)
            observations[sensor.id] = sensor_obs

        return observations

    def run(self, duration: float, dt: float = 0.1):
        """
        Run the simulation for a specified duration.

        Args:
            duration: Total simulation time in seconds
            dt: Time step in seconds
        """
        steps = int(duration / dt)
        all_observations = []

        for _ in range(steps):
            obs = self.step(dt)
            all_observations.append({
                'time': self.time,
                'observations': obs
            })

        return all_observations
