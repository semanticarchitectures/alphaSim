"""
Terrain data loader for Washington, DC area
"""

import numpy as np
from typing import Tuple, Optional


class TerrainData:
    """
    Manages terrain elevation data for the simulation area.
    """

    def __init__(self, bounds: Tuple[float, float, float, float], resolution: float = 0.001):
        """
        Initialize terrain data.

        Args:
            bounds: (min_lat, max_lat, min_lon, max_lon)
            resolution: Grid resolution in degrees
        """
        self.bounds = bounds
        self.resolution = resolution

        # Create grid
        lat_points = int((bounds[1] - bounds[0]) / resolution)
        lon_points = int((bounds[3] - bounds[2]) / resolution)

        self.elevations = np.zeros((lat_points, lon_points))
        self.lat_grid = np.linspace(bounds[0], bounds[1], lat_points)
        self.lon_grid = np.linspace(bounds[2], bounds[3], lon_points)

    def load_from_file(self, filepath: str):
        """
        Load terrain data from a file.

        Args:
            filepath: Path to terrain data file
        """
        # Placeholder for loading real terrain data (e.g., SRTM, USGS DEM)
        pass

    def get_elevation(self, lat: float, lon: float) -> Optional[float]:
        """
        Get elevation at a specific location.

        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees

        Returns:
            Elevation in meters, or None if out of bounds
        """
        if not self._in_bounds(lat, lon):
            return None

        # Find nearest grid point
        lat_idx = np.argmin(np.abs(self.lat_grid - lat))
        lon_idx = np.argmin(np.abs(self.lon_grid - lon))

        return self.elevations[lat_idx, lon_idx]

    def _in_bounds(self, lat: float, lon: float) -> bool:
        """Check if coordinates are within terrain bounds"""
        return (self.bounds[0] <= lat <= self.bounds[1] and
                self.bounds[2] <= lon <= self.bounds[3])

    def generate_synthetic(self, base_elevation: float = 50.0, variation: float = 100.0):
        """
        Generate synthetic terrain data for testing.

        Args:
            base_elevation: Base elevation in meters
            variation: Maximum elevation variation in meters
        """
        # Simple random terrain generation for testing
        self.elevations = base_elevation + variation * np.random.random(self.elevations.shape)
