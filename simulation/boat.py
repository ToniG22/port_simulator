"""
Module: boat
Defines the Boat class for electric recreational vessels,
including battery status, charging logic, and energy modeling.
"""

from typing import Dict


class Boat:
    """
    Represents an electric boat with battery, motor, and operational characteristics.
    """

    def __init__(self, name: str, specs: Dict):
        """
        Initializes a Boat instance.

        Args:
            name (str): Name of the boat.
            specs (Dict): Dictionary containing boat specifications:
                - battery_capacity_wh (float)
                - charging_rate_w (float)
                - soc_percent (float)
                - length (float)
                - width (float)
                - passenger_capacity (int)
                - cruise_speed_kmh (float)
                - base_consumption_wh_per_km (float)
                - motor_power_w (float)
                - motor_efficiency (float)
        """
        self.name = name
        self.battery_capacity_wh = specs.get("battery_capacity_wh", 0.0)
        self.charging_rate_w = specs.get("charging_rate_w", 0.0)
        self.soc_percent = specs.get("soc_percent", 100.0)
        self.length = specs.get("length", 0.0)
        self.width = specs.get("width", 0.0)
        self.passenger_capacity = specs.get("passenger_capacity", 0)
        self.cruise_speed_kmh = specs.get("cruise_speed_kmh", 0.0)
        self.base_consumption_wh_per_km = specs.get("base_consumption_wh_per_km", 0.0)
        self.motor_power_w = specs.get("motor_power_w", 0.0)
        self.motor_efficiency = specs.get("motor_efficiency", 1.0)

    def get_available_energy_wh(self) -> float:
        """
        Calculates the currently available energy in watt-hours.

        Returns:
            float: Available energy in Wh.
        """
        return self.battery_capacity_wh * (self.soc_percent / 100)

    def estimate_energy_for_trip(self, distance_m: float) -> float:
        """
        Estimates the energy required for a trip of a given distance.

        Args:
            distance_m (float): Trip distance in meters.

        Returns:
            float: Estimated energy consumption in Wh.
        """
        distance_km = distance_m / 1000
        return self.base_consumption_wh_per_km * distance_km

    def charge(self, time_s: int, site_max_power_w: float) -> None:
        """
        Charges the boat for a given time duration based on available power.

        Args:
            time_s (int): Charging time in seconds.
            site_max_power_w (float): Maximum power available to this boat in watts.
        """
        effective_rate_w = min(self.charging_rate_w, site_max_power_w)
        energy_added_wh = (effective_rate_w * time_s) / 3600
        new_energy = self.get_available_energy_wh() + energy_added_wh
        self.soc_percent = min(100, (new_energy / self.battery_capacity_wh) * 100)
