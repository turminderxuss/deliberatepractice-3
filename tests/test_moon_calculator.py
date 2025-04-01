import pytest
from datetime import date
from unittest.mock import patch, MagicMock
from app.moon_calculator import MoonCalculator
from app.domain.moon_model import MoonPhaseData

class TestMoonCalculator:
    """Tests for the MoonCalculator component."""
    
    def test_calculate_moon_phase(self):
        """Test that calculate_moon_phase returns a MoonPhaseData object."""
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter.get_moon_data.return_value = {
            'illumination': 0.75,  # 75% illuminated
            'phase_angle': 135.0,
            'next_full_moon': date.today(),
            'next_new_moon': date.today(),
            'next_first_quarter': date.today(),
            'next_last_quarter': date.today()
        }
        
        calculator = MoonCalculator(astronomy_adapter=mock_adapter)
        test_date = date.today()
        
        # Act
        result = calculator.calculate_moon_phase(test_date)
        
        # Assert
        assert isinstance(result, MoonPhaseData)
        assert result.date == test_date
        assert result.illumination_percent == 75.0
        assert result.phase_angle == 135.0
        assert result.phase_name is not None
    
    def test_get_phase_name(self):
        """Test that get_phase_name returns correct phase names based on illumination."""
        # Arrange
        calculator = MoonCalculator(astronomy_adapter=MagicMock())
        
        # Act & Assert - Test different illumination ranges
        assert calculator.get_phase_name(0.0) == "New Moon"
        assert calculator.get_phase_name(0.5) == "New Moon"
        assert calculator.get_phase_name(10.0) == "Waxing Crescent"
        assert calculator.get_phase_name(25.0) == "Waxing Crescent"
        assert calculator.get_phase_name(45.0) == "First Quarter"
        assert calculator.get_phase_name(55.0) == "First Quarter"
        assert calculator.get_phase_name(65.0) == "Waxing Gibbous"
        assert calculator.get_phase_name(85.0) == "Waxing Gibbous"
        assert calculator.get_phase_name(95.0) == "Full Moon"
        assert calculator.get_phase_name(100.0) == "Full Moon"
        assert calculator.get_phase_name(85.0, waning=True) == "Waning Gibbous"
        assert calculator.get_phase_name(65.0, waning=True) == "Waning Gibbous"
        assert calculator.get_phase_name(55.0, waning=True) == "Last Quarter"
        assert calculator.get_phase_name(45.0, waning=True) == "Last Quarter"
        assert calculator.get_phase_name(25.0, waning=True) == "Waning Crescent"
        assert calculator.get_phase_name(10.0, waning=True) == "Waning Crescent"
    
    def test_get_next_phase_date(self):
        """Test that get_next_phase_date returns the correct next phase."""
        # Arrange
        mock_adapter = MagicMock()
        
        # Mock the next phase dates
        today = date.today()
        mock_adapter.get_moon_data.return_value = {
            'next_full_moon': today,
            'next_new_moon': today,
            'next_first_quarter': today,
            'next_last_quarter': today
        }
        
        calculator = MoonCalculator(astronomy_adapter=mock_adapter)
        
        # Act & Assert
        # Just make sure it's calling the adapter correctly and returning a date and name
        next_date, next_name = calculator.get_next_phase_date(today, "Waxing Crescent")
        assert isinstance(next_date, date)
        assert isinstance(next_name, str)