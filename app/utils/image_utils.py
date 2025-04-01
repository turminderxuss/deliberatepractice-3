import numpy as np
from PIL import Image, ImageDraw
from typing import Optional, Tuple

def create_circular_mask(h: int, w: int, center: Optional[Tuple[int, int]] = None, 
                         radius: Optional[int] = None) -> np.ndarray:
    """
    Create a circular mask for image processing.
    
    Args:
        h: Height of the mask
        w: Width of the mask
        center: (x, y) coordinates of the center of the circle. Default is the center of the image.
        radius: Radius of the circle. Default is the minimum distance between the center and image walls.
        
    Returns:
        ndarray: A boolean array where True represents the area inside the circle
    """
    if center is None:
        center = (int(w/2), int(h/2))
    if radius is None:
        radius = min(center[0], center[1], w-center[0], h-center[1])
        
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    
    mask = dist_from_center <= radius
    return mask

def apply_phase_to_image(image: Image.Image, illumination_percent: float, 
                         phase_angle: float) -> Image.Image:
    """
    Apply moon phase effects to a base moon image.
    
    Args:
        image: The base moon image (typically a full moon)
        illumination_percent: Percentage of the moon that is illuminated (0-100)
        phase_angle: The phase angle in degrees (0-360)
        
    Returns:
        Image: The modified image showing the correct moon phase
    """
    # Create a copy of the image to avoid modifying the original
    result = image.copy()
    
    # Get image dimensions
    width, height = result.size
    
    # Create a drawing object
    draw = ImageDraw.Draw(result)
    
    # Determine if the moon is waxing or waning
    waning = phase_angle > 180.0
    
    # Calculate the portion of the moon to shade based on illumination
    # For a circle, we'll use an ellipse to shade a portion
    shade_amount = 1.0 - (illumination_percent / 100.0)
    
    # Calculate ellipse parameters to create the shadow
    # We adjust based on waxing/waning to get the shadow on the correct side
    if illumination_percent < 100.0:
        # Full moon doesn't need shadows
        ellipse_width = width * 2 * shade_amount
        
        if waning:
            # Shadow on the left side for waning moon
            ellipse_x0 = width - ellipse_width
            ellipse_x1 = width + ellipse_width
        else:
            # Shadow on the right side for waxing moon
            ellipse_x0 = -ellipse_width
            ellipse_x1 = ellipse_width
        
        # Draw the shadow ellipse
        draw.ellipse((ellipse_x0, -height, ellipse_x1, height * 2), fill='black')
    
    # For really small illumination (crescent), we need special handling
    if illumination_percent < 5.0:
        # Almost new moon - just show a small sliver
        if waning:
            draw.rectangle((width * 0.1, 0, width, height), fill='black')
        else:
            draw.rectangle((0, 0, width * 0.9, height), fill='black')
    
    # For new moon (0% illumination), make it all black
    if illumination_percent <= 1.0:
        draw.ellipse((0, 0, width, height), fill='black')
    
    return result