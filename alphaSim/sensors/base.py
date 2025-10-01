"""
Base sensor class
"""

import numpy as np
from typing import Optional, Tuple


class Sensor:
    """
    Base class for all sensor types.
    """

    def __init__(self, sensor_id: str, position: Tuple[float, float, float],
                 max_range: float, field_of_view: float):
        """
        Initialize a sensor.

        Args:
            sensor_id: Unique identifier for the sensor
            position: (latitude, longitude, altitude) in degrees and meters
            max_range: Maximum detection range in meters
            field_of_view: Field of view in degrees
        """
        self.id = sensor_id
        self.position = np.array(position)
        self.max_range = max_range
        self.field_of_view = field_of_view

    def observe(self, aircraft, terrain_data) -> Optional[dict]:
        """
        Attempt to observe an aircraft.

        Args:
            aircraft: Aircraft object to observe
            terrain_data: Terrain elevation data

        Returns:
            Observation dictionary with quality metrics, or None if not detected
        """
        # Calculate distance to aircraft
        distance = self._calculate_distance(aircraft.position)

        # Check if within range
        if distance > self.max_range:
            return None

        # Check if within field of view
        if not self._in_field_of_view(aircraft.position):
            return None

        # Check line of sight (terrain occlusion)
        if not self._has_line_of_sight(aircraft.position, terrain_data):
            return None

        # Calculate observation quality
        quality = self._calculate_quality(distance, aircraft)

        return {
            'sensor_id': self.id,
            'aircraft_id': aircraft.id,
            'distance': distance,
            'quality': quality,
            'position': aircraft.position.copy()
        }

    def _calculate_distance(self, target_position: np.ndarray) -> float:
        """Calculate distance to target in meters"""
        # Simplified distance calculation (should use proper geodetic distance)
        return np.linalg.norm(self.position - target_position)

    def _in_field_of_view(self, target_position: np.ndarray) -> bool:
        """Check if target is within sensor's field of view"""
        # Simplified FOV check
        return True  # To be implemented by subclasses

    def _has_line_of_sight(self, target_position: np.ndarray,
                           terrain_data) -> bool:
        """Check if there is clear line of sight to target"""
        # Simplified LOS check (should check terrain occlusion)
        return True  # To be implemented with terrain data

    def _calculate_quality(self, distance: float, aircraft) -> float:
        """
        Calculate observation quality (0-1).

        Quality decreases with distance and can be affected by other factors.
        """
        # Simple distance-based quality
        quality = 1.0 - (distance / self.max_range)
        return max(0.0, min(1.0, quality))
