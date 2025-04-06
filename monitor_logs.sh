#!/bin/bash

# This script provides log content to the extract_food_responses.py script
# It can be modified to fetch logs from various sources (files, APIs, etc.)

# Check if a log file is provided as an argument
if [ $# -eq 1 ]; then
    LOG_FILE="$1"
    if [ -f "$LOG_FILE" ]; then
        cat "$LOG_FILE"
        exit 0
    else
        echo "Error: Log file '$LOG_FILE' not found." >&2
        exit 1
    fi
fi

# If no argument is provided, use the default server_logs.txt
if [ -f "server_logs.txt" ]; then
    cat "server_logs.txt"
    exit 0
else
    # If server_logs.txt doesn't exist, provide a sample log
    echo "No log file found. Providing sample log content..."
    echo "2025-04-05T23:17:47.718694+00:00 app[web.1]: ✅ New client connected!"
    echo "🍽️ FOOD/CALORIE RESPONSE:"
    echo "2025-04-05T23:17:47.765729+00:00 app[web.1]: 📨 Message received: It looks like you're holding a can of Celsius Sparkling Energy Drink, which features flavors like strawberry and kiwi. If you're looking for nutritional information or calorie content for this drink, let me know!"
    echo "----------------------------------------"
    echo "2025-04-05T23:23:15.042911+00:00 app[web.1]: ✅ New client connected!"
    echo "🍽️ FOOD/CALORIE RESPONSE:"
    echo "2025-04-05T23:23:15.091706+00:00 app[web.1]: 📨 Message received: If you're looking to track calories, typically a can like this has around 10 calories or fewer, but it's always good to check the specific label for accurate information."
    echo "----------------------------------------"
    echo "2025-04-05T23:27:43.607157+00:00 app[web.1]: ✅ New client connected!"
    echo "🍽️ FOOD/CALORIE RESPONSE:"
    echo "2025-04-05T23:27:43.681387+00:00 app[web.1]: 📨 Message received: It looks like you have a can of Celsius Sparkling Kiwi Strawberry in your hand. This drink is often marketed as a fitness beverage, providing essential energy and metabolism-boosting benefits with zero calories."
    exit 0
fi 