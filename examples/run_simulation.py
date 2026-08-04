"""
Track Digital Operations Sandbox (TDOS)

run_simulation.py

Example demonstrating a complete TDOS simulation.
"""

from tdos.interfaces.simulation_api import SimulationAPI
from tdos.models.simulation import SimulationConfig


def main() -> None:

    simulation = SimulationAPI()

    config = SimulationConfig(
        simulation_name="Demo Simulation",
        duration_steps=100,
        timestep_seconds=1,
    )

    simulation.create(config)

    simulation.start()

    simulation.run()

    results = simulation.results()

    print("\nSimulation Complete\n")

    print(results)


if __name__ == "__main__":

    main()
