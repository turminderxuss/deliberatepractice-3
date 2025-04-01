import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from app.app import create_app
from app.domain.moon_model import MoonPhaseData

@pytest.fixture
def client():
    """Create a test client for the Flask app with test configuration."""
    app = create_app(test_config={
        'TESTING': True,
        'SERVER_NAME': 'test.local'
    })
    
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestFlaskApp:
    """Tests for the Flask web application."""
    
    @patch('app.app.AppService')
    def test_index_route(self, mock_app_service_class, client):
        """Test that the index route returns a page with moon data."""
        # Mock the app service to return test data
        mock_app_service = MagicMock()
        mock_app_service_class.return_value = mock_app_service
        
        # Set up the mock return values
        test_date = date.today()
        mock_app_service.get_complete_moon_data.return_value = {
            'date': test_date,
            'illumination_percent': 75.0,
            'phase_name': 'Waxing Gibbous',
            'phase_angle': 135.0,
            'next_phase_date': test_date,
            'next_phase_name': 'Full Moon',
            'days_until_next_phase': 3,
            'visualization_path': '/app/static/images/test_image.png'
        }
        
        # Make a request to the index route
        response = client.get('/')
        
        # Check that the response is successful
        assert response.status_code == 200
        
        # Check that the response contains expected content
        html = response.data.decode('utf-8')
        assert 'Moon Phase Visualization' in html
        assert 'Waxing Gibbous' in html
        assert '75' in html  # For 75% illumination
        
        # Verify that the app service was called
        mock_app_service.get_complete_moon_data.assert_called_once()
    
    @patch('app.app.send_from_directory')
    def test_serve_image_route(self, mock_send_from_directory, client):
        """Test that the serve_image route serves images correctly."""
        # Set up the mock return value
        mock_send_from_directory.return_value = 'mocked image response'
        
        # Make a request to the serve_image route
        response = client.get('/images/test_image.png')
        
        # Check that send_from_directory was called with the correct arguments
        mock_send_from_directory.assert_called_once()
        
    def test_error_handler(self, client):
        """Test that the error handler returns an error page."""
        # Create a route that will raise an exception
        with patch('app.app.AppService') as mock_app_service_class:
            mock_app_service = MagicMock()
            mock_app_service_class.return_value = mock_app_service
            mock_app_service.get_complete_moon_data.side_effect = Exception('Test error')
            
            # Make a request to the index route which will trigger the error
            response = client.get('/')
            
            # Check that the response is a 500 error
            assert response.status_code == 500
            
            # Check that the response contains the error message
            html = response.data.decode('utf-8')
            assert 'Something went wrong' in html
            assert 'Test error' in html