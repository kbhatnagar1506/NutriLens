#!/usr/bin/env python3
import re
import time
from datetime import datetime
import json
import websocket
import threading
import queue
from flask import Flask, render_template_string

# Flask app configuration
app = Flask(__name__)

# Global variables
SERVER_RESPONSES = []
log_queue = queue.Queue()

# WebSocket configuration
WEBSOCKET_ROOT_URL = "wss://krishna-websocket-123-cbb50832eaae.herokuapp.com"
WEBSOCKET_URL = f"{WEBSOCKET_ROOT_URL}/socket.io/?EIO=4&transport=websocket"

# Add new interactive features
INTERACTIVE_FEATURES = {
    "meal_planner": True,
    "nutrition_tracker": True,
    "food_search": True,
    "personalized_recommendations": True
}

# Enhanced food analysis data with more details
FOOD_ANALYSIS_DATA = [
    {
        "id": 1,
        "name": "Peanut Butter Sandwich",
        "calories": 350,
        "protein": 15,
        "carbs": 42,
        "fat": 16,
        "fiber": 4,
        "sugar": 8,
        "sodium": 380,
        "potassium": 180,
        "vitamins": ["B6", "E", "Niacin"],
        "minerals": ["Iron", "Magnesium", "Zinc"],
        "benefits": [
            "Good source of plant-based protein",
            "Contains heart-healthy monounsaturated fats",
            "Provides sustained energy through complex carbs",
            "Rich in fiber for digestive health"
        ],
        "drawbacks": [
            "High in calories per serving",
            "Contains added sugars in some brands",
            "May contain allergens (peanuts)"
        ],
        "alternatives": [
            "Almond butter (higher in calcium)",
            "Sunflower seed butter (allergen-free option)",
            "Hummus (lower in calories, higher in fiber)"
        ],
        "timestamp": "2023-06-15 08:30:45",
        "meal_type": "Breakfast",
        "glycemic_index": "Medium",
        "satiety_index": "High",
        "processing_level": "Minimally processed",
        "sustainability_score": "Medium",
        "cost_per_serving": "$0.75",
        "preparation_time": "5 minutes",
        "storage_life": "5 days",
        "seasonal_availability": "Year-round",
        "environmental_impact": "Low",
        "allergen_info": ["Peanuts", "Wheat", "Dairy"],
        "allergy_precautions": [
            "Contains peanuts - avoid if you have a peanut allergy",
            "Contains wheat - avoid if you have celiac disease or gluten sensitivity",
            "May contain dairy - check ingredients if you have a dairy allergy",
            "May contain traces of tree nuts - check packaging for allergen warnings"
        ],
        "portion_size": "1 sandwich",
        "serving_weight": "150g",
        "nutrient_density_score": 8.5,
        "health_score": 7.8,
        "sustainability_rating": "Good",
        "price_per_100g": "$0.50",
        "carbon_footprint": "0.2 kg CO2",
        "water_footprint": "500 liters",
        "packaging": "Minimal",
        "origin": "Local",
        "certifications": ["Organic", "Non-GMO"],
        "recipe_complexity": "Easy",
        "cooking_method": "No cooking required",
        "equipment_needed": ["Knife", "Plate"],
        "skill_level": "Beginner",
        "time_of_day": "Morning",
        "meal_prep_friendly": True,
        "freezer_friendly": False,
        "microwave_friendly": False,
        "portable": True,
        "kid_friendly": True,
        "vegetarian": True,
        "vegan": True,
        "gluten_free_option": True,
        "dairy_free_option": True,
        "nut_free_option": False,
        "low_fodmap": True,
        "keto_friendly": False,
        "paleo_friendly": False,
        "mediterranean_diet": True,
        "dash_diet": True,
        "weight_loss_friendly": True,
        "muscle_gain_friendly": True,
        "heart_healthy": True,
        "diabetes_friendly": True,
        "blood_pressure_friendly": True,
        "cholesterol_friendly": True,
        "bone_health": True,
        "brain_health": True,
        "immune_system": True,
        "gut_health": True,
        "skin_health": True,
        "hair_health": True,
        "eye_health": True,
        "dental_health": True,
        "energy_level": "High",
        "satiety_duration": "3-4 hours",
        "digestion_time": "2-3 hours",
        "blood_sugar_impact": "Moderate",
        "hormone_impact": "Positive",
        "inflammation_impact": "Low",
        "oxidative_stress": "Low",
        "antioxidant_content": "Moderate",
        "phytochemical_content": "High",
        "prebiotic_content": "Moderate",
        "probiotic_content": "None",
        "fiber_types": ["Soluble", "Insoluble"],
        "protein_quality": "Good",
        "fat_types": ["Monounsaturated", "Polyunsaturated", "Saturated"],
        "carb_types": ["Complex", "Simple"],
        "mineral_bioavailability": "High",
        "vitamin_bioavailability": "High",
        "nutrient_interactions": ["Iron-Vitamin C", "Calcium-Vitamin D"],
        "food_combinations": ["Banana", "Honey", "Jelly"],
        "cultural_significance": "American",
        "historical_background": "Popular since 1900s",
        "social_aspects": ["Lunch box staple", "Quick meal"],
        "psychological_benefits": ["Comfort food", "Satisfying"],
        "economic_aspects": ["Budget-friendly", "Cost-effective"],
        "sustainability_aspects": ["Low waste", "Local ingredients"],
        "future_trends": ["Plant-based alternatives", "Clean label"],
        "research_background": ["Clinical studies", "Nutritional research"],
        "expert_recommendations": ["Dietitians", "Nutritionists"],
        "user_ratings": {
            "taste": 4.5,
            "health": 4.2,
            "convenience": 4.8,
            "value": 4.6,
            "sustainability": 4.3
        },
        "expert_ratings": {
            "nutrition": 4.4,
            "sustainability": 4.1,
            "health_impact": 4.3,
            "environmental_impact": 4.2
        },
        "market_trends": {
            "popularity": "Increasing",
            "demand": "High",
            "price_trend": "Stable",
            "availability": "Wide"
        },
        "scientific_background": {
            "studies": ["Nutrition Journal 2022", "Food Science Review 2023"],
            "findings": ["Positive health outcomes", "Sustainable choice"],
            "recommendations": ["Regular consumption", "Portion control"]
        }
    },
    {
        "id": 2,
        "name": "Chicken and Rice Bowl",
        "calories": 520,
        "protein": 35,
        "carbs": 65,
        "fat": 12,
        "fiber": 3,
        "sugar": 1,
        "sodium": 420,
        "potassium": 320,
        "vitamins": ["B12", "B6", "Niacin", "Folate"],
        "minerals": ["Iron", "Selenium", "Zinc", "Phosphorus"],
        "benefits": [
            "Complete protein source with all essential amino acids",
            "Complex carbohydrates for sustained energy",
            "Low in saturated fat",
            "Good source of B vitamins for energy metabolism"
        ],
        "drawbacks": [
            "May be high in sodium depending on preparation",
            "White rice has lower fiber than brown rice",
            "Portion size can easily exceed calorie needs"
        ],
        "alternatives": [
            "Brown rice (higher in fiber and nutrients)",
            "Quinoa (complete protein, higher in minerals)",
            "Cauliflower rice (lower in calories and carbs)"
        ],
        "timestamp": "2023-06-15 12:15:22",
        "meal_type": "Lunch",
        "glycemic_index": "Medium",
        "satiety_index": "High",
        "processing_level": "Minimally processed",
        "sustainability_score": "Medium",
        "cost_per_serving": "$2.50",
        "preparation_time": "20 minutes",
        "storage_life": "3 days",
        "seasonal_availability": "Year-round",
        "environmental_impact": "Medium",
        "allergen_info": ["Soy", "Eggs", "Sesame"],
        "allergy_precautions": [
            "May contain soy sauce - avoid if you have a soy allergy",
            "May contain eggs in sauces - check ingredients if you have an egg allergy",
            "May contain sesame oil - avoid if you have a sesame allergy",
            "Cross-contamination with nuts possible in restaurant settings"
        ],
        "portion_size": "1 bowl",
        "serving_weight": "350g",
        "nutrient_density_score": 7.8,
        "health_score": 8.2,
        "sustainability_rating": "Medium",
        "price_per_100g": "$0.71",
        "carbon_footprint": "0.8 kg CO2",
        "water_footprint": "1200 liters",
        "packaging": "Minimal",
        "origin": "Local",
        "certifications": ["Organic"],
        "recipe_complexity": "Medium",
        "cooking_method": "Stovetop",
        "equipment_needed": ["Pot", "Pan", "Knife", "Cutting board"],
        "skill_level": "Intermediate",
        "time_of_day": "Lunch",
        "meal_prep_friendly": True,
        "freezer_friendly": True,
        "microwave_friendly": True,
        "portable": True,
        "kid_friendly": True,
        "vegetarian": False,
        "vegan": False,
        "gluten_free_option": True,
        "dairy_free_option": True,
        "nut_free_option": True,
        "low_fodmap": False,
        "keto_friendly": False,
        "paleo_friendly": False,
        "mediterranean_diet": True,
        "dash_diet": True,
        "weight_loss_friendly": True,
        "muscle_gain_friendly": True,
        "heart_healthy": True,
        "diabetes_friendly": True,
        "blood_pressure_friendly": True,
        "cholesterol_friendly": True,
        "bone_health": True,
        "brain_health": True,
        "immune_system": True,
        "gut_health": True,
        "skin_health": True,
        "hair_health": True,
        "eye_health": True,
        "dental_health": True,
        "energy_level": "High",
        "satiety_duration": "4-5 hours",
        "digestion_time": "3-4 hours",
        "blood_sugar_impact": "Moderate",
        "hormone_impact": "Positive",
        "inflammation_impact": "Low",
        "oxidative_stress": "Low",
        "antioxidant_content": "Moderate",
        "phytochemical_content": "Moderate",
        "prebiotic_content": "Low",
        "probiotic_content": "None",
        "fiber_types": ["Insoluble"],
        "protein_quality": "Excellent",
        "fat_types": ["Monounsaturated", "Polyunsaturated", "Saturated"],
        "carb_types": ["Complex"],
        "mineral_bioavailability": "High",
        "vitamin_bioavailability": "High",
        "nutrient_interactions": ["Iron-Vitamin C", "Zinc-Vitamin A"],
        "food_combinations": ["Vegetables", "Sauces", "Spices"],
        "cultural_significance": "Asian-inspired",
        "historical_background": "Modern fusion dish",
        "social_aspects": ["Lunch option", "Meal prep staple"],
        "psychological_benefits": ["Satisfying", "Comfort food"],
        "economic_aspects": ["Cost-effective", "Budget-friendly"],
        "sustainability_aspects": ["Local ingredients", "Minimal waste"],
        "future_trends": ["Plant-based alternatives", "Clean label"],
        "research_background": ["Nutritional studies", "Dietary research"],
        "expert_recommendations": ["Dietitians", "Nutritionists"],
        "user_ratings": {
            "taste": 4.7,
            "health": 4.5,
            "convenience": 4.3,
            "value": 4.6,
            "sustainability": 4.2
        },
        "expert_ratings": {
            "nutrition": 4.6,
            "sustainability": 4.3,
            "health_impact": 4.5,
            "environmental_impact": 4.1
        },
        "market_trends": {
            "popularity": "High",
            "demand": "High",
            "price_trend": "Stable",
            "availability": "Wide"
        },
        "scientific_background": {
            "studies": ["Nutrition Journal 2022", "Food Science Review 2023"],
            "findings": ["Positive health outcomes", "Balanced nutrition"],
            "recommendations": ["Regular consumption", "Portion control"]
        }
    },
    {
        "id": 3,
        "name": "Spaghetti with Tomato Sauce",
        "calories": 480,
        "protein": 12,
        "carbs": 82,
        "fat": 8,
        "fiber": 5,
        "sugar": 8,
        "sodium": 580,
        "potassium": 420,
        "vitamins": ["C", "A", "K", "B6", "Folate"],
        "minerals": ["Iron", "Potassium", "Manganese"],
        "benefits": [
            "Good source of lycopene (antioxidant in tomatoes)",
            "Provides complex carbohydrates for energy",
            "Contains fiber for digestive health",
            "Rich in vitamins A and C for immune function"
        ],
        "drawbacks": [
            "High in refined carbohydrates",
            "Can be high in sodium",
            "Limited protein content",
            "May cause blood sugar spikes"
        ],
        "alternatives": [
            "Zucchini noodles (lower in calories and carbs)",
            "Lentil pasta (higher in protein and fiber)",
            "Whole grain spaghetti (higher in fiber and nutrients)"
        ],
        "timestamp": "2023-06-15 18:45:10",
        "meal_type": "Dinner",
        "glycemic_index": "High",
        "satiety_index": "Medium",
        "processing_level": "Moderately processed",
        "sustainability_score": "Medium",
        "cost_per_serving": "$1.75",
        "preparation_time": "25 minutes",
        "storage_life": "3 days",
        "seasonal_availability": "Year-round",
        "environmental_impact": "Low",
        "allergen_info": ["Wheat", "Eggs", "Garlic", "Onion"],
        "allergy_precautions": [
            "Contains wheat - avoid if you have celiac disease or gluten sensitivity",
            "Contains eggs in pasta - check ingredients if you have an egg allergy",
            "Contains garlic and onion - avoid if you have FODMAP sensitivity",
            "May contain traces of nuts - check packaging for allergen warnings"
        ],
        "portion_size": "1 plate",
        "serving_weight": "300g",
        "nutrient_density_score": 6.5,
        "health_score": 6.8,
        "sustainability_rating": "Medium",
        "price_per_100g": "$0.58",
        "carbon_footprint": "0.5 kg CO2",
        "water_footprint": "800 liters",
        "packaging": "Minimal",
        "origin": "Italian-inspired",
        "certifications": ["Organic"],
        "recipe_complexity": "Easy",
        "cooking_method": "Stovetop",
        "equipment_needed": ["Pot", "Pan", "Colander", "Spoon"],
        "skill_level": "Beginner",
        "time_of_day": "Evening",
        "meal_prep_friendly": True,
        "freezer_friendly": True,
        "microwave_friendly": True,
        "portable": False,
        "kid_friendly": True,
        "vegetarian": True,
        "vegan": True,
        "gluten_free_option": True,
        "dairy_free_option": True,
        "nut_free_option": True,
        "low_fodmap": False,
        "keto_friendly": False,
        "paleo_friendly": False,
        "mediterranean_diet": True,
        "dash_diet": False,
        "weight_loss_friendly": False,
        "muscle_gain_friendly": False,
        "heart_healthy": True,
        "diabetes_friendly": False,
        "blood_pressure_friendly": False,
        "cholesterol_friendly": True,
        "bone_health": True,
        "brain_health": True,
        "immune_system": True,
        "gut_health": True,
        "skin_health": True,
        "hair_health": True,
        "eye_health": True,
        "dental_health": True,
        "energy_level": "High",
        "satiety_duration": "2-3 hours",
        "digestion_time": "2-3 hours",
        "blood_sugar_impact": "High",
        "hormone_impact": "Neutral",
        "inflammation_impact": "Low",
        "oxidative_stress": "Low",
        "antioxidant_content": "High",
        "phytochemical_content": "High",
        "prebiotic_content": "Low",
        "probiotic_content": "None",
        "fiber_types": ["Insoluble"],
        "protein_quality": "Low",
        "fat_types": ["Monounsaturated", "Polyunsaturated", "Saturated"],
        "carb_types": ["Complex", "Simple"],
        "mineral_bioavailability": "Medium",
        "vitamin_bioavailability": "High",
        "nutrient_interactions": ["Iron-Vitamin C", "Lycopene-Fat"],
        "food_combinations": ["Parmesan cheese", "Basil", "Olive oil"],
        "cultural_significance": "Italian",
        "historical_background": "Traditional Italian dish",
        "social_aspects": ["Family meal", "Comfort food"],
        "psychological_benefits": ["Comfort food", "Satisfying"],
        "economic_aspects": ["Budget-friendly", "Cost-effective"],
        "sustainability_aspects": ["Plant-based", "Local ingredients"],
        "future_trends": ["Plant-based alternatives", "Clean label"],
        "research_background": ["Nutritional studies", "Dietary research"],
        "expert_recommendations": ["Dietitians", "Nutritionists"],
        "user_ratings": {
            "taste": 4.8,
            "health": 4.0,
            "convenience": 4.5,
            "value": 4.7,
            "sustainability": 4.3
        },
        "expert_ratings": {
            "nutrition": 4.2,
            "sustainability": 4.4,
            "health_impact": 4.1,
            "environmental_impact": 4.5
        },
        "market_trends": {
            "popularity": "High",
            "demand": "High",
            "price_trend": "Stable",
            "availability": "Wide"
        },
        "scientific_background": {
            "studies": ["Nutrition Journal 2022", "Food Science Review 2023"],
            "findings": ["Positive health outcomes", "Antioxidant benefits"],
            "recommendations": ["Moderate consumption", "Portion control"]
        }
    },
    {
        "id": 4,
        "name": "Greek Yogurt with Granola",
        "calories": 320,
        "protein": 20,
        "carbs": 35,
        "fat": 10,
        "fiber": 4,
        "sugar": 18,
        "sodium": 65,
        "potassium": 240,
        "vitamins": ["B12", "Riboflavin", "B6", "D"],
        "minerals": ["Calcium", "Phosphorus", "Selenium", "Zinc"],
        "benefits": [
            "Excellent source of protein and calcium",
            "Contains probiotics for gut health",
            "Provides sustained energy through complex carbs",
            "Rich in B vitamins for energy metabolism"
        ],
        "drawbacks": [
            "Can be high in added sugars",
            "Granola is calorie-dense",
            "May contain allergens (nuts, dairy)"
        ],
        "alternatives": [
            "Plain yogurt with fresh fruit (lower in sugar)",
            "Cottage cheese with berries (higher in protein)",
            "Overnight oats (higher in fiber, lower in sugar)"
        ],
        "timestamp": "2023-06-16 07:20:33",
        "meal_type": "Breakfast",
        "glycemic_index": "Medium",
        "satiety_index": "High",
        "processing_level": "Minimally to moderately processed",
        "sustainability_score": "Medium",
        "cost_per_serving": "$2.25",
        "preparation_time": "5 minutes",
        "storage_life": "7 days",
        "seasonal_availability": "Year-round",
        "environmental_impact": "Medium",
        "allergen_info": ["Dairy", "Nuts", "Wheat", "Soy"],
        "allergy_precautions": [
            "Contains dairy - avoid if you have a dairy allergy or lactose intolerance",
            "Contains nuts in granola - avoid if you have a nut allergy",
            "Contains wheat in granola - avoid if you have celiac disease or gluten sensitivity",
            "May contain soy - check ingredients if you have a soy allergy",
            "Cross-contamination with other allergens possible in manufacturing facilities"
        ],
        "portion_size": "1 bowl",
        "serving_weight": "200g",
        "nutrient_density_score": 8.2,
        "health_score": 8.5,
        "sustainability_rating": "Medium",
        "price_per_100g": "$1.13",
        "carbon_footprint": "0.6 kg CO2",
        "water_footprint": "900 liters",
        "packaging": "Plastic container",
        "origin": "Greek-inspired",
        "certifications": ["Organic", "Non-GMO"],
        "recipe_complexity": "Easy",
        "cooking_method": "No cooking required",
        "equipment_needed": ["Bowl", "Spoon"],
        "skill_level": "Beginner",
        "time_of_day": "Morning",
        "meal_prep_friendly": True,
        "freezer_friendly": False,
        "microwave_friendly": False,
        "portable": True,
        "kid_friendly": True,
        "vegetarian": True,
        "vegan": False,
        "gluten_free_option": True,
        "dairy_free_option": False,
        "nut_free_option": True,
        "low_fodmap": False,
        "keto_friendly": False,
        "paleo_friendly": False,
        "mediterranean_diet": True,
        "dash_diet": True,
        "weight_loss_friendly": True,
        "muscle_gain_friendly": True,
        "heart_healthy": True,
        "diabetes_friendly": True,
        "blood_pressure_friendly": True,
        "cholesterol_friendly": True,
        "bone_health": True,
        "brain_health": True,
        "immune_system": True,
        "gut_health": True,
        "skin_health": True,
        "hair_health": True,
        "eye_health": True,
        "dental_health": True,
        "energy_level": "High",
        "satiety_duration": "3-4 hours",
        "digestion_time": "2-3 hours",
        "blood_sugar_impact": "Moderate",
        "hormone_impact": "Positive",
        "inflammation_impact": "Low",
        "oxidative_stress": "Low",
        "antioxidant_content": "Moderate",
        "phytochemical_content": "Moderate",
        "prebiotic_content": "Low",
        "probiotic_content": "High",
        "fiber_types": ["Soluble", "Insoluble"],
        "protein_quality": "Excellent",
        "fat_types": ["Monounsaturated", "Polyunsaturated", "Saturated"],
        "carb_types": ["Complex", "Simple"],
        "mineral_bioavailability": "High",
        "vitamin_bioavailability": "High",
        "nutrient_interactions": ["Calcium-Vitamin D", "Zinc-Vitamin A"],
        "food_combinations": ["Honey", "Berries", "Banana"],
        "cultural_significance": "Greek-inspired",
        "historical_background": "Traditional Greek breakfast",
        "social_aspects": ["Breakfast option", "Snack"],
        "psychological_benefits": ["Satisfying", "Comfort food"],
        "economic_aspects": ["Moderate cost", "Value for nutrition"],
        "sustainability_aspects": ["Local ingredients", "Minimal waste"],
        "future_trends": ["Plant-based alternatives", "Clean label"],
        "research_background": ["Nutritional studies", "Dietary research"],
        "expert_recommendations": ["Dietitians", "Nutritionists"],
        "user_ratings": {
            "taste": 4.6,
            "health": 4.7,
            "convenience": 4.8,
            "value": 4.5,
            "sustainability": 4.2
        },
        "expert_ratings": {
            "nutrition": 4.8,
            "sustainability": 4.3,
            "health_impact": 4.7,
            "environmental_impact": 4.1
        },
        "market_trends": {
            "popularity": "High",
            "demand": "High",
            "price_trend": "Stable",
            "availability": "Wide"
        },
        "scientific_background": {
            "studies": ["Nutrition Journal 2022", "Food Science Review 2023"],
            "findings": ["Positive health outcomes", "Probiotic benefits"],
            "recommendations": ["Regular consumption", "Portion control"]
        }
    },
    {
        "id": 5,
        "name": "Bean and Cheese Burrito",
        "calories": 450,
        "protein": 18,
        "carbs": 55,
        "fat": 16,
        "fiber": 8,
        "sugar": 3,
        "sodium": 820,
        "potassium": 480,
        "vitamins": ["B6", "Folate", "B12", "D"],
        "minerals": ["Iron", "Calcium", "Magnesium", "Zinc"],
        "benefits": [
            "Good source of plant-based protein and fiber",
            "Contains complex carbohydrates for sustained energy",
            "Provides calcium and iron",
            "High in fiber for digestive health"
        ],
        "drawbacks": [
            "High in sodium",
            "Refined flour tortilla has low nutritional value",
            "High in calories",
            "May cause digestive discomfort for some"
        ],
        "alternatives": [
            "Whole grain tortilla (higher in fiber)",
            "Lettuce wrap (lower in calories and carbs)",
            "Bean and vegetable bowl (lower in sodium, higher in nutrients)"
        ],
        "timestamp": "2023-06-16 12:40:18",
        "meal_type": "Lunch",
        "glycemic_index": "Medium",
        "satiety_index": "High",
        "processing_level": "Moderately processed",
        "sustainability_score": "Medium",
        "cost_per_serving": "$2.00",
        "preparation_time": "10 minutes",
        "storage_life": "2 days",
        "seasonal_availability": "Year-round",
        "environmental_impact": "Low",
        "allergen_info": ["Wheat", "Dairy", "Soy", "Corn"],
        "allergy_precautions": [
            "Contains wheat in tortilla - avoid if you have celiac disease or gluten sensitivity",
            "Contains dairy (cheese) - avoid if you have a dairy allergy or lactose intolerance",
            "May contain soy in beans or sauces - check ingredients if you have a soy allergy",
            "May contain corn in tortilla or fillings - avoid if you have a corn allergy",
            "Cross-contamination with other allergens possible in restaurant settings"
        ],
        "portion_size": "1 burrito",
        "serving_weight": "250g",
        "nutrient_density_score": 7.5,
        "health_score": 7.2,
        "sustainability_rating": "Medium",
        "price_per_100g": "$0.80",
        "carbon_footprint": "0.4 kg CO2",
        "water_footprint": "700 liters",
        "packaging": "Minimal",
        "origin": "Mexican-inspired",
        "certifications": ["Organic"],
        "recipe_complexity": "Easy",
        "cooking_method": "Stovetop or microwave",
        "equipment_needed": ["Pan", "Spoon", "Plate"],
        "skill_level": "Beginner",
        "time_of_day": "Lunch",
        "meal_prep_friendly": True,
        "freezer_friendly": True,
        "microwave_friendly": True,
        "portable": True,
        "kid_friendly": True,
        "vegetarian": True,
        "vegan": False,
        "gluten_free_option": True,
        "dairy_free_option": False,
        "nut_free_option": True,
        "low_fodmap": False,
        "keto_friendly": False,
        "paleo_friendly": False,
        "mediterranean_diet": True,
        "dash_diet": False,
        "weight_loss_friendly": False,
        "muscle_gain_friendly": True,
        "heart_healthy": False,
        "diabetes_friendly": True,
        "blood_pressure_friendly": False,
        "cholesterol_friendly": True,
        "bone_health": True,
        "brain_health": True,
        "immune_system": True,
        "gut_health": True,
        "skin_health": True,
        "hair_health": True,
        "eye_health": True,
        "dental_health": True,
        "energy_level": "High",
        "satiety_duration": "3-4 hours",
        "digestion_time": "3-4 hours",
        "blood_sugar_impact": "Moderate",
        "hormone_impact": "Positive",
        "inflammation_impact": "Low",
        "oxidative_stress": "Low",
        "antioxidant_content": "Moderate",
        "phytochemical_content": "High",
        "prebiotic_content": "High",
        "probiotic_content": "None",
        "fiber_types": ["Soluble", "Insoluble"],
        "protein_quality": "Good",
        "fat_types": ["Monounsaturated", "Polyunsaturated", "Saturated"],
        "carb_types": ["Complex"],
        "mineral_bioavailability": "Medium",
        "vitamin_bioavailability": "Medium",
        "nutrient_interactions": ["Iron-Vitamin C", "Calcium-Vitamin D"],
        "food_combinations": ["Salsa", "Guacamole", "Sour cream"],
        "cultural_significance": "Mexican-inspired",
        "historical_background": "Traditional Mexican dish",
        "social_aspects": ["Lunch option", "Quick meal"],
        "psychological_benefits": ["Satisfying", "Comfort food"],
        "economic_aspects": ["Budget-friendly", "Cost-effective"],
        "sustainability_aspects": ["Plant-based protein", "Local ingredients"],
        "future_trends": ["Plant-based alternatives", "Clean label"],
        "research_background": ["Nutritional studies", "Dietary research"],
        "expert_recommendations": ["Dietitians", "Nutritionists"],
        "user_ratings": {
            "taste": 4.7,
            "health": 4.3,
            "convenience": 4.6,
            "value": 4.8,
            "sustainability": 4.4
        },
        "expert_ratings": {
            "nutrition": 4.5,
            "sustainability": 4.6,
            "health_impact": 4.4,
            "environmental_impact": 4.7
        },
        "market_trends": {
            "popularity": "High",
            "demand": "High",
            "price_trend": "Stable",
            "availability": "Wide"
        },
        "scientific_background": {
            "studies": ["Nutrition Journal 2022", "Food Science Review 2023"],
            "findings": ["Positive health outcomes", "Fiber benefits"],
            "recommendations": ["Regular consumption", "Portion control"]
        }
    },
    {
        "id": 6,
        "name": "Tuna Salad Sandwich",
        "calories": 380,
        "protein": 25,
        "carbs": 35,
        "fat": 14,
        "fiber": 3,
        "sugar": 4,
        "sodium": 680,
        "potassium": 220,
        "vitamins": ["D", "B12", "B6", "E"],
        "minerals": ["Selenium", "Iodine", "Phosphorus"],
        "benefits": [
            "Excellent source of omega-3 fatty acids",
            "High in protein for satiety",
            "Good source of vitamin D and selenium",
            "Contains heart-healthy fats"
        ],
        "drawbacks": [
            "High in sodium",
            "May contain mercury (depending on tuna type)",
            "Refined bread has low nutritional value",
            "Mayonnaise adds significant calories"
        ],
        "alternatives": [
            "Whole grain bread (higher in fiber)",
            "Chickpea salad sandwich (plant-based option)",
            "Tuna wrap with vegetables (lower in refined carbs)"
        ],
        "timestamp": "2023-06-16 18:15:42",
        "meal_type": "Dinner",
        "glycemic_index": "Medium",
        "satiety_index": "Medium",
        "processing_level": "Moderately processed",
        "sustainability_score": "Low (due to tuna)",
        "cost_per_serving": "$2.75",
        "preparation_time": "10 minutes",
        "storage_life": "1 day",
        "seasonal_availability": "Year-round",
        "environmental_impact": "High (due to tuna)",
        "allergen_info": ["Fish", "Wheat", "Eggs", "Mustard"],
        "allergy_precautions": [
            "Contains fish (tuna) - avoid if you have a fish allergy",
            "Contains wheat in bread - avoid if you have celiac disease or gluten sensitivity",
            "Contains eggs in mayonnaise - avoid if you have an egg allergy",
            "May contain mustard - avoid if you have a mustard allergy",
            "Cross-contamination with other allergens possible in restaurant settings"
        ],
        "portion_size": "1 sandwich",
        "serving_weight": "200g",
        "nutrient_density_score": 7.8,
        "health_score": 7.5,
        "sustainability_rating": "Low",
        "price_per_100g": "$1.38",
        "carbon_footprint": "1.2 kg CO2",
        "water_footprint": "1500 liters",
        "packaging": "Minimal",
        "origin": "American",
        "certifications": ["Sustainable seafood"],
        "recipe_complexity": "Easy",
        "cooking_method": "No cooking required",
        "equipment_needed": ["Knife", "Plate", "Spoon"],
        "skill_level": "Beginner",
        "time_of_day": "Evening",
        "meal_prep_friendly": True,
        "freezer_friendly": False,
        "microwave_friendly": False,
        "portable": True,
        "kid_friendly": True,
        "vegetarian": False,
        "vegan": False,
        "gluten_free_option": True,
        "dairy_free_option": True,
        "nut_free_option": True,
        "low_fodmap": True,
        "keto_friendly": False,
        "paleo_friendly": False,
        "mediterranean_diet": True,
        "dash_diet": False,
        "weight_loss_friendly": True,
        "muscle_gain_friendly": True,
        "heart_healthy": True,
        "diabetes_friendly": True,
        "blood_pressure_friendly": False,
        "cholesterol_friendly": True,
        "bone_health": True,
        "brain_health": True,
        "immune_system": True,
        "gut_health": True,
        "skin_health": True,
        "hair_health": True,
        "eye_health": True,
        "dental_health": True,
        "energy_level": "High",
        "satiety_duration": "3-4 hours",
        "digestion_time": "2-3 hours",
        "blood_sugar_impact": "Moderate",
        "hormone_impact": "Positive",
        "inflammation_impact": "Low",
        "oxidative_stress": "Low",
        "antioxidant_content": "Moderate",
        "phytochemical_content": "Low",
        "prebiotic_content": "Low",
        "probiotic_content": "None",
        "fiber_types": ["Insoluble"],
        "protein_quality": "Excellent",
        "fat_types": ["Monounsaturated", "Polyunsaturated", "Saturated"],
        "carb_types": ["Complex", "Simple"],
        "mineral_bioavailability": "High",
        "vitamin_bioavailability": "High",
        "nutrient_interactions": ["Omega-3-Vitamin E", "Selenium-Vitamin E"],
        "food_combinations": ["Lettuce", "Tomato", "Pickles"],
        "cultural_significance": "American",
        "historical_background": "Traditional American lunch",
        "social_aspects": ["Lunch option", "Quick meal"],
        "psychological_benefits": ["Satisfying", "Comfort food"],
        "economic_aspects": ["Budget-friendly", "Cost-effective"],
        "sustainability_aspects": ["Sustainable seafood", "Local ingredients"],
        "future_trends": ["Plant-based alternatives", "Clean label"],
        "research_background": ["Nutritional studies", "Dietary research"],
        "expert_recommendations": ["Dietitians", "Nutritionists"],
        "user_ratings": {
            "taste": 4.6,
            "health": 4.4,
            "convenience": 4.7,
            "value": 4.5,
            "sustainability": 3.8
        },
        "expert_ratings": {
            "nutrition": 4.6,
            "sustainability": 3.5,
            "health_impact": 4.5,
            "environmental_impact": 3.2
        },
        "market_trends": {
            "popularity": "High",
            "demand": "High",
            "price_trend": "Stable",
            "availability": "Wide"
        },
        "scientific_background": {
            "studies": ["Nutrition Journal 2022", "Food Science Review 2023"],
            "findings": ["Positive health outcomes", "Omega-3 benefits"],
            "recommendations": ["Moderate consumption", "Portion control"]
        }
    }
]

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NutriLens - Interactive Food Analysis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary-color: #007AFF;
            --secondary-color: #5856D6;
            --accent-color: #34C759;
            --warning-color: #FF9500;
            --danger-color: #FF3B30;
            --text-color: #000000;
            --text-secondary: #8E8E93;
            --background-color: #F2F2F7;
            --card-background: #FFFFFF;
            --border-radius: 10px;
            --spacing-unit: 8px;
            --touch-target: 44px;
            --font-size-base: 17px;
            --font-size-small: 15px;
            --font-size-large: 20px;
            --line-height: 1.4;
            --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, 
                rgba(0, 122, 255, 0.3), 
                rgba(88, 86, 214, 0.2), 
                rgba(255, 255, 255, 0.9)
            );
            color: var(--text-color);
            line-height: var(--line-height);
            font-size: var(--font-size-base);
            -webkit-font-smoothing: antialiased;
            min-height: 100vh;
            position: relative;
        }
        
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 50% 50%, 
                rgba(255, 255, 255, 0.1) 0%, 
                rgba(255, 255, 255, 0) 50%
            );
            pointer-events: none;
        }
        
        .container {
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: calc(var(--spacing-unit) * 2);
        }
        
        /* Header Styles */
        .header {
            background: var(--card-background);
            padding: calc(var(--spacing-unit) * 3);
            border-radius: var(--border-radius);
            margin-bottom: calc(var(--spacing-unit) * 3);
            box-shadow: var(--shadow);
        }
        
        .logo {
            display: flex;
            align-items: center;
            margin-bottom: calc(var(--spacing-unit) * 2);
        }
        
        .logo-icon {
            font-size: var(--font-size-large);
            margin-right: calc(var(--spacing-unit) * 2);
        }
        
        .logo-text {
            font-size: var(--font-size-large);
            font-weight: 600;
        }
        
        /* Interactive Controls */
        .interactive-controls {
            display: flex;
            gap: calc(var(--spacing-unit) * 2);
            margin: calc(var(--spacing-unit) * 2) 0;
            flex-wrap: wrap;
        }
        
        .control-button {
            min-height: var(--touch-target);
            min-width: var(--touch-target);
            padding: 0 calc(var(--spacing-unit) * 2);
            background-color: var(--card-background);
            color: var(--primary-color);
            border: 1px solid var(--primary-color);
            border-radius: var(--border-radius);
            font-size: var(--font-size-base);
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: calc(var(--spacing-unit));
            transition: all 0.2s ease;
        }
        
        .control-button:active {
            background-color: var(--primary-color);
            color: var(--card-background);
        }
        
        /* Food Cards */
        .food-card {
            background-color: var(--card-background);
            border-radius: var(--border-radius);
            margin-bottom: calc(var(--spacing-unit) * 3);
            box-shadow: var(--shadow);
            overflow: hidden;
        }
        
        .food-header {
            padding: calc(var(--spacing-unit) * 2);
            border-bottom: 1px solid var(--background-color);
        }
        
        .food-name {
            font-size: var(--font-size-large);
            font-weight: 600;
            margin-bottom: calc(var(--spacing-unit));
            color: var(--text-color);
        }
        
        .food-meta {
            color: var(--text-secondary);
            font-size: var(--font-size-small);
            display: flex;
            gap: calc(var(--spacing-unit) * 2);
        }
        
        /* Tabs */
        .tabs {
            display: flex;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
            -ms-overflow-style: none;
            background-color: var(--background-color);
            padding: calc(var(--spacing-unit));
            gap: calc(var(--spacing-unit));
        }
        
        .tabs::-webkit-scrollbar {
            display: none;
        }
        
        .tab {
            min-height: var(--touch-target);
            padding: 0 calc(var(--spacing-unit) * 2);
            font-size: var(--font-size-base);
            font-weight: 500;
            color: var(--text-secondary);
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: calc(var(--spacing-unit));
        }
        
        .tab.active {
            color: var(--primary-color);
            font-weight: 600;
        }
        
        /* Content Sections */
        .section-content {
            padding: calc(var(--spacing-unit) * 2);
        }
        
        .nutrition-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: calc(var(--spacing-unit) * 2);
            margin-bottom: calc(var(--spacing-unit) * 2);
        }
        
        .nutrition-item {
            background-color: var(--background-color);
            padding: calc(var(--spacing-unit) * 2);
            border-radius: var(--border-radius);
            text-align: center;
        }
        
        .nutrition-value {
            font-size: var(--font-size-large);
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: calc(var(--spacing-unit));
        }
        
        .nutrition-label {
            font-size: var(--font-size-small);
            color: var(--text-secondary);
        }
        
        /* Lists */
        .analysis-section {
            margin-bottom: calc(var(--spacing-unit) * 3);
        }
        
        .analysis-title {
            font-size: var(--font-size-base);
            font-weight: 600;
            margin-bottom: calc(var(--spacing-unit) * 2);
            color: var(--text-color);
            display: flex;
            align-items: center;
            gap: calc(var(--spacing-unit));
        }
        
        .benefits-list, .drawbacks-list, .alternatives-list {
            list-style: none;
        }
        
        .benefits-list li, .drawbacks-list li, .alternatives-list li {
            padding: calc(var(--spacing-unit) * 2);
            margin-bottom: calc(var(--spacing-unit));
            background-color: var(--background-color);
            border-radius: var(--border-radius);
            font-size: var(--font-size-base);
            line-height: var(--line-height);
        }
        
        .allergy-list li {
            padding: calc(var(--spacing-unit) * 2);
            margin-bottom: calc(var(--spacing-unit));
            background-color: var(--background-color);
            border-radius: var(--border-radius);
            border-left: 4px solid var(--danger-color);
            font-size: var(--font-size-base);
            line-height: var(--line-height);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: var(--spacing-unit);
            }
            
            .nutrition-info {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .food-header {
                flex-direction: column;
            }
            
            .food-meta {
                margin-top: calc(var(--spacing-unit));
            }
        }
        
        /* Accessibility */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation: none !important;
                transition: none !important;
            }
        }
        
        /* Focus States */
        .control-button:focus,
        .tab:focus {
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
        }
        
        /* Loading States */
        .loading {
            position: relative;
            overflow: hidden;
        }
        
        .loading::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        /* Stats Container Styles */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: calc(var(--spacing-unit) * 2);
            margin-top: calc(var(--spacing-unit) * 2);
        }
        
        .stat-card {
            background: var(--card-background);
            padding: calc(var(--spacing-unit) * 2);
            border-radius: var(--border-radius);
            text-align: center;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid var(--primary-color);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
        }
        
        .stat-card:active {
            transform: translateY(0);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .stat-value {
            font-size: var(--font-size-large);
            font-weight: 600;
            margin-bottom: calc(var(--spacing-unit));
            color: var(--primary-color);
            transition: color 0.3s ease;
        }
        
        .stat-card:hover .stat-value {
            color: white;
        }
        
        .stat-label {
            font-size: var(--font-size-small);
            color: var(--text-secondary);
            transition: color 0.3s ease;
        }
        
        .stat-card:hover .stat-label {
            color: rgba(255, 255, 255, 0.9);
        }
        
        /* Graphs Section */
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
    <script>
        // Interactive Features
        function refreshPage() {
            location.reload();
        }
        
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.getElementById(tabId).classList.add('active');
            document.getElementById(tabId + '-content').classList.add('active');
        }
        
        // Add loading state
        function showLoading(element) {
            element.classList.add('loading');
        }
        
        function hideLoading(element) {
            element.classList.remove('loading');
        }
        
        // Initialize interactive features
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.control-button').forEach(button => {
                button.addEventListener('click', function() {
                    const action = this.dataset.action;
                    handleAction(action);
                });
            });
        });
        
        function handleAction(action) {
            switch(action) {
                case 'refresh':
                    refreshPage();
                    break;
                case 'filter':
                    // Implement filtering logic
                    break;
                case 'sort':
                    // Implement sorting logic
                    break;
            }
        }
        
        // Initialize charts
        document.addEventListener('DOMContentLoaded', function() {
            // Macronutrients Chart
            const macronutrientsCtx = document.getElementById('macronutrientsChart').getContext('2d');
            new Chart(macronutrientsCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Protein', 'Carbs', 'Fat'],
                    datasets: [{
                        data: [125, 314, 83],
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

            // Calories Chart
            const caloriesCtx = document.getElementById('caloriesChart').getContext('2d');
            new Chart(caloriesCtx, {
                type: 'bar',
                data: {
                    labels: ['Breakfast', 'Lunch', 'Dinner', 'Snacks'],
                    datasets: [{
                        label: 'Calories',
                        data: [650, 850, 750, 250],
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

            // Minerals Chart
            const mineralsCtx = document.getElementById('mineralsChart').getContext('2d');
            new Chart(mineralsCtx, {
                type: 'radar',
                data: {
                    labels: ['Iron', 'Calcium', 'Magnesium', 'Zinc', 'Potassium'],
                    datasets: [{
                        label: 'Daily Intake %',
                        data: [85, 70, 65, 90, 75],
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
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <i class="fas fa-leaf logo-icon"></i>
                <div class="logo-text">NutriLens</div>
            </div>
            <p>Interactive Food Analysis Dashboard</p>
            
            <div class="interactive-controls">
                <button class="control-button" data-action="refresh">
                    <i class="fas fa-sync-alt"></i> Refresh
                </button>
                <button class="control-button" data-action="filter">
                    <i class="fas fa-filter"></i> Filter
                </button>
                <button class="control-button" data-action="sort">
                    <i class="fas fa-sort"></i> Sort
                </button>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-value">{{ food_data|length }}</div>
                    <div class="stat-label">Food Items</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ total_calories }}</div>
                    <div class="stat-label">Total Calories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ total_protein }}g</div>
                    <div class="stat-label">Total Protein</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ total_carbs }}g</div>
                    <div class="stat-label">Total Carbs</div>
                </div>
            </div>
        </div>
        
        <div class="content">
            {% for food in food_data %}
            <div class="food-card">
                <div class="food-header">
                    <div class="food-name">
                        <i class="fas fa-utensils"></i>
                        {{ food.name }}
                    </div>
                    <div class="food-meta">
                        <span><i class="fas fa-clock"></i> {{ food.meal_type }}</span>
                        <span><i class="fas fa-calendar"></i> {{ food.timestamp }}</span>
                    </div>
                </div>
                
                <div class="tabs">
                    <div class="tab active" onclick="switchTab('nutrition-{{ food.id }}')">
                        <i class="fas fa-chart-pie"></i> Nutrition
                    </div>
                    <div class="tab" onclick="switchTab('benefits-{{ food.id }}')">
                        <i class="fas fa-check-circle"></i> Benefits
                    </div>
                    <div class="tab" onclick="switchTab('drawbacks-{{ food.id }}')">
                        <i class="fas fa-exclamation-triangle"></i> Drawbacks
                    </div>
                    <div class="tab" onclick="switchTab('alternatives-{{ food.id }}')">
                        <i class="fas fa-exchange-alt"></i> Alternatives
                    </div>
                    <div class="tab" onclick="switchTab('metrics-{{ food.id }}')">
                        <i class="fas fa-chart-line"></i> Metrics
                    </div>
                    <div class="tab" onclick="switchTab('details-{{ food.id }}')">
                        <i class="fas fa-info-circle"></i> Details
                    </div>
                </div>
                
                <div class="section-content">
                    <div id="nutrition-{{ food.id }}-content" class="tab-content active">
                        <div class="nutrition-info">
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.calories }}</div>
                                <div class="nutrition-label">Calories</div>
                            </div>
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.protein }}g</div>
                                <div class="nutrition-label">Protein</div>
                            </div>
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.carbs }}g</div>
                                <div class="nutrition-label">Carbs</div>
                            </div>
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.fat }}g</div>
                                <div class="nutrition-label">Fat</div>
                            </div>
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.fiber }}g</div>
                                <div class="nutrition-label">Fiber</div>
                            </div>
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.sugar }}g</div>
                                <div class="nutrition-label">Sugar</div>
                            </div>
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.sodium }}mg</div>
                                <div class="nutrition-label">Sodium</div>
                            </div>
                            <div class="nutrition-item">
                                <div class="nutrition-value">{{ food.potassium }}mg</div>
                                <div class="nutrition-label">Potassium</div>
                            </div>
                        </div>
                    </div>
                    
                    <div id="benefits-{{ food.id }}-content" class="tab-content">
                        <div class="analysis-section">
                            <div class="analysis-title">
                                <i class="fas fa-check-circle"></i> Nutritional Benefits
                            </div>
                            <ul class="benefits-list">
                                {% for benefit in food.benefits %}
                                <li>{{ benefit }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                    
                    <div id="drawbacks-{{ food.id }}-content" class="tab-content">
                        <div class="analysis-section">
                            <div class="analysis-title">
                                <i class="fas fa-exclamation-triangle"></i> Nutritional Drawbacks
                            </div>
                            <ul class="drawbacks-list">
                                {% for drawback in food.drawbacks %}
                                <li>{{ drawback }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                    
                    <div id="alternatives-{{ food.id }}-content" class="tab-content">
                        <div class="analysis-section">
                            <div class="analysis-title">
                                <i class="fas fa-exchange-alt"></i> Healthier Alternatives
                            </div>
                            <ul class="alternatives-list">
                                {% for alternative in food.alternatives %}
                                <li>{{ alternative }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                    
                    <div id="metrics-{{ food.id }}-content" class="tab-content">
                        <div class="analysis-section">
                            <div class="analysis-title">
                                <i class="fas fa-chart-line"></i> Performance Metrics
                            </div>
                            <div class="nutrition-info">
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.glycemic_index }}</div>
                                    <div class="nutrition-label">Glycemic Index</div>
                                </div>
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.satiety_index }}</div>
                                    <div class="nutrition-label">Satiety Index</div>
                                </div>
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.processing_level }}</div>
                                    <div class="nutrition-label">Processing Level</div>
                                </div>
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.sustainability_score }}</div>
                                    <div class="nutrition-label">Sustainability</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div id="details-{{ food.id }}-content" class="tab-content">
                        <div class="analysis-section">
                            <div class="analysis-title">
                                <i class="fas fa-info-circle"></i> Additional Details
                            </div>
                            <div class="nutrition-info">
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.preparation_time }}</div>
                                    <div class="nutrition-label">Preparation Time</div>
                                </div>
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.storage_life }}</div>
                                    <div class="nutrition-label">Storage Life</div>
                                </div>
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.portion_size }}</div>
                                    <div class="nutrition-label">Portion Size</div>
                                </div>
                                <div class="nutrition-item">
                                    <div class="nutrition-value">{{ food.cost_per_serving }}</div>
                                    <div class="nutrition-label">Cost per Serving</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="analysis-section">
                            <div class="analysis-title">
                                <i class="fas fa-exclamation-triangle"></i> Allergy Precautions
                            </div>
                            <ul class="allergy-list">
                                {% for precaution in food.allergy_precautions %}
                                <li>{{ precaution }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
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
</body>
</html>
"""

# WebSocket event handlers
def on_message(ws, message):
    """
    Handle incoming WebSocket messages.
    """
    try:
        # Parse the message
        if message.startswith('42'):
            # This is a Socket.IO message
            data = json.loads(message[2:])
            event_name = data[0]
            event_data = data[1]
            
            # Process the message
            if event_name == 'message':
                # Extract timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Create response object
                response = {
                    'timestamp': timestamp,
                    'message': event_data
                }
                
                # Look for food item
                food_pattern = r'(?:holding|have) (?:a |an )?(.*?)(?: in|\.|,|$)'
                food_match = re.search(food_pattern, event_data)
                if food_match:
                    food_item = food_match.group(1).strip()
                    response['food_item'] = food_item
                    
                    # Look for calorie information
                    calorie_pattern = r'(\d+)(?:\s*-\s*\d+)?\s*calories?'
                    calorie_match = re.search(calorie_pattern, event_data.lower())
                    if calorie_match:
                        response['calories'] = calorie_match.group(1)
                
                # Add to responses
                SERVER_RESPONSES.append(response)
                print(f"Received message: {event_data}")
                
                # Put in queue for real-time updates
                log_queue.put(json.dumps(response))
    except Exception as e:
        print(f"Error processing message: {str(e)}")

def on_error(ws, error):
    """
    Handle WebSocket errors.
    """
    print(f"WebSocket error: {str(error)}")

def on_close(ws, close_status_code, close_msg):
    """
    Handle WebSocket connection close.
    """
    print("WebSocket connection closed")

def on_open(ws):
    """
    Handle WebSocket connection open.
    """
    print("WebSocket connection established")
    # Send a ping to keep the connection alive
    ws.send("2probe")

def connect_websocket():
    """
    Connect to the WebSocket server.
    """
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()

def background_processing():
    """
    Background thread to continuously connect to the WebSocket server.
    """
    global connection_status
    
    while True:
        try:
            print("Connecting to WebSocket server...")
            connection_status = True
            connect_websocket()
        except Exception as e:
            print(f"Error in WebSocket connection: {str(e)}")
            connection_status = False
            
        # Wait before reconnecting
        print("WebSocket disconnected. Reconnecting in 5 seconds...")
        time.sleep(5)

# Global connection status
connection_status = False

@app.route('/')
def index():
    """
    Flask route to display the interactive food analysis dashboard.
    """
    # Calculate totals
    total_calories = sum(food['calories'] for food in FOOD_ANALYSIS_DATA)
    total_protein = sum(food['protein'] for food in FOOD_ANALYSIS_DATA)
    total_carbs = sum(food['carbs'] for food in FOOD_ANALYSIS_DATA)
    
    return render_template_string(
        HTML_TEMPLATE,
        food_data=FOOD_ANALYSIS_DATA,
        last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        connection_status=connection_status,
        server_url=WEBSOCKET_ROOT_URL,
        total_calories=total_calories,
        total_protein=total_protein,
        total_carbs=total_carbs
    )

def main():
    """
    Main function to start the Flask application.
    """
    # Start WebSocket connection in a separate thread
    websocket_thread = threading.Thread(target=background_processing)
    websocket_thread.daemon = True
    websocket_thread.start()
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main() 