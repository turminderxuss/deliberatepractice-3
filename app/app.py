import os
from flask import Flask, render_template, request, send_from_directory
from datetime import date

from app.config import load_config
from app.app_service import AppService
from app.moon_calculator import MoonCalculator
from app.image_provider import ImageProvider
from app.adapters.astronomy_adapter import AstronomyAdapter

def create_app(test_config=None):
    """
    Create and configure the Flask application.
    
    Args:
        test_config: Configuration to use for testing (optional)
        
    Returns:
        Flask: The configured Flask application
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the configuration
    config = load_config()
    app.config.from_mapping(config)
    
    if test_config:
        app.config.update(test_config)
    
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static')
    images_dir = os.path.join(static_dir, 'images')
    
    # Ensure the images directory exists
    os.makedirs(images_dir, exist_ok=True)
    
    # Setup dependencies
    astronomy_adapter = AstronomyAdapter()
    moon_calculator = MoonCalculator(astronomy_adapter=astronomy_adapter)
    image_provider = ImageProvider(base_path=images_dir)
    app_service = AppService(
        moon_calculator=moon_calculator,
        image_provider=image_provider
    )
    
    # Register routes
    @app.route('/')
    def index():
        """
        Main route that displays the moon phase visualization.
        
        Returns:
            str: Rendered HTML page
        """
        # Get the complete moon data
        moon_data = app_service.get_complete_moon_data()
        
        # Extract the image path from the complete data
        image_path = moon_data.pop('visualization_path', '')
        
        # Get just the filename from the path
        image_filename = os.path.basename(image_path)
        
        return render_template(
            'index.html',
            moon_data=moon_data,
            image_filename=image_filename
        )
    
    @app.route('/images/<path:filename>')
    def serve_image(filename):
        """
        Serve moon images from the images directory.
        
        Args:
            filename: The name of the image file to serve
            
        Returns:
            Response: The image file
        """
        return send_from_directory(images_dir, filename)
    
    @app.errorhandler(Exception)
    def handle_error(error):
        """
        Handle application errors.
        
        Args:
            error: The error that occurred
            
        Returns:
            tuple: (error page, status code)
        """
        app.logger.error(f"An error occurred: {str(error)}")
        return render_template('error.html', error=str(error)), 500
    
    return app