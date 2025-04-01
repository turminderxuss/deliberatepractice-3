import pytest
import os
from datetime import date
from unittest.mock import patch, MagicMock
from app.image_provider import ImageProvider
from app.domain.moon_model import MoonPhaseData

class TestImageProvider:
    """Tests for the ImageProvider component."""
    
    def test_get_moon_image(self):
        """Test that get_moon_image returns a valid image path."""
        # Arrange
        provider = ImageProvider(base_path="/mnt/c/Users/turmi/Desktop/deliberatepractice-3/app/static/images")
        moon_data = MoonPhaseData(
            date=date.today(),
            illumination_percent=75.0,
            phase_name="Waxing Gibbous",
            phase_angle=135.0
        )
        
        # Mock the generate_moon_image method to avoid actual image generation
        with patch.object(provider, 'generate_moon_image', return_value="generated_image.png"):
            # Act
            result = provider.get_moon_image(moon_data)
            
            # Assert
            assert isinstance(result, str)
            assert result.endswith(".png") or result.endswith(".jpg")
    
    def test_get_static_moon_image(self):
        """Test that get_static_moon_image returns the correct path for a phase."""
        # Arrange
        provider = ImageProvider(base_path="/mnt/c/Users/turmi/Desktop/deliberatepractice-3/app/static/images")
        
        # Act
        result = provider.get_static_moon_image("Full Moon")
        
        # Assert
        assert isinstance(result, str)
        assert "full_moon" in result.lower()
        
        # Test another phase
        result = provider.get_static_moon_image("New Moon")
        assert "new_moon" in result.lower()
    
    def test_generate_moon_image(self):
        """Test that generate_moon_image creates an image based on phase data."""
        # Arrange
        provider = ImageProvider(base_path="/mnt/c/Users/turmi/Desktop/deliberatepractice-3/app/static/images")
        
        # Mock the Image module from PIL to avoid actual image creation
        with patch('app.image_provider.Image') as mock_image, \
             patch('app.image_provider.ImageDraw') as mock_draw, \
             patch('app.utils.image_utils.create_circular_mask', return_value=MagicMock()), \
             patch('app.utils.image_utils.apply_phase_to_image', return_value=MagicMock()):
            
            # Mock the Image.new to return a mock image
            mock_image.new.return_value = MagicMock()
            
            # Mock the save method
            mock_image.new.return_value.save = MagicMock()
            
            # Act
            result = provider.generate_moon_image(75.0, 135.0)
            
            # Assert
            assert isinstance(result, str)
            assert result.endswith(".png")
            
            # Verify that methods were called with expected arguments
            mock_image.new.assert_called_once()
            mock_image.new.return_value.save.assert_called_once()