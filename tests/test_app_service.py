import pytest
from datetime import date
from unittest.mock import patch, MagicMock

from app.app_service import AppService
from app.domain.moon_model import MoonPhaseData

class TestAppService:
    """Tests for the AppService component."""
    
    def test_get_moon_phase_data(self):
        """Test that get_moon_phase_data calls the calculator and returns data."""
        # Arrange
        mock_calculator = MagicMock()
        mock_calculator.calculate_moon_phase.return_value = MoonPhaseData(
            date=date.today(),
            illumination_percent=75.0,
            phase_name="Waxing Gibbous",
            phase_angle=135.0
        )
        
        mock_image_provider = MagicMock()
        
        service = AppService(
            moon_calculator=mock_calculator,
            image_provider=mock_image_provider
        )
        
        test_date = date.today()
        
        # Act
        result = service.get_moon_phase_data(test_date)
        
        # Assert
        assert isinstance(result, MoonPhaseData)
        mock_calculator.calculate_moon_phase.assert_called_once_with(test_date)
    
    def test_get_moon_visualization(self):
        """Test that get_moon_visualization calls the image provider and returns a path."""
        # Arrange
        mock_calculator = MagicMock()
        mock_image_provider = MagicMock()
        mock_image_provider.get_moon_image.return_value = "/path/to/image.png"
        
        service = AppService(
            moon_calculator=mock_calculator,
            image_provider=mock_image_provider
        )
        
        moon_data = MoonPhaseData(
            date=date.today(),
            illumination_percent=85.0,
            phase_name="Waxing Gibbous",
            phase_angle=150.0
        )
        
        # Act
        result = service.get_moon_visualization(moon_data)
        
        # Assert
        assert result == "/path/to/image.png"
        mock_image_provider.get_moon_image.assert_called_once_with(moon_data)
    
    def test_get_complete_moon_data(self):
        """Test that get_complete_moon_data returns a complete data dictionary."""
        # Arrange
        test_date = date.today()
        moon_data = MoonPhaseData(
            date=test_date,
            illumination_percent=65.0,
            phase_name="Waxing Gibbous",
            phase_angle=120.0
        )
        
        mock_calculator = MagicMock()
        mock_calculator.calculate_moon_phase.return_value = moon_data
        
        mock_image_provider = MagicMock()
        mock_image_provider.get_moon_image.return_value = "/path/to/image.png"
        
        service = AppService(
            moon_calculator=mock_calculator,
            image_provider=mock_image_provider
        )
        
        # Act
        result = service.get_complete_moon_data(test_date)
        
        # Assert
        assert isinstance(result, dict)
        assert result["date"] == test_date
        assert result["illumination_percent"] == 65.0
        assert result["phase_name"] == "Waxing Gibbous"
        assert result["phase_angle"] == 120.0
        assert result["visualization_path"] == "/path/to/image.png"
        
        # Verify the calculator was called with the right date
        mock_calculator.calculate_moon_phase.assert_called_once_with(test_date)
        
        # Verify the image provider was called with the right moon data
        mock_image_provider.get_moon_image.assert_called_once_with(moon_data)
    
    def test_get_complete_moon_data_with_default_date(self):
        """Test that get_complete_moon_data uses current date when not specified."""
        # Arrange
        moon_data = MoonPhaseData(
            date=date.today(),
            illumination_percent=65.0,
            phase_name="Waxing Gibbous",
            phase_angle=120.0
        )
        
        mock_calculator = MagicMock()
        mock_calculator.calculate_moon_phase.return_value = moon_data
        
        mock_image_provider = MagicMock()
        mock_image_provider.get_moon_image.return_value = "/path/to/image.png"
        
        service = AppService(
            moon_calculator=mock_calculator,
            image_provider=mock_image_provider
        )
        
        # Mock the get_current_date function
        with patch('app.app_service.get_current_date') as mock_get_date:
            mock_get_date.return_value = date.today()
            
            # Act
            result = service.get_complete_moon_data()  # No date specified
            
            # Assert
            assert isinstance(result, dict)
            
            # Verify get_current_date was called
            mock_get_date.assert_called_once()
            
            # Verify the calculator was called with the current date
            mock_calculator.calculate_moon_phase.assert_called_once_with(date.today())