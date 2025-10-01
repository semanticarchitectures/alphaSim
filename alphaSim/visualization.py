"""
Visualization tools for alphaSim
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import List, Dict


def plot_simulation_map(simulation, observations, figsize=(12, 10)):
    """
    Plot a map showing the simulation area, sensors, and aircraft trajectory.

    Args:
        simulation: Simulation object
        observations: List of observation dictionaries from simulation.run()
        figsize: Figure size tuple
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Plot 1: Map view
    ax1.set_xlabel('Longitude (degrees)')
    ax1.set_ylabel('Latitude (degrees)')
    ax1.set_title('Simulation Area: Washington, DC')
    ax1.grid(True, alpha=0.3)

    # Draw simulation bounds
    bounds = simulation.bounds
    ax1.plot([bounds[2], bounds[3], bounds[3], bounds[2], bounds[2]],
             [bounds[0], bounds[0], bounds[1], bounds[1], bounds[0]],
             'k--', alpha=0.3, label='Simulation bounds')

    # Plot sensors
    for sensor in simulation.sensors:
        ax1.plot(sensor.position[1], sensor.position[0], 'rs',
                markersize=12, label=f'Sensor {sensor.id}')
        # Draw sensor range circle
        circle = Circle((sensor.position[1], sensor.position[0]),
                       sensor.max_range / 111000,  # Convert meters to degrees (approximate)
                       fill=False, color='red', alpha=0.2, linestyle='--')
        ax1.add_patch(circle)

    # Plot aircraft trajectories
    colors = ['blue', 'green', 'orange', 'purple', 'cyan']
    for idx, aircraft in enumerate(simulation.aircraft):
        trajectory = aircraft.get_trajectory()
        color = colors[idx % len(colors)]

        # Plot full trajectory
        ax1.plot(trajectory[:, 1], trajectory[:, 0],
                color=color, alpha=0.6, linewidth=2, label=f'Aircraft {aircraft.id}')

        # Mark start and end
        ax1.plot(trajectory[0, 1], trajectory[0, 0], 'o',
                color=color, markersize=8, markeredgecolor='black', markeredgewidth=1)
        ax1.plot(trajectory[-1, 1], trajectory[-1, 0], '^',
                color=color, markersize=10, markeredgecolor='black', markeredgewidth=1)

    ax1.legend(loc='best', fontsize=8)
    ax1.set_aspect('equal', adjustable='box')

    # Plot 2: Altitude profile
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Altitude (meters)')
    ax2.set_title('Aircraft Altitude Over Time')
    ax2.grid(True, alpha=0.3)

    for idx, aircraft in enumerate(simulation.aircraft):
        trajectory = aircraft.get_trajectory()
        times = np.arange(len(trajectory)) * (observations[-1]['time'] / len(trajectory))
        color = colors[idx % len(colors)]
        ax2.plot(times, trajectory[:, 2], color=color,
                linewidth=2, label=f'Aircraft {aircraft.id}')

    ax2.legend(loc='best')

    plt.tight_layout()
    return fig


def plot_observations_vs_truth(simulation, observations, figsize=(14, 10)):
    """
    Plot observations vs truth data for position and distance.

    Args:
        simulation: Simulation object
        observations: List of observation dictionaries from simulation.run()
        figsize: Figure size tuple
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # Organize data by sensor and aircraft
    for sensor in simulation.sensors:
        sensor_data = {
            'times': [],
            'observed_distances': [],
            'true_distances': [],
            'observed_positions': [],
            'true_positions': [],
            'qualities': []
        }

        for obs_record in observations:
            time = obs_record['time']
            sensor_obs = obs_record['observations'].get(sensor.id, [])

            for obs in sensor_obs:
                aircraft_id = obs['aircraft_id']
                # Find the aircraft
                aircraft = next((a for a in simulation.aircraft if a.id == aircraft_id), None)
                if aircraft:
                    sensor_data['times'].append(time)
                    sensor_data['observed_distances'].append(obs['distance'])
                    sensor_data['observed_positions'].append(obs['position'])
                    sensor_data['qualities'].append(obs['quality'])

                    # Calculate true distance at this time
                    true_dist = np.linalg.norm(obs['position'] - sensor.position)
                    sensor_data['true_distances'].append(true_dist)
                    sensor_data['true_positions'].append(obs['position'])

        if not sensor_data['times']:
            continue

        times = np.array(sensor_data['times'])
        obs_dist = np.array(sensor_data['observed_distances'])
        true_dist = np.array(sensor_data['true_distances'])
        qualities = np.array(sensor_data['qualities'])

        # Plot 1: Distance over time
        ax = axes[0, 0]
        ax.plot(times, obs_dist, 'o-', alpha=0.6, markersize=3, label=f'{sensor.id} (observed)')
        ax.plot(times, true_dist, '--', alpha=0.8, label=f'{sensor.id} (truth)')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Distance (meters)')
        ax.set_title('Sensor-to-Aircraft Distance')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=8)

        # Plot 2: Observation quality over time
        ax = axes[0, 1]
        ax.plot(times, qualities, 'o-', alpha=0.6, markersize=3, label=f'{sensor.id}')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Observation Quality (0-1)')
        ax.set_title('Observation Quality Over Time')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=8)
        ax.set_ylim([0, 1.1])

        # Plot 3: Distance error
        ax = axes[1, 0]
        distance_error = obs_dist - true_dist
        ax.plot(times, distance_error, 'o-', alpha=0.6, markersize=3, label=f'{sensor.id}')
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Distance Error (meters)')
        ax.set_title('Observation Error (Observed - Truth)')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=8)

        # Plot 4: Quality vs Distance
        ax = axes[1, 1]
        scatter = ax.scatter(true_dist, qualities, c=times, cmap='viridis',
                           alpha=0.6, s=20, label=f'{sensor.id}')
        ax.set_xlabel('True Distance (meters)')
        ax.set_ylabel('Observation Quality (0-1)')
        ax.set_title('Quality vs Distance (colored by time)')
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.1])
        plt.colorbar(scatter, ax=ax, label='Time (s)')

    plt.tight_layout()
    return fig


def save_plots(simulation, observations, output_dir='outputs'):
    """
    Generate and save all plots.

    Args:
        simulation: Simulation object
        observations: List of observation dictionaries
        output_dir: Directory to save plots
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Generate and save map
    fig1 = plot_simulation_map(simulation, observations)
    fig1.savefig(f'{output_dir}/simulation_map.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/simulation_map.png")

    # Generate and save observations plot
    fig2 = plot_observations_vs_truth(simulation, observations)
    fig2.savefig(f'{output_dir}/observations_vs_truth.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/observations_vs_truth.png")

    plt.close('all')
