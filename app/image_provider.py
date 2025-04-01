import os
import time
from PIL import Image, ImageDraw
from typing import Dict

from app.domain.moon_model import MoonPhaseData
from app.utils.image_utils import create_circular_mask, apply_phase_to_image

class ImageProvider:
    """
    Provider for moon phase visualizations.
    
    This class is responsible for retrieving or generating
    appropriate visual representations of moon phases.
    """
    
    # Mapping of phase names to file names for static images
    PHASE_IMAGE_MAP = {
        "New Moon": "new_moon.png",
        "Waxing Crescent": "waxing_crescent.png",
        "First Quarter": "first_quarter.png",
        "Waxing Gibbous": "waxing_gibbous.png",
        "Full Moon": "full_moon.png",
        "Waning Gibbous": "waning_gibbous.png",
        "Last Quarter": "last_quarter.png",
        "Waning Crescent": "waning_crescent.png"
    }
    
    def __init__(self, base_path: str):
        """
        Initialize the ImageProvider with the path to static images.
        
        Args:
            base_path: Path to the directory containing moon images
        """
        self.base_path = base_path
        self._ensure_base_path_exists()
    
    def get_moon_image(self, moon_phase_data: MoonPhaseData) -> str:
        """
        Get an appropriate moon image based on phase data.
        
        Args:
            moon_phase_data: The moon phase data to visualize
            
        Returns:
            str: Path to the moon image
        """
        # Try to get a static image first
        try:
            static_image_path = self.get_static_moon_image(moon_phase_data.phase_name)
            if os.path.exists(static_image_path):
                return static_image_path
        except Exception:
            # If static image retrieval fails, fall back to generation
            pass
        
        # Generate an image if no static one exists or if it failed
        return self.generate_moon_image(
            moon_phase_data.illumination_percent,
            moon_phase_data.phase_angle
        )
    
    def get_static_moon_image(self, phase_name: str) -> str:
        """
        Get the path to a static moon image for a given phase.
        
        Args:
            phase_name: The name of the moon phase
            
        Returns:
            str: Path to the static image for the phase
        """
        # Get the filename for the phase
        filename = self.PHASE_IMAGE_MAP.get(phase_name, "full_moon.png")
        
        # Return the full path
        return os.path.join(self.base_path, filename)
    
    def generate_moon_image(self, illumination_percent: float, phase_angle: float) -> str:
        """
        Generate a moon image based on phase data.
        
        Args:
            illumination_percent: Percentage of the moon that is illuminated (0-100)
            phase_angle: The phase angle in degrees (0-360)
            
        Returns:
            str: Path to the generated image
        """
        # Create a unique filename based on phase data
        filename = f"moon_{int(illumination_percent)}_{int(phase_angle)}_{int(time.time())}.png"
        output_path = os.path.join(self.base_path, filename)
        
        # Create a base full moon image
        SIZE = 400  # Size of the image (square)
        image = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw the basic moon circle (white for a full moon)
        draw.ellipse((0, 0, SIZE, SIZE), fill='white', outline='lightgray')
        
        # Apply phase effects
        result = apply_phase_to_image(image, illumination_percent, phase_angle)
        
        # Save the result
        result.save(output_path)
        
        return output_path
    
    def _ensure_base_path_exists(self):
        """Ensure that the base path directory exists, create it if not."""
        os.makedirs(self.base_path, exist_ok=True)