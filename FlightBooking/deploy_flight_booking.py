# deploy_flight_booking.py
import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import json
import webbrowser
from datetime import datetime

class FlightBookingDeployer:
    def __init__(self, app_name="flight-booking-app", port=5000, host="0.0.0.0"):
        """
        Initialize the flight booking application deployer
        
        Args:
            app_name: Name of the application
            port: Port to run the application on (default: 5000)
            host: Host to bind the application to
        """
        self.app_name = app_name
        self.port = port  # Using port 5000
        self.host = host
        self.project_dir = Path.cwd() / app_name
        self.static_dir = self.project_dir / "static"
        self.templates_dir = self.project_dir / "templates"
        
    def create_directory_structure(self):
        """Create the necessary directory structure for the application"""
        print("📁 Creating directory structure...")
        
        directories = [
            self.project_dir,
            self.static_dir,
            self.static_dir / "css",
            self.static_dir / "js",
            self.static_dir / "images",
            self.templates_dir,
            self.project_dir / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created: {directory}")
            
        return True
    
    def create_config_files(self):
        """Create configuration files"""
        print("⚙️  Creating configuration files...")
        
        # Create requirements.txt with your requirements
        requirements = [
            "Flask>=2.3.0",
            "Flask-CORS>=4.0.0",
            "python-dotenv>=1.0.0",
            "requests>=2.31.0"
        ]
        
        with open(self.project_dir / "requirements.txt", "w") as f:
            f.write("\n".join(requirements))
        print(f"  ✓ Created requirements.txt with {len(requirements)} packages")
        
        # Create .env file with port 5000
        env_content = f"""# Flight Booking Application Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
API_BASE_URL=https://api.your-flight-booking-backend.com
FRONTEND_PORT={self.port}  # Using port {self.port}
HOST={self.host}
"""
        
        with open(self.project_dir / ".env", "w") as f:
            f.write(env_content)
        print("  ✓ Created .env configuration file")
        
        return True
    
    def create_flask_app(self):
        """Create the main Flask application"""
        print("🚀 Creating Flask application...")
        
        app_content = f'''# app.py
from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Enable CORS if needed
    CORS(app)
    
    # Setup logging
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        filename='logs/app.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    @app.route('/')
    def index():
        """Serve the main application page"""
        return render_template('index.html')
    
    @app.route('/search')
    def search():
        """Serve the flight search page"""
        return render_template('search.html')
    
    @app.route('/booking')
    def booking():
        """Serve the booking page"""
        return render_template('booking.html')
    
    @app.route('/confirmation')
    def confirmation():
        """Serve the booking confirmation page"""
        return render_template('confirmation.html')
    
    @app.route('/my-bookings')
    def my_bookings():
        """Serve the user bookings page"""
        return render_template('my-bookings.html')
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({{
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'flight-booking-frontend',
            'port': {self.port}
        }})
    
    @app.route('/api/flights/search', methods=['GET'])
    def search_flights():
        """Mock flight search endpoint"""
        # In production, this would call your backend API
        try:
            # Extract query parameters
            origin = request.args.get('origin', '')
            destination = request.args.get('destination', '')
            departure_date = request.args.get('departure_date', '')
            return_date = request.args.get('return_date', '')
            passengers = request.args.get('passengers', 1)
            
            # Mock flight data
            mock_flights = [
                {{
                    'id': 'FL123',
                    'airline': 'Sky Airlines',
                    'flight_number': 'SA789',
                    'origin': origin or 'JFK',
                    'destination': destination or 'LAX',
                    'departure_time': '08:00 AM',
                    'arrival_time': '11:00 AM',
                    'duration': '6h 0m',
                    'price': 299.99,
                    'currency': 'USD',
                    'seats_available': 45
                }},
                {{
                    'id': 'FL456',
                    'airline': 'Global Airways',
                    'flight_number': 'GA456',
                    'origin': origin or 'JFK',
                    'destination': destination or 'LAX',
                    'departure_time': '02:00 PM',
                    'arrival_time': '05:00 PM',
                    'duration': '6h 0m',
                    'price': 349.99,
                    'currency': 'USD',
                    'seats_available': 28
                }}
            ]
            
            return jsonify({{
                'success': True,
                'flights': mock_flights,
                'count': len(mock_flights),
                'search_params': {{
                    'origin': origin,
                    'destination': destination,
                    'departure_date': departure_date,
                    'return_date': return_date,
                    'passengers': passengers
                }}
            }})
            
        except Exception as e:
            logging.error(f"Error searching flights: {{e}}")
            return jsonify({{
                'success': False,
                'error': 'Failed to search flights'
            }}), 500
    
    @app.route('/api/bookings', methods=['POST'])
    def create_booking():
        """Mock booking creation endpoint"""
        try:
            data = request.get_json()
            
            # Mock booking response
            booking_reference = f"BK{{datetime.now().strftime('%Y%m%d%H%M%S')}}"
            
            return jsonify({{
                'success': True,
                'booking_reference': booking_reference,
                'message': 'Booking created successfully',
                'booking_details': {{
                    **data,
                    'status': 'confirmed',
                    'created_at': datetime.now().isoformat()
                }}
            }})
            
        except Exception as e:
            logging.error(f"Error creating booking: {{e}}")
            return jsonify({{
                'success': False,
                'error': 'Failed to create booking'
            }}), 500
    
    # Serve static files
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f"Server Error: {{error}}")
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('FRONTEND_PORT', {self.port}))
    host = os.getenv('HOST', '{self.host}')
    print(f"Starting Flight Booking App on {{host}}:{{port}}")
    app.run(host=host, port=port, debug=app.config['DEBUG'])
'''
        
        with open(self.project_dir / "app.py", "w") as f:
            f.write(app_content)
        
        print("  ✓ Created Flask application (app.py)")
        return True
    
    def create_html_templates(self):
        """Create HTML templates for the application"""
        print("🎨 Creating HTML templates...")
        
        # Base template
        base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SkyJet - Flight Booking{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    {% block head_extra %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <a href="/" class="logo">
                <i class="fas fa-plane"></i>
                <span>SkyJet</span>
            </a>
            <div class="nav-links">
                <a href="/search"><i class="fas fa-search"></i> Search Flights</a>
                <a href="/my-bookings"><i class="fas fa-ticket-alt"></i> My Bookings</a>
                <a href="#" id="login-btn"><i class="fas fa-user"></i> Sign In</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>SkyJet</h4>
                    <p>Your trusted partner for flight bookings. Find the best deals and travel with comfort.</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <a href="/search">Search Flights</a>
                    <a href="/my-bookings">My Bookings</a>
                    <a href="#">Contact Us</a>
                </div>
                <div class="footer-section">
                    <h4>Contact</h4>
                    <p><i class="fas fa-envelope"></i> support@skyjet.com</p>
                    <p><i class="fas fa-phone"></i> +1-800-FLY-SKYJET</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 SkyJet Flight Booking. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''
        
        # Index page
        index_template = '''{% extends "base.html" %}

{% block title %}SkyJet - Book Flights Worldwide{% endblock %}

{% block content %}
<div class="hero">
    <div class="container">
        <h1>Find Your Perfect Flight</h1>
        <p>Search and book flights across 500+ airlines worldwide</p>
        
        <!-- Search Form -->
        <div class="search-box">
            <form id="flight-search-form" action="/search" method="GET">
                <div class="form-row">
                    <div class="form-group">
                        <label for="origin"><i class="fas fa-plane-departure"></i> From</label>
                        <input type="text" id="origin" name="origin" placeholder="City or Airport" required>
                    </div>
                    <div class="form-group">
                        <label for="destination"><i class="fas fa-plane-arrival"></i> To</label>
                        <input type="text" id="destination" name="destination" placeholder="City or Airport" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="departure"><i class="fas fa-calendar-alt"></i> Departure</label>
                        <input type="date" id="departure" name="departure_date" required>
                    </div>
                    <div class="form-group">
                        <label for="return"><i class="fas fa-calendar-alt"></i> Return (Optional)</label>
                        <input type="date" id="return" name="return_date">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="passengers"><i class="fas fa-users"></i> Passengers</label>
                        <select id="passengers" name="passengers">
                            <option value="1">1 Passenger</option>
                            <option value="2">2 Passengers</option>
                            <option value="3">3 Passengers</option>
                            <option value="4">4 Passengers</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <button type="submit" class="btn-primary">
                            <i class="fas fa-search"></i> Search Flights
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>

<div class="features">
    <div class="container">
        <h2>Why Choose SkyJet?</h2>
        <div class="features-grid">
            <div class="feature-card">
                <i class="fas fa-bolt"></i>
                <h3>Instant Booking</h3>
                <p>Book your flights instantly with real-time confirmation</p>
            </div>
            <div class="feature-card">
                <i class="fas fa-shield-alt"></i>
                <h3>Secure Payment</h3>
                <p>100% secure payment with multiple options</p>
            </div>
            <div class="feature-card">
                <i class="fas fa-headset"></i>
                <h3>24/7 Support</h3>
                <p>Round-the-clock customer support</p>
            </div>
            <div class="feature-card">
                <i class="fas fa-tag"></i>
                <h3>Best Price Guarantee</h3>
                <p>We guarantee the best prices for your flights</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
        
        # Create simple templates for other pages
        search_template = '''{% extends "base.html" %}

{% block title %}Search Flights - SkyJet{% endblock %}

{% block content %}
<div class="container">
    <h1>Search Flights</h1>
    <p>Search functionality will be implemented here.</p>
</div>
{% endblock %}'''

        booking_template = '''{% extends "base.html" %}

{% block title %}Book Flight - SkyJet{% endblock %}

{% block content %}
<div class="container">
    <h1>Book Your Flight</h1>
    <p>Booking functionality will be implemented here.</p>
</div>
{% endblock %}'''

        confirmation_template = '''{% extends "base.html" %}

{% block title %}Booking Confirmed - SkyJet{% endblock %}

{% block content %}
<div class="container">
    <h1>🎉 Booking Confirmed!</h1>
    <p>Your flight has been successfully booked.</p>
</div>
{% endblock %}'''

        my_bookings_template = '''{% extends "base.html" %}

{% block title %}My Bookings - SkyJet{% endblock %}

{% block content %}
<div class="container">
    <h1>My Bookings</h1>
    <p>View and manage your bookings here.</p>
</div>
{% endblock %}'''
        
        # Save templates
        templates = {
            "base.html": base_template,
            "index.html": index_template,
            "search.html": search_template,
            "booking.html": booking_template,
            "confirmation.html": confirmation_template,
            "my-bookings.html": my_bookings_template,
            "404.html": "<h1>404 - Page Not Found</h1><p>The page you're looking for doesn't exist.</p>",
            "500.html": "<h1>500 - Server Error</h1><p>Something went wrong on our server.</p>"
        }
        
        for filename, content in templates.items():
            with open(self.templates_dir / filename, "w") as f:
                f.write(content)
        
        print(f"  ✓ Created {len(templates)} HTML templates")
        return True
    
    def create_static_files(self):
        """Create CSS and JavaScript files"""
        print("🎨 Creating static files...")
        
        # CSS file
        css_content = '''/* style.css */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 1rem 0;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: #667eea;
    font-size: 1.5rem;
    font-weight: 700;
}

.logo i {
    margin-right: 10px;
    font-size: 1.8rem;
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-links a {
    text-decoration: none;
    color: #666;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #667eea;
}

/* Hero Section */
.hero {
    padding: 4rem 0;
    color: white;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 3rem;
    opacity: 0.9;
}

/* Search Box */
.search-box {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    max-width: 800px;
    margin: 0 auto;
}

.form-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.form-group {
    flex: 1;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #666;
    font-weight: 500;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #e1e1e1;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: #667eea;
}

/* Buttons */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    transition: transform 0.3s;
}

.btn-primary:hover {
    transform: translateY(-2px);
}

/* Features */
.features {
    padding: 4rem 0;
    background: white;
}

.features h2 {
    text-align: center;
    margin-bottom: 3rem;
    font-size: 2rem;
    color: #333;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.feature-card {
    text-align: center;
    padding: 2rem;
    border-radius: 10px;
    background: #f8f9fa;
    transition: transform 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-card i {
    font-size: 2.5rem;
    color: #667eea;
    margin-bottom: 1rem;
}

.feature-card h3 {
    margin-bottom: 1rem;
    color: #333;
}

/* Main content area */
.main-content {
    min-height: 60vh;
    padding: 2rem 0;
}

.container h1 {
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.container p {
    color: white;
    text-align: center;
    font-size: 1.2rem;
}

/* Footer */
.footer {
    background: #333;
    color: white;
    padding: 3rem 0 1rem;
    margin-top: 4rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h4 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
}

.footer-section a {
    display: block;
    color: #ccc;
    text-decoration: none;
    margin-bottom: 0.5rem;
    transition: color 0.3s;
}

.footer-section a:hover {
    color: white;
}

.footer-section p {
    color: #ccc;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #444;
    color: #ccc;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }
    
    .form-row {
        flex-direction: column;
    }
    
    .nav-links {
        gap: 1rem;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
}'''
        
        # JavaScript file
        js_content = '''// main.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flight Booking Application loaded');
    
    // Set minimum date for departure to today
    const today = new Date().toISOString().split('T')[0];
    const departureInput = document.getElementById('departure');
    const returnInput = document.getElementById('return');
    
    if (departureInput) {
        departureInput.min = today;
        departureInput.value = today;
        
        // Set return date minimum to departure date
        departureInput.addEventListener('change', function() {
            if (returnInput) {
                returnInput.min = this.value;
                if (returnInput.value && returnInput.value < this.value) {
                    returnInput.value = this.value;
                }
            }
        });
    }
    
    // Login button functionality
    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Login functionality would open here.\\nFor demo purposes, you are logged in as a guest.');
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input[required], select[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#dc3545';
                } else {
                    input.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
});'''
        
        # Save static files
        with open(self.static_dir / "css" / "style.css", "w") as f:
            f.write(css_content)
        
        with open(self.static_dir / "js" / "main.js", "w") as f:
            f.write(js_content)
        
        # Create a sample image placeholder
        with open(self.static_dir / "images" / "README.md", "w") as f:
            f.write("Place flight-related images here (airplane icons, banners, etc.)")
        
        print("  ✓ Created CSS and JavaScript files")
        return True
    
    def create_dockerfile(self):
        """Create Dockerfile"""
        print("🐳 Creating Dockerfile...")
        
        dockerfile_content = f'''# Dockerfile for Flight Booking Frontend
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Your Name"
LABEL description="Flight Booking Frontend Application"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Copy requirements.txt FIRST for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port {self.port}
EXPOSE {self.port}

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:{self.port}/api/health', timeout=2)"

# Run the Flask application
CMD ["python", "app.py"]
'''
        
        with open(self.project_dir / "Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        print("  ✓ Created Dockerfile")
        return True
    
    def create_docker_compose(self):
        """Create docker-compose.yml"""
        print("🐳 Creating docker-compose.yml...")
        
        docker_compose_content = f'''# docker-compose.yml
version: '3.8'

services:
  flight-booking-frontend:
    build: .
    container_name: flight-booking-frontend
    ports:
      - "{self.port}:{self.port}"  # Host:Container port mapping
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${{SECRET_KEY:-your-production-secret-key}}
      - API_BASE_URL=${{API_BASE_URL:-http://backend:8000}}
      - FRONTEND_PORT={self.port}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:{self.port}/api/health', timeout=2)"]
      interval: 30s
      timeout: 10s
      retries: 3
'''
        
        with open(self.project_dir / "docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        
        print("  ✓ Created docker-compose.yml")
        return True
    
    def install_dependencies(self):
        """Install Python dependencies from requirements.txt"""
        print("📦 Installing dependencies from requirements.txt...")
        
        requirements_file = self.project_dir / "requirements.txt"
        
        if not requirements_file.exists():
            print("  ✗ requirements.txt not found!")
            return False
        
        try:
            # Read requirements
            with open(requirements_file, 'r') as f:
                requirements = f.read().splitlines()
            
            print(f"  Found {len(requirements)} packages in requirements.txt")
            
            # Install each package
            for req in requirements:
                if req.strip() and not req.strip().startswith('#'):
                    print(f"  Installing: {req}")
            
            # Install all packages
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "-r", str(requirements_file)
            ])
            
            print("  ✓ All dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to install dependencies: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    def create_run_script(self):
        """Create a simple run script"""
        print("⚡ Creating run script...")
        
        run_script = f'''#!/usr/bin/env python3
# run.py - Simple runner for Flight Booking App

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Get configuration
    port = int(os.getenv('FRONTEND_PORT', {self.port}))
    host = os.getenv('HOST', '{self.host}')
    
    print('=' * 60)
    print('✈️  Flight Booking Frontend Application')
    print('=' * 60)
    print(f'Local URL:    http://localhost:{{port}}')
    print(f'Network URL:  http://{{host}}:{{port}}')
    print(f'Health Check: http://localhost:{{port}}/api/health')
    print('=' * 60)
    print('Press Ctrl+C to stop the application')
    print('=' * 60)
    
    app.run(host=host, port=port, debug=True)
'''
        
        with open(self.project_dir / "run.py", "w") as f:
            f.write(run_script)
        
        print("  ✓ Created run.py script")
        return True
    
    def run_application(self):
        """Run the Flask application"""
        print(f"\n{'='*60}")
        print("🚀 STARTING FLIGHT BOOKING APPLICATION")
        print(f"📡 Port: {self.port}")
        print(f"🌐 Host: {self.host}")
        print("="*60)
        
        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(self.project_dir)
        
        try:
            # Try to open browser
            try:
                webbrowser.open(f"http://localhost:{self.port}")
                print(f"  ✓ Opening browser: http://localhost:{self.port}")
            except:
                print(f"  ℹ️  Application will be available at: http://localhost:{self.port}")
            
            # Run the application
            print("\nStarting Flask server...")
            subprocess.run([
                sys.executable, "app.py"
            ])
            
        except KeyboardInterrupt:
            print("\n\n🛑 Application stopped by user")
        except Exception as e:
            print(f"\n❌ Error running application: {e}")
        finally:
            os.chdir(original_dir)
    
    def deploy(self, skip_install=False):
        """Deploy the flight booking application"""
        print(f"\n{'='*60}")
        print("✈️  DEPLOYING FLIGHT BOOKING FRONTEND APPLICATION")
        print(f"📁 Project: {self.app_name}")
        print(f"📡 Port: {self.port}")
        print("="*60)
        
        try:
            # Create project structure
            self.create_directory_structure()
            print()
            
            # Create config files (including requirements.txt)
            self.create_config_files()
            print()
            
            # Create Flask app
            self.create_flask_app()
            print()
            
            # Create HTML templates
            self.create_html_templates()
            print()
            
            # Create static files
            self.create_static_files()
            print()
            
            # Create Docker config
            self.create_dockerfile()
            self.create_docker_compose()
            print()
            
            # Create run script
            self.create_run_script()
            print()
            
            # Install dependencies if not skipped
            if not skip_install:
                success = self.install_dependencies()
                if not success:
                    print("\n⚠️  Dependency installation failed or skipped")
                    print("   You can manually install with: pip install -r requirements.txt")
            print()
            
            print("="*60)
            print("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
            print("="*60)
            
            # Print next steps
            print("\n📋 NEXT STEPS:")
            print(f"1. Go to project directory: cd {self.app_name}")
            print("2. Run the application:")
            print(f"   - Quick start: python app.py")
            print(f"   - Using script: python run.py")
            print(f"   - With Docker: docker-compose up")
            print("\n🔧 CONFIGURATION:")
            print(f"   - Port: {self.port} (configurable in .env)")
            print("   - Backend API URL: Set in .env file")
            print("\n🌐 ACCESS:")
            print(f"   - Local: http://localhost:{self.port}")
            print(f"   - Health: http://localhost:{self.port}/api/health")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Deployment failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main function to parse arguments and run deployment"""
    parser = argparse.ArgumentParser(
        description="Deploy Flight Booking Frontend Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Deploy with default settings
  %(prog)s --name my-app        # Custom project name
  %(prog)s --port 8080          # Use port 8080
  %(prog)s --skip-install       # Skip dependency installation
  %(prog)s --run                # Run after deployment
        """
    )
    
    parser.add_argument("--name", default="flight-booking-app", 
                       help="Name of the application directory (default: %(default)s)")
    parser.add_argument("--port", type=int, default=5000,
                       help=f"Port to run the application on (default: %(default)s)")
    parser.add_argument("--host", default="0.0.0.0",
                       help="Host to bind the application to (default: %(default)s)")
    parser.add_argument("--skip-install", action="store_true",
                       help="Skip installing Python dependencies")
    parser.add_argument("--run", action="store_true",
                       help="Run the application after deployment")
    
    args = parser.parse_args()
    
    # Create deployer instance
    deployer = FlightBookingDeployer(
        app_name=args.name,
        port=args.port,
        host=args.host
    )
    
    # Check if directory already exists
    if deployer.project_dir.exists():
        print(f"⚠️  Directory '{args.name}' already exists.")
        response = input("Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Deployment cancelled.")
            return
    
    # Deploy the application
    success = deployer.deploy(skip_install=args.skip_install)
    
    # Run the application if requested
    if success and args.run:
        print("\n" + "="*60)
        response = input("Start the application now? (y/n): ").strip().lower()
        if response == 'y':
            deployer.run_application()

if __name__ == "__main__":
    main()
