"""
Module: trip
Defines the Trip class used to simulate boat voyages and energy usage.
"""

from datetime import datetime
from typing import Optional
from simulation.boat import Boat


class Trip:
    """
    Represents a scheduled trip for a boat, including expected and actual energy usage.
    """

    def __init__(self, departure_time: datetime, arrival_time: datetime, distance_m: float):
        """
        Initializes a new Trip instance.

        Args:
            departure_time (datetime): Scheduled departure time.
            arrival_time (datetime): Scheduled arrival time.
            distance_m (float): Distance of the trip in meters.
        """
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.distance_m = distance_m
        self.duration_s = (arrival_time - departure_time).total_seconds()
        self.boat: Optional[Boat] = None
        self.expected_energy_wh: Optional[float] = None
        self.actual_energy_wh: Optional[float] = None

    def assign_boat(self, boat: Boat) -> None:
        """
        Assigns a boat to this trip and estimates the expected energy usage.

        Args:
            boat (Boat): The boat assigned to perform the trip.
        """
        self.boat = boat
        self.expected_energy_wh = boat.estimate_energy_for_trip(self.distance_m)

    def simulate_trip(self) -> None:
        """
        Simulates the trip and reduces the boat's state of charge based on energy used.

        Raises:
            RuntimeError: If no boat has been assigned to the trip.
        """
        if not self.boat:
            raise RuntimeError("Trip simulation failed: no boat assigned.")
        self.actual_energy_wh = self.expected_energy_wh # NOTE: Change this later to actual simulate things I don't know currently
        energy_ratio = self.actual_energy_wh / self.boat.battery_capacity_wh
        self.boat.soc_percent = max(0, self.boat.soc_percent - (energy_ratio * 100))
