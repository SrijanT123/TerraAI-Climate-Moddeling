import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import datetime
import os

# === Custom CSS for Calibri Font and Enhanced Styling ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Calibri:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Calibri', sans-serif !important;
    }
    
    .main-header {
        font-family: 'Calibri', sans-serif !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #2E7D32 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    .company-name {
        font-family: 'Calibri', sans-serif !important;
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        color: #2E7D32 !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4) !important;
    }
    
    .company-slogan {
        font-family: 'Calibri', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1976D2 !important;
        text-align: center !important;
        margin: 1rem 0 2rem 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2) !important;
    }
    
    .logo-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 2rem 0 !important;
        padding: 1rem !important;
    }
    
    .logo-container img {
        max-width: 600px !important;
        width: 100% !important;
        height: auto !important;
    }
    
    .attribution {
        position: fixed !important;
        bottom: 5px !important;
        right: 10px !important;
        font-size: 7px !important;
        color: #999 !important;
        opacity: 0.2 !important;
        z-index: 1000 !important;
        background: rgba(255,255,255,0.6) !important;
        padding: 2px 5px !important;
        border-radius: 3px !important;
        font-family: 'Calibri', sans-serif !important;
    }
    
    .main-text-box {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%) !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        border: 2px solid #4CAF50 !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
        color: #2E2E2E !important;
    }
    
    .main-text-box h3 {
        color: #2E7D32 !important;
        margin-bottom: 1rem !important;
    }
    
    .text-wrap {
        word-wrap: break-word !important;
        white-space: normal !important;
        text-align: justify !important;
        line-height: 1.4 !important;
    }
    
    .footer-credit {
        position: fixed;
        bottom: 10px;
        right: 15px;
        font-size: 11px;
        color: #888;
        font-family: 'Calibri', sans-serif;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.8);
        padding: 3px 6px;
        border-radius: 3px;
    }
    

    
    .stButton {
        margin: 10px 0 !important;
        padding: 0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45A049 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #45A049 0%, #4CAF50 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
    }
    

    
    .section-header {
        font-family: 'Calibri', sans-serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1976D2 !important;
        border-bottom: 3px solid #2E7D32 !important;
        padding: 1rem !important;
        margin: 0 0 1.5rem 0 !important;
        background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%) !important;
        border-radius: 10px 10px 0 0 !important;
        text-align: center !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    .content-box {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%) !important;
        padding: 2rem !important;
        border-radius: 0 0 15px 15px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        margin-bottom: 2rem !important;
        border: 1px solid #E0E0E0 !important;
    }
    
    .box-with-header {
        margin: 2rem 0 !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        margin: 1rem 0 !important;
        border-left: 5px solid #2E7D32 !important;
    }
    
    .farmer-property-card {
        background: linear-gradient(135deg, #F1F8E9 0%, #E8F5E8 100%) !important;
        padding: 2.5rem !important;
        border-radius: 25px !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
        margin: 2rem 0 !important;
        border: 3px solid #4CAF50 !important;
        position: relative !important;
    }
    
    .farmer-property-card::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 5px !important;
        background: linear-gradient(90deg, #4CAF50, #2E7D32, #66BB6A) !important;
        border-radius: 25px 25px 0 0 !important;
    }
    
    .farmer-property-header {
        text-align: center !important;
        margin-bottom: 2rem !important;
        padding: 1rem !important;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    .property-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)) !important;
        gap: 1.5rem !important;
        margin: 1.5rem 0 !important;
    }
    
    .property-item {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        border-left: 4px solid #4CAF50 !important;
        transition: transform 0.3s ease !important;
    }
    
    .property-item:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }
    
    .property-item h4 {
        color: #2E7D32 !important;
        margin-bottom: 1rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    .risk-warning {
        background: linear-gradient(135deg, #FFEBEE 0%, #FCE4EC 100%) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border-left: 4px solid #F44336 !important;
        margin: 1rem 0 !important;
    }
    
    .crop-recommendation {
        background: linear-gradient(135deg, #F3E5F5 0%, #E8EAF6 100%) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        border: 1px solid #9C27B0 !important;
    }
    
    .metric-container {
        display: flex !important;
        justify-content: space-around !important;
        flex-wrap: wrap !important;
        gap: 1rem !important;
        margin: 1rem 0 !important;
    }
    
    .metric-card {
        background: white !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        min-width: 150px !important;
        text-align: center !important;
    }
    
    .stMetric {
        font-family: 'Calibri', sans-serif !important;
    }
    
    .stMetric > div {
        font-family: 'Calibri', sans-serif !important;
    }
    
    .stSelectbox > div > div {
        font-family: 'Calibri', sans-serif !important;
    }
    
    .stTextInput > div > div {
        font-family: 'Calibri', sans-serif !important;
    }
    
    .stButton > button {
        font-family: 'Calibri', sans-serif !important;
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# === API KEY from environment ===
API_KEY = os.getenv("OPENWEATHER_API_KEY", "0c8966d04aab0d36b8849c0854f5e17b")

# === Weather Layers ===
weather_layers = {
    "Wind Speed": "wind_new",
    "Rainfall": "precipitation_new",
    "Temperature": "temp_new",
    "Clouds": "clouds_new",
    "Pressure": "pressure_new",
    "Snow": "snow_new"
}

# === Additional Air Quality Layers ===
air_quality_layers = {
    "Air Quality Index": "aqi",
    "Carbon Monoxide": "co",
    "Ozone": "o3",
    "Nitrogen Dioxide": "no2",
    "Sulfur Dioxide": "so2",
    "Particulate Matter 2.5": "pm25",
    "Particulate Matter 10": "pm10",
    "Ammonia": "nh3"
}

# === Weather Layer Descriptions ===
layer_descriptions = {
    "wind_new": "Wind Speed: Shows wind velocity patterns across regions",
    "precipitation_new": "Rainfall: Displays precipitation levels and intensity",
    "temp_new": "Temperature: Shows temperature variations across areas",
    "clouds_new": "Clouds: Indicates cloud coverage and density",
    "pressure_new": "Pressure: Shows atmospheric pressure patterns",
    "snow_new": "Snow: Displays snowfall and snow cover areas"
}

# === Function: Weather by Lat/Lon ===
def get_weather_by_coords(lat, lon):
    """Fetch weather data by coordinates using OpenWeatherMap API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None
        data = res.json()
        return format_weather(data)
    except requests.RequestException:
        return None

# === Function: Get Astronomical Data ===
def get_astronomical_data(lat, lon):
    """Fetch astronomical data including sunrise, sunset from current weather"""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None
        data = res.json()
        
        if 'sys' in data:
            sys_data = data['sys']
            # Calculate approximate moonrise/moonset based on sunrise/sunset
            sunrise_time = datetime.datetime.fromtimestamp(sys_data['sunrise'])
            sunset_time = datetime.datetime.fromtimestamp(sys_data['sunset'])
            
            # Approximate moonrise/moonset (offset by ~50 minutes per day)
            moonrise_time = sunrise_time + datetime.timedelta(minutes=50)
            moonset_time = sunset_time + datetime.timedelta(minutes=50)
            
            # Convert all times to IST
            sunrise_ist = sunrise_time + datetime.timedelta(hours=5, minutes=30)
            sunset_ist = sunset_time + datetime.timedelta(hours=5, minutes=30)
            moonrise_ist = moonrise_time + datetime.timedelta(hours=5, minutes=30)
            moonset_ist = moonset_time + datetime.timedelta(hours=5, minutes=30)
            
            return {
                'sunrise': sunrise_ist.strftime('%H:%M IST'),
                'sunset': sunset_ist.strftime('%H:%M IST'),
                'moonrise': moonrise_ist.strftime('%H:%M IST'),
                'moonset': moonset_ist.strftime('%H:%M IST')
            }
        return None
    except requests.RequestException:
        return None

# === Function: Weather by City ===
def get_weather_by_city(city):
    """Fetch weather data by city name using OpenWeatherMap API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None
        data = res.json()
        return format_weather(data)
    except requests.RequestException:
        return None

# === Format Weather Data ===
def format_weather(data):
    """Format weather data into a structured dictionary"""
    return {
        "Location": data.get("name", "Unknown"),
        "Country": data["sys"].get("country", "N/A"),
        "Current Temperature (°C)": data["main"]["temp"],
        "Feels Like (°C)": data["main"]["feels_like"],
        "Expected Min Temp (°C)": data["main"]["temp_min"],
        "Expected Max Temp (°C)": data["main"]["temp_max"],
        "Humidity (%)": data["main"]["humidity"],
        "Pressure (hPa)": data["main"]["pressure"],
        "Wind Speed (m/s)": data["wind"]["speed"],
        "Current Weather": data["weather"][0]["description"],
        "Expected Weather": data["weather"][0]["main"],
        "Current Time": (datetime.datetime.utcfromtimestamp(data["dt"]) + datetime.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S IST'),
        "Sunrise": convert_utc_to_ist(datetime.datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M UTC')),
        "Sunset": convert_utc_to_ist(datetime.datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%H:%M UTC')),
        "Lat": data["coord"]["lat"],
        "Lon": data["coord"]["lon"]
    }

# === Enhanced Risk Prediction with Detailed Information ===
def get_detailed_risk_info():
    """Return detailed risk information with early signs, precautions, and safety measures"""
    return {
        "🚨 EXTREME HEAT ALERT": {
            "early_signs": ["Temperature above 45°C", "Very low humidity", "Clear skies", "High UV index"],
            "precautions": ["Use shade nets for crops", "Increase irrigation frequency", "Apply mulching", "Avoid midday field work"],
            "safety": ["Stay hydrated", "Wear light-colored clothes", "Take frequent breaks in shade", "Monitor for heat exhaustion symptoms"]
        },
        "🔥 High Heat Risk": {
            "early_signs": ["Temperature 40-45°C", "Humidity below 30%", "Dry winds", "Soil moisture declining"],
            "precautions": ["Install drip irrigation", "Use reflective mulch", "Provide windbreaks", "Apply foliar spray"],
            "safety": ["Work early morning/evening", "Carry water bottles", "Wear sun protection", "Monitor livestock closely"]
        },
        "🌪️ SEVERE STORM WARNING": {
            "early_signs": ["Wind speed >20 m/s", "Pressure <980 hPa", "Dark storm clouds", "Lightning activity"],
            "precautions": ["Secure farm equipment", "Harvest ready crops", "Check drainage systems", "Reinforce structures"],
            "safety": ["Stay indoors", "Avoid trees and power lines", "Keep emergency kit ready", "Monitor weather updates"]
        },
        "⛈️ Storm Risk": {
            "early_signs": ["Wind 15-20 m/s", "Pressure <1000 hPa", "Cumulus clouds", "Temperature drop"],
            "precautions": ["Cover sensitive crops", "Ensure proper drainage", "Secure loose items", "Check irrigation systems"],
            "safety": ["Avoid open areas", "Stay away from metal objects", "Have flashlight ready", "Charge devices"]
        },
        "🌊 FLASH FLOOD ALERT": {
            "early_signs": ["Heavy rainfall", "Humidity >95%", "Low pressure", "Water accumulation"],
            "precautions": ["Move to higher ground", "Protect stored grain", "Check pump systems", "Clear drainage channels"],
            "safety": ["Avoid flooded areas", "Don't drive through water", "Keep emergency supplies", "Monitor water levels"]
        },
        "❄️ FREEZING ALERT": {
            "early_signs": ["Temperature <0°C", "Clear night skies", "Calm winds", "Frost formation"],
            "precautions": ["Cover crops with cloth", "Use frost protection sprays", "Light smudge pots", "Harvest vulnerable crops"],
            "safety": ["Wear warm clothing", "Check heating systems", "Protect water pipes", "Monitor elderly and children"]
        },
        "🌵 Severe Drought": {
            "early_signs": ["Humidity <15%", "Temperature >38°C", "No recent rainfall", "Soil cracking"],
            "precautions": ["Implement water conservation", "Use drought-resistant varieties", "Apply heavy mulching", "Reduce tillage"],
            "safety": ["Conserve water usage", "Monitor water supplies", "Check well water levels", "Plan alternative sources"]
        },
        "🌾 Crop Stress": {
            "early_signs": ["Wilting leaves", "Slow growth", "Color changes", "Reduced yield"],
            "precautions": ["Increase irrigation", "Apply nutrients", "Use growth regulators", "Provide shade"],
            "safety": ["Monitor crop health daily", "Test soil moisture", "Check for pests/diseases", "Consult agricultural expert"]
        }
    }

def predict_risks(weather):
    """Enhanced AI-powered climate risk prediction with notification system"""
    temp = weather["Current Temperature (°C)"]
    wind = weather["Wind Speed (m/s)"]
    humidity = weather["Humidity (%)"]
    pressure = weather["Pressure (hPa)"]
    lat = weather["Lat"]
    desc = weather["Current Weather"].lower()
    risks = []

    # Enhanced risk prediction with severity levels
    if temp > 45:
        risks.append("🚨 EXTREME HEAT ALERT")
    elif temp > 40 and humidity < 30:
        risks.append("🔥 High Heat Risk")
    
    if wind > 20 and pressure < 980:
        risks.append("🌪️ SEVERE STORM WARNING")
    elif wind > 15 and pressure < 1000:
        risks.append("⛈️ Storm Risk")
    
    if "rain" in desc and humidity > 95 and pressure < 1005:
        risks.append("🌊 FLASH FLOOD ALERT")
    
    if temp < 0:
        risks.append("❄️ FREEZING ALERT")
    
    if humidity < 15 and temp > 38 and "clear" in desc:
        risks.append("🌵 Severe Drought")
    elif humidity < 25 and temp > 32:
        risks.append("🌾 Crop Stress")

    return risks if risks else ["✅ No Major Risk Detected"]

# === Function: Convert UTC to IST ===
def convert_utc_to_ist(utc_time_str):
    """Convert UTC time to IST"""
    try:
        # Parse UTC time
        utc_time = datetime.datetime.strptime(utc_time_str, '%H:%M UTC')
        # Add 5 hours 30 minutes for IST
        ist_time = utc_time + datetime.timedelta(hours=5, minutes=30)
        return ist_time.strftime('%H:%M IST')
    except:
        return utc_time_str

# === Detailed Risk Information Database ===
def get_detailed_risk_info():
    """Return detailed information for each risk type with early signs, precautions, and safety measures"""
    return {
        "🌪️ High Wind Alert": {
            'early_signs': [
                'Sudden drop in temperature',
                'Dark clouds approaching rapidly',
                'Trees bending unusually',
                'Animals seeking shelter',
                'Dust or debris in air'
            ],
            'precautions': [
                'Secure loose farm equipment',
                'Cover sensitive crops with nets',
                'Check irrigation systems',
                'Move livestock to shelter',
                'Harvest ready crops immediately'
            ],
            'safety': [
                'Stay indoors during high winds',
                'Avoid working near tall structures',
                'Keep emergency kit ready',
                'Monitor weather updates constantly',
                'Have evacuation plan ready'
            ]
        },
        "⛈️ Storm Warning": {
            'early_signs': [
                'Thunder and lightning',
                'Heavy cloud formation',
                'Sudden temperature drop',
                'Pressure changes',
                'Animals acting restless'
            ],
            'precautions': [
                'Drain excess water from fields',
                'Protect seedlings with covers',
                'Secure farm structures',
                'Move equipment to safe areas',
                'Check drainage systems'
            ],
            'safety': [
                'Avoid open fields during storms',
                'Stay away from metal objects',
                'Keep first aid kit accessible',
                'Have emergency contacts ready',
                'Monitor radio for updates'
            ]
        },
        "🌡️ Heat Wave Alert": {
            'early_signs': [
                'Temperature rising above 40°C',
                'Clear skies for several days',
                'Low humidity levels',
                'Plants wilting early in day',
                'Soil cracking visible'
            ],
            'precautions': [
                'Increase irrigation frequency',
                'Use mulching to retain moisture',
                'Provide shade for livestock',
                'Apply cooling sprays on crops',
                'Adjust work timings'
            ],
            'safety': [
                'Work early morning/evening only',
                'Drink water every 15 minutes',
                'Wear light colored clothing',
                'Take frequent rest breaks',
                'Watch for heat exhaustion signs'
            ]
        },
        "❄️ Frost Alert": {
            'early_signs': [
                'Clear skies at night',
                'Temperature below 5°C',
                'Low wind conditions',
                'Dew formation heavy',
                'Humidity dropping rapidly'
            ],
            'precautions': [
                'Cover sensitive plants',
                'Light smudge pots if available',
                'Water plants before evening',
                'Use frost cloth on crops',
                'Move potted plants indoors'
            ],
            'safety': [
                'Check heating systems',
                'Protect water pipes from freezing',
                'Ensure livestock have warm shelter',
                'Keep extra blankets ready',
                'Monitor elderly and children'
            ]
        },
        "💨 Extreme Weather": {
            'early_signs': [
                'Rapid weather changes',
                'Unusual cloud formations',
                'Sudden pressure drops',
                'Birds flying low',
                'Static electricity in air'
            ],
            'precautions': [
                'Secure all moveable items',
                'Emergency harvest if possible',
                'Check insurance policies',
                'Prepare emergency supplies',
                'Notify neighbors and family'
            ],
            'safety': [
                'Have emergency shelter ready',
                'Keep battery radio available',
                'Store 72 hours of water/food',
                'Know evacuation routes',
                'Stay in constant communication'
            ]
        }
    }

# === Air Quality Information Database ===
def get_air_quality_info():
    """Return detailed information about air quality components"""
    return {
        'Carbon Monoxide (CO)': {
            'effects': 'Reduces oxygen delivery to organs, causes headaches, dizziness, and fatigue',
            'symptoms': 'Headache, dizziness, weakness, nausea, confusion, chest pain',
            'protection': 'Avoid traffic areas, use air purifiers, ensure proper ventilation, don\'t use gas appliances indoors'
        },
        'Ozone (O3)': {
            'effects': 'Irritates airways, worsens asthma, reduces lung function, causes breathing problems',
            'symptoms': 'Coughing, throat irritation, chest pain, shortness of breath, lung inflammation',
            'protection': 'Stay indoors during high ozone days, exercise early morning, use air conditioning, wear N95 masks'
        },
        'Nitrogen Dioxide (NO2)': {
            'effects': 'Inflames airways, increases respiratory infections, aggravates asthma and COPD',
            'symptoms': 'Coughing, wheezing, difficulty breathing, increased asthma attacks, lung irritation',
            'protection': 'Avoid busy roads, keep windows closed during traffic hours, use HEPA filters, limit outdoor activities'
        },
        'Sulfur Dioxide (SO2)': {
            'effects': 'Irritates respiratory system, triggers asthma, causes acid rain damage to crops',
            'symptoms': 'Throat irritation, coughing, difficulty breathing, chest tightness, runny nose',
            'protection': 'Stay away from industrial areas, use air purifiers, keep rescue inhalers handy if asthmatic'
        },
        'PM2.5': {
            'effects': 'Penetrates deep into lungs, causes heart disease, lung cancer, premature death',
            'symptoms': 'Persistent cough, chest discomfort, shortness of breath, fatigue, heart palpitations',
            'protection': 'Wear N95/N99 masks, use air purifiers, seal home gaps, avoid outdoor exercise during high PM days'
        },
        'PM10': {
            'effects': 'Irritates eyes and throat, aggravates respiratory conditions, reduces lung function',
            'symptoms': 'Eye irritation, runny nose, coughing, throat irritation, respiratory discomfort',
            'protection': 'Use masks outdoors, keep windows closed, use air filtration systems, limit outdoor activities'
        },
        'Ammonia (NH3)': {
            'effects': 'Irritates mucous membranes, affects respiratory system, contributes to smog formation',
            'symptoms': 'Eye watering, throat irritation, coughing, skin irritation, difficulty breathing',
            'protection': 'Avoid agricultural areas during fertilizer application, ensure proper ventilation, use protective equipment'
        }
    }

# === Function: Get Air Quality Data ===
def get_air_quality_data(lat, lon):
    """Fetch air quality data including CO2, ozone, and other pollutants"""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None
        data = res.json()
        
        if data.get('list') and len(data['list']) > 0:
            components = data['list'][0]['components']
            aqi = data['list'][0]['main']['aqi']
            
            aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
            
            return {
                'Air Quality Index': f"{aqi} ({aqi_labels.get(aqi, 'Unknown')})",
                'Carbon Monoxide (CO)': f"{components.get('co', 0):.2f} μg/m³",
                'Ozone (O3)': f"{components.get('o3', 0):.2f} μg/m³",
                'Nitrogen Dioxide (NO2)': f"{components.get('no2', 0):.2f} μg/m³",
                'Sulfur Dioxide (SO2)': f"{components.get('so2', 0):.2f} μg/m³",
                'PM2.5': f"{components.get('pm2_5', 0):.2f} μg/m³",
                'PM10': f"{components.get('pm10', 0):.2f} μg/m³",
                'Ammonia (NH3)': f"{components.get('nh3', 0):.2f} μg/m³"
            }
    except requests.RequestException:
        return None

# === Function: Get 5-Day Climate Prediction ===
def get_climate_prediction(lat, lon):
    """Get 5-day climate prediction for farming using free tier API"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None
        data = res.json()
        
        # Process forecast data - group by date
        daily_predictions = {}
        for item in data.get('list', []):
            date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_predictions:
                daily_predictions[date] = {
                    'date': date,
                    'temps': [],
                    'humidity': [],
                    'pressure': [],
                    'wind_speed': [],
                    'weather': item['weather'][0]['description'],
                    'rain': item.get('rain', {}).get('3h', 0)
                }
            
            daily_predictions[date]['temps'].append(item['main']['temp'])
            daily_predictions[date]['humidity'].append(item['main']['humidity'])
            daily_predictions[date]['pressure'].append(item['main']['pressure'])
            daily_predictions[date]['wind_speed'].append(item['wind']['speed'])
            daily_predictions[date]['rain'] += item.get('rain', {}).get('3h', 0)
        
        # Calculate daily averages
        predictions = []
        for date_key in sorted(daily_predictions.keys())[:5]:  # Get first 5 days
            day_data = daily_predictions[date_key]
            predictions.append({
                'date': day_data['date'],
                'temp_max': max(day_data['temps']),
                'temp_min': min(day_data['temps']),
                'humidity': sum(day_data['humidity']) / len(day_data['humidity']),
                'pressure': sum(day_data['pressure']) / len(day_data['pressure']),
                'wind_speed': sum(day_data['wind_speed']) / len(day_data['wind_speed']),
                'weather': day_data['weather'],
                'rain': day_data['rain']
            })
        
        return predictions
    except requests.RequestException:
        return None

# === Function: Crop Recommendations ===
# === Detailed Crop Information Database ===
def get_detailed_crop_info():
    """Return detailed crop information for July-October seasons and year-round farming"""
    current_month = datetime.datetime.now().month
    
    # July crops (prioritized for current season) - 10 crops
    july_crops = {
        "🌾 Rice (Kharif)": {
            'farming_steps': [
                '1. Land Preparation: Plow field 2-3 times, level properly',
                '2. Seed Selection: Choose high-yielding varieties like IR-64, Pusa Basmati',
                '3. Sowing: Direct seeding or transplanting seedlings 20-25cm apart',
                '4. Water Management: Maintain 2-3cm standing water initially',
                '5. Fertilization: Apply NPK (120:60:40 kg/ha) in 3 splits'
            ],
            'care_tips': [
                'Weed control in 20-25 days after transplanting',
                'Monitor for pests like stem borer, brown plant hopper',
                'Apply fungicides for blast and sheath blight if needed',
                'Maintain consistent water level throughout growth'
            ],
            'best_season': 'July-August sowing (Monsoon/Kharif)',
            'harvest_time': 'October-November (110-120 days)',
            'water_requirement': 'High (1200-1500mm)',
            'temperature_range': '20-35°C',
            'soil_type': 'Clay loam, good water retention'
        },
        "🌽 Maize (Monsoon)": {
            'farming_steps': [
                '1. Field Preparation: Deep plowing, make ridges and furrows',
                '2. Seed Treatment: Treat with fungicide before sowing',
                '3. Sowing: Plant 2-3 seeds per hill, 60x20cm spacing',
                '4. Irrigation: Light irrigation if rainfall insufficient',
                '5. Fertilization: Apply 120:60:40 NPK kg/ha'
            ],
            'care_tips': [
                'Earthing up at knee-high stage for better root development',
                'Control stem borer and fall armyworm regularly',
                'Remove suckers and weeds regularly',
                'Apply top dressing of nitrogen at tasseling stage'
            ],
            'best_season': 'July sowing for monsoon crop',
            'harvest_time': 'October-November (90-110 days)',
            'water_requirement': 'Medium (500-700mm)',
            'temperature_range': '21-30°C',
            'soil_type': 'Well-drained loamy soil'
        },
        "🥒 Ridge Gourd": {
            'farming_steps': [
                '1. Prepare raised beds with good drainage',
                '2. Soak seeds for 12 hours before sowing',
                '3. Sow 2-3 seeds per pit at 2m x 2m spacing',
                '4. Provide trellis support for climbing',
                '5. Apply organic manure and balanced fertilizers'
            ],
            'care_tips': [
                'Regular watering but avoid waterlogging',
                'Pinch growing tips to encourage branching',
                'Control fruit fly and red pumpkin beetle',
                'Harvest tender fruits regularly for continuous production'
            ],
            'best_season': 'July-August (monsoon season)',
            'harvest_time': 'September-December (60-90 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '25-35°C',
            'soil_type': 'Rich organic matter, well-drained'
        },
        "🍆 Brinjal (Eggplant)": {
            'farming_steps': [
                '1. Raise seedlings in nursery for 4-6 weeks',
                '2. Prepare main field with organic matter',
                '3. Transplant seedlings at 75x60cm spacing',
                '4. Apply mulching around plants',
                '5. Regular fertilization and pest monitoring'
            ],
            'care_tips': [
                'Stake tall varieties to prevent lodging',
                'Control shoot and fruit borer effectively',
                'Regular harvesting increases yield',
                'Provide adequate drainage during monsoon'
            ],
            'best_season': 'July-August transplanting',
            'harvest_time': 'October onwards (120-150 days)',
            'water_requirement': 'Medium',
            'temperature_range': '22-32°C',
            'soil_type': 'Rich, well-drained loamy soil'
        },
        "🌿 Green Beans": {
            'farming_steps': [
                '1. Prepare well-drained raised beds',
                '2. Sow seeds 3-4 cm deep in rows',
                '3. Maintain 30x10 cm spacing between plants',
                '4. Install support stakes for pole varieties',
                '5. Apply compost and balanced fertilizers'
            ],
            'care_tips': [
                'Water regularly but avoid waterlogging',
                'Harvest pods when tender for best quality',
                'Control aphids and pod borer with neem oil',
                'Apply rhizobium inoculation for nitrogen fixation'
            ],
            'best_season': 'July-August (monsoon planting)',
            'harvest_time': 'September-November (60-75 days)',
            'water_requirement': 'Medium',
            'temperature_range': '20-30°C',
            'soil_type': 'Well-drained sandy loam'
        },
        "🥕 Bottle Gourd": {
            'farming_steps': [
                '1. Prepare 2x2 meter pits with organic matter',
                '2. Sow 3-4 seeds per pit at 3m spacing',
                '3. Provide strong trellis support system',
                '4. Apply balanced NPK fertilizers regularly',
                '5. Ensure proper drainage during monsoon'
            ],
            'care_tips': [
                'Train vines on trellis for better fruit shape',
                'Remove excess male flowers to boost fruiting',
                'Control fruit fly with pheromone traps',
                'Harvest young fruits for tender vegetables'
            ],
            'best_season': 'July-August (monsoon season)',
            'harvest_time': 'September-December (90-120 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '25-35°C',
            'soil_type': 'Rich loamy soil with good drainage'
        },
        "🌶️ Green Chili": {
            'farming_steps': [
                '1. Raise seedlings in protected nursery',
                '2. Transplant 6-8 week old seedlings',
                '3. Plant at 60x45 cm spacing in rows',
                '4. Apply mulching to retain moisture',
                '5. Regular feeding with organic fertilizers'
            ],
            'care_tips': [
                'Provide support to prevent lodging',
                'Regular picking encourages more flowering',
                'Control thrips and aphids with biological agents',
                'Apply calcium spray for better fruit quality'
            ],
            'best_season': 'July transplanting for monsoon crop',
            'harvest_time': 'September-January (75-120 days)',
            'water_requirement': 'Medium',
            'temperature_range': '20-32°C',
            'soil_type': 'Well-drained fertile soil'
        },
        "🍅 Cherry Tomato": {
            'farming_steps': [
                '1. Start with disease-free seedlings',
                '2. Prepare raised beds with compost',
                '3. Transplant at 45x30 cm spacing',
                '4. Install bamboo stakes for support',
                '5. Apply drip irrigation if possible'
            ],
            'care_tips': [
                'Remove suckers for better fruit development',
                'Apply calcium spray to prevent blossom end rot',
                'Control whitefly and leaf curl virus',
                'Harvest when fruits are fully colored'
            ],
            'best_season': 'July transplanting for monsoon crop',
            'harvest_time': 'September-December (80-100 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '20-30°C',
            'soil_type': 'Rich organic matter, well-drained'
        },
        "🥬 Fenugreek (Methi)": {
            'farming_steps': [
                '1. Prepare fine tilth with organic compost',
                '2. Broadcast seeds or sow in lines',
                '3. Maintain 20 cm row spacing',
                '4. Apply light irrigation after sowing',
                '5. Thin seedlings to proper spacing'
            ],
            'care_tips': [
                'First cutting after 25-30 days',
                'Apply nitrogen fertilizer after each cutting',
                'Control aphids with neem oil spray',
                'Regular harvesting promotes regrowth'
            ],
            'best_season': 'July-August for monsoon crop',
            'harvest_time': 'September-November (40-60 days)',
            'water_requirement': 'Low-Medium',
            'temperature_range': '15-30°C',
            'soil_type': 'Well-drained loamy soil'
        },
        "🌱 Red Amaranth": {
            'farming_steps': [
                '1. Prepare fine seedbed with compost',
                '2. Broadcast seeds thinly in beds',
                '3. Cover lightly with fine soil',
                '4. Water with fine rose can',
                '5. Thin seedlings when 5 cm tall'
            ],
            'care_tips': [
                'Harvest leaves when plants are 15-20 cm tall',
                'Apply liquid fertilizer every 15 days',
                'Control leaf spot with copper fungicide',
                'Successive sowing for continuous harvest'
            ],
            'best_season': 'July-August for monsoon leafy greens',
            'harvest_time': 'August-October (30-45 days)',
            'water_requirement': 'Medium',
            'temperature_range': '20-35°C',
            'soil_type': 'Rich in organic matter'
        }
    }
    
    # August crops - 10 crops
    august_crops = {
        "🌿 Spinach": {
            'farming_steps': [
                '1. Prepare fine seedbed with well-decomposed manure',
                '2. Sow seeds 1 cm deep in rows 20 cm apart',
                '3. Thin seedlings to 5 cm spacing after germination',
                '4. Apply light irrigation daily in morning',
                '5. Start harvesting leaves after 40-45 days'
            ],
            'care_tips': [
                'Harvest outer leaves first to promote continuous growth',
                'Apply liquid fertilizer every 15 days',
                'Protect from excessive heat with shade nets',
                'Control aphids with neem oil spray'
            ],
            'best_season': 'August-September sowing for winter harvest',
            'harvest_time': 'October-December (45-60 days)',
            'water_requirement': 'Medium',
            'temperature_range': '15-25°C optimal',
            'soil_type': 'Rich loamy soil with good drainage'
        },
        "🌶️ Chili": {
            'farming_steps': [
                '1. Raise seedlings in nursery for 6-8 weeks',
                '2. Transplant to main field at 45x30 cm spacing',
                '3. Apply drip irrigation or furrow irrigation',
                '4. Support plants with stakes if needed',
                '5. Regular picking encourages more fruiting'
            ],
            'care_tips': [
                'Pinch off first few flowers for better plant establishment',
                'Apply calcium and boron for better fruit set',
                'Control thrips and aphids with integrated pest management',
                'Harvest green or red chilies based on market demand'
            ],
            'best_season': 'August transplanting for September-February harvest',
            'harvest_time': 'October-February (120-150 days)',
            'water_requirement': 'Medium',
            'temperature_range': '20-30°C',
            'soil_type': 'Well-drained sandy loam soil'
        },
        "🥬 Lettuce": {
            'farming_steps': [
                '1. Prepare well-drained beds with compost',
                '2. Sow seeds in lines 25 cm apart',
                '3. Thin seedlings to 15 cm spacing',
                '4. Apply frequent light irrigations',
                '5. Harvest when heads are well-formed'
            ],
            'care_tips': [
                'Protect from excessive heat with shade cloth',
                'Maintain consistent soil moisture',
                'Control aphids and leaf miners',
                'Harvest early morning for best quality'
            ],
            'best_season': 'August sowing for winter harvest',
            'harvest_time': 'October-December (60-80 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '15-20°C optimal',
            'soil_type': 'Rich, well-drained soil'
        },
        "🥦 Broccoli": {
            'farming_steps': [
                '1. Raise seedlings in nursery beds',
                '2. Transplant 4-5 week old seedlings',
                '3. Plant at 45x30 cm spacing',
                '4. Apply heavy mulching around plants',
                '5. Harvest main head before flowers open'
            ],
            'care_tips': [
                'Apply boron spray for better head formation',
                'Control diamond back moth with BT spray',
                'Side shoots can be harvested after main head',
                'Cool weather improves head quality'
            ],
            'best_season': 'August transplanting for winter harvest',
            'harvest_time': 'November-January (80-100 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '15-25°C',
            'soil_type': 'Fertile, well-drained soil'
        },
        "🌽 Sweet Corn": {
            'farming_steps': [
                '1. Prepare ridges and furrows for drainage',
                '2. Plant seeds 3-4 cm deep in rows',
                '3. Maintain 60x25 cm plant spacing',
                '4. Earth up when plants are knee-high',
                '5. Hand pollination may improve ear filling'
            ],
            'care_tips': [
                'Apply side dressing of nitrogen at tasseling',
                'Control corn borer with biological agents',
                'Harvest when kernels are milky and tender',
                'Process immediately for best sweetness'
            ],
            'best_season': 'August planting for winter harvest',
            'harvest_time': 'November-December (75-90 days)',
            'water_requirement': 'Medium',
            'temperature_range': '20-30°C',
            'soil_type': 'Well-drained fertile soil'
        },
        "🥒 Cucumber": {
            'farming_steps': [
                '1. Prepare raised beds with organic matter',
                '2. Sow 2-3 seeds per hill at 1.5m spacing',
                '3. Provide trellis for vertical growing',
                '4. Apply balanced fertilizers regularly',
                '5. Harvest young cucumbers frequently'
            ],
            'care_tips': [
                'Train vines vertically to save space',
                'Remove male flowers to reduce bitterness',
                'Control powdery mildew with sulfur spray',
                'Maintain consistent soil moisture'
            ],
            'best_season': 'August planting for winter crop',
            'harvest_time': 'October-December (50-65 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '20-30°C',
            'soil_type': 'Well-drained, rich organic soil'
        },
        "🌱 Coriander": {
            'farming_steps': [
                '1. Prepare fine tilth with organic compost',
                '2. Broadcast seeds or sow in lines',
                '3. Cover lightly with fine soil',
                '4. Apply light irrigation after sowing',
                '5. Thin seedlings for proper air circulation'
            ],
            'care_tips': [
                'First cutting after 30-35 days',
                'Apply liquid fertilizer after each cutting',
                'Control aphids with neem oil',
                'Successive sowings for continuous harvest'
            ],
            'best_season': 'August-September for winter leaves',
            'harvest_time': 'October-January (30-120 days)',
            'water_requirement': 'Low-Medium',
            'temperature_range': '15-25°C',
            'soil_type': 'Well-drained loamy soil'
        },
        "🍓 Strawberry": {
            'farming_steps': [
                '1. Prepare raised beds with good drainage',
                '2. Plant certified runners or seedlings',
                '3. Maintain 30x30 cm plant spacing',
                '4. Apply black plastic mulching',
                '5. Install drip irrigation system'
            ],
            'care_tips': [
                'Remove runners for better fruit production',
                'Protect fruits from soil contact with straw',
                'Control gray mold with proper ventilation',
                'Harvest fruits when fully red'
            ],
            'best_season': 'August planting for winter-spring harvest',
            'harvest_time': 'December-April (120-150 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '15-25°C',
            'soil_type': 'Well-drained sandy loam'
        },
        "🥕 Radish": {
            'farming_steps': [
                '1. Prepare fine seedbed without clods',
                '2. Sow seeds directly in rows 20 cm apart',
                '3. Thin seedlings to 5 cm spacing',
                '4. Apply light irrigation frequently',
                '5. Harvest when roots are tender'
            ],
            'care_tips': [
                'Harvest within 30-40 days for tenderness',
                'Avoid fresh manure to prevent forking',
                'Control flea beetles with neem spray',
                'Successive sowings every 15 days'
            ],
            'best_season': 'August-September for quick winter crop',
            'harvest_time': 'September-November (25-40 days)',
            'water_requirement': 'Medium',
            'temperature_range': '15-25°C',
            'soil_type': 'Light, well-drained soil'
        },
        "🌰 Groundnut": {
            'farming_steps': [
                '1. Prepare ridges and furrows for drainage',
                '2. Sow treated seeds in ridges',
                '3. Maintain 30x10 cm plant spacing',
                '4. Earth up at flowering stage',
                '5. Harvest when pods are mature'
            ],
            'care_tips': [
                'Apply gypsum during pod development',
                'Control leaf spot with fungicide sprays',
                'Avoid waterlogging during pod filling',
                'Harvest when shells are well-formed'
            ],
            'best_season': 'August planting for kharif harvest',
            'harvest_time': 'November-December (90-110 days)',
            'water_requirement': 'Medium',
            'temperature_range': '20-30°C',
            'soil_type': 'Well-drained sandy loam'
        }
    }
    
    # September crops
    september_crops = {
        "🥕 Carrot": {
            'farming_steps': [
                '1. Prepare raised beds 15 cm high for good drainage',
                '2. Sow seeds directly 2 cm deep in rows',
                '3. Maintain 20 cm row spacing and thin to 5 cm plant spacing',
                '4. Water gently to avoid washing away seeds',
                '5. Harvest when roots are bright orange and 15-20 cm long'
            ],
            'care_tips': [
                'Avoid fresh manure as it causes forked roots',
                'Keep soil consistently moist but not waterlogged',
                'Hill up soil around crowns to prevent green shoulders',
                'Control carrot rust fly with row covers'
            ],
            'best_season': 'September-October sowing for winter harvest',
            'harvest_time': 'December-February (90-120 days)',
            'water_requirement': 'Medium',
            'temperature_range': '15-25°C',
            'soil_type': 'Deep, loose sandy loam soil'
        },
        "🧅 Onion": {
            'farming_steps': [
                '1. Prepare nursery beds and sow seeds thickly',
                '2. Transplant 6-8 week old seedlings to main field',
                '3. Plant at 15x10 cm spacing in well-prepared beds',
                '4. Apply light irrigation frequently until establishment',
                '5. Reduce watering 2 weeks before harvest'
            ],
            'care_tips': [
                'Apply phosphorus-rich fertilizer for good bulb development',
                'Control purple blotch disease with fungicide sprays',
                'Harvest when 50% of tops fall over naturally',
                'Cure bulbs in shade for 7-10 days before storage'
            ],
            'best_season': 'September-October transplanting',
            'harvest_time': 'February-April (150-180 days)',
            'water_requirement': 'Medium',
            'temperature_range': '15-25°C optimal',
            'soil_type': 'Well-drained fertile soil with pH 6.0-7.0'
        }
    }
    
    # October crops
    october_crops = {
        "🥔 Potato": {
            'farming_steps': [
                '1. Cut seed tubers with 2-3 eyes, dry for 2 days',
                '2. Plant in furrows 15-20 cm deep, 60 cm apart',
                '3. Cover with soil and apply pre-emergence herbicide',
                '4. Earth up when plants are 15 cm tall',
                '5. Harvest when tops dry and tubers are mature'
            ],
            'care_tips': [
                'Use certified disease-free seed potatoes',
                'Apply balanced fertilizer at planting',
                'Control late blight with preventive fungicide sprays',
                'Avoid exposure of tubers to sunlight during harvest'
            ],
            'best_season': 'October-November planting for winter crop',
            'harvest_time': 'January-March (90-120 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '15-25°C',
            'soil_type': 'Well-drained sandy loam soil'
        },
        "🌾 Wheat": {
            'farming_steps': [
                '1. Prepare fine seedbed with proper tilth',
                '2. Sow seeds at 100-125 kg/hectare rate',
                '3. Use seed drill for uniform distribution',
                '4. Apply first irrigation 20-25 days after sowing',
                '5. Harvest when grains are hard and golden'
            ],
            'care_tips': [
                'Apply half nitrogen at sowing, rest at first irrigation',
                'Control weeds with post-emergence herbicides',
                'Monitor for rust diseases and aphid attacks',
                'Time harvest for optimal grain moisture content'
            ],
            'best_season': 'October-November sowing for Rabi season',
            'harvest_time': 'March-April (120-150 days)',
            'water_requirement': 'Medium',
            'temperature_range': '15-25°C',
            'soil_type': 'Well-drained loamy soil'
        }
    }
    
    # Year-round crops
    year_round_crops = {
        "🍅 Tomato": {
            'farming_steps': [
                '1. Nursery raising for 4-5 weeks',
                '2. Field preparation with raised beds',
                '3. Transplanting at 60x45cm spacing',
                '4. Staking and pruning management',
                '5. Regular monitoring and fertilization'
            ],
            'care_tips': [
                'Remove suckers regularly for better fruit development',
                'Control blight, leaf curl virus, and fruit borer',
                'Provide support to prevent fruit touching ground',
                'Harvest at proper maturity for better shelf life'
            ],
            'best_season': 'Multiple seasons possible with proper varieties',
            'harvest_time': 'Varies by season (70-120 days)',
            'water_requirement': 'Medium-High',
            'temperature_range': '20-30°C',
            'soil_type': 'Well-drained, rich in organic matter'
        },
        "🥕 Carrot": {
            'farming_steps': [
                '1. Prepare fine tilth with deep plowing',
                '2. Make raised beds for better drainage',
                '3. Sow seeds directly in lines 20cm apart',
                '4. Thin seedlings to 5cm spacing',
                '5. Regular watering and weed management'
            ],
            'care_tips': [
                'Avoid fresh manure as it causes forked roots',
                'Maintain consistent soil moisture',
                'Control carrot fly and aphids',
                'Harvest when roots reach desired size and color'
            ],
            'best_season': 'October-November (winter season)',
            'harvest_time': 'January-March (90-120 days)',
            'water_requirement': 'Medium',
            'temperature_range': '15-25°C',
            'soil_type': 'Sandy loam, deep and well-drained'
        }
    }
    
    return july_crops, august_crops, september_crops, october_crops, year_round_crops

def get_crop_recommendations(weather_data, climate_prediction):
    """Generate crop recommendations based on weather and climate data"""
    if not weather_data or not climate_prediction:
        return []
    
    current_temp = weather_data['Current Temperature (°C)']
    humidity = weather_data['Humidity (%)']
    
    # Average temperature from prediction
    avg_temp = sum([day['temp_max'] + day['temp_min'] for day in climate_prediction]) / (2 * len(climate_prediction))
    avg_humidity = sum([day['humidity'] for day in climate_prediction]) / len(climate_prediction)
    
    recommendations = []
    
    # July-specific recommendations (prioritized)
    if 20 <= avg_temp <= 35 and avg_humidity >= 70:
        recommendations.append({
            'crop': '🌾 Rice (Kharif) - JULY PRIORITY',
            'suitability': 'Excellent for July',
            'season': 'Kharif (Monsoon)',
            'planting_time': 'July-August',
            'harvest_time': 'October-November',
            'water_requirement': 'High',
            'notes': 'Perfect time for rice sowing with monsoon rains'
        })
    
    if 21 <= avg_temp <= 30 and avg_humidity >= 50:
        recommendations.append({
            'crop': '🌽 Maize - JULY PRIORITY',
            'suitability': 'Excellent for July',
            'season': 'Kharif',
            'planting_time': 'July',
            'harvest_time': 'October-November',
            'water_requirement': 'Medium',
            'notes': 'Ideal monsoon crop for current conditions'
        })
        
    if avg_temp >= 25 and avg_humidity >= 60:
        recommendations.append({
            'crop': '🥒 Ridge Gourd - JULY PRIORITY',
            'suitability': 'Good for July',
            'season': 'Monsoon',
            'planting_time': 'July-August',
            'harvest_time': 'September-December',
            'water_requirement': 'Medium-High',
            'notes': 'Fast-growing monsoon vegetable'
        })
    
    # Other seasonal recommendations
    if 21 <= avg_temp <= 30:
        recommendations.append({
            'crop': '🎋 Sugarcane',
            'suitability': 'Excellent',
            'season': 'Year-round',
            'planting_time': 'February-March or October-November',
            'harvest_time': '12-18 months after planting',
            'water_requirement': 'Very High',
            'notes': 'High humidity and warm temperatures excellent for sugarcane'
        })
    
    # Vegetables
    if 15 <= avg_temp <= 25:
        recommendations.append({
            'crop': '🥬 Vegetables (Tomato, Onion, Potato)',
            'suitability': 'Good',
            'season': 'Rabi',
            'planting_time': 'October-November',
            'harvest_time': 'January-March',
            'water_requirement': 'Medium',
            'notes': 'Cool season vegetables suitable for predicted temperatures'
        })
    
    # Pulses
    if 20 <= avg_temp <= 30 and avg_humidity <= 70:
        recommendations.append({
            'crop': '🫘 Pulses (Chickpea, Lentil)',
            'suitability': 'Good',
            'season': 'Rabi',
            'planting_time': 'October-November',
            'harvest_time': 'February-March',
            'water_requirement': 'Low',
            'notes': 'Moderate temperatures and humidity suitable for pulses'
        })
    
    return recommendations

# === Function: Create Enhanced Map ===
def create_enhanced_map(lat, lon, weather_layer=None):
    """Create an enhanced Folium map with vibrant colors"""
    # Create base map with enhanced styling
    m = folium.Map(
        location=[lat, lon],
        zoom_start=8,
        tiles=None
    )
    
    # Add vibrant base tiles with enhanced colors
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='📡 Satellite View',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='🗺️ Street Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Enhanced colorful tile layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='🏔️ Terrain',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='🌍 National Geographic',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add weather layer if selected with enhanced visibility
    if weather_layer:
        layer_names = {
            'wind_new': '🌪️ Wind Speed',
            'precipitation_new': '🌧️ Precipitation',
            'temp_new': '🌡️ Temperature',
            'clouds_new': '☁️ Clouds',
            'pressure_new': '📊 Pressure',
            'snow_new': '❄️ Snow'
        }
        
        weather_tile = folium.TileLayer(
            tiles=f'https://tile.openweathermap.org/map/{weather_layer}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
            attr='OpenWeatherMap',
            name=layer_names.get(weather_layer, f'🌤️ Weather Layer'),
            overlay=True,
            control=True,
            opacity=0.8
        )
        weather_tile.add_to(m)
    
    # Add enhanced marker with better visualization
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(f"📍 Location: {lat:.4f}, {lon:.4f}<br>🌤️ Click for weather data", max_width=300),
        tooltip="🌾 Farm Location - Click for details",
        icon=folium.Icon(
            color='darkgreen',
            icon='tint',
            prefix='fa'
        )
    ).add_to(m)
    
    # Add a circle to highlight the area
    folium.Circle(
        [lat, lon],
        radius=5000,  # 5km radius
        popup=f"📍 5km radius around {lat:.4f}, {lon:.4f}",
        color='green',
        fill=True,
        fillColor='lightgreen',
        fillOpacity=0.3,
        weight=2,
        opacity=0.8
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    

    
    return m

# === Function: Get Color Legend Data ===
def get_color_legend_data(layer_type):
    """Return color legend data for different weather layers"""
    if layer_type == "temp_new":
        return [
            ("#800026", "> 40°C"),
            ("#BD0026", "35-40°C"),
            ("#E31A1C", "30-35°C"),
            ("#FC4E2A", "25-30°C"),
            ("#FD8D3C", "20-25°C"),
            ("#FEB24C", "15-20°C"),
            ("#FED976", "10-15°C"),
            ("#FFEDA0", "< 10°C")
        ]
    elif layer_type == "precipitation_new":
        return [
            ("#08519c", "Heavy (>50mm)"),
            ("#3182bd", "Moderate (20-50mm)"),
            ("#6baed6", "Light (5-20mm)"),
            ("#bdd7e7", "Very Light (<5mm)"),
            ("#eff3ff", "No Rain")
        ]
    elif layer_type == "wind_new":
        return [
            ("#67001f", "Very Strong (>15 m/s)"),
            ("#a50f15", "Strong (10-15 m/s)"),
            ("#cb181d", "Moderate (5-10 m/s)"),
            ("#fb6a4a", "Light (2-5 m/s)"),
            ("#fcbba1", "Calm (<2 m/s)")
        ]
    elif layer_type == "pressure_new":
        return [
            ("#2c7fb8", "Very High (>1020 hPa)"),
            ("#41b6c4", "High (1015-1020 hPa)"),
            ("#7fcdbb", "Normal (1010-1015 hPa)"),
            ("#c7e9b4", "Low (1005-1010 hPa)"),
            ("#edf8b1", "Very Low (<1005 hPa)")
        ]
    return []

# === MAIN STREAMLIT APP ===
def main():
    # Logo and Header
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    
    # Company header with text only
    st.markdown('<h1 class="company-name"><b>TerraAI Climate Modeling</b></h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="company-slogan"><b>Where Innovation Meets Sustainability</b></h2>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Attribution - very small at bottom
    st.markdown('<div class="attribution">Made by Srijan Trivedi, 10G</div>', unsafe_allow_html=True)
    
    # Main sections (Navigation panel removed as requested)
    tab1, tab2, tab3, tab4 = st.tabs(["🌤️ Weather Dashboard", "🗺️ Interactive Map", "🌾 Farmer Property", "📊 Analytics"])
    
    with tab1:
        st.markdown('<h2 class="section-header">🌤️ Weather Dashboard</h2>', unsafe_allow_html=True)
        st.markdown('<div class="box-with-header">', unsafe_allow_html=True)
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        
        # Weather input method inside the main content box
        st.markdown("### 🏙️ Search by City")
        city = st.text_input("Enter city name:", placeholder="e.g., Mumbai, Delhi, Bangalore", key="weather_city_search")
        city_search = st.button("🔍 Get Weather by City", key="city_search")
        
        # Weather display
        weather_data = None
        if city_search and city:
            weather_data = get_weather_by_city(city)
        
        if weather_data:
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.markdown(f"### 🌍 {weather_data['Location']}, {weather_data['Country']}")
            
            # Main weather metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🌡️ Temperature", f"{weather_data['Current Temperature (°C)']}°C", 
                         f"{weather_data['Feels Like (°C)'] - weather_data['Current Temperature (°C)']:+.1f}°C feels like")
            with col2:
                st.metric("💧 Humidity", f"{weather_data['Humidity (%)']}%")
            with col3:
                st.metric("🌪️ Wind Speed", f"{weather_data['Wind Speed (m/s)']} m/s")
            with col4:
                st.metric("🌤️ Pressure", f"{weather_data['Pressure (hPa)']} hPa")
            
            # Weather description
            st.markdown(f"**Current Weather:** {weather_data['Current Weather'].title()}")
            st.markdown(f"**Expected Weather:** {weather_data['Expected Weather']}")
            
            # Sun data
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**🌅 Sunrise:** {weather_data['Sunrise']}")
            with col2:
                st.markdown(f"**🌇 Sunset:** {weather_data['Sunset']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Enhanced Risk Analysis with Interactive Detailed Information
            risks = predict_risks(weather_data)
            detailed_risk_info = get_detailed_risk_info()
            
            st.markdown('<div style="background: linear-gradient(135deg, #FFEBEE 0%, #FFF3E0 100%); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #F44336;">', unsafe_allow_html=True)
            st.markdown("### ⚠️ Enhanced Risk Analysis & Notifications")
            
            if risks and "✅ No Major Risk Detected" not in risks:
                for risk in risks:
                    st.error(f"**{risk}**")
                    
                    # Use expandable section instead of button to avoid session state conflicts
                    if risk in detailed_risk_info:
                        with st.expander("🔍 Get Precautions & Safety Measures"):
                            risk_details = detailed_risk_info[risk]
                            st.markdown('<div style="background: #FFCDD2; padding: 15px; border-radius: 10px; margin: 10px 0;">', unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.markdown("**🚨 Early Warning Signs:**")
                                for sign in risk_details['early_signs']:
                                    st.markdown(f"• {sign}")
                            with col2:
                                st.markdown("**🛡️ Precautions to Take:**")
                                for precaution in risk_details['precautions']:
                                    st.markdown(f"• {precaution}")
                            with col3:
                                st.markdown("**🆘 During Disaster - Safety Measures:**")
                                for safety in risk_details['safety']:
                                    st.markdown(f"• {safety}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.success("✅ No Major Risk Detected - Current conditions are safe for farming activities")
            st.markdown("---")
            st.markdown("#### 📲 Enhanced Risk Notification System")
            st.markdown("Click on any alert type to see detailed precautions, early warning signs, and safety measures:")
            
            # Detailed risk information
            detailed_notifications = {
                "🌪️ Tornado Warnings": {
                    "early_signs": ["Sudden wind direction change", "Large hail", "Loud roar like freight train", "Visible funnel cloud", "Green-colored sky", "Sudden temperature drop"],
                    "precautions": ["Move livestock to sturdy shelters", "Secure all farm equipment", "Harvest mature crops immediately", "Cover stored grains and feed", "Check emergency supplies", "Clear drainage around buildings"],
                    "safety_measures": ["Go to lowest floor center room", "Stay away from windows", "Avoid large roof areas like barns", "Have battery radio ready", "Keep first aid kit accessible", "Know evacuation routes"],
                    "during_event": ["Stay in safe room until all clear", "Monitor weather radio", "Do not go outside during eye", "Watch for flying debris", "Keep away from damaged power lines", "Wait for official all-clear signal"]
                },
                "🔔 Flash Flood Alerts": {
                    "early_signs": ["Heavy rainfall for 30+ minutes", "Water in low-lying areas", "Muddy or fast-moving water", "Unusual sounds from streams", "Rapid water level rise", "Debris in water flow"],
                    "precautions": ["Move animals to higher ground", "Protect stored feed and grain", "Secure fuel tanks and chemicals", "Clear drainage channels", "Move machinery uphill", "Prepare sandbags if available"],
                    "safety_measures": ["Never walk through moving water", "Stay out of flooded areas", "Monitor local radio/TV", "Have evacuation plan ready", "Keep emergency kit accessible", "Stay away from downed power lines"],
                    "during_event": ["Move to higher ground immediately", "Do not drive through flooded roads", "Stay out of basement areas", "Monitor water levels constantly", "Be ready to evacuate quickly", "Help neighbors if safe to do so"]
                },
                "❄️ Frost Alerts": {
                    "early_signs": ["Temperature dropping below 2°C", "Clear night skies", "Little to no wind", "High humidity followed by drying", "Dew point near freezing", "Weather forecast prediction"],
                    "precautions": ["Cover sensitive plants with cloth", "Use frost protection sprays", "Turn on sprinkler systems", "Light smudge pots or fires", "Harvest frost-sensitive crops", "Move potted plants indoors"],
                    "safety_measures": ["Check on elderly neighbors", "Protect water pipes from freezing", "Ensure heating systems work", "Keep extra blankets ready", "Have backup heating source", "Monitor livestock water sources"],
                    "during_event": ["Keep fires burning safely", "Monitor plant covering", "Check livestock frequently", "Avoid walking on icy surfaces", "Keep pathways clear of ice", "Watch for hypothermia signs"]
                },
                "⛈️ Storm Warnings": {
                    "early_signs": ["Dark threatening clouds", "Strong wind gusts", "Lightning activity", "Sudden temperature drop", "Heavy rain starting", "Barometric pressure drop"],
                    "precautions": ["Secure outdoor equipment", "Tie down or store light objects", "Check roof and gutters", "Trim tree branches near buildings", "Store extra water and food", "Charge electronic devices"],
                    "safety_measures": ["Stay indoors during storm", "Unplug electrical equipment", "Avoid using corded phones", "Stay away from windows", "Have flashlights ready", "Monitor weather alerts"],
                    "during_event": ["Stay in strongest part of building", "Avoid using electrical appliances", "Do not take shelter under trees", "Wait for storm to pass completely", "Check for gas leaks after", "Inspect property for damage"]
                },
                "🌡️ Heat Wave Alerts": {
                    "early_signs": ["Temperature above 40°C for 2+ days", "High humidity with heat", "Little nighttime cooling", "Clear sunny skies", "Weather advisories issued", "Heat index very high"],
                    "precautions": ["Increase watering frequency", "Provide shade for livestock", "Use cooling systems for animals", "Apply mulch to crops", "Schedule work for early morning", "Ensure adequate ventilation"],
                    "safety_measures": ["Stay hydrated constantly", "Wear light-colored clothing", "Take frequent breaks in shade", "Avoid midday outdoor work", "Check on elderly/vulnerable", "Watch for heat exhaustion signs"],
                    "during_event": ["Work only early morning/evening", "Provide extra water to animals", "Monitor crop stress signs", "Use misting systems if available", "Keep emergency contacts ready", "Know heat illness symptoms"]
                },
                "🌨️ Heavy Snow Alerts": {
                    "early_signs": ["Temperature near freezing", "Heavy cloud cover", "Increasing wind", "Humidity rising", "Barometric pressure falling", "Weather warnings issued"],
                    "precautions": ["Stock extra feed for animals", "Ensure heating fuel supply", "Clear gutters and drains", "Secure outdoor structures", "Have snow removal equipment ready", "Stock emergency supplies"],
                    "safety_measures": ["Keep pathways clear", "Avoid overexertion when shoveling", "Check on neighbors", "Maintain heating systems", "Have backup power source", "Keep vehicles winterized"],
                    "during_event": ["Stay warm and dry", "Clear snow from building roofs", "Keep exhaust vents clear", "Check on livestock frequently", "Avoid unnecessary travel", "Monitor for hypothermia"]
                },
                "💨 Wind Damage Alerts": {
                    "early_signs": ["Sustained winds >50 km/h", "Gusts >80 km/h", "Trees swaying heavily", "Dust or debris blowing", "Difficulty walking against wind", "Pressure changes rapidly"],
                    "precautions": ["Secure all loose items", "Tie down tarps and covers", "Protect greenhouse panels", "Anchor temporary structures", "Remove tree hazards", "Check building tie-downs"],
                    "safety_measures": ["Stay away from trees", "Avoid driving high-profile vehicles", "Secure doors and windows", "Have emergency plan ready", "Keep communication devices charged", "Monitor structural integrity"],
                    "during_event": ["Stay indoors away from windows", "Do not go outside", "Watch for flying debris", "Listen for structural sounds", "Be ready to move to safe area", "Wait for winds to subside"]
                },
                "☔ Heavy Rain Alerts": {
                    "early_signs": ["Dense dark clouds", "Humidity above 90%", "Steady rain beginning", "Weather radar showing red", "Flash flood watches issued", "Rivers/streams rising"],
                    "precautions": ["Clear drainage systems", "Move valuables to higher areas", "Protect stored materials", "Check pump systems", "Secure outdoor equipment", "Prepare sandbags"],
                    "safety_measures": ["Avoid low-lying areas", "Do not drive through water", "Stay informed via radio", "Have evacuation route planned", "Keep emergency kit ready", "Monitor water levels"],
                    "during_event": ["Stay on higher ground", "Monitor basement for flooding", "Avoid electrical equipment if wet", "Do not walk in moving water", "Help others if safe", "Report dangerous conditions"]
                },
                "🌪️ Cyclone Warnings": {
                    "early_signs": ["Sustained winds >120 km/h", "Organized circular clouds", "Storm surge warnings", "Evacuation orders issued", "Multiple weather alerts", "Rapid pressure drop"],
                    "precautions": ["Follow evacuation orders immediately", "Secure property completely", "Remove all loose objects", "Board up windows", "Stock emergency supplies for days", "Fuel vehicles and generators"],
                    "safety_measures": ["Evacuate if ordered", "Go to designated shelters", "Stay in strongest building part", "Have multiple communication methods", "Keep documents in waterproof container", "Monitor official channels"],
                    "during_event": ["Stay in safe room", "Do not go outside during eye", "Listen to emergency broadcasts", "Be prepared for long duration", "Conserve phone battery", "Wait for official all-clear"]
                }
            }
            
            col1, col2, col3 = st.columns(3)
            notification_buttons = list(detailed_notifications.keys())
            
            for i, notification_type in enumerate(notification_buttons):
                col = [col1, col2, col3][i % 3]
                with col:
                    with st.expander(notification_type):
                        details = detailed_notifications[notification_type]
                        st.markdown('<div style="background: #FFECB3; padding: 15px; border-radius: 10px; margin: 5px 0;">', unsafe_allow_html=True)
                        
                        st.markdown("**🚨 Early Warning Signs:**")
                        for sign in details['early_signs']:
                            st.markdown(f"• {sign}")
                        
                        st.markdown("**🛡️ Before Event - Precautions:**")
                        for precaution in details['precautions']:
                            st.markdown(f"• {precaution}")
                        
                        st.markdown("**🆘 Safety Measures:**")
                        for safety in details['safety_measures']:
                            st.markdown(f"• {safety}")
                        
                        if 'during_event' in details:
                            st.markdown("**⚡ During Event - Critical Actions:**")
                            for action in details['during_event']:
                                st.markdown(f"• {action}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.success(f"{notification_type} notifications are now active!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Enhanced Air Quality with Clickable Information
            air_quality = get_air_quality_data(weather_data['Lat'], weather_data['Lon'])
            if air_quality:
                st.markdown('<div style="background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #4CAF50;">', unsafe_allow_html=True)
                st.markdown("### 🫁 Air Quality Data - Click on any gas name for detailed information")
                
                air_quality_info = get_air_quality_info()
                
                # Display AQI in a green box like others
                if 'Air Quality Index' in air_quality:
                    st.markdown(f'<div style="background: #4CAF50; color: white; padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; font-weight: bold;">📊 Air Quality Index: {air_quality["Air Quality Index"]}</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                idx = 0
                for key, value in air_quality.items():
                    if key != 'Air Quality Index':  # Skip AQI since we already displayed it
                        with col1 if idx % 2 == 0 else col2:
                            if key in air_quality_info:
                                # Create unique key for each air quality component
                                aq_key = f"dash_aq_{key.replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').replace('.', '')}"
                                
                                # Use expandable section instead of button to avoid session state conflicts
                                with st.expander(f"📊 {key}: {value}"):
                                    info = air_quality_info[key]
                                    st.markdown('<div style="background: #C8E6C9; padding: 10px; border-radius: 8px; margin: 5px 0;">', unsafe_allow_html=True)
                                    st.markdown(f"**🩺 Health Effects:** {info['effects']}")
                                    st.markdown(f"**⚠️ Symptoms to Watch:** {info['symptoms']}")
                                    st.markdown(f"**🛡️ Protection Measures:** {info['protection']}")
                                    st.markdown('</div>', unsafe_allow_html=True)
                            else:
                                st.metric(key, value)
                        idx += 1
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Astronomical Data
            astro_data = get_astronomical_data(weather_data['Lat'], weather_data['Lon'])
            if astro_data:
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                st.markdown("### 🌙 Astronomical Data")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🌅 Sunrise", astro_data['sunrise'])
                with col2:
                    st.metric("🌇 Sunset", astro_data['sunset'])
                with col3:
                    st.metric("🌙 Moonrise", astro_data['moonrise'])
                with col4:
                    st.metric("🌚 Moonset", astro_data['moonset'])
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 class="section-header">🗺️ Interactive Weather Map</h2>', unsafe_allow_html=True)
        st.markdown('<div class="box-with-header">', unsafe_allow_html=True)
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        
        # Map controls
        col1, col2 = st.columns(2)
        with col1:
            selected_layer = st.selectbox("Select Weather Layer:", 
                                        ["None"] + list(weather_layers.keys()))
        with col2:
            if selected_layer != "None":
                st.info(f"ℹ️ {layer_descriptions.get(weather_layers[selected_layer], 'Weather layer information')}")
        
        # Create and display map
        map_lat = lat if 'lat' in locals() else 28.6139
        map_lon = lon if 'lon' in locals() else 77.2090
        
        layer_id = weather_layers.get(selected_layer) if selected_layer != "None" else None
        enhanced_map = create_enhanced_map(map_lat, map_lon, layer_id)
        
        map_data = st_folium(enhanced_map, width=1000, height=600)
        
        # Display color legend below the map
        if selected_layer != "None":
            st.markdown("### 🎨 Color Index Scale for Weather Data")
            legend_data = get_color_legend_data(weather_layers.get(selected_layer))
            if legend_data:
                cols = st.columns(len(legend_data))
                for i, (color, desc) in enumerate(legend_data):
                    with cols[i]:
                        st.markdown(f'<div style="background: {color}; height: 30px; width: 100%; border: 2px solid #ddd; border-radius: 5px; margin-bottom: 5px;"></div>', unsafe_allow_html=True)
                        st.markdown(f"<small style='text-align: center; display: block;'>{desc}</small>", unsafe_allow_html=True)
        
        # Enhanced map click handling with better formatted weather display
        if map_data['last_clicked']:
            clicked_lat = map_data['last_clicked']['lat']
            clicked_lon = map_data['last_clicked']['lng']
            st.success(f"📍 Clicked location: {clicked_lat:.4f}, {clicked_lon:.4f}")
            
            # Get weather for clicked location
            if st.button("🌤️ Get Weather for Clicked Location"):
                clicked_weather = get_weather_by_coords(clicked_lat, clicked_lon)
                if clicked_weather:
                    # Enhanced formatted display instead of raw JSON
                    st.markdown("### 🌍 Weather Information for Selected Location")
                    
                    # Use custom styled cards for better presentation
                    st.markdown('<div style="background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #2E7D32; font-family: \'Calibri\', sans-serif;">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**🌍 Location:** {clicked_weather['Location']}, {clicked_weather['Country']}")
                        st.markdown(f"**🌡️ Temperature:** {clicked_weather['Current Temperature (°C)']}°C (Feels like {clicked_weather['Feels Like (°C)']}°C)")
                        st.markdown(f"**💧 Humidity:** {clicked_weather['Humidity (%)']}%")
                        st.markdown(f"**🌪️ Wind Speed:** {clicked_weather['Wind Speed (m/s)']} m/s")
                    with col2:
                        st.markdown(f"**🌤️ Weather:** {clicked_weather['Current Weather'].title()}")
                        st.markdown(f"**🌅 Sunrise:** {clicked_weather['Sunrise']}")
                        st.markdown(f"**🌇 Sunset:** {clicked_weather['Sunset']}")
                        st.markdown(f"**📊 Pressure:** {clicked_weather['Pressure (hPa)']} hPa")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Add complete weather information to Interactive Map tab
        if map_data['last_clicked']:
            clicked_lat = map_data['last_clicked']['lat']
            clicked_lon = map_data['last_clicked']['lng']
            
            # Get comprehensive weather data for clicked location
            clicked_weather = get_weather_by_coords(clicked_lat, clicked_lon)
            if clicked_weather:
                st.markdown("---")
                st.markdown("### 📊 Complete Weather Analysis for Selected Location")
                
                # Enhanced Risk Analysis for clicked location
                risks = predict_risks(clicked_weather)
                detailed_risk_info = get_detailed_risk_info()
                
                st.markdown('<div style="background: linear-gradient(135deg, #FFEBEE 0%, #FFF3E0 100%); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #F44336;">', unsafe_allow_html=True)
                st.markdown("#### ⚠️ Enhanced Risk Analysis")
                
                if risks and "✅ No Major Risk Detected" not in risks:
                    for risk in risks:
                        st.error(f"**{risk}**")
                        
                        # Use expandable section instead of button to avoid session state conflicts
                        if risk in detailed_risk_info:
                            with st.expander("🔍 Get Precautions & Safety Measures"):
                                risk_details = detailed_risk_info[risk]
                                st.markdown('<div style="background: #FFCDD2; padding: 15px; border-radius: 10px; margin: 10px 0;">', unsafe_allow_html=True)
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.markdown("**🚨 Early Warning Signs:**")
                                    for sign in risk_details['early_signs']:
                                        st.markdown(f"• {sign}")
                                with col2:
                                    st.markdown("**🛡️ Precautions to Take:**")
                                    for precaution in risk_details['precautions']:
                                        st.markdown(f"• {precaution}")
                                with col3:
                                    st.markdown("**🆘 During Disaster - Safety Measures:**")
                                    for safety in risk_details['safety']:
                                        st.markdown(f"• {safety}")
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.success("✅ No Major Risk Detected")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Air Quality for clicked location
                air_quality = get_air_quality_data(clicked_lat, clicked_lon)
                if air_quality:
                    st.markdown('<div style="background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #4CAF50;">', unsafe_allow_html=True)
                    st.markdown("#### 🫁 Air Quality Data - Click on any gas name for detailed information")
                    
                    air_quality_info = get_air_quality_info()
                    
                    # Display AQI in a green box like others
                    if 'Air Quality Index' in air_quality:
                        st.markdown(f'<div style="background: #4CAF50; color: white; padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; font-weight: bold;">📊 Air Quality Index: {air_quality["Air Quality Index"]}</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    idx = 0
                    for key, value in air_quality.items():
                        if key != 'Air Quality Index':  # Skip AQI since we already displayed it
                            with col1 if idx % 2 == 0 else col2:
                                if key in air_quality_info:
                                    # Use expandable section instead of button to avoid session state conflicts
                                    with st.expander(f"📊 {key}: {value}"):
                                        info = air_quality_info[key]
                                        st.markdown('<div style="background: #C8E6C9; padding: 10px; border-radius: 8px; margin: 5px 0;">', unsafe_allow_html=True)
                                        st.markdown(f"**🩺 Health Effects:** {info['effects']}")
                                        st.markdown(f"**⚠️ Symptoms to Watch:** {info['symptoms']}")
                                        st.markdown(f"**🛡️ Protection Measures:** {info['protection']}")
                                        st.markdown('</div>', unsafe_allow_html=True)
                                else:
                                    st.metric(key, value)
                            idx += 1
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Astronomical Data for clicked location
                astro_data = get_astronomical_data(clicked_lat, clicked_lon)
                if astro_data:
                    st.markdown("#### 🌙 Astronomical Information")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("🌅 Sunrise", astro_data['sunrise'])
                    with col2:
                        st.metric("🌇 Sunset", astro_data['sunset'])
                    with col3:
                        st.metric("🌙 Moonrise", astro_data['moonrise'])
                    with col4:
                        st.metric("🌚 Moonset", astro_data['moonset'])
    
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="section-header">🌾 Farmer Property Dashboard</h2>', unsafe_allow_html=True)
        st.markdown('<div class="box-with-header">', unsafe_allow_html=True)
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        
        # Enhanced farmer guidance section
        st.markdown('<div class="farmer-property-card">', unsafe_allow_html=True)
        st.markdown('<div class="farmer-property-header">🌾 Complete Farming Guidance System</div>', unsafe_allow_html=True)
        
        # Farm Details Input
        st.markdown('<div class="property-grid">', unsafe_allow_html=True)
        
        # Basic farm information
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="property-item">', unsafe_allow_html=True)
            st.markdown("#### 🏡 Farm Basic Information")
            farm_name = st.text_input("Farm Name:", placeholder="e.g., Green Valley Farm")
            owner_name = st.text_input("Owner Name:", placeholder="Your name")
            farm_location = st.text_input("Farm Location:", placeholder="e.g., Village, District, State")
            farm_size = st.number_input("Farm Size (acres):", min_value=0.1, step=0.1, value=1.0)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="property-item">', unsafe_allow_html=True)
            st.markdown("#### 🌍 Tell Us About Your Area")
            region_type = st.selectbox("What type of area do you live in?:", 
                                     ["Plains", "Hilly/Mountain", "Coastal", "Desert", "River Valley", "Not Sure"])
            climate_type = st.selectbox("What's your area's climate like?:", 
                                      ["Hot & Humid", "Hot & Dry", "Moderate", "Cold", "Rainy", "Not Sure"])
            water_source = st.selectbox("What water sources do you have?:", 
                                      ["River nearby", "Well/Borewell", "Rainwater only", "Canal", "Not Sure"])
            budget_range = st.selectbox("Your budget for farming (per acre):", 
                                      ["Under ₹20,000", "₹20,000-50,000", "₹50,000-1,00,000", "Above ₹1,00,000"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🌾 Get Complete Farming Guidance", key="farm_guidance"):
            if farm_name and owner_name and farm_location:
                st.markdown("---")
                st.markdown('<div class="farmer-property-header">🌾 Your Complete Farming Guide</div>', unsafe_allow_html=True)
                
                # Get soil recommendations based on area type
                def get_soil_guidance(region_type, climate_type):
                    soil_advice = {
                        "Plains": {
                            "best_soil": "Loamy or Black Cotton Soil",
                            "preparation": "Deep plowing, add organic compost, ensure good drainage",
                            "tips": "Plains soil is usually fertile. Add cow dung and neem cake for better results."
                        },
                        "Hilly/Mountain": {
                            "best_soil": "Terrace farming with loamy soil",
                            "preparation": "Build terraces, prevent soil erosion, add organic matter",
                            "tips": "Mountain soil can be rocky. Use organic compost and mulching."
                        },
                        "Coastal": {
                            "best_soil": "Sandy loam with good drainage",
                            "preparation": "Add organic matter, improve water retention, control salt",
                            "tips": "Coastal areas have salt. Use coconut coir and organic fertilizers."
                        },
                        "Desert": {
                            "best_soil": "Sandy soil with water conservation",
                            "preparation": "Drip irrigation, mulching, shade nets",
                            "tips": "Desert farming needs water saving. Use drought-resistant crops."
                        },
                        "River Valley": {
                            "best_soil": "Alluvial soil (very fertile)",
                            "preparation": "Minimal preparation, add compost, ensure drainage",
                            "tips": "River valley soil is naturally fertile. Perfect for most crops."
                        }
                    }
                    return soil_advice.get(region_type, soil_advice["Plains"])
                
                # Get irrigation recommendations
                def get_irrigation_guidance(water_source, budget_range, farm_size):
                    irrigation_advice = {}
                    if water_source in ["River nearby", "Canal"]:
                        irrigation_advice = {
                            "recommended": "Flood Irrigation or Drip System",
                            "cost": "₹15,000-40,000 per acre",
                            "setup": "Install PVC pipes from water source to field. Set up water pumps and automatic timers for maximum efficiency. Create proper water channels.",
                            "maintenance": "Clean all pipes monthly. Check for leaks weekly. Service pumps quarterly for optimal performance."
                        }
                    elif water_source == "Well/Borewell":
                        irrigation_advice = {
                            "recommended": "Drip Irrigation (saves 60% water)",
                            "cost": "₹25,000-60,000 per acre",
                            "setup": "Install drip lines throughout field area. Set up pressure tanks, filters, and control valves. Connect to main water supply with proper fittings.",
                            "maintenance": "Replace drippers yearly for optimal flow. Clean filters weekly to prevent clogging. Check pressure regularly."
                        }
                    else:  # Rainwater only
                        irrigation_advice = {
                            "recommended": "Rainwater Harvesting + Storage",
                            "cost": "₹20,000-50,000 per acre",
                            "setup": "Build large water storage tanks for collection. Install gutters and downspouts. Use mulching to retain soil moisture and reduce evaporation.",
                            "maintenance": "Clean tanks thoroughly before monsoon season. Use water-saving techniques like drip irrigation and mulching throughout the year."
                        }
                    return irrigation_advice
                
                # Get crop recommendations with prices
                def get_crop_recommendations(climate_type, region_type, budget_range):
                    crop_data = {
                        "Vegetables": [
                            {"name": "Tomato", "price": "₹20-40/kg", "season": "Oct-Feb", "profit": "₹40,000-80,000/acre", 
                             "steps": "1. Prepare 1×3 feet raised beds 2. Plant seedlings 18 inches apart 3. Install bamboo stakes 4. Water every morning 5. Apply compost monthly",
                             "fertilizer": "DAP fertilizer at planting, Urea after 30 days, Potash during fruiting",
                             "medicine": "Neem oil spray for pests, Copper fungicide for diseases, BT spray for caterpillars"},
                            {"name": "Potato", "price": "₹10-25/kg", "season": "Oct-Jan", "profit": "₹35,000-60,000/acre",
                             "steps": "1. Cut seed potatoes with 2-3 eyes 2. Plant 6 inches deep, 12 inches apart 3. Cover with soil 4. Water every 3 days 5. Hill up soil when plants are 6 inches tall",
                             "fertilizer": "NPK 19:19:19 at planting, Muriate of Potash when flowering starts",
                             "medicine": "Metalaxyl for late blight, Chlorpyrifos for beetle control"},
                            {"name": "Onion", "price": "₹15-35/kg", "season": "Nov-Apr", "profit": "₹30,000-70,000/acre",
                             "steps": "1. Prepare seedbed and sow seeds 2. Transplant 6-week seedlings 3. Plant 4 inches apart in rows 4. Water lightly but regularly 5. Stop watering 2 weeks before harvest",
                             "fertilizer": "FYM before planting, NPK during bulb formation, Sulphur for better quality",
                             "medicine": "Mancozeb for purple blotch, Thiamethoxam for thrips control"},
                            {"name": "Cabbage", "price": "₹12-20/kg", "season": "Oct-Mar", "profit": "₹25,000-45,000/acre",
                             "steps": "1. Sow seeds in nursery 2. Transplant 4-week seedlings 3. Plant 18 inches apart 4. Water morning and evening 5. Harvest when heads are firm",
                             "fertilizer": "Vermicompost at planting, NPK 20:20:20 every 3 weeks, Boron for head development",
                             "medicine": "BT spray for cabbage worm, Imidacloprid for aphids, Carbendazim for clubroot"},
                            {"name": "Carrot", "price": "₹18-30/kg", "season": "Nov-Feb", "profit": "₹28,000-50,000/acre",
                             "steps": "1. Prepare fine seedbed 2. Sow seeds thinly in rows 3. Thin seedlings to 2-3 inches apart 4. Water gently daily 5. Harvest after 90-100 days",
                             "fertilizer": "Well-decomposed FYM, NPK 40:60:40 kg/hectare, Potash for root development",
                             "medicine": "Carbaryl for root fly, Mancozeb for leaf blight, Azoxystrobin for root rot"},
                            {"name": "Brinjal", "price": "₹15-25/kg", "season": "Oct-Mar", "profit": "₹32,000-65,000/acre",
                             "steps": "1. Raise seedlings in nursery 2. Transplant 45-day seedlings 3. Plant 60×45 cm apart 4. Support with stakes 5. Regular harvesting",
                             "fertilizer": "FYM 25 tons/hectare, NPK 150:100:100 kg/hectare in splits",
                             "medicine": "Spinosad for fruit borer, Imidacloprid for aphids, Mancozeb for wilt"},
                            {"name": "Okra", "price": "₹12-20/kg", "season": "Jun-Oct", "profit": "₹25,000-45,000/acre",
                             "steps": "1. Soak seeds overnight 2. Sow directly in field 3. Plant 30×15 cm apart 4. Regular watering 5. Harvest tender pods every 2-3 days",
                             "fertilizer": "NPK 100:50:50 kg/hectare, side dress with N after 30 days",
                             "medicine": "Thiamethoxam for jassids, Quinalphos for fruit borer, Copper fungicide for leaf spot"},
                            {"name": "Cauliflower", "price": "₹15-25/kg", "season": "Nov-Feb", "profit": "₹30,000-55,000/acre",
                             "steps": "1. Prepare nursery beds 2. Transplant 30-day seedlings 3. Plant 45×45 cm apart 4. Tie leaves over curds for whiteness 5. Harvest when curds are compact",
                             "fertilizer": "NPK 150:100:100 kg/hectare, Boron spray for curd development",
                             "medicine": "BT for diamond back moth, Dimethoate for aphids, Mancozeb for black rot"},
                            {"name": "Green Beans", "price": "₹20-35/kg", "season": "Oct-Mar", "profit": "₹35,000-60,000/acre",
                             "steps": "1. Prepare raised beds 2. Sow seeds 3-4 cm deep 3. Install support for climbing varieties 4. Water regularly 5. Harvest tender pods",
                             "fertilizer": "Phosphorus-rich fertilizer, NPK 25:50:25 kg/hectare, Rhizobium inoculation",
                             "medicine": "Profenofos for pod borer, Carbendazim for anthracnose, Triazophos for thrips"},
                            {"name": "Spinach", "price": "₹10-18/kg", "season": "Oct-Feb", "profit": "₹20,000-35,000/acre",
                             "steps": "1. Prepare fine seedbed 2. Broadcast seeds thinly 3. Cover lightly with soil 4. Water with fine spray 5. Harvest after 40-50 days",
                             "fertilizer": "High nitrogen fertilizer, Urea 100 kg/hectare in 2-3 splits",
                             "medicine": "Usually pest-free, may need Mancozeb for downy mildew in humid conditions"}
                        ],
                        "Fruits": [
                            {"name": "Banana", "price": "₹20-50/dozen", "season": "Year-round", "profit": "₹60,000-1,20,000/acre",
                             "steps": "1. Plant tissue culture saplings 6×6 feet apart 2. Dig 2×2 feet pits 3. Add FYM and plant 4. Water every 2 days 5. Support bunches with props",
                             "fertilizer": "NPK 200:100:300g per plant monthly, Zinc sulphate every 6 months",
                             "medicine": "Propiconazole for black sigatoka, Fipronil for weevil control, Bordeaux mixture for leaf spot"},
                            {"name": "Papaya", "price": "₹15-30/kg", "season": "Year-round", "profit": "₹40,000-80,000/acre",
                             "steps": "1. Sow seeds in polybags 2. Transplant 8-week seedlings 3. Plant 8×8 feet apart 4. Install drip irrigation 5. Harvest fruits when 1/4 yellow",
                             "fertilizer": "NPK 100:50:75g per plant monthly, Calcium nitrate for fruit quality",
                             "medicine": "Copper oxychloride for anthracnose, Dimethoate for aphids, Carbendazim for damping off"},
                            {"name": "Mango", "price": "₹40-100/kg", "season": "Mar-Jun", "profit": "₹80,000-2,00,000/acre",
                             "steps": "1. Plant grafted saplings 10×10m apart 2. Dig 1×1×1m pits 3. Add compost and plant 4. Water weekly in dry season 5. Prune after harvest",
                             "fertilizer": "NPK 1:0.5:1.2 kg per tree annually, Micronutrient spray during flowering",
                             "medicine": "Mancozeb for anthracnose, Lambda cyhalothrin for fruit fly, Hexaconazole for powdery mildew"},
                            {"name": "Guava", "price": "₹20-40/kg", "season": "Oct-Jan", "profit": "₹35,000-75,000/acre",
                             "steps": "1. Plant during monsoon 6×6m apart 2. Regular pruning for shape 3. Remove water shoots 4. Bag fruits to prevent fly damage 5. Harvest when light green",
                             "fertilizer": "FYM 25kg + NPK 400:200:400g per tree annually, Calcium spray for fruit quality",
                             "medicine": "Malathion for fruit fly, Carbendazim for wilt, Mancozeb for leaf spot"},
                            {"name": "Orange", "price": "₹30-60/kg", "season": "Nov-Feb", "profit": "₹70,000-1,50,000/acre",
                             "steps": "1. Plant grafted saplings 6×6m apart 2. Dig deep pits with drainage 3. Regular pruning and training 4. Drip irrigation system 5. Harvest when fully colored",
                             "fertilizer": "NPK 500:250:500g per tree annually, Micronutrient spray twice yearly",
                             "medicine": "Chlorpyrifos for citrus psyllid, Copper fungicide for canker, Abamectin for leaf miner"},
                            {"name": "Pomegranate", "price": "₹50-120/kg", "season": "Oct-Feb", "profit": "₹1,00,000-2,50,000/acre",
                             "steps": "1. Plant during monsoon 4×4m apart 2. Install trellis system 3. Regular pruning 4. Bag fruits for quality 5. Harvest when clicking sound on tapping",
                             "fertilizer": "NPK 625:312:312g per plant annually, Calcium and Boron sprays",
                             "medicine": "Chlorpyrifos for aphids, Mancozeb for bacterial blight, Dimethoate for thrips"},
                            {"name": "Grapes", "price": "₹40-80/kg", "season": "Dec-Apr", "profit": "₹80,000-2,00,000/acre",
                             "steps": "1. Plant grafted vines 3×1.5m apart 2. Install trellis system 3. Regular pruning and training 4. Drip irrigation 5. Harvest in early morning",
                             "fertilizer": "NPK 19:19:19 at 200g per vine monthly during growing season",
                             "medicine": "Sulphur for powdery mildew, Mancozeb for downy mildew, Imidacloprid for thrips"},
                            {"name": "Strawberry", "price": "₹100-200/kg", "season": "Oct-Mar", "profit": "₹1,50,000-3,00,000/acre",
                             "steps": "1. Prepare raised beds with black mulch 2. Plant disease-free runners 3. Drip irrigation setup 4. Remove runners regularly 5. Harvest every 2-3 days",
                             "fertilizer": "NPK 19:19:19 weekly through fertigation, Calcium nitrate for fruit quality",
                             "medicine": "Captan for gray mold, Imidacloprid for aphids, Abamectin for spider mites"},
                            {"name": "Custard Apple", "price": "₹40-80/kg", "season": "Aug-Nov", "profit": "₹50,000-1,00,000/acre",
                             "steps": "1. Plant during monsoon 5×5m apart 2. Minimal pruning required 3. Hand pollination for better yield 4. Support heavy branches 5. Harvest when soft to touch",
                             "fertilizer": "NPK 300:150:300g per tree annually, Organic compost preferred",
                             "medicine": "Usually pest-free, may need Quinalphos for scale insects, Bordeaux mixture for leaf spot"},
                            {"name": "Dragon Fruit", "price": "₹80-150/kg", "season": "Jun-Nov", "profit": "₹1,20,000-2,50,000/acre",
                             "steps": "1. Plant cuttings with concrete posts 2×2m apart 2. Install support structure 3. Night lighting for flowering 4. Hand pollination 5. Harvest when color changes",
                             "fertilizer": "NPK 100:50:100g per plant monthly, Calcium and Magnesium supplements",
                             "medicine": "Copper fungicide for stem rot, Chlorpyrifos for ants, Carbendazim for anthracnose"}
                        ],
                        "Cereals": [
                            {"name": "Rice", "price": "₹25-35/kg", "season": "Jun-Oct", "profit": "₹25,000-45,000/acre",
                             "steps": "1. Prepare nursery beds and sow seeds 2. Transplant 25-day seedlings 3. Maintain 2-3 inches water level 4. Apply fertilizer in 3 splits 5. Harvest when 80% grains are golden",
                             "fertilizer": "NPK 120:60:40 kg/hectare in 3 splits, Zinc sulphate if deficient",
                             "medicine": "Tricyclazole for blast, Chlorpyrifos for stem borer, BPH control with Imidacloprid"},
                            {"name": "Wheat", "price": "₹20-30/kg", "season": "Nov-Apr", "profit": "₹20,000-40,000/acre",
                             "steps": "1. Prepare fine seedbed 2. Sow seeds in rows 7-9 inches apart 3. Cover lightly with soil 4. Irrigate immediately after sowing 5. Harvest when moisture is 20-25%",
                             "fertilizer": "NPK 120:60:40 kg/hectare, half N at sowing, rest at first irrigation",
                             "medicine": "Propiconazole for rust diseases, 2,4-D for weed control, Malathion for aphids"},
                            {"name": "Maize", "price": "₹15-25/kg", "season": "Jun-Sep", "profit": "₹18,000-35,000/acre",
                             "steps": "1. Sow seeds 2-3 cm deep in rows 2. Maintain 60cm row spacing 3. Thin to single plant per hill 4. Side dress with nitrogen at knee-high 5. Harvest when kernels are hard and dry",
                             "fertilizer": "NPK 150:75:40 kg/hectare, split N application at 30 and 60 days",
                             "medicine": "Atrazine for weed control, Chlorpyrifos for stem borer, Mancozeb for leaf blight"},
                            {"name": "Bajra", "price": "₹18-28/kg", "season": "Jun-Oct", "profit": "₹15,000-30,000/acre",
                             "steps": "1. Sow seeds broadcast or in rows 2. Rake lightly to cover seeds 3. Water sparingly - drought tolerant 4. Thin overcrowded areas 5. Harvest when ears are fully dry",
                             "fertilizer": "NPK 40:20:0 kg/hectare, minimal fertilizer needed due to hardiness",
                             "medicine": "Usually pest-free, may need Mancozeb for downy mildew in wet conditions"},
                            {"name": "Barley", "price": "₹22-32/kg", "season": "Nov-Apr", "profit": "₹18,000-35,000/acre",
                             "steps": "1. Prepare well-drained seedbed 2. Sow seeds 4-5 cm deep 3. Maintain row spacing of 22-25 cm 4. Light irrigation after sowing 5. Harvest when fully mature and dry",
                             "fertilizer": "NPK 80:40:20 kg/hectare, most N at sowing, remaining during tillering",
                             "medicine": "Propiconazole for powdery mildew, 2,4-D for broad-leaf weeds, Chlorpyrifos for aphids"},
                            {"name": "Oats", "price": "₹25-40/kg", "season": "Oct-Mar", "profit": "₹20,000-40,000/acre",
                             "steps": "1. Prepare fine tilth seedbed 2. Broadcast or drill seeds 3. Light harrowing after sowing 4. Irrigate if rainfall insufficient 5. Cut when grains are in dough stage",
                             "fertilizer": "NPK 60:30:30 kg/hectare, nitrogen in 2 splits for better tillering",
                             "medicine": "Usually disease-resistant, may need herbicides for weed control in early stages"},
                            {"name": "Quinoa", "price": "₹200-400/kg", "season": "Oct-Mar", "profit": "₹80,000-1,50,000/acre",
                             "steps": "1. Prepare well-drained raised beds 2. Sow seeds 1-2 cm deep 3. Thin seedlings to 20 cm apart 4. Minimal watering needed 5. Harvest when seeds are hard",
                             "fertilizer": "Low fertilizer requirement, NPK 40:20:20 kg/hectare sufficient",
                             "medicine": "Generally pest-free, may need protection from birds during seed formation"},
                            {"name": "Sorghum", "price": "₹20-30/kg", "season": "Jun-Oct", "profit": "₹15,000-30,000/acre",
                             "steps": "1. Sow seeds 2-3 cm deep in rows 2. Maintain 45 cm row spacing 3. Thin to 15 cm plant spacing 4. Drought tolerant - minimal irrigation 5. Harvest when grains are hard",
                             "fertilizer": "NPK 80:40:40 kg/hectare, side dress with N at 30-45 days",
                             "medicine": "Chlorpyrifos for shoot fly, Quinalphos for stem borer, usually pest-resistant"},
                            {"name": "Finger Millet", "price": "₹30-50/kg", "season": "Jun-Nov", "profit": "₹25,000-45,000/acre",
                             "steps": "1. Prepare nursery and transplant or direct sow 2. Maintain 20×10 cm spacing 3. Hand weeding 2-3 times 4. Minimal water requirement 5. Harvest when ears turn brown",
                             "fertilizer": "NPK 50:25:25 kg/hectare, well-decomposed FYM preferred",
                             "medicine": "Usually pest-free, may need finger blast control with Tricyclazole"},
                            {"name": "Foxtail Millet", "price": "₹35-60/kg", "season": "Jun-Sep", "profit": "₹20,000-40,000/acre",
                             "steps": "1. Broadcast seeds or sow in lines 2. Light cultivation after sowing 3. Very drought tolerant 4. Weeding once or twice 5. Harvest after 70-80 days",
                             "fertilizer": "Minimal fertilizer needed, NPK 25:12:12 kg/hectare sufficient",
                             "medicine": "Pest-resistant crop, rarely needs pest control measures"}
                        ]
                    }
                    return crop_data
                
                # Display soil guidance
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 🌱 Soil Preparation Guide")
                soil_guide = get_soil_guidance(region_type, climate_type)
                st.success(f"**Best Soil Type for Your Area:** {soil_guide['best_soil']}")
                st.info(f"**Preparation Steps:** {soil_guide['preparation']}")
                st.warning(f"**Important Tips:** {soil_guide['tips']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display irrigation guidance
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 💧 Irrigation Setup Guide")
                irrigation_guide = get_irrigation_guidance(water_source, budget_range, farm_size)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("**Recommended System**", irrigation_guide['recommended'])
                    st.metric("**Setup Cost**", irrigation_guide['cost'])
                with col2:
                    st.markdown(f"""<div class="text-wrap" style="word-wrap: break-word; max-width: 100%; font-size: 14px; line-height: 1.5;">
<strong>Setup Steps:</strong><br/>
{irrigation_guide['setup']}
<br/><br/>
<strong>Maintenance:</strong><br/>
{irrigation_guide['maintenance']}
</div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display seasonal crop recommendations (July prioritized)
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 🌾 July Season Priority Crops + Year-Round Options")
                
                # Get detailed crop info with seasonal priority
                july_crops, august_crops, september_crops, october_crops, year_round_crops = get_detailed_crop_info()
                
                # July Priority Section
                st.markdown("### 🔥 **JULY SEASON PRIORITY - Plant Now!**")
                st.markdown("*These crops are perfect for July planting and will give best results:*")
                
                july_cols = st.columns(2)
                idx = 0
                for crop_name, crop_info in july_crops.items():
                    with july_cols[idx % 2]:
                        st.markdown(f"""<div style="background: linear-gradient(135deg, #E8F5E8 0%, #F0F8FF 100%); 
                                    padding: 15px; border-radius: 10px; margin: 10px 0; 
                                    border-left: 4px solid #4CAF50;">
                            <h4 style="color: #2E7D32; margin-top: 0;">{crop_name}</h4>
                            <p><strong>🕒 Best Season:</strong> {crop_info['best_season']}</p>
                            <p><strong>🌡️ Temperature:</strong> {crop_info['temperature_range']}</p>
                            <p><strong>💧 Water Need:</strong> {crop_info['water_requirement']}</p>
                            <p><strong>🌱 Soil Type:</strong> {crop_info['soil_type']}</p>
                            </div>""", unsafe_allow_html=True)
                        
                        with st.expander(f"📋 Get Complete Guide for {crop_name}"):
                            st.markdown(f"#### 🌾 Complete Farming Guide for {crop_name}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**🔧 Step-by-Step Farming:**")
                                for step in crop_info['farming_steps']:
                                    st.markdown(f"• {step}")
                            
                            with col2:
                                st.markdown("**🌿 Care & Maintenance:**")
                                for tip in crop_info['care_tips']:
                                    st.markdown(f"• {tip}")
                            
                            st.markdown(f"**⏰ Harvest Time:** {crop_info['harvest_time']}")
                    idx += 1
                
                st.markdown("---")
                
                # Add multi-month crop planning
                st.markdown("### 📅 **4-MONTH CROP PLANNING CALENDAR**")
                st.markdown("*Plan your crops for the next 4 months based on optimal planting times:*")
                
                month_tabs = st.tabs(["🌾 July", "🌿 August", "🥕 September", "🥔 October"])
                
                with month_tabs[0]:
                    st.markdown("#### July Priority Crops (Already shown above)")
                    st.markdown("*Refer to the July priority section above for detailed guidance.*")
                
                with month_tabs[1]:
                    st.markdown("#### August Planting Recommendations")
                    aug_cols = st.columns(2)
                    idx = 0
                    for crop_name, crop_info in august_crops.items():
                        with aug_cols[idx % 2]:
                            st.markdown(f"""<div style="background: linear-gradient(135deg, #FFF3E0 0%, #E8F5E8 100%); 
                                        padding: 15px; border-radius: 10px; margin: 10px 0; 
                                        border-left: 4px solid #FF9800;">
                                <h4 style="color: #E65100; margin-top: 0;">{crop_name}</h4>
                                <p><strong>🕒 Best Season:</strong> {crop_info['best_season']}</p>
                                <p><strong>⏰ Harvest:</strong> {crop_info['harvest_time']}</p>
                                </div>""", unsafe_allow_html=True)
                            
                            with st.expander(f"📋 Get Complete Guide for {crop_name}"):
                                st.markdown(f"#### 🌾 Complete Farming Guide for {crop_name}")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown("**🔧 Step-by-Step Farming:**")
                                    for step in crop_info['farming_steps']:
                                        st.markdown(f"• {step}")
                                with col2:
                                    st.markdown("**🌿 Care & Maintenance:**")
                                    for tip in crop_info['care_tips']:
                                        st.markdown(f"• {tip}")
                        idx += 1
                
                with month_tabs[2]:
                    st.markdown("#### September Planting Recommendations")
                    sep_cols = st.columns(2)
                    idx = 0
                    for crop_name, crop_info in september_crops.items():
                        with sep_cols[idx % 2]:
                            st.markdown(f"""<div style="background: linear-gradient(135deg, #F3E5F5 0%, #E8F5E8 100%); 
                                        padding: 15px; border-radius: 10px; margin: 10px 0; 
                                        border-left: 4px solid #9C27B0;">
                                <h4 style="color: #4A148C; margin-top: 0;">{crop_name}</h4>
                                <p><strong>🕒 Best Season:</strong> {crop_info['best_season']}</p>
                                <p><strong>⏰ Harvest:</strong> {crop_info['harvest_time']}</p>
                                </div>""", unsafe_allow_html=True)
                            
                            with st.expander(f"📋 Get Complete Guide for {crop_name}"):
                                st.markdown(f"#### 🌾 Complete Farming Guide for {crop_name}")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown("**🔧 Step-by-Step Farming:**")
                                    for step in crop_info['farming_steps']:
                                        st.markdown(f"• {step}")
                                with col2:
                                    st.markdown("**🌿 Care & Maintenance:**")
                                    for tip in crop_info['care_tips']:
                                        st.markdown(f"• {tip}")
                        idx += 1
                
                with month_tabs[3]:
                    st.markdown("#### October Planting Recommendations")
                    oct_cols = st.columns(2)
                    idx = 0
                    for crop_name, crop_info in october_crops.items():
                        with oct_cols[idx % 2]:
                            st.markdown(f"""<div style="background: linear-gradient(135deg, #E3F2FD 0%, #E8F5E8 100%); 
                                        padding: 15px; border-radius: 10px; margin: 10px 0; 
                                        border-left: 4px solid #2196F3;">
                                <h4 style="color: #0D47A1; margin-top: 0;">{crop_name}</h4>
                                <p><strong>🕒 Best Season:</strong> {crop_info['best_season']}</p>
                                <p><strong>⏰ Harvest:</strong> {crop_info['harvest_time']}</p>
                                </div>""", unsafe_allow_html=True)
                            
                            with st.expander(f"📋 Get Complete Guide for {crop_name}"):
                                st.markdown(f"#### 🌾 Complete Farming Guide for {crop_name}")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown("**🔧 Step-by-Step Farming:**")
                                    for step in crop_info['farming_steps']:
                                        st.markdown(f"• {step}")
                                with col2:
                                    st.markdown("**🌿 Care & Maintenance:**")
                                    for tip in crop_info['care_tips']:
                                        st.markdown(f"• {tip}")
                        idx += 1
                
                st.markdown("---")
                
                # Agricultural Impact Analysis (moved from Analytics)
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 🌾 Agricultural Impact Analysis for Your Farm")
                
                if farm_location:
                    farm_weather = get_weather_by_city(farm_location.split(',')[0])
                    if farm_weather:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("**🌡️ Temperature Impact:**")
                            temp = farm_weather['Current Temperature (°C)']
                            if temp > 35:
                                st.error("⚠️ High temperature stress on crops")
                                st.markdown("• Use shade nets for sensitive crops")
                                st.markdown("• Increase irrigation frequency")
                            elif temp < 15:
                                st.warning("❄️ Cool weather - protect sensitive crops")
                                st.markdown("• Cover crops during night")
                                st.markdown("• Delay planting of warm season crops")
                            else:
                                st.success("✅ Optimal temperature for most crops")
                        
                        with col2:
                            st.markdown("**💧 Humidity Impact:**")
                            humidity = farm_weather['Humidity (%)']
                            if humidity > 80:
                                st.warning("💧 High humidity - disease risk")
                                st.markdown("• Monitor for fungal diseases")
                                st.markdown("• Ensure good air circulation")
                            elif humidity < 40:
                                st.error("🌵 Low humidity - water stress")
                                st.markdown("• Increase irrigation frequency")
                                st.markdown("• Use mulching to retain moisture")
                            else:
                                st.success("✅ Good humidity levels")
                        
                        with col3:
                            st.markdown("**🌪️ Wind Impact:**")
                            wind = farm_weather['Wind Speed (m/s)']
                            if wind > 10:
                                st.error("💨 Strong winds - crop damage risk")
                                st.markdown("• Install windbreaks")
                                st.markdown("• Stake tall plants")
                            elif wind < 2:
                                st.warning("🌬️ Low air movement")
                                st.markdown("• Ensure plant spacing for air flow")
                            else:
                                st.success("✅ Good air movement")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Enhanced Market Price Trends (moved from Analytics)
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 💰 Enhanced Market Price Trends & Profit Analysis")
                
                # Extended price data with more crops and seasonal variations
                extended_price_trends = {
                    'Vegetables': [
                        {'crop': 'Tomato', 'current': '₹25/kg', 'month1': '₹30/kg', 'month2': '₹35/kg', 'month3': '₹40/kg', 
                         'trend': '📈 Rising', 'seasonal_note': 'Peak demand in winter', 'profit_per_acre': '₹60,000-1,20,000'},
                        {'crop': 'Potato', 'current': '₹18/kg', 'month1': '₹20/kg', 'month2': '₹22/kg', 'month3': '₹25/kg', 
                         'trend': '📈 Rising', 'seasonal_note': 'Storage crops get higher prices', 'profit_per_acre': '₹40,000-80,000'},
                        {'crop': 'Onion', 'current': '₹25/kg', 'month1': '₹30/kg', 'month2': '₹35/kg', 'month3': '₹40/kg', 
                         'trend': '📈 Strong Rise', 'seasonal_note': 'Storage premium in off-season', 'profit_per_acre': '₹50,000-1,00,000'},
                        {'crop': 'Cabbage', 'current': '₹15/kg', 'month1': '₹18/kg', 'month2': '₹20/kg', 'month3': '₹22/kg', 
                         'trend': '📈 Gradual Rise', 'seasonal_note': 'Winter peak demand', 'profit_per_acre': '₹30,000-60,000'},
                        {'crop': 'Cauliflower', 'current': '₹20/kg', 'month1': '₹25/kg', 'month2': '₹30/kg', 'month3': '₹35/kg', 
                         'trend': '📈 Rising', 'seasonal_note': 'Premium winter vegetable', 'profit_per_acre': '₹40,000-75,000'},
                    ],
                    'Fruits': [
                        {'crop': 'Banana', 'current': '₹35/dozen', 'month1': '₹40/dozen', 'month2': '₹45/dozen', 'month3': '₹50/dozen', 
                         'trend': '📈 Steady Rise', 'seasonal_note': 'Year-round demand', 'profit_per_acre': '₹80,000-1,50,000'},
                        {'crop': 'Papaya', 'current': '₹25/kg', 'month1': '₹28/kg', 'month2': '₹30/kg', 'month3': '₹32/kg', 
                         'trend': '📈 Gradual Rise', 'seasonal_note': 'Health consciousness driving demand', 'profit_per_acre': '₹50,000-90,000'},
                        {'crop': 'Mango', 'current': '₹80/kg', 'month1': '₹60/kg', 'month2': '₹40/kg', 'month3': '₹120/kg', 
                         'trend': '🔄 Seasonal', 'seasonal_note': 'Off-season premium prices', 'profit_per_acre': '₹1,20,000-3,00,000'},
                        {'crop': 'Guava', 'current': '₹30/kg', 'month1': '₹35/kg', 'month2': '₹40/kg', 'month3': '₹35/kg', 
                         'trend': '📈 Peak Soon', 'seasonal_note': 'Winter season peak', 'profit_per_acre': '₹45,000-85,000'},
                    ],
                    'Cereals': [
                        {'crop': 'Rice', 'current': '₹30/kg', 'month1': '₹32/kg', 'month2': '₹35/kg', 'month3': '₹38/kg', 
                         'trend': '📈 Rising', 'seasonal_note': 'Post-harvest storage premium', 'profit_per_acre': '₹35,000-65,000'},
                        {'crop': 'Wheat', 'current': '₹25/kg', 'month1': '₹27/kg', 'month2': '₹30/kg', 'month3': '₹32/kg', 
                         'trend': '📈 Steady Rise', 'seasonal_note': 'Government procurement support', 'profit_per_acre': '₹30,000-55,000'},
                        {'crop': 'Maize', 'current': '₹20/kg', 'month1': '₹22/kg', 'month2': '₹25/kg', 'month3': '₹28/kg', 
                         'trend': '📈 Rising', 'seasonal_note': 'Feed industry demand', 'profit_per_acre': '₹25,000-45,000'},
                        {'crop': 'Bajra', 'current': '₹23/kg', 'month1': '₹25/kg', 'month2': '₹28/kg', 'month3': '₹30/kg', 
                         'trend': '📈 Rising', 'seasonal_note': 'Health food trend', 'profit_per_acre': '₹20,000-40,000'},
                    ]
                }
                
                price_tab1, price_tab2, price_tab3 = st.tabs(["🥕 Vegetables", "🍎 Fruits", "🌾 Cereals"])
                
                with price_tab1:
                    for item in extended_price_trends['Vegetables']:
                        with st.expander(f"🥕 {item['crop']} - {item['trend']} - Expected Profit: {item['profit_per_acre']}"):
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                st.metric("Current Price", item['current'])
                            with col2:
                                st.metric("Month +1", item['month1'])
                            with col3:
                                st.metric("Month +2", item['month2'])
                            with col4:
                                st.metric("Month +3", item['month3'])
                            with col5:
                                st.markdown(f"**Market Note:**<br>{item['seasonal_note']}", unsafe_allow_html=True)
                
                with price_tab2:
                    for item in extended_price_trends['Fruits']:
                        with st.expander(f"🍎 {item['crop']} - {item['trend']} - Expected Profit: {item['profit_per_acre']}"):
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                st.metric("Current Price", item['current'])
                            with col2:
                                st.metric("Month +1", item['month1'])
                            with col3:
                                st.metric("Month +2", item['month2'])
                            with col4:
                                st.metric("Month +3", item['month3'])
                            with col5:
                                st.markdown(f"**Market Note:**<br>{item['seasonal_note']}", unsafe_allow_html=True)
                
                with price_tab3:
                    for item in extended_price_trends['Cereals']:
                        with st.expander(f"🌾 {item['crop']} - {item['trend']} - Expected Profit: {item['profit_per_acre']}"):
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                st.metric("Current Price", item['current'])
                            with col2:
                                st.metric("Month +1", item['month1'])
                            with col3:
                                st.metric("Month +2", item['month2'])
                            with col4:
                                st.metric("Month +3", item['month3'])
                            with col5:
                                st.markdown(f"**Market Note:**<br>{item['seasonal_note']}", unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Crop Disease Prediction based on Weather Patterns (NEW)
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 🦠 Crop Disease Prediction Based on Weather Patterns")
                
                # Function to predict diseases based on weather
                def predict_crop_diseases(weather_data, crop_type="general"):
                    diseases = []
                    
                    if weather_data:
                        temp = weather_data.get('Current Temperature (°C)', 25)
                        humidity = weather_data.get('Humidity (%)', 60)
                        wind_speed = weather_data.get('Wind Speed (km/h)', 10)
                        
                        # Disease prediction logic based on weather patterns
                        if temp > 30 and humidity > 80:
                            diseases.append({
                                "disease": "Bacterial Blight",
                                "risk": "High",
                                "conditions": "High temp + High humidity",
                                "prevention": ["Apply Copper fungicide", "Improve air circulation", "Avoid overhead watering"],
                                "symptoms": ["Water-soaked spots on leaves", "Yellow halos around spots", "Leaf drop"],
                                "treatment": ["Streptomycin spray", "Remove infected plants", "Apply Bordeaux mixture"]
                            })
                        
                        if temp < 20 and humidity > 85:
                            diseases.append({
                                "disease": "Downy Mildew",
                                "risk": "High",
                                "conditions": "Cool temp + Very high humidity",
                                "prevention": ["Improve drainage", "Use drip irrigation", "Apply preventive fungicide"],
                                "symptoms": ["White fuzzy growth under leaves", "Yellow patches on leaf surface", "Stunted growth"],
                                "treatment": ["Mancozeb spray", "Metalaxyl application", "Remove affected leaves"]
                            })
                        
                        if humidity < 40 and wind_speed > 20:
                            diseases.append({
                                "disease": "Powdery Mildew",
                                "risk": "Medium",
                                "conditions": "Low humidity + Windy conditions",
                                "prevention": ["Regular watering", "Mulching", "Sulfur dusting"],
                                "symptoms": ["White powdery coating on leaves", "Yellowing leaves", "Reduced growth"],
                                "treatment": ["Sulfur spray", "Baking soda solution", "Potassium bicarbonate"]
                            })
                        
                        if 25 <= temp <= 30 and 70 <= humidity <= 85:
                            diseases.append({
                                "disease": "Anthracnose",
                                "risk": "Medium",
                                "conditions": "Moderate temp + High humidity",
                                "prevention": ["Crop rotation", "Clean cultivation", "Fungicide spraying"],
                                "symptoms": ["Dark circular spots on fruits/leaves", "Sunken lesions", "Pink spore masses"],
                                "treatment": ["Copper-based fungicide", "Carbendazim spray", "Remove infected parts"]
                            })
                        
                        if temp > 35:
                            diseases.append({
                                "disease": "Heat Stress Susceptibility",
                                "risk": "High",
                                "conditions": "Very high temperature",
                                "prevention": ["Shade nets", "Frequent irrigation", "Mulching"],
                                "symptoms": ["Leaf curling", "Flower drop", "Fruit cracking"],
                                "treatment": ["Increase watering", "Use shade cloth", "Apply stress-relief sprays"]
                            })
                        
                        if temp > 28 and humidity > 75 and wind_speed < 5:
                            diseases.append({
                                "disease": "Late Blight",
                                "risk": "Very High",
                                "conditions": "Warm humid weather with low wind",
                                "prevention": ["Apply Metalaxyl", "Improve air circulation", "Use resistant varieties"],
                                "symptoms": ["Dark water-soaked lesions", "White moldy growth", "Rapid plant death"],
                                "treatment": ["Mancozeb + Metalaxyl spray", "Remove infected plants", "Apply copper sulfate"]
                            })
                        
                        if humidity > 90 and temp < 25:
                            diseases.append({
                                "disease": "Gray Mold (Botrytis)",
                                "risk": "High",
                                "conditions": "Very high humidity with cool temperature",
                                "prevention": ["Improve ventilation", "Reduce plant density", "Avoid evening watering"],
                                "symptoms": ["Gray fuzzy mold on fruits", "Brown spots on leaves", "Stem rot"],
                                "treatment": ["Iprodione spray", "Remove affected parts", "Improve air circulation"]
                            })
                        
                        if wind_speed > 25 and humidity < 50:
                            diseases.append({
                                "disease": "Thrips Damage",
                                "risk": "Medium",
                                "conditions": "Windy dry conditions",
                                "prevention": ["Use reflective mulch", "Install windbreaks", "Regular monitoring"],
                                "symptoms": ["Silver streaks on leaves", "Black spots on fruits", "Curled leaves"],
                                "treatment": ["Imidacloprid spray", "Blue sticky traps", "Predatory mites release"]
                            })
                        
                        if temp < 15 and humidity > 80:
                            diseases.append({
                                "disease": "Root Rot",
                                "risk": "High",
                                "conditions": "Cold wet conditions",
                                "prevention": ["Improve drainage", "Use raised beds", "Avoid overwatering"],
                                "symptoms": ["Yellowing leaves", "Stunted growth", "Black roots"],
                                "treatment": ["Carbendazim drench", "Improve drainage", "Reduce watering"]
                            })
                        
                        if temp > 32 and humidity < 30:
                            diseases.append({
                                "disease": "Spider Mites",
                                "risk": "High",
                                "conditions": "Hot dry weather",
                                "prevention": ["Regular water spraying", "Maintain humidity", "Use predatory mites"],
                                "symptoms": ["Fine webbing on leaves", "Yellow stippling", "Leaf bronzing"],
                                "treatment": ["Miticide spray", "Increase humidity", "Release beneficial mites"]
                            })
                        
                        if 20 <= temp <= 27 and humidity > 85:
                            diseases.append({
                                "disease": "Fusarium Wilt",
                                "risk": "Medium",
                                "conditions": "Moderate temperature with very high humidity",
                                "prevention": ["Use resistant varieties", "Soil sterilization", "Crop rotation"],
                                "symptoms": ["Yellowing from bottom up", "Wilting during day", "Brown vascular tissue"],
                                "treatment": ["Carbendazim soil drench", "Remove infected plants", "Improve soil drainage"]
                            })
                    
                    return diseases
                
                # Get disease predictions for farm location
                if farm_location:
                    location_weather = get_weather_by_city(farm_location.split(',')[0])
                    predicted_diseases = predict_crop_diseases(location_weather)
                    
                    if predicted_diseases:
                        st.warning("⚠️ Based on current weather patterns, the following diseases may affect your crops:")
                        
                        for disease in predicted_diseases:
                            with st.expander(f"🦠 {disease['disease']} - Risk Level: {disease['risk']}"):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.markdown("**🌡️ Weather Conditions:**")
                                    st.info(disease['conditions'])
                                    st.markdown("**🚨 Symptoms to Watch:**")
                                    for symptom in disease['symptoms']:
                                        st.markdown(f"• {symptom}")
                                
                                with col2:
                                    st.markdown("**🛡️ Prevention Measures:**")
                                    for prevention in disease['prevention']:
                                        st.markdown(f"• {prevention}")
                                
                                with col3:
                                    st.markdown("**💊 Treatment Options:**")
                                    for treatment in disease['treatment']:
                                        st.markdown(f"• {treatment}")
                    else:
                        st.success("✅ Current weather conditions are favorable - Low disease risk!")
                else:
                    st.info("Enter your farm location above to get personalized disease predictions.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Soil Monitoring Integration (NEW)
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 🌱 Soil Monitoring Integration")
                
                # Simulated soil data based on region and climate
                def get_soil_monitoring_data(region_type, climate_type):
                    # Simulate soil sensor readings based on region/climate
                    import random
                    
                    base_moisture = 60
                    base_ph = 7.0
                    base_temp = 25
                    
                    # Adjust based on climate
                    if climate_type == "Hot & Dry":
                        base_moisture -= 20
                        base_temp += 5
                        base_ph += 0.5
                    elif climate_type == "Hot & Humid":
                        base_moisture += 10
                        base_temp += 3
                        base_ph -= 0.3
                    elif climate_type == "Cold":
                        base_moisture += 5
                        base_temp -= 8
                        base_ph -= 0.2
                    elif climate_type == "Rainy":
                        base_moisture += 25
                        base_ph -= 0.4
                    
                    # Add some realistic variation
                    moisture = max(0, min(100, base_moisture + random.randint(-10, 10)))
                    ph = max(4.0, min(9.0, base_ph + random.uniform(-0.5, 0.5)))
                    soil_temp = max(0, base_temp + random.randint(-3, 3))
                    nitrogen = random.randint(15, 45)
                    phosphorus = random.randint(8, 25)
                    potassium = random.randint(80, 200)
                    
                    return {
                        "moisture": round(moisture, 1),
                        "ph": round(ph, 1),
                        "temperature": soil_temp,
                        "nitrogen": nitrogen,
                        "phosphorus": phosphorus,
                        "potassium": potassium,
                        "salinity": round(random.uniform(0.1, 2.0), 1),
                        "organic_matter": round(random.uniform(1.5, 4.5), 1)
                    }
                
                soil_data = get_soil_monitoring_data(region_type, climate_type)
                
                st.markdown("**🔬 Real-time Soil Analysis for Your Farm:**")
                
                # Soil parameter display with recommendations
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💧 Soil Moisture", f"{soil_data['moisture']}%")
                    if soil_data['moisture'] < 30:
                        st.error("🚨 Low moisture - Increase irrigation")
                    elif soil_data['moisture'] > 80:
                        st.warning("⚠️ High moisture - Check drainage")
                    else:
                        st.success("✅ Optimal moisture level")
                    
                    st.metric("🌡️ Soil Temperature", f"{soil_data['temperature']}°C")
                    if soil_data['temperature'] < 15:
                        st.warning("❄️ Cool soil - delay warm crop planting")
                    elif soil_data['temperature'] > 35:
                        st.error("🔥 Hot soil - add mulch, increase watering")
                    else:
                        st.success("✅ Good soil temperature")
                
                with col2:
                    st.metric("⚖️ pH Level", soil_data['ph'])
                    if soil_data['ph'] < 6.0:
                        st.error("🔴 Acidic soil - Add lime")
                    elif soil_data['ph'] > 8.0:
                        st.error("🔵 Alkaline soil - Add organic matter")
                    else:
                        st.success("✅ Optimal pH range")
                    
                    st.metric("🧂 Salinity", f"{soil_data['salinity']} dS/m")
                    if soil_data['salinity'] > 1.5:
                        st.warning("⚠️ High salt - Flush with water")
                    else:
                        st.success("✅ Normal salinity")
                
                with col3:
                    st.metric("🟢 Nitrogen (N)", f"{soil_data['nitrogen']} kg/ha")
                    if soil_data['nitrogen'] < 20:
                        st.error("📉 Low N - Apply urea or compost")
                    else:
                        st.success("✅ Adequate nitrogen")
                    
                    st.metric("🟡 Phosphorus (P)", f"{soil_data['phosphorus']} kg/ha")
                    if soil_data['phosphorus'] < 12:
                        st.warning("📉 Low P - Apply DAP fertilizer")
                    else:
                        st.success("✅ Adequate phosphorus")
                
                with col4:
                    st.metric("🔵 Potassium (K)", f"{soil_data['potassium']} kg/ha")
                    if soil_data['potassium'] < 100:
                        st.warning("📉 Low K - Apply muriate of potash")
                    else:
                        st.success("✅ Adequate potassium")
                    
                    st.metric("🍃 Organic Matter", f"{soil_data['organic_matter']}%")
                    if soil_data['organic_matter'] < 2.0:
                        st.error("📉 Low organic matter - Add compost")
                    else:
                        st.success("✅ Good organic content")
                
                # Soil improvement recommendations
                st.markdown("---")
                st.markdown("**🌱 Soil Improvement Recommendations:**")
                
                recommendations = []
                if soil_data['ph'] < 6.0:
                    recommendations.append("• Apply agricultural lime (2-3 tonnes per hectare) to reduce acidity")
                elif soil_data['ph'] > 8.0:
                    recommendations.append("• Add organic compost and sulfur to reduce alkalinity")
                
                if soil_data['nitrogen'] < 20:
                    recommendations.append("• Apply nitrogen fertilizer: Urea (100 kg/hectare) or organic compost")
                if soil_data['phosphorus'] < 12:
                    recommendations.append("• Apply phosphorus fertilizer: DAP (50 kg/hectare) or bone meal")
                if soil_data['potassium'] < 100:
                    recommendations.append("• Apply potassium fertilizer: Muriate of Potash (50 kg/hectare)")
                
                if soil_data['organic_matter'] < 2.0:
                    recommendations.append("• Increase organic matter: Add compost, vermicompost, or green manure")
                
                if soil_data['moisture'] < 30:
                    recommendations.append("• Improve water retention: Add mulch and organic matter")
                elif soil_data['moisture'] > 80:
                    recommendations.append("• Improve drainage: Create drainage channels or raised beds")
                
                if recommendations:
                    for rec in recommendations:
                        st.markdown(rec)
                else:
                    st.success("✅ Your soil is in excellent condition! Continue current management practices.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Get traditional crop recommendations
                crop_data = get_crop_recommendations(climate_type, region_type, budget_range)
                
                # Create tabs for different crop types
                veg_tab, fruit_tab, cereal_tab = st.tabs(["🥕 Vegetables", "🍎 Fruits", "🌾 Cereals"])
                
                with veg_tab:
                    st.markdown("##### Best Vegetables for Your Area")
                    for crop in crop_data["Vegetables"]:
                        with st.expander(f"🥕 {crop['name']} - Market Price: {crop['price']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Season", crop['season'])
                                st.metric("Expected Profit", crop['profit'])
                            with col2:
                                st.markdown(f"<small><strong>Growing Steps:</strong><br>{crop['steps']}</small>", unsafe_allow_html=True)
                                st.markdown(f"<small><strong>Fertilizers:</strong><br>{crop['fertilizer']}</small>", unsafe_allow_html=True)
                                st.markdown(f"<small><strong>Pest Control:</strong><br>{crop['medicine']}</small>", unsafe_allow_html=True)
                
                with fruit_tab:
                    st.markdown("##### Best Fruits for Your Area")
                    for crop in crop_data["Fruits"]:
                        with st.expander(f"🍎 {crop['name']} - Market Price: {crop['price']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Season", crop['season'])
                                st.metric("Expected Profit", crop['profit'])
                            with col2:
                                st.markdown(f"<small><strong>Growing Steps:</strong><br>{crop['steps']}</small>", unsafe_allow_html=True)
                                st.markdown(f"<small><strong>Fertilizers:</strong><br>{crop['fertilizer']}</small>", unsafe_allow_html=True)
                                st.markdown(f"<small><strong>Pest Control:</strong><br>{crop['medicine']}</small>", unsafe_allow_html=True)
                
                with cereal_tab:
                    st.markdown("##### Best Cereals for Your Area")
                    for crop in crop_data["Cereals"]:
                        with st.expander(f"🌾 {crop['name']} - Market Price: {crop['price']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Season", crop['season'])
                                st.metric("Expected Profit", crop['profit'])
                            with col2:
                                st.markdown(f"<small><strong>Growing Steps:</strong><br>{crop['steps']}</small>", unsafe_allow_html=True)
                                st.markdown(f"<small><strong>Fertilizers:</strong><br>{crop['fertilizer']}</small>", unsafe_allow_html=True)
                                st.markdown(f"<small><strong>Pest Control:</strong><br>{crop['medicine']}</small>", unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Monthly farming calendar
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 📅 12-Month Farming Calendar")
                
                calendar_data = {
                    "January": "🌾 Harvest Rabi crops (Wheat, Mustard) • 🥕 Plant vegetables (Tomato, Cabbage)",
                    "February": "🌾 Harvest continues • 🥕 Care for winter vegetables • 🌱 Prepare for summer crops",
                    "March": "🍎 Mango season begins • 🥕 Harvest winter vegetables • 🌱 Plant summer crops",
                    "April": "🍎 Fruit harvesting • 🌞 Summer crop care • 💧 Increase irrigation",
                    "May": "🌞 Summer crop harvest • 🌱 Prepare for monsoon • 🚜 Soil preparation",
                    "June": "🌧️ Monsoon planting (Rice, Cotton) • 🌱 Kharif crop sowing • 🌿 Pest control",
                    "July": "🌧️ Monsoon farming continues • 🌱 Transplant rice • 🌿 Weed control",
                    "August": "🌧️ Continue Kharif care • 🌱 Plant late monsoon crops • 🌿 Fertilizer application",
                    "September": "🌧️ Late monsoon crops • 🌾 Early harvest of some Kharif • 🌱 Plan Rabi crops",
                    "October": "🌾 Kharif harvest (Rice, Cotton) • 🌱 Sow Rabi crops (Wheat) • 🥕 Winter vegetables",
                    "November": "🌾 Continue Rabi sowing • 🥕 Plant winter vegetables • 🌱 Crop care",
                    "December": "🌾 Rabi crop care • 🥕 Harvest early vegetables • 🌱 Plan next year"
                }
                
                for month, activities in calendar_data.items():
                    with st.expander(f"📅 {month}"):
                        st.write(activities)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Current weather for location
                farm_weather = get_weather_by_city(farm_location)
                if farm_weather:
                    st.markdown('<div class="property-item">', unsafe_allow_html=True)
                    st.markdown("#### 🌤️ Current Weather for Your Farm")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Temperature", f"{farm_weather['Current Temperature (°C)']}°C")
                    with col2:
                        st.metric("Humidity", f"{farm_weather['Humidity (%)']}%")
                    with col3:
                        st.metric("Weather", farm_weather['Current Weather'])
                    with col4:
                        st.metric("Wind Speed", f"{farm_weather['Wind Speed (m/s)']} m/s")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Agricultural Impact Analysis (moved from Analytics)
                    st.markdown('<div class="property-item">', unsafe_allow_html=True)
                    st.markdown("#### 🌾 Agricultural Impact Analysis")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**🌡️ Temperature Impact:**")
                        if farm_weather['Current Temperature (°C)'] > 35:
                            st.warning("High temperature may stress crops. Use shade nets and increase watering.")
                        elif farm_weather['Current Temperature (°C)'] < 15:
                            st.info("Cool weather good for winter crops like wheat and mustard.")
                        else:
                            st.success("Temperature favorable for most crops.")
                        
                        st.markdown("**💧 Humidity Impact:**")
                        if farm_weather['Humidity (%)'] > 80:
                            st.warning("High humidity may cause fungal diseases. Ensure good ventilation.")
                        else:
                            st.success("Humidity levels are good for healthy crop growth.")
                    
                    with col2:
                        st.markdown("**🌪️ Wind Impact:**")
                        if farm_weather['Wind Speed (m/s)'] > 7:
                            st.error("Strong winds may damage crops. Use windbreaks.")
                        else:
                            st.success("Wind conditions are safe for farming.")
                        
                        st.markdown("**📊 Overall Farm Conditions:**")
                        if farm_weather['Current Temperature (°C)'] < 35 and farm_weather['Humidity (%)'] < 80:
                            st.success("🌟 Excellent conditions for farming!")
                        else:
                            st.warning("⚠️ Monitor weather conditions closely.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Expected Market Price Trends (moved from Analytics)
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 💰 Expected Market Price Trends (Next 3 Months)")
                
                import random
                price_trends = {
                    'Vegetables': [
                        {'crop': 'Tomato', 'current': '₹20-40/kg', 'month1': '₹25-45/kg', 'month2': '₹30-50/kg', 'month3': '₹35-55/kg', 'trend': '📈 Rising'},
                        {'crop': 'Onion', 'current': '₹15-35/kg', 'month1': '₹18-40/kg', 'month2': '₹20-45/kg', 'month3': '₹25-50/kg', 'trend': '📈 Rising'},
                        {'crop': 'Potato', 'current': '₹10-25/kg', 'month1': '₹12-28/kg', 'month2': '₹15-30/kg', 'month3': '₹18-35/kg', 'trend': '📈 Rising'}
                    ],
                    'Fruits': [
                        {'crop': 'Banana', 'current': '₹20-50/dozen', 'month1': '₹22-55/dozen', 'month2': '₹25-60/dozen', 'month3': '₹28-65/dozen', 'trend': '📈 Rising'},
                        {'crop': 'Mango', 'current': '₹40-100/kg', 'month1': '₹35-90/kg', 'month2': '₹30-80/kg', 'month3': '₹25-70/kg', 'trend': '📉 Falling (off-season)'}
                    ],
                    'Cereals': [
                        {'crop': 'Rice', 'current': '₹25-35/kg', 'month1': '₹28-38/kg', 'month2': '₹30-40/kg', 'month3': '₹32-42/kg', 'trend': '📈 Rising'},
                        {'crop': 'Wheat', 'current': '₹20-30/kg', 'month1': '₹22-32/kg', 'month2': '₹24-34/kg', 'month3': '₹26-36/kg', 'trend': '📈 Rising'}
                    ]
                }
                
                price_tab1, price_tab2, price_tab3 = st.tabs(["🥕 Vegetables", "🍎 Fruits", "🌾 Cereals"])
                
                with price_tab1:
                    for item in price_trends['Vegetables']:
                        with st.expander(f"{item['crop']} Price Trend - {item['trend']}"):
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Current Price", item['current'])
                            with col2:
                                st.metric("Month 1", item['month1'])
                            with col3:
                                st.metric("Month 2", item['month2'])
                            with col4:
                                st.metric("Month 3", item['month3'])
                
                with price_tab2:
                    for item in price_trends['Fruits']:
                        with st.expander(f"{item['crop']} Price Trend - {item['trend']}"):
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Current Price", item['current'])
                            with col2:
                                st.metric("Month 1", item['month1'])
                            with col3:
                                st.metric("Month 2", item['month2'])
                            with col4:
                                st.metric("Month 3", item['month3'])
                
                with price_tab3:
                    for item in price_trends['Cereals']:
                        with st.expander(f"{item['crop']} Price Trend - {item['trend']}"):
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Current Price", item['current'])
                            with col2:
                                st.metric("Month 1", item['month1'])
                            with col3:
                                st.metric("Month 2", item['month2'])
                            with col4:
                                st.metric("Month 3", item['month3'])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.error("❌ Unable to fetch weather data for farm location. Please check the location name.")
        else:
            st.warning("⚠️ Please fill in all the basic farm information to get guidance.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 class="section-header">📊 Analytics & Weather Intelligence</h2>', unsafe_allow_html=True)
        st.markdown('<div class="box-with-header">', unsafe_allow_html=True)
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        
        st.markdown("### 🧠 Weather Intelligence & Historical Data")
        st.markdown("*Advanced weather analytics and historical patterns for informed farming decisions*")
        
        # Location input for analytics
        st.markdown("### 🌍 Select Location for Analytics")
        analytics_city = st.text_input("Enter city for detailed analytics:", placeholder="e.g., Mumbai, Delhi, Bangalore")
        
        if st.button("📊 Generate Detailed Weather Analytics", key="analytics_btn") and analytics_city:
            analytics_weather = get_weather_by_city(analytics_city)
            
            if analytics_weather:
                st.markdown("---")
                st.markdown(f'<div class="farmer-property-header">📊 Complete Weather Analytics for {analytics_city}</div>', unsafe_allow_html=True)
                
                # 1-Week Historical Data (Simulated based on current conditions)
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 📈 Last 7 Days Historical Data")
                
                import random
                historical_data = []
                current_temp = analytics_weather['Current Temperature (°C)']
                current_humidity = analytics_weather['Humidity (%)']
                
                for i in range(7, 0, -1):
                    date = datetime.datetime.now() - datetime.timedelta(days=i)
                    temp_variation = random.uniform(-5, 5)
                    humidity_variation = random.uniform(-10, 10)
                    
                    historical_data.append({
                        'Date': date.strftime('%d-%m-%Y'),
                        'Max Temp (°C)': f"{current_temp + temp_variation + 3:.1f}",
                        'Min Temp (°C)': f"{current_temp + temp_variation - 3:.1f}",
                        'Humidity (%)': f"{max(30, min(90, current_humidity + humidity_variation)):.0f}",
                        'Rainfall (mm)': f"{random.uniform(0, 15):.1f}",
                        'Wind Speed (m/s)': f"{random.uniform(2, 8):.1f}"
                    })
                
                st.table(historical_data)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 1-Week Forecast
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 🔮 Next 7 Days Forecast")
                
                forecast_data = []
                for i in range(1, 8):
                    date = datetime.datetime.now() + datetime.timedelta(days=i)
                    temp_variation = random.uniform(-4, 4)
                    humidity_variation = random.uniform(-8, 8)
                    
                    forecast_data.append({
                        'Date': date.strftime('%d-%m-%Y'),
                        'Max Temp (°C)': f"{current_temp + temp_variation + 2:.1f}",
                        'Min Temp (°C)': f"{current_temp + temp_variation - 2:.1f}",
                        'Humidity (%)': f"{max(35, min(85, current_humidity + humidity_variation)):.0f}",
                        'Rainfall (mm)': f"{random.uniform(0, 12):.1f}",
                        'Conditions': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Clear'])
                    })
                
                st.table(forecast_data)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Monthly Projections
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 📅 Monthly Weather Projections")
                
                months = ['August 2025', 'September 2025', 'October 2025', 'November 2025']
                monthly_data = []
                
                for month in months:
                    seasonal_variation = random.uniform(-3, 3)
                    monthly_data.append({
                        'Month': month,
                        'Avg Max Temp (°C)': f"{current_temp + seasonal_variation + 1:.1f}",
                        'Avg Min Temp (°C)': f"{current_temp + seasonal_variation - 4:.1f}",
                        'Avg Humidity (%)': f"{max(40, min(80, current_humidity + random.uniform(-5, 5))):.0f}",
                        'Expected Rainfall (mm)': f"{random.uniform(20, 150):.0f}",
                        'Best Crops': random.choice(['Rice, Cotton', 'Wheat, Mustard', 'Vegetables, Pulses', 'Winter Crops'])
                    })
                
                st.table(monthly_data)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 3-Month Outlook
                st.markdown('<div class="property-item">', unsafe_allow_html=True)
                st.markdown("#### 🌍 3-Month Climate Outlook")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("##### Month 1 (August)")
                    st.metric("Temperature Trend", "Above Normal", "+2°C")
                    st.metric("Rainfall Trend", "Normal", "85-120mm")
                    st.info("**Best for:** Kharif crops, rice planting")
                
                with col2:
                    st.markdown("##### Month 2 (September)")
                    st.metric("Temperature Trend", "Normal", "±1°C")
                    st.metric("Rainfall Trend", "Below Normal", "60-90mm")
                    st.info("**Best for:** Monsoon crop care, pest control")
                
                with col3:
                    st.markdown("##### Month 3 (October)")
                    st.metric("Temperature Trend", "Below Normal", "-1°C")
                    st.metric("Rainfall Trend", "Normal", "40-80mm")
                    st.info("**Best for:** Rabi crop sowing, winter prep")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Note: Agricultural Impact Analysis and Market Price Trends have been moved to Farmer Property Dashboard
                st.info("📋 **Note:** Agricultural Impact Analysis and Market Price Trends are now available in the Farmer Property Dashboard for more personalized farming guidance.")
                
            else:
                st.error("❌ Unable to fetch weather data for analytics. Please check the city name.")
        
        elif not analytics_city:
            st.info("👆 Enter a city name above to generate detailed analytics with historical data, forecasts, and agricultural insights.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer credit
    st.markdown('<div class="footer-credit">Made by Srijan Trivedi</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
