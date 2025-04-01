import ephem
from datetime import date, datetime, timedelta
from typing import Dict, Any, Tuple

class AstronomyAdapter:
    """
    Adapter for the ephem astronomy library.
    
    This class provides an interface to astronomical calculations
    using the ephem library, specifically for moon phase information.
    """
    
    def get_moon_data(self, date_obj: date, time_str: str = '22:00:00') -> Dict[str, Any]:
        """
        Get moon data for the specified date and time.
        
        Args:
            date_obj: The date for which to calculate moon data
            time_str: The time of day as a string in format "HH:MM:SS", defaults to 10 PM
            
        Returns:
            dict: Dictionary containing moon illumination, phase angle, and next phase dates
        """
        # Convert date and time to ephem date format (Dublin JD)
        date_str = date_obj.strftime('%Y/%m/%d')
        date_time_str = f"{date_str} {time_str}"
        obs_date = ephem.Date(date_time_str)
        
        # Create an observer at approximately sea level
        observer = ephem.Observer()
        observer.date = obs_date
        observer.pressure = 0  # Ignore atmospheric refraction
        
        # Calculate moon position and illumination
        moon = ephem.Moon(observer)
        illumination = moon.phase / 100.0  # ephem.Moon.phase returns percentage 0-100
        
        # Calculate phase angle (0-360 degrees)
        phase_angle = self._calculate_moon_phase_angle(moon, observer)
        
        # Calculate next phase dates
        next_full_moon = ephem.next_full_moon(obs_date)
        next_new_moon = ephem.next_new_moon(obs_date)
        next_first_quarter = ephem.next_first_quarter_moon(obs_date)
        next_last_quarter = ephem.next_last_quarter_moon(obs_date)
        
        return {
            'illumination': illumination,
            'phase_angle': phase_angle,
            'next_full_moon': self._ephem_date_to_python_date(next_full_moon),
            'next_new_moon': self._ephem_date_to_python_date(next_new_moon),
            'next_first_quarter': self._ephem_date_to_python_date(next_first_quarter),
            'next_last_quarter': self._ephem_date_to_python_date(next_last_quarter)
        }
    
    def calculate_illumination(self, moon_data: Dict[str, Any]) -> float:
        """
        Calculate the percentage of moon illumination.
        
        Args:
            moon_data: Dictionary containing moon data with 'illumination' key
            
        Returns:
            float: Percentage of illumination (0.0 to 100.0)
        """
        # Convert from 0-1 range to 0-100 percentage
        return moon_data['illumination'] * 100.0
    
    def calculate_phase_angle(self, moon_data: Dict[str, Any]) -> float:
        """
        Get the phase angle of the moon.
        
        Args:
            moon_data: Dictionary containing moon data with 'phase_angle' key
            
        Returns:
            float: Moon phase angle in degrees (0-360)
        """
        return moon_data['phase_angle']
    
    def _calculate_moon_phase_angle(self, moon, observer) -> float:
        """
        Calculate the moon phase angle in degrees (0-360).
        
        Args:
            moon: ephem.Moon object
            observer: ephem.Observer object
            
        Returns:
            float: Phase angle in degrees
        """
        # Calculate the phase angle based on elongation
        earth_to_moon = moon.earth_distance
        earth_to_sun = ephem.Sun(observer).earth_distance
        moon_to_sun = ephem.separation(moon, ephem.Sun(observer))
        
        # Calculate phase angle using the law of cosines
        try:
            cos_phase_angle = (earth_to_moon**2 + earth_to_sun**2 - 2*earth_to_moon*earth_to_sun*
                               ephem.cos(moon_to_sun)) / (2*earth_to_moon*earth_to_sun)
            phase_angle = ephem.degrees(ephem.acos(cos_phase_angle))
            
            # Convert to degrees and ensure range 0-360
            angle_deg = float(phase_angle) * 180.0 / ephem.pi
            
            # Adjust based on waxing/waning to ensure full cycle
            sun_ra = ephem.Sun(observer).ra
            moon_ra = moon.ra
            
            # If the Moon is to the west of the Sun, it's waxing
            if self._normalize_angle(moon_ra - sun_ra) < ephem.pi:
                return angle_deg
            else:
                return 360.0 - angle_deg
            
        except (ValueError, ZeroDivisionError):
            # Fallback calculation: use moon.phase to estimate angle
            # This is less accurate but provides a reasonable approximation
            return moon.phase * 3.6  # Convert 0-100 phase to 0-360 angle
    
    def _normalize_angle(self, angle):
        """Normalize an angle to be between 0 and 2π."""
        two_pi = 2 * ephem.pi
        return angle - two_pi * ephem.floor(angle / two_pi)
    
    def _ephem_date_to_python_date(self, ephem_date) -> date:
        """
        Convert an ephem date to a Python date object.
        
        Args:
            ephem_date: Date in ephem format (Dublin JD)
            
        Returns:
            date: Python date object
        """
        # Convert ephem date to tuple
        date_tuple = ephem.Date(ephem_date).tuple()
        
        # Create datetime object and extract date
        dt = datetime(date_tuple[0], date_tuple[1], date_tuple[2],
                      date_tuple[3], date_tuple[4], int(date_tuple[5]))
        return dt.date()