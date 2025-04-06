# NutriLens - Dynamic Food Analysis

A modern web application for analyzing and tracking nutritional information of food items in real-time.

## Features

- Real-time food analysis dashboard
- Interactive nutritional charts
- Dynamic data updates using WebSocket
- SQLite database for data persistence
- Modern UI with Apple Design Guidelines
- Responsive design for all devices

## Project Structure

```
nutrilens/
├── src/
│   ├── static/         # Static files (CSS, JS)
│   ├── templates/      # HTML templates
│   └── database/       # Database files
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nutrilens.git
cd nutrilens
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/app.py
```

The application will be available at `http://localhost:8080`

## Technologies Used

- Flask (Python web framework)
- Flask-SocketIO (WebSocket support)
- SQLite (Database)
- Chart.js (Data visualization)
- Pandas (Data processing)
- HTML5/CSS3 (Frontend)

## License

MIT License 