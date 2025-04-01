# Moon Phase Visualization Application - Modules and Methods

## 1. Web Layer

### 1.1 `app.py`
Main Flask application entry point.

**Methods:**
- `create_app()` → Flask Application
  - Creates and configures the Flask application
  - Registers routes and error handlers
  - Returns the configured app instance

- `index()` → HTML Response
  - Main route handler for the homepage
  - Obtains moon phase data for current date
  - Renders the template with moon data

- `handle_error(error)` → HTML Response
  - Error handler for application exceptions
  - Logs errors and returns appropriate error pages

### 1.2 `config.py`
Application configuration settings.

**Methods:**
- `load_config()` → dict
  - Loads configuration from environment or defaults
  - Sets Flask and application-specific settings

## 2. Application Core

### 2.1 `app_service.py`
Orchestrates the application workflow.

**Methods:**
- `get_moon_phase_data(date=None)` → MoonPhaseData
  - Orchestrates the process to get moon phase data for a given date (defaults to current date)
  - Calls the moon phase calculator and processes the results
  - Returns a domain model with the complete moon data

- `get_moon_visualization(moon_phase_data)` → str
  - Gets appropriate moon visualization based on phase data
  - Coordinates with the image provider
  - Returns the path or data for the visualization

### 2.2 `moon_calculator.py`
Handles astronomical calculations for moon phases.

**Methods:**
- `calculate_moon_phase(date, time='22:00:00')` → MoonPhaseData
  - Calculates the moon phase for a specific date and time
  - Uses the astronomy library to perform calculations
  - Returns a domain model with phase information

- `get_phase_name(illumination_percent)` → str
  - Determines the name of the moon phase based on illumination percentage
  - Maps numerical values to descriptive phase names

- `get_next_phase_date(current_date, current_phase)` → (date, str)
  - Calculates the date of the next major moon phase
  - Returns a tuple with the date and phase name

### 2.3 `image_provider.py`
Provides visual representations of moon phases.

**Methods:**
- `get_moon_image(moon_phase_data)` → str
  - Gets or generates the appropriate moon image
  - Returns the path to the image or image data

- `generate_moon_image(illumination_percent, phase_angle)` → str
  - Dynamically generates a moon image based on phase data
  - Used if pre-rendered images aren't available
  - Returns the path to the generated image

- `get_static_moon_image(phase_name)` → str
  - Retrieves a pre-rendered moon image based on phase name
  - Returns the path to the static image

## 3. Domain Models

### 3.1 `moon_model.py`
Domain entities and value objects.

**Classes:**
- `MoonPhaseData`
  - Properties:
    - `date` (date): The date for which the phase is calculated
    - `illumination_percent` (float): Percentage of illumination (0-100)
    - `phase_name` (str): Name of the current phase
    - `phase_angle` (float): Angle of the phase in degrees
    - `next_phase_date` (date): Date of the next major phase
    - `next_phase_name` (str): Name of the next major phase
  
  - Methods:
    - `__init__(date, illumination_percent, phase_name, phase_angle, next_phase_date=None, next_phase_name=None)`
    - `is_full_moon()` → bool
    - `is_new_moon()` → bool
    - `days_until_next_phase()` → int
    - `to_dict()` → dict

## 4. Adapters

### 4.1 `astronomy_adapter.py`
Adapter for the astronomy library.

**Methods:**
- `get_moon_data(date, time='22:00:00')` → dict
  - Interfaces with the chosen astronomy library
  - Calculates raw astronomical data for the moon
  - Returns a dictionary with astronomical information

- `calculate_illumination(moon_data)` → float
  - Calculates the percentage of moon illumination
  - Returns a value between 0 and 100

- `calculate_phase_angle(moon_data)` → float
  - Calculates the phase angle of the moon
  - Returns the angle in degrees (0-360)

### 4.2 `template_adapter.py`
Adapter for the template engine.

**Methods:**
- `render_moon_page(moon_phase_data, image_path)` → str
  - Renders the HTML template with moon data
  - Returns the complete HTML page

## 5. Utils

### 5.1 `date_utils.py`
Utility functions for date handling.

**Methods:**
- `get_current_date()` → date
  - Gets the current date in the appropriate format
  - Handles timezone considerations if necessary

- `format_date(date_obj, format_str='%Y-%m-%d')` → str
  - Formats a date object into a string
  - Uses the specified format string

### 5.2 `image_utils.py`
Utility functions for image processing.

**Methods:**
- `create_circular_mask(h, w, center=None, radius=None)` → ndarray
  - Creates a circular mask for image processing
  - Used for generating moon images

- `apply_phase_to_image(image, illumination_percent, phase_angle)` → ndarray
  - Applies phase effects to a base moon image
  - Creates realistic moon phase visualization

## 6. Static Assets

### 6.1 `static/css/styles.css`
Main stylesheet for the application.

### 6.2 `static/js/main.js`
Client-side JavaScript for the application (minimal functionality).

### 6.3 `static/images/`
Directory for static moon images and other visual assets.

## 7. Templates

### 7.1 `templates/index.html`
Main template for the homepage.

### 7.2 `templates/error.html`
Template for error pages.

### 7.3 `templates/base.html`
Base template with common layout elements.