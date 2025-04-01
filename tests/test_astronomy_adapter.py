import pytest
from datetime import date, datetime
from app.adapters.astronomy_adapter import AstronomyAdapter

class TestAstronomyAdapter:
    """Tests for the AstronomyAdapter component."""
    
    def test_get_moon_data(self):
        """Test that get_moon_data returns the expected data structure."""
        # Arrange
        adapter = AstronomyAdapter()
        test_date = date.today()
        test_time = "22:00:00"
        
        # Act
        result = adapter.get_moon_data(test_date, test_time)
        
        # Assert
        assert isinstance(result, dict)
        assert 'illumination' in result
        assert 'phase_angle' in result
        assert 'next_full_moon' in result
        assert 'next_new_moon' in result
        assert 'next_first_quarter' in result
        assert 'next_last_quarter' in result
        
        assert 0 <= result['illumination'] <= 1  # Illumination should be between 0 and 1
        assert 0 <= result['phase_angle'] <= 360  # Phase angle should be between 0 and 360
        
        # Verify that next phase dates are all date objects
        assert isinstance(result['next_full_moon'], date)
        assert isinstance(result['next_new_moon'], date)
        assert isinstance(result['next_first_quarter'], date)
        assert isinstance(result['next_last_quarter'], date)
    
    def test_calculate_illumination(self):
        """Test that calculate_illumination correctly processes moon data."""
        # Arrange
        adapter = AstronomyAdapter()
        moon_data = {'illumination': 0.75}  # 75% illumination
        
        # Act
        result = adapter.calculate_illumination(moon_data)
        
        # Assert
        assert result == 75.0  # Should convert from 0.75 to 75.0
    
    def test_calculate_phase_angle(self):
        """Test that calculate_phase_angle correctly processes moon data."""
        # Arrange
        adapter = AstronomyAdapter()
        moon_data = {'phase_angle': 135.5}
        
        # Act
        result = adapter.calculate_phase_angle(moon_data)
        
        # Assert
        assert result == 135.5