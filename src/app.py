from flask import Flask, render_template_string, jsonify
import json
import sqlite3
from datetime import datetime
import pandas as pd
import numpy as np
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database setup
def init_db():
    conn = sqlite3.connect('food_analysis.db')
    c = conn.cursor()
    
    # Create food items table
    c.execute('''CREATE TABLE IF NOT EXISTS food_items
                 (id INTEGER PRIMARY KEY, name TEXT, calories INTEGER, 
                  protein REAL, carbs REAL, fat REAL, fiber REAL,
                  iron REAL, calcium REAL, magnesium REAL, zinc REAL, potassium REAL,
                  benefits TEXT, drawbacks TEXT, alternatives TEXT,
                  timestamp DATETIME)''')
    
    # Create meal_logs table
    c.execute('''CREATE TABLE IF NOT EXISTS meal_logs
                 (id INTEGER PRIMARY KEY, food_id INTEGER, meal_type TEXT,
                  timestamp DATETIME, FOREIGN KEY (food_id) REFERENCES food_items(id))''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

def calculate_nutritional_stats():
    conn = sqlite3.connect('food_analysis.db')
    df = pd.read_sql_query("SELECT * FROM food_items", conn)
    
    if df.empty:
        return {
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fat': 0,
            'total_fiber': 0
        }
    
    stats = {
        'total_calories': df['calories'].sum(),
        'total_protein': df['protein'].sum(),
        'total_carbs': df['carbs'].sum(),
        'total_fat': df['fat'].sum(),
        'total_fiber': df['fiber'].sum()
    }
    
    conn.close()
    return stats

def get_meal_distribution():
    conn = sqlite3.connect('food_analysis.db')
    df = pd.read_sql_query("""
        SELECT meal_type, SUM(f.calories) as total_calories
        FROM meal_logs m
        JOIN food_items f ON m.food_id = f.id
        GROUP BY meal_type
    """, conn)
    
    meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snacks']
    calories = [0] * 4
    
    for i, meal_type in enumerate(meal_types):
        if meal_type in df['meal_type'].values:
            calories[i] = df[df['meal_type'] == meal_type]['total_calories'].iloc[0]
    
    conn.close()
    return calories

def get_mineral_intake():
    conn = sqlite3.connect('food_analysis.db')
    df = pd.read_sql_query("""
        SELECT 
            AVG(iron) as iron,
            AVG(calcium) as calcium,
            AVG(magnesium) as magnesium,
            AVG(zinc) as zinc,
            AVG(potassium) as potassium
        FROM food_items
    """, conn)
    
    # Convert to percentages (assuming daily recommended values)
    daily_values = {
        'iron': 18,  # mg
        'calcium': 1000,  # mg
        'magnesium': 400,  # mg
        'zinc': 11,  # mg
        'potassium': 3500  # mg
    }
    
    minerals = {
        'iron': (df['iron'].iloc[0] / daily_values['iron']) * 100,
        'calcium': (df['calcium'].iloc[0] / daily_values['calcium']) * 100,
        'magnesium': (df['magnesium'].iloc[0] / daily_values['magnesium']) * 100,
        'zinc': (df['zinc'].iloc[0] / daily_values['zinc']) * 100,
        'potassium': (df['potassium'].iloc[0] / daily_values['potassium']) * 100
    }
    
    conn.close()
    return list(minerals.values())

def get_macronutrient_distribution():
    conn = sqlite3.connect('food_analysis.db')
    df = pd.read_sql_query("""
        SELECT SUM(protein) as total_protein,
               SUM(carbs) as total_carbs,
               SUM(fat) as total_fat
        FROM food_items
    """, conn)
    
    total = df['total_protein'].iloc[0] + df['total_carbs'].iloc[0] + df['total_fat'].iloc[0]
    if total == 0:
        return [0, 0, 0]
    
    distribution = [
        (df['total_protein'].iloc[0] / total) * 100,
        (df['total_carbs'].iloc[0] / total) * 100,
        (df['total_fat'].iloc[0] / total) * 100
    ]
    
    conn.close()
    return distribution

# HTML Template (same as before, but with dynamic data)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NutriLens - Dynamic Food Analysis</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        /* Same CSS as before */
        :root {
            --primary-color: #007AFF;
            --text-color: #000000;
            --background-color: #F2F2F7;
            --card-background: #FFFFFF;
            --border-radius: 12px;
            --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            --spacing-unit: 8px;
            --font-size-base: 16px;
            --font-size-small: 14px;
            --font-size-large: 20px;
        }

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, 
                rgba(0, 122, 255, 0.3) 0%,
                rgba(88, 86, 214, 0.2) 50%,
                rgba(255, 255, 255, 0.9) 100%);
            min-height: 100vh;
            color: var(--text-color);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: calc(var(--spacing-unit) * 3);
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: calc(var(--spacing-unit) * 4);
            padding: calc(var(--spacing-unit) * 2);
            background: var(--card-background);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
        }

        .logo {
            font-size: var(--font-size-large);
            font-weight: 600;
            color: var(--primary-color);
        }

        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: calc(var(--spacing-unit) * 2);
            margin-bottom: calc(var(--spacing-unit) * 4);
        }

        .stat-card {
            background: var(--card-background);
            padding: calc(var(--spacing-unit) * 2);
            border-radius: var(--border-radius);
            text-align: center;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            background: linear-gradient(135deg, var(--primary-color), #5856D6);
        }

        .stat-card:hover .stat-value,
        .stat-card:hover .stat-label {
            color: white;
        }

        .stat-value {
            font-size: var(--font-size-large);
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: var(--spacing-unit);
            transition: color 0.3s ease;
        }

        .stat-label {
            font-size: var(--font-size-small);
            color: var(--text-color);
            transition: color 0.3s ease;
        }

        .controls {
            display: flex;
            gap: calc(var(--spacing-unit) * 2);
            margin-bottom: calc(var(--spacing-unit) * 4);
        }

        .button {
            padding: calc(var(--spacing-unit) * 1.5) calc(var(--spacing-unit) * 3);
            border: none;
            border-radius: var(--border-radius);
            background: var(--primary-color);
            color: white;
            font-size: var(--font-size-base);
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .button:hover {
            background: #0056b3;
            transform: translateY(-2px);
        }

        .food-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: calc(var(--spacing-unit) * 3);
            margin-bottom: calc(var(--spacing-unit) * 4);
        }

        .food-card {
            background: var(--card-background);
            border-radius: var(--border-radius);
            padding: calc(var(--spacing-unit) * 2);
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }

        .food-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .food-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: calc(var(--spacing-unit) * 2);
        }

        .food-name {
            font-size: var(--font-size-large);
            font-weight: 600;
            color: var(--text-color);
        }

        .food-calories {
            font-size: var(--font-size-base);
            color: var(--primary-color);
            font-weight: 500;
        }

        .nutrition-info {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: calc(var(--spacing-unit) * 2);
            margin-bottom: calc(var(--spacing-unit) * 2);
        }

        .nutrition-item {
            display: flex;
            flex-direction: column;
        }

        .nutrition-label {
            font-size: var(--font-size-small);
            color: #666;
        }

        .nutrition-value {
            font-size: var(--font-size-base);
            font-weight: 500;
        }

        .food-details {
            margin-top: calc(var(--spacing-unit) * 2);
            padding-top: calc(var(--spacing-unit) * 2);
            border-top: 1px solid #eee;
        }

        .detail-section {
            margin-bottom: calc(var(--spacing-unit) * 2);
        }

        .detail-title {
            font-size: var(--font-size-base);
            font-weight: 600;
            margin-bottom: var(--spacing-unit);
            color: var(--text-color);
        }

        .detail-content {
            font-size: var(--font-size-small);
            color: #666;
            line-height: 1.5;
        }

        .graphs-section {
            margin-top: calc(var(--spacing-unit) * 4);
            padding: calc(var(--spacing-unit) * 3);
            background: var(--card-background);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
        }

        .graphs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: calc(var(--spacing-unit) * 3);
            margin-top: calc(var(--spacing-unit) * 2);
        }

        .graph-container {
            background: var(--background-color);
            padding: calc(var(--spacing-unit) * 2);
            border-radius: var(--border-radius);
            height: 300px;
        }

        .graph-title {
            font-size: var(--font-size-base);
            font-weight: 600;
            margin-bottom: calc(var(--spacing-unit) * 2);
            color: var(--text-color);
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">NutriLens</div>
            <div class="controls">
                <button class="button" onclick="refreshData()">Refresh</button>
                <button class="button" onclick="filterData()">Filter</button>
                <button class="button" onclick="sortData()">Sort</button>
            </div>
        </div>

        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value" id="total-items">0</div>
                <div class="stat-label">Food Items</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-calories">0</div>
                <div class="stat-label">Total Calories</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-protein">0g</div>
                <div class="stat-label">Total Protein</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-fiber">0g</div>
                <div class="stat-label">Total Fiber</div>
            </div>
        </div>

        <div class="food-grid" id="food-grid">
            <!-- Food items will be dynamically inserted here -->
        </div>

        <div class="graphs-section">
            <div class="graph-title">Nutritional Analytics</div>
            <div class="graphs-grid">
                <div class="graph-container">
                    <canvas id="macronutrientsChart"></canvas>
                </div>
                <div class="graph-container">
                    <canvas id="caloriesChart"></canvas>
                </div>
                <div class="graph-container">
                    <canvas id="mineralsChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        let macronutrientsChart, caloriesChart, mineralsChart;

        function updateStats(stats) {
            document.getElementById('total-items').textContent = stats.total_items;
            document.getElementById('total-calories').textContent = stats.total_calories;
            document.getElementById('total-protein').textContent = stats.total_protein + 'g';
            document.getElementById('total-fiber').textContent = stats.total_fiber + 'g';
        }

        function updateFoodGrid(foods) {
            const grid = document.getElementById('food-grid');
            grid.innerHTML = '';
            
            foods.forEach(food => {
                const card = document.createElement('div');
                card.className = 'food-card';
                card.innerHTML = `
                    <div class="food-header">
                        <div class="food-name">${food.name}</div>
                        <div class="food-calories">${food.calories} kcal</div>
                    </div>
                    <div class="nutrition-info">
                        <div class="nutrition-item">
                            <div class="nutrition-label">Protein</div>
                            <div class="nutrition-value">${food.protein}g</div>
                        </div>
                        <div class="nutrition-item">
                            <div class="nutrition-label">Carbs</div>
                            <div class="nutrition-value">${food.carbs}g</div>
                        </div>
                        <div class="nutrition-item">
                            <div class="nutrition-label">Fat</div>
                            <div class="nutrition-value">${food.fat}g</div>
                        </div>
                        <div class="nutrition-item">
                            <div class="nutrition-label">Fiber</div>
                            <div class="nutrition-value">${food.fiber}g</div>
                        </div>
                    </div>
                    <div class="food-details">
                        <div class="detail-section">
                            <div class="detail-title">Benefits</div>
                            <div class="detail-content">${food.benefits}</div>
                        </div>
                        <div class="detail-section">
                            <div class="detail-title">Drawbacks</div>
                            <div class="detail-content">${food.drawbacks}</div>
                        </div>
                        <div class="detail-section">
                            <div class="detail-title">Alternatives</div>
                            <div class="detail-content">${food.alternatives}</div>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function updateCharts(data) {
            // Update Macronutrients Chart
            if (macronutrientsChart) {
                macronutrientsChart.destroy();
            }
            const macronutrientsCtx = document.getElementById('macronutrientsChart').getContext('2d');
            macronutrientsChart = new Chart(macronutrientsCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Protein', 'Carbs', 'Fat'],
                    datasets: [{
                        data: data.macronutrients,
                        backgroundColor: [
                            'rgba(52, 199, 89, 0.8)',
                            'rgba(0, 122, 255, 0.8)',
                            'rgba(255, 149, 0, 0.8)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Macronutrient Distribution'
                        }
                    }
                }
            });

            // Update Calories Chart
            if (caloriesChart) {
                caloriesChart.destroy();
            }
            const caloriesCtx = document.getElementById('caloriesChart').getContext('2d');
            caloriesChart = new Chart(caloriesCtx, {
                type: 'bar',
                data: {
                    labels: ['Breakfast', 'Lunch', 'Dinner', 'Snacks'],
                    datasets: [{
                        label: 'Calories',
                        data: data.meal_calories,
                        backgroundColor: 'rgba(88, 86, 214, 0.8)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Calories by Meal'
                        }
                    }
                }
            });

            // Update Minerals Chart
            if (mineralsChart) {
                mineralsChart.destroy();
            }
            const mineralsCtx = document.getElementById('mineralsChart').getContext('2d');
            mineralsChart = new Chart(mineralsCtx, {
                type: 'radar',
                data: {
                    labels: ['Iron', 'Calcium', 'Magnesium', 'Zinc', 'Potassium'],
                    datasets: [{
                        label: 'Daily Intake %',
                        data: data.minerals,
                        backgroundColor: 'rgba(0, 122, 255, 0.2)',
                        borderColor: 'rgba(0, 122, 255, 0.8)',
                        pointBackgroundColor: 'rgba(0, 122, 255, 0.8)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Mineral Intake'
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        function refreshData() {
            socket.emit('refresh_data');
        }

        function filterData() {
            // Implement filtering logic
        }

        function sortData() {
            // Implement sorting logic
        }

        socket.on('update_data', function(data) {
            updateStats(data.stats);
            updateFoodGrid(data.foods);
            updateCharts(data.charts);
        });

        // Initial data load
        socket.emit('refresh_data');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    return jsonify(calculate_nutritional_stats())

@app.route('/api/foods')
def get_foods():
    conn = sqlite3.connect('food_analysis.db')
    c = conn.cursor()
    c.execute("SELECT * FROM food_items ORDER BY timestamp DESC")
    foods = [dict(zip([col[0] for col in c.description], row)) for row in c.fetchall()]
    conn.close()
    return jsonify(foods)

@app.route('/api/charts')
def get_charts_data():
    return jsonify({
        'macronutrients': get_macronutrient_distribution(),
        'meal_calories': get_meal_distribution(),
        'minerals': get_mineral_intake()
    })

@socketio.on('refresh_data')
def handle_refresh():
    stats = calculate_nutritional_stats()
    foods = get_foods().json
    charts = {
        'macronutrients': get_macronutrient_distribution(),
        'meal_calories': get_meal_distribution(),
        'minerals': get_mineral_intake()
    }
    
    socketio.emit('update_data', {
        'stats': stats,
        'foods': foods,
        'charts': charts
    })

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True) 