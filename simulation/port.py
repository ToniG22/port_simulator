"""
Module: port
Defines the Port class used to manage electric boat docking and charging.
"""

from typing import List
from simulation.boat import Boat


class Port:
    """
    Represents a recreational electric port with a fixed number of boats and chargers.
    Manages charging constraints and boat assignments.
    """

    def __init__(self, name: str, capacity: int, lat: float, lon: float,
                 power_settings: dict, num_chargers: int):
        """
        Initializes a new Port instance.

        Args:
            name (str): Name of the port.
            capacity (int): Maximum number of boats the port can host.
            lat (float): Latitude of the port.
            lon (float): Longitude of the port.
            power_settings (dict): Dictionary with keys:
                - 'site_max_power_w' (int): Total power available for the port.
                - 'charger_max_power_w' (int): Max power per individual charger.
            num_chargers (int): Number of available chargers.
        """
        self.name = name
        self.capacity = capacity
        self.lat = lat
        self.lon = lon
        self.max_site_power_w = power_settings.get("site_max_power_w")
        self.max_charger_power_w = power_settings.get("charger_max_power_w")
        self.num_chargers = num_chargers
        self.boats: List[Boat] = []

    def add_boat(self, boat: Boat) -> None:
        """
        Adds a boat to the port if capacity allows.

        Args:
            boat (Boat): The boat to add.

        Raises:
            ValueError: If the port is at full capacity.
        """
        if len(self.boats) >= self.capacity:
            raise ValueError(f"Port '{self.name}' is at full capacity ({self.capacity} boats).")
        self.boats.append(boat)

    def simulate_charging(self, time_s: int) -> None:
        """
        Simulates the charging process for each boat over a given period.

        Args:
            time_s (int): Charging time in seconds.
        """
        if self.num_chargers == 0:
            return

        site_power_per_boat = self.max_site_power_w / self.num_chargers
        for boat in self.boats:
            boat.charge(time_s, site_power_per_boat)
