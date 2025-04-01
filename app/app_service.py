from datetime import date
from typing import Optional, Dict, Any

from app.domain.moon_model import MoonPhaseData
from app.moon_calculator import MoonCalculator
from app.image_provider import ImageProvider
from app.utils.date_utils import get_current_date

class AppService:
    """
    Application service that orchestrates the workflow of the application.
    
    This service coordinates between different components and implements
    the core application use cases.
    """
    
    def __init__(self, moon_calculator: MoonCalculator, image_provider: ImageProvider):
        """
        Initialize the AppService with required dependencies.
        
        Args:
            moon_calculator: The calculator for moon phase data
            image_provider: The provider for moon visualizations
        """
        self.moon_calculator = moon_calculator
        self.image_provider = image_provider
    
    def get_moon_phase_data(self, date_obj: Optional[date] = None) -> MoonPhaseData:
        """
        Get moon phase data for the specified date (or current date if not specified).
        
        Args:
            date_obj: The date for which to get moon phase data (optional)
            
        Returns:
            MoonPhaseData: The moon phase data for the specified date
        """
        # Use the current date if none provided
        if date_obj is None:
            date_obj = get_current_date()
        
        # Calculate the moon phase
        return self.moon_calculator.calculate_moon_phase(date_obj)
    
    def get_moon_visualization(self, moon_phase_data: MoonPhaseData) -> str:
        """
        Get the visualization for the specified moon phase data.
        
        Args:
            moon_phase_data: The moon phase data to visualize
            
        Returns:
            str: Path to the visualization image
        """
        return self.image_provider.get_moon_image(moon_phase_data)
    
    def get_complete_moon_data(self, date_obj: Optional[date] = None) -> Dict[str, Any]:
        """
        Get complete moon data including phase information and visualization.
        
        Args:
            date_obj: The date for which to get moon data (optional)
            
        Returns:
            dict: Dictionary containing moon phase data and visualization path
        """
        # Get the moon phase data
        moon_data = self.get_moon_phase_data(date_obj)
        
        # Get the visualization
        visualization_path = self.get_moon_visualization(moon_data)
        
        # Convert moon data to dictionary and add visualization path
        result = moon_data.to_dict()
        result['visualization_path'] = visualization_path
        
        return result