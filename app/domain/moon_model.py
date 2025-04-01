from datetime import date
from typing import Optional

class MoonPhaseData:
    """
    Domain entity representing moon phase data for a specific date.
    Contains information about the moon's phase, illumination percentage,
    and details about the next major phase change.
    """
    
    def __init__(
        self,
        date: date,
        illumination_percent: float,
        phase_name: str,
        phase_angle: float,
        next_phase_date: Optional[date] = None,
        next_phase_name: Optional[str] = None
    ):
        """
        Initialize a new MoonPhaseData instance.
        
        Args:
            date: The date for which the phase is calculated
            illumination_percent: Percentage of the moon that is illuminated (0.0 to 100.0)
            phase_name: The name of the current moon phase
            phase_angle: The phase angle in degrees (0-360)
            next_phase_date: The date of the next major phase change (optional)
            next_phase_name: The name of the next major phase (optional)
        """
        self.date = date
        self.illumination_percent = illumination_percent
        self.phase_name = phase_name
        self.phase_angle = phase_angle
        self.next_phase_date = next_phase_date
        self.next_phase_name = next_phase_name
    
    def is_full_moon(self) -> bool:
        """
        Check if the current phase is a full moon.
        
        Returns:
            bool: True if this is a full moon, False otherwise
        """
        return self.phase_name == "Full Moon" and self.illumination_percent >= 99.0
    
    def is_new_moon(self) -> bool:
        """
        Check if the current phase is a new moon.
        
        Returns:
            bool: True if this is a new moon, False otherwise
        """
        return self.phase_name == "New Moon" and self.illumination_percent <= 1.0
    
    def days_until_next_phase(self) -> int:
        """
        Calculate the number of days until the next major phase change.
        
        Returns:
            int: Number of days until the next phase, or 0 if next_phase_date is not set
        """
        if not self.next_phase_date:
            return 0
        
        delta = self.next_phase_date - self.date
        return delta.days
    
    def to_dict(self) -> dict:
        """
        Convert the MoonPhaseData object to a dictionary.
        
        Returns:
            dict: Dictionary containing all the moon phase data
        """
        return {
            "date": self.date,
            "illumination_percent": self.illumination_percent,
            "phase_name": self.phase_name,
            "phase_angle": self.phase_angle,
            "next_phase_date": self.next_phase_date,
            "next_phase_name": self.next_phase_name,
            "days_until_next_phase": self.days_until_next_phase()
        }