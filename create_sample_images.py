"""
Script to generate sample moon phase images.
This helps ensure we have images for all phases even if the app hasn't generated them yet.
"""

import os
from PIL import Image, ImageDraw
from app.utils.image_utils import apply_phase_to_image

def create_sample_moon_images():
    """Create sample moon images for all phases."""
    # Ensure the images directory exists
    images_dir = os.path.join('app', 'static', 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Define the phases to generate
    phases = {
        "new_moon.png": (0.0, 0.0),  # 0% illumination
        "waxing_crescent.png": (25.0, 45.0),  # 25% illumination, waxing
        "first_quarter.png": (50.0, 90.0),  # 50% illumination, waxing
        "waxing_gibbous.png": (75.0, 135.0),  # 75% illumination, waxing
        "full_moon.png": (100.0, 180.0),  # 100% illumination
        "waning_gibbous.png": (75.0, 225.0),  # 75% illumination, waning
        "last_quarter.png": (50.0, 270.0),  # 50% illumination, waning
        "waning_crescent.png": (25.0, 315.0),  # 25% illumination, waning
    }
    
    # Size of the images
    SIZE = 400
    
    # Create each phase image
    for filename, (illumination, phase_angle) in phases.items():
        # Create a base full moon image
        image = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw the basic moon circle (white for a full moon)
        draw.ellipse((0, 0, SIZE, SIZE), fill='white', outline='lightgray')
        
        # Apply phase effects
        result = apply_phase_to_image(image, illumination, phase_angle)
        
        # Save the result
        output_path = os.path.join(images_dir, filename)
        result.save(output_path)
        print(f"Created {output_path}")

if __name__ == "__main__":
    create_sample_moon_images()