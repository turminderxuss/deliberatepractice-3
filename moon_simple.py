"""
Minimalist Moon Phase Visualization
Shows only the moon on a black background as it appears in the night sky
"""

from flask import Flask, render_template_string
from datetime import datetime
import math

app = Flask(__name__)

# Minimalist HTML template
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Moon</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .moon-container {
            position: relative;
            width: min(80vw, 80vh);
            padding-bottom: min(80vw, 80vh); /* Creates a perfect square */
        }
        
        .moon {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            overflow: hidden;
            box-shadow: 0 0 50px rgba(255, 255, 255, 0.2);
        }
        
        .moon-surface {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: radial-gradient(circle at 50% 50%, 
                #f5f5f5 0%, 
                #e0e0e0 50%, 
                #d0d0d0 100%);
            position: relative;
        }

        /* Moon details - subtle craters */
        .moon-surface::before {
            content: "";
            position: absolute;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 30% 40%, rgba(200,200,200,0.3) 0%, rgba(200,200,200,0) 20%),
                        radial-gradient(circle at 70% 30%, rgba(200,200,200,0.3) 0%, rgba(200,200,200,0) 15%),
                        radial-gradient(circle at 40% 70%, rgba(200,200,200,0.3) 0%, rgba(200,200,200,0) 25%),
                        radial-gradient(circle at 60% 50%, rgba(200,200,200,0.3) 0%, rgba(200,200,200,0) 10%);
        }
        
        .shadow {
            position: absolute;
            top: 0;
            height: 100%;
            border-radius: 50%;
            background: #000000;
            {{ shadow_style }}
        }
    </style>
</head>
<body>
    <div class="moon-container">
        <div class="moon">
            <div class="moon-surface"></div>
            <div class="shadow"></div>
        </div>
    </div>
</body>
</html>
"""

def calculate_moon_phase():
    """Calculate current moon phase using a simplified algorithm."""
    # Moon cycle is approximately 29.53 days
    LUNAR_CYCLE = 29.53
    
    # Reference date for a known new moon (Jan 6, 2000)
    reference_date = datetime(2000, 1, 6)  # New moon date
    current_date = datetime.now()
    
    # Calculate days since reference date
    days_since_reference = (current_date - reference_date).days
    
    # Calculate the current phase as a fraction of the lunar cycle
    lunar_phase = (days_since_reference % LUNAR_CYCLE) / LUNAR_CYCLE
    
    # Convert to an angle (0-360 degrees)
    phase_angle = lunar_phase * 360
    
    # Calculate illumination percentage (0-100%)
    # Using cosine function for proper illumination curve
    illumination = 50 * (1 - math.cos(math.radians(phase_angle)))
    
    # Generate CSS for the shadow based on the phase
    if phase_angle <= 180:  # Waxing
        shadow_position = "left: 0;"
        # Calculate shadow width - creates a curve from full width to 0
        shadow_width_percent = 100 * (1 - 2 * (illumination / 100))
        shadow_style = f"{shadow_position} width: {max(0, shadow_width_percent)}%;"
    else:  # Waning
        shadow_position = "right: 0;"
        # Calculate shadow width - creates a curve from 0 to full width
        shadow_width_percent = 100 * (2 * (illumination / 100) - 1)
        shadow_style = f"{shadow_position} width: {max(0, shadow_width_percent)}%;"
    
    return {
        'shadow_style': shadow_style
    }

@app.route('/')
def index():
    """Render the moon visualization."""
    moon_data = calculate_moon_phase()
    return render_template_string(TEMPLATE, **moon_data)

if __name__ == '__main__':
    print("Starting Minimalist Moon Visualization...")
    print("Open your web browser and go to: http://YOUR_SERVER_IP:8080")
    print("If running locally, use: http://127.0.0.1:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)