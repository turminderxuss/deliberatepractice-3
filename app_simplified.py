"""
Simplified Moon Phase App that doesn't require complex dependencies.
This standalone script shows the current moon phase using pre-calculated data.
"""

from flask import Flask, render_template_string
from datetime import datetime, timedelta
import math

app = Flask(__name__)

# HTML template for the app
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moon Phase Visualization</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #121212 0%, #2c3e50 100%);
            color: white;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            width: 90%;
            text-align: center;
        }
        h1 {
            margin-bottom: 10px;
        }
        .subtitle {
            color: #ccc;
            margin-bottom: 30px;
        }
        .moon {
            width: 300px;
            height: 300px;
            border-radius: 50%;
            margin: 30px auto;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        .moon-surface {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-color: #f0f0f0;
        }
        .shadow {
            position: absolute;
            top: 0;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: black;
            {{ shadow_style }}
        }
        .data-container {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            max-width: 500px;
            width: 100%;
        }
        .data-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .data-label {
            font-weight: bold;
            color: #aaa;
        }
        .illumination-bar {
            width: 100%;
            height: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            margin: 10px 0;
            overflow: hidden;
        }
        .illumination-fill {
            height: 100%;
            background: linear-gradient(90deg, #f5f5f5, #fff);
            border-radius: 10px;
            width: {{ illumination }}%;
        }
        footer {
            margin-top: 40px;
            color: #999;
            font-size: 0.9rem;
        }
        @media (max-width: 600px) {
            .moon {
                width: 200px;
                height: 200px;
            }
            .shadow {
                width: 200px;
                height: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Moon Phase Visualization</h1>
        <p class="subtitle">The moon at 10 PM tonight ({{ date }})</p>
        
        <div class="moon">
            <div class="moon-surface"></div>
            <div class="shadow"></div>
        </div>
        
        <div class="data-container">
            <h2>Moon Phase Information</h2>
            
            <div class="data-item">
                <span class="data-label">Phase:</span>
                <span>{{ phase_name }}</span>
            </div>
            
            <div class="data-item">
                <span class="data-label">Illumination:</span>
                <span>{{ illumination }}%</span>
            </div>
            
            <div class="illumination-bar">
                <div class="illumination-fill"></div>
            </div>
            
            <div class="data-item">
                <span class="data-label">Date:</span>
                <span>{{ date }}</span>
            </div>
            
            <div class="data-item">
                <span class="data-label">Next Phase:</span>
                <span>{{ next_phase_name }} (in {{ days_until_next_phase }} days)</span>
            </div>
        </div>
        
        <footer>
            <p>&copy; {{ current_year }} Moon Phase Visualization App</p>
        </footer>
    </div>
</body>
</html>
"""

def calculate_moon_phase():
    """Calculate the current moon phase based on a simplified algorithm."""
    # Moon cycle is approximately 29.53 days
    LUNAR_CYCLE = 29.53
    
    # Reference date for a known new moon (January 1, 2000)
    reference_date = datetime(2000, 1, 1)
    current_date = datetime.now()
    
    # Calculate days since reference date
    days_since_reference = (current_date - reference_date).days
    
    # Calculate the current phase as a fraction of the lunar cycle
    lunar_phase = (days_since_reference % LUNAR_CYCLE) / LUNAR_CYCLE
    
    # Convert to an angle (0-360 degrees)
    phase_angle = lunar_phase * 360
    
    # Calculate illumination percentage (0-100%)
    illumination = 50 * (1 - math.cos(math.radians(phase_angle)))
    
    # Determine if waxing or waning
    waxing = phase_angle <= 180
    
    # Determine the phase name
    if 0 <= phase_angle < 1 or phase_angle > 359:
        phase_name = "New Moon"
    elif 1 <= phase_angle < 45:
        phase_name = "Waxing Crescent"
    elif 45 <= phase_angle < 90:
        phase_name = "First Quarter"
    elif 90 <= phase_angle < 135:
        phase_name = "Waxing Gibbous"
    elif 135 <= phase_angle < 180:
        phase_name = "Full Moon"
    elif 180 <= phase_angle < 225:
        phase_name = "Waning Gibbous"
    elif 225 <= phase_angle < 270:
        phase_name = "Last Quarter"
    else:  # 270 <= phase_angle < 359
        phase_name = "Waning Crescent"
    
    # Calculate approximate date of next major phase
    if phase_angle < 90:
        next_phase_name = "First Quarter"
        days_until_next_phase = int((90 - phase_angle) / 360 * LUNAR_CYCLE)
    elif phase_angle < 180:
        next_phase_name = "Full Moon"
        days_until_next_phase = int((180 - phase_angle) / 360 * LUNAR_CYCLE)
    elif phase_angle < 270:
        next_phase_name = "Last Quarter"
        days_until_next_phase = int((270 - phase_angle) / 360 * LUNAR_CYCLE)
    else:
        next_phase_name = "New Moon"
        days_until_next_phase = int((360 - phase_angle) / 360 * LUNAR_CYCLE)
    
    # If days is 0, set to next cycle
    if days_until_next_phase == 0:
        days_until_next_phase = int(LUNAR_CYCLE)
    
    # Generate CSS for the shadow based on the phase
    if phase_angle <= 180:  # Waxing
        shadow_width = 300 * (1 - 2 * (illumination / 100))
        shadow_style = f"left: 0; width: {shadow_width}px;"
    else:  # Waning
        shadow_width = 300 * (2 * (illumination / 100) - 1)
        shadow_style = f"right: 0; width: {shadow_width}px;"
    
    return {
        'illumination': round(illumination),
        'phase_name': phase_name,
        'phase_angle': phase_angle,
        'next_phase_name': next_phase_name,
        'days_until_next_phase': days_until_next_phase,
        'shadow_style': shadow_style,
        'date': current_date.strftime('%B %d, %Y'),
        'current_year': current_date.year
    }

@app.route('/')
def index():
    """Render the main page with moon phase visualization."""
    moon_data = calculate_moon_phase()
    return render_template_string(TEMPLATE, **moon_data)

if __name__ == '__main__':
    print("Starting Moon Phase Visualization App...")
    print("Open your web browser and go to: http://127.0.0.1:5000")
    app.run(debug=True)