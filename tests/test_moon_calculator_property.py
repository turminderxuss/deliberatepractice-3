import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock
from hypothesis import given, strategies as st

from app.moon_calculator import MoonCalculator
from app.domain.moon_model import MoonPhaseData

class TestMoonCalculatorProperties:
    """Property-based tests for the MoonCalculator component."""
    
    @given(
        illumination=st.floats(min_value=0.0, max_value=100.0),
        waning=st.booleans()
    )
    def test_phase_name_properties(self, illumination, waning):
        """Test that phase names satisfy expected properties."""
        # Arrange
        calculator = MoonCalculator(astronomy_adapter=MagicMock())
        
        # Act
        phase_name = calculator.get_phase_name(illumination, waning)
        
        # Assert - Phase name should be one of the expected values
        expected_phase_names = [
            "New Moon", 
            "Waxing Crescent", "Waning Crescent",
            "First Quarter", "Last Quarter",
            "Waxing Gibbous", "Waning Gibbous",
            "Full Moon"
        ]
        assert phase_name in expected_phase_names
        
        # Phase name should follow illumination percentage
        if illumination <= 1.0:
            assert phase_name == "New Moon"
        elif illumination >= 99.0:
            assert phase_name == "Full Moon"
        elif "Crescent" in phase_name:
            assert illumination <= 45.0
        elif "Quarter" in phase_name:
            assert 45.0 <= illumination <= 55.0
        elif "Gibbous" in phase_name:
            assert 55.0 <= illumination <= 99.0
        
        # Waxing/waning should be reflected in the name correctly
        if 1.0 < illumination < 99.0:  # Not new or full moon
            if waning:
                assert phase_name in ["Waning Crescent", "Last Quarter", "Waning Gibbous"]
            else:
                assert phase_name in ["Waxing Crescent", "First Quarter", "Waxing Gibbous"]
    
    @given(
        days=st.integers(min_value=1, max_value=365)
    )
    def test_get_next_phase_date_properties(self, days):
        """Test that next phase date satisfies expected properties."""
        # Arrange
        today = date.today()
        next_phase_date = today + timedelta(days=days)
        
        # Create mock astronomy adapter
        mock_adapter = MagicMock()
        mock_adapter.get_moon_data.return_value = {
            'next_full_moon': next_phase_date,
            'next_new_moon': next_phase_date,
            'next_first_quarter': next_phase_date,
            'next_last_quarter': next_phase_date
        }
        
        calculator = MoonCalculator(astronomy_adapter=mock_adapter)
        
        # Act
        result_date, result_name = calculator.get_next_phase_date(today, "Waxing Crescent")
        
        # Assert
        assert result_date == next_phase_date
        assert result_name in ["New Moon", "Full Moon", "First Quarter", "Last Quarter"]
        
        # The next phase date should be after the current date
        assert result_date > today
        
        # The days difference should match our input
        assert (result_date - today).days == days