"""
Example usage of alphaSim
"""

from alphaSim.simulation import Simulation
from alphaSim.sensors.base import Sensor
from alphaSim.aircraft.base import Aircraft
from alphaSim.terrain.loader import TerrainData
from alphaSim.visualization import save_plots
import matplotlib.pyplot as plt


def main():
    """
    Run a simple simulation example.
    """
    # Create simulation for Washington, DC area
    sim = Simulation(bounds=(38.8, 39.0, -77.2, -76.9))

    # Create and load terrain
    terrain = TerrainData(bounds=sim.bounds)
    terrain.generate_synthetic(base_elevation=50.0, variation=100.0)
    sim.load_terrain(terrain)

    # Add sensors at various locations in DC
    sensor1 = Sensor("sensor_1", position=(38.9, -77.0, 50.0),
                     max_range=10000.0, field_of_view=120.0)
    sensor2 = Sensor("sensor_2", position=(38.85, -77.1, 75.0),
                     max_range=15000.0, field_of_view=90.0)

    sim.add_sensor(sensor1)
    sim.add_sensor(sensor2)

    # Add aircraft with flight path
    aircraft1 = Aircraft("aircraft_1",
                        initial_position=(38.85, -77.15, 1000.0),
                        velocity=(0.001, 0.001, 0.0))  # Moving NE

    sim.add_aircraft(aircraft1)

    # Run simulation for 100 seconds
    print("Running simulation...")
    observations = sim.run(duration=100.0, dt=1.0)

    # Print summary
    print(f"\nSimulation completed: {len(observations)} time steps")
    print(f"Total observations recorded: {sum(len(obs['observations']) for obs in observations)}")

    # Print sample observations
    for i, obs in enumerate(observations[:5]):
        print(f"\nTime {obs['time']:.1f}s:")
        for sensor_id, sensor_obs in obs['observations'].items():
            print(f"  {sensor_id}: {len(sensor_obs)} detections")
            for detection in sensor_obs:
                print(f"    Aircraft {detection['aircraft_id']}: "
                      f"distance={detection['distance']:.1f}m, "
                      f"quality={detection['quality']:.2f}")

    # Generate and save visualizations
    print("\nGenerating visualizations...")
    save_plots(sim, observations)
    print("\nVisualization complete! Check the 'outputs' directory for plots.")


if __name__ == "__main__":
    main()
