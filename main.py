"""
Main simulation script for the Port Digital Twin.
Creates a port, boats, and trips, and simulates operations.
"""

from datetime import datetime, timedelta
import logging
import coloredlogs
from simulation.port import Port
from simulation.boat import Boat
from simulation.trip import Trip

# Setup logging
logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO", logger=logger, fmt='%(asctime)s %(levelname)s %(message)s')


def create_boats() -> list:
    """
    Creates and returns a list of sample boats.
    """
    specs1 = {
        "battery_capacity_wh": 80000,
        "charging_rate_w": 10000,
        "soc_percent": 80,
        "length": 8.5,
        "width": 2.4,
        "passenger_capacity": 12,
        "cruise_speed_kmh": 25,
        "base_consumption_wh_per_km": 300,
        "motor_power_w": 40000,
        "motor_efficiency": 0.9,
    }

    specs2 = specs1.copy()
    specs2["battery_capacity_wh"] = 100000
    specs2["name"] = "Boat 2"

    return [
        Boat("EcoWave", specs1),
        Boat("SeaVolt", specs2),
    ]


def create_trips() -> list:
    """
    Creates and returns a list of sample trips.
    """
    now = datetime.now()
    return [
        Trip(now + timedelta(hours=1), now + timedelta(hours=2), 10000),  # 10 km
        Trip(now + timedelta(hours=3), now + timedelta(hours=4), 15000),  # 15 km
    ]


def main():
    """
    Entry point for the simulation.
    """
    logger.info("🚢 Starting Port Simulation...")

    # 1. Create port
    power_config = {
        "site_max_power_w": 20000,
        "charger_max_power_w": 10000,
    }
    port = Port("Marina Verde", capacity=5, lat=38.72, lon=-9.14, power_settings=power_config, num_chargers=2)

    # 2. Create and register boats
    boats = create_boats()
    for boat in boats:
        port.add_boat(boat)
    logger.info("✅ Registered %s boats at port '%s'", len(boats), port.name)

    # 3. Create trips
    trips = create_trips()

    # 4. Assign trips to boats (round-robin)
    for i, trip in enumerate(trips):
        boat = boats[i % len(boats)]
        trip.assign_boat(boat)
        logger.info("🛳️  Trip %s assigned to %s — Distance: %.1f km", i + 1, boat.name, trip.distance_m / 1000)

    # 5. Simulate each trip
    for trip in trips:
        trip.simulate_trip()
        logger.info("⚡ %s used ~%.0f Wh — New SoC: %.1f%%", trip.boat.name, trip.actual_energy_wh, trip.boat.soc_percent)

    # 6. Simulate 1 hour of charging
    logger.info("🔌 Charging for 1 hour...")
    port.simulate_charging(time_s=3600)

    # 7. Show updated SoC
    for boat in boats:
        logger.info("🔋 %s SoC after charging: %.1f%%", boat.name, boat.soc_percent)

    logger.info("✅ Simulation Complete!")


if __name__ == "__main__":
    main()
