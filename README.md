# Moon Phase Visualization App

A simple web application that displays an image of the moon as it appears at 10 PM on the current date.

## Features

- Shows current moon phase with accurate visualization
- Displays illumination percentage and phase name
- Works on mobile and desktop devices
- Clean, minimalist interface

## Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python run.py`

## Testing

Run tests with: `pytest`

## Architecture

This application follows a hexagonal (ports and adapters) architecture with clean separation of concerns:

- Web layer: Flask web server and templates
- Application core: Services for orchestrating the workflow
- Domain: Core entities and business logic
- Adapters: Connections to external libraries and services
