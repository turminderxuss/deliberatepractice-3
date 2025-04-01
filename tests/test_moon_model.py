import pytest
from datetime import date, timedelta
from app.domain.moon_model import MoonPhaseData

class TestMoonPhaseData:
    """Tests for the MoonPhaseData domain model."""
    
    def test_initialization(self):
        """Test that MoonPhaseData initializes correctly."""
        # Arrange
        test_date = date.today()
        illumination = 75.5
        phase_name = "Waxing Gibbous"
        phase_angle = 135.0
        next_phase_date = test_date + timedelta(days=3)
        next_phase_name = "Full Moon"
        
        # Act
        moon_data = MoonPhaseData(
            date=test_date,
            illumination_percent=illumination,
            phase_name=phase_name,
            phase_angle=phase_angle,
            next_phase_date=next_phase_date,
            next_phase_name=next_phase_name
        )
        
        # Assert
        assert moon_data.date == test_date
        assert moon_data.illumination_percent == illumination
        assert moon_data.phase_name == phase_name
        assert moon_data.phase_angle == phase_angle
        assert moon_data.next_phase_date == next_phase_date
        assert moon_data.next_phase_name == next_phase_name
    
    def test_is_full_moon(self):
        """Test that is_full_moon returns correct values."""
        # Arrange
        full_moon = MoonPhaseData(
            date=date.today(),
            illumination_percent=100.0,
            phase_name="Full Moon",
            phase_angle=180.0
        )
        
        not_full_moon = MoonPhaseData(
            date=date.today(),
            illumination_percent=75.0,
            phase_name="Waxing Gibbous",
            phase_angle=135.0
        )
        
        # Act & Assert
        assert full_moon.is_full_moon() is True
        assert not_full_moon.is_full_moon() is False
    
    def test_is_new_moon(self):
        """Test that is_new_moon returns correct values."""
        # Arrange
        new_moon = MoonPhaseData(
            date=date.today(),
            illumination_percent=0.0,
            phase_name="New Moon",
            phase_angle=0.0
        )
        
        not_new_moon = MoonPhaseData(
            date=date.today(),
            illumination_percent=25.0,
            phase_name="Waxing Crescent",
            phase_angle=45.0
        )
        
        # Act & Assert
        assert new_moon.is_new_moon() is True
        assert not_new_moon.is_new_moon() is False
    
    def test_days_until_next_phase(self):
        """Test that days_until_next_phase calculates correctly."""
        # Arrange
        today = date.today()
        next_phase_date = today + timedelta(days=5)
        
        moon_data = MoonPhaseData(
            date=today,
            illumination_percent=65.0,
            phase_name="Waxing Gibbous",
            phase_angle=120.0,
            next_phase_date=next_phase_date,
            next_phase_name="Full Moon"
        )
        
        # Act
        days = moon_data.days_until_next_phase()
        
        # Assert
        assert days == 5
    
    def test_to_dict(self):
        """Test that to_dict returns all properties as a dictionary."""
        # Arrange
        today = date.today()
        next_phase_date = today + timedelta(days=2)
        
        moon_data = MoonPhaseData(
            date=today,
            illumination_percent=85.0,
            phase_name="Waxing Gibbous",
            phase_angle=150.0,
            next_phase_date=next_phase_date,
            next_phase_name="Full Moon"
        )
        
        # Act
        result = moon_data.to_dict()
        
        # Assert
        assert result["date"] == today
        assert result["illumination_percent"] == 85.0
        assert result["phase_name"] == "Waxing Gibbous"
        assert result["phase_angle"] == 150.0
        assert result["next_phase_date"] == next_phase_date
        assert result["next_phase_name"] == "Full Moon"
        assert result["days_until_next_phase"] == 2