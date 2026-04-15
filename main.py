

"""
SmartTravel Builder
"""

from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
import json
import os
import random
import hashlib
import secrets
import string

from cities import get_city_options, get_city_data
from hotels import get_hotels_for_city, AIRPORTS_DEPARTURE
from flights import get_flights
from attractions import get_attractions
from weather import get_weather
from filters import get_filter_options

app = FastAPI(title="SmartTravel Builder")
app.mount("/static", StaticFiles(directory="static"), name="static")

USERS = {}
SESSIONS = {}
BOOKINGS = {}
FAVORITES = {}
NOTIFICATIONS = {}
PAYMENTS = {}
REVIEWS = {}
SUPPORT_TICKETS = {}

# Реферальная система
REFERRAL_BONUS = 500
REGISTRATION_BONUS = 300
USER_BALANCES = {}
REFERRAL_CODES = {}
REFERRAL_LINKS = {}

AVATARS = [
    "👤", "👨", "👩", "🧑", "👨‍🦰", "👩‍🦰", "👨‍🦳", "👩‍🦳",
    "🐱", "🐶", "🦊", "🐼", "🐨", "🐸", "🐧", "🦄"
]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_nights(start_date, end_date):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return max(1, (end - start).days)
    except:
        return 7

def get_current_user(session_token: str = None):
    if session_token and session_token in SESSIONS:
        return SESSIONS[session_token]
    return None

def create_session_token(username):
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = username
    return token

def remove_session(token):
    if token in SESSIONS:
        del SESSIONS[token]

def generate_referral_code(username):
    prefix = username[:3].upper()
    suffix = ''.join(random.choices(string.digits, k=4))
    code = f"{prefix}{suffix}"
    while code in REFERRAL_LINKS:
        suffix = ''.join(random.choices(string.digits, k=4))
        code = f"{prefix}{suffix}"
    return code

def get_referral_link(username):
    if username not in REFERRAL_CODES:
        REFERRAL_CODES[username] = generate_referral_code(username)
        code = REFERRAL_CODES[username]
        REFERRAL_LINKS[code] = username
    return f"/register?ref={REFERRAL_CODES[username]}"

def get_map_script(city_data, hotels, attractions):
    lat = city_data["lat"] if city_data else 55.7558
    lng = city_data["lng"] if city_data else 37.6173
    zoom = city_data.get("zoom", 10) if city_data else 10
    
    hotels_data = []
    for i, h in enumerate(hotels[:10]):
        hotels_data.append({
            "name": h["name"],
            "lat": lat + random.uniform(-0.02, 0.02),
            "lng": lng + random.uniform(-0.02, 0.02),
            "price": h["price"],
            "stars": h["stars"]
        })
    
    attractions_data = []
    for a in attractions[:5]:
        attractions_data.append({
            "name": a["name"],
            "lat": lat + random.uniform(-0.03, 0.03),
            "lng": lng + random.uniform(-0.03, 0.03),
            "icon": a["icon"],
            "price": a["price"]
        })
    
    hotels_json = json.dumps(hotels_data, ensure_ascii=False)
    attractions_json = json.dumps(attractions_data, ensure_ascii=False)
    
    return f'''
    <div id="map" style="height: 500px; width: 100%; border-radius: 16px; margin-bottom: 20px;"></div>
    <script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU"></script>
    <script>
        let hotelsData = {hotels_json};
        let attractionsData = {attractions_json};
        
        ymaps.ready(init);
        
        function init() {{
            const map = new ymaps.Map("map", {{
                center: [{lat}, {lng}],
                zoom: {zoom},
                controls: ["zoomControl", "fullscreenControl"]
            }});
            
            hotelsData.forEach(hotel => {{
                const placemark = new ymaps.Placemark(
                    [hotel.lat, hotel.lng],
                    {{
                        balloonContentHeader: `<b>${{hotel.name}}</b>`,
                        balloonContentBody: `⭐ ${{hotel.stars}} звезд<br>💰 ${{hotel.price.toLocaleString()}} ₽/ночь`,
                        hintContent: hotel.name
                    }},
                    {{ preset: "islands#blueHotelIcon" }}
                );
                map.geoObjects.add(placemark);
            }});
            
            attractionsData.forEach(attr => {{
                const placemark = new ymaps.Placemark(
                    [attr.lat, attr.lng],
                    {{
                        balloonContentHeader: `<b>${{attr.icon}} ${{attr.name}}</b>`,
                        balloonContentBody: `💰 ${{attr.price.toLocaleString()}} ₽`,
                        hintContent: attr.name
                    }},
                    {{ preset: "islands#greenTourismIcon" }}
                );
                map.geoObjects.add(placemark);
            }});
        }}
    </script>
    '''

# ============= ГЛАВНАЯ СТРАНИЦА =============
CITY_OPTIONS = get_city_options()
AIRPORTS_OPTIONS = ''.join([f'<option value="{a["code"]}">{a["name"]}</option>' for a in AIRPORTS_DEPARTURE])
FILTERS_OPTIONS = get_filter_options()

MAIN_PAGE = f'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>SmartTravel Builder</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #10b981;
            --dark: #0f172a;
            --gray: #64748b;
            --gray-light: #e2e8f0;
            --white: #ffffff;
            --bg-light: #f8fafc;
        }}
        body.dark-theme {{
            --primary: #3b82f6;
            --dark: #f1f5f9;
            --gray: #94a3b8;
            --gray-light: #334155;
            --white: #1e293b;
            --bg-light: #0f172a;
        }}
        body.dark-theme select, body.dark-theme option {{
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg-light);
            color: var(--dark);
            transition: all 0.3s;
        }}
        .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
        .header {{ text-align: center; padding: 60px 0 40px; }}
        .header h1 {{ font-size: 3rem; font-weight: 700; margin-bottom: 16px; }}
        .header h1 span {{ background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }}
        .header p {{ font-size: 1.125rem; color: var(--gray); }}
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--white);
            padding: 12px 28px;
            border-radius: 80px;
            margin: 20px 0;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            border: 1px solid var(--gray-light);
        }}
        .logo {{ font-size: 1.25rem; font-weight: 600; color: var(--dark); }}
        .logo span {{ color: var(--primary); }}
        .nav-links {{ display: flex; gap: 24px; align-items: center; flex-wrap: wrap; }}
        .nav-links a {{ text-decoration: none; color: var(--gray); font-weight: 500; font-size: 0.875rem; }}
        .nav-links a:hover {{ color: var(--primary); }}
        .theme-btn, .btn-login, .btn-logout {{ padding: 8px 16px; border-radius: 40px; cursor: pointer; font-size: 0.875rem; font-weight: 500; transition: all 0.2s; }}
        .theme-btn {{ background: var(--gray-light); border: none; color: var(--dark); }}
        .theme-btn:hover {{ background: var(--primary); color: white; }}
        .btn-login {{ background: var(--primary); color: white; text-decoration: none; }}
        .btn-login:hover {{ background: var(--primary-dark); }}
        .btn-logout {{ background: var(--gray-light); color: var(--dark); text-decoration: none; }}
        .tabs {{ display: flex; gap: 12px; justify-content: center; margin-bottom: 32px; flex-wrap: wrap; }}
        .tab-btn {{
            padding: 10px 28px;
            background: var(--white);
            border: 1px solid var(--gray-light);
            border-radius: 60px;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--gray);
        }}
        .tab-btn:hover {{ border-color: var(--primary); color: var(--primary); }}
        .tab-btn.active {{ background: var(--primary); border-color: var(--primary); color: white; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .search-card, .advanced-card {{
            background: var(--white);
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
            border: 1px solid var(--gray-light);
        }}
        .search-header h2 {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 8px; }}
        .search-header p {{ color: var(--gray); margin-bottom: 28px; font-size: 0.875rem; }}
        .search-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px; }}
        .search-field {{ display: flex; flex-direction: column; }}
        .search-field label {{ font-size: 0.75rem; font-weight: 600; margin-bottom: 6px; color: var(--gray); text-transform: uppercase; letter-spacing: 0.5px; }}
        .search-field input, .search-field select {{ padding: 12px 0; border: none; border-bottom: 1.5px solid var(--gray-light); background: transparent; font-size: 0.875rem; outline: none; color: var(--dark); }}
        .search-field input:focus, .search-field select:focus {{ border-bottom-color: var(--primary); }}
        .search-row {{ display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 24px; }}
        .search-field.half {{ flex: 1; min-width: 140px; }}
        .search-btn, .btn-submit {{
            background: var(--primary);
            color: white;
            padding: 14px 32px;
            border: none;
            border-radius: 60px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
        }}
        .search-btn:hover, .btn-submit:hover {{ background: var(--primary-dark); }}
        .interests-section {{ margin-top: 28px; padding-top: 28px; border-top: 1px solid var(--gray-light); }}
        .interests-section label {{ font-weight: 600; margin-bottom: 12px; display: block; font-size: 0.875rem; color: var(--gray); text-transform: uppercase; letter-spacing: 0.5px; }}
        .interests-buttons {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .interest-btn {{ padding: 8px 20px; background: var(--gray-light); border: none; border-radius: 60px; cursor: pointer; font-size: 0.8rem; font-weight: 500; color: var(--dark); }}
        .interest-btn.active {{ background: var(--primary); color: white; }}
        .popular-section {{ margin-top: 40px; padding-top: 40px; border-top: 1px solid var(--gray-light); }}
        .section-title {{ font-size: 1.25rem; font-weight: 600; margin-bottom: 8px; }}
        .section-subtitle {{ color: var(--gray); margin-bottom: 24px; font-size: 0.875rem; }}
        .destinations-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .destination-card {{
            background: var(--white);
            border-radius: 16px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid var(--gray-light);
            text-align: left;
            width: 100%;
            font-family: inherit;
        }}
        .destination-card:hover {{
            transform: translateY(-2px);
            border-color: var(--primary);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .destination-name {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--dark);
        }}
        .destination-attractions {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
        }}
        .attraction-tag {{
            background: var(--gray-light);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 500;
            color: var(--primary);
        }}
        .destination-price {{
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--secondary);
        }}
        .near-card {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            border-radius: 20px;
            padding: 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 40px;
            color: white;
        }}
        .near-card button {{ background: white; color: var(--primary); border: none; padding: 10px 28px; border-radius: 40px; cursor: pointer; }}
        .form-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 28px; }}
        .form-group {{ display: flex; flex-direction: column; }}
        .form-group label {{ font-weight: 600; margin-bottom: 6px; color: var(--gray); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; }}
        .form-group input, .form-group select {{ padding: 10px 12px; border: 1px solid var(--gray-light); border-radius: 10px; background: var(--white); font-size: 0.875rem; outline: none; color: var(--dark); }}
        .form-group input:focus, .form-group select:focus {{ border-color: var(--primary); }}
        .filter-group {{ margin-bottom: 20px; }}
        .filter-group label {{ display: block; font-weight: 600; margin-bottom: 10px; color: var(--gray); font-size: 0.75rem; text-transform: uppercase; }}
        .filter-buttons {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .filter-btn {{ padding: 6px 14px; background: var(--gray-light); border: none; border-radius: 60px; cursor: pointer; font-size: 0.75rem; color: var(--dark); }}
        .filter-btn.active {{ background: var(--primary); color: white; }}
        .active-filters {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; padding: 12px; background: var(--gray-light); border-radius: 50px; }}
        .active-filter {{ background: var(--white); padding: 4px 12px; border-radius: 30px; font-size: 0.75rem; display: flex; align-items: center; gap: 8px; }}
        .remove-filter {{ cursor: pointer; color: #ef4444; font-weight: bold; }}
        
        /* Чат поддержки с пульсацией */
        .chat-button {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 56px;
            height: 56px;
            border-radius: 28px;
            background: var(--primary);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            z-index: 1000;
            animation: pulse 2s infinite;
        }}
        .chat-button:hover {{
            transform: scale(1.05);
            background: var(--primary-dark);
            animation: none;
        }}
        @keyframes pulse {{
            0% {{
                box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7);
            }}
            70% {{
                box-shadow: 0 0 0 12px rgba(37, 99, 235, 0);
            }}
            100% {{
                box-shadow: 0 0 0 0 rgba(37, 99, 235, 0);
            }}
        }}
        body.dark-theme .chat-button {{
            background: #3b82f6;
        }}
        body.dark-theme .chat-button:hover {{
            background: #2563eb;
        }}
        .chat-modal {{
            display: none;
            position: fixed;
            bottom: 90px;
            right: 24px;
            width: 350px;
            max-width: calc(100vw - 48px);
            background: var(--white);
            border-radius: 16px;
            box-shadow: 0 20px 35px -8px rgba(0,0,0,0.2);
            z-index: 1001;
            overflow: hidden;
            border: 1px solid var(--gray-light);
        }}
        body.dark-theme .chat-modal {{
            background: #1e1e2e;
            border-color: #2d2d44;
        }}
        .chat-modal.active {{
            display: block;
        }}
        .chat-header {{
            padding: 16px;
            background: var(--primary);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .chat-close {{
            background: none;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }}
        .chat-messages {{
            height: 300px;
            overflow-y: auto;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .chat-message {{
            padding: 10px 12px;
            border-radius: 12px;
            max-width: 85%;
            word-wrap: break-word;
            font-size: 0.875rem;
        }}
        .chat-message.user {{
            background: var(--primary);
            color: white;
            align-self: flex-end;
        }}
        .chat-message.support {{
            background: var(--gray-light);
            color: var(--dark);
            align-self: flex-start;
        }}
        .chat-input-area {{
            padding: 12px;
            border-top: 1px solid var(--gray-light);
            display: flex;
            gap: 8px;
        }}
        .chat-input {{
            flex: 1;
            padding: 10px 12px;
            border: 1px solid var(--gray-light);
            border-radius: 24px;
            background: var(--white);
            color: var(--dark);
            font-family: inherit;
            font-size: 0.875rem;
        }}
        body.dark-theme .chat-input {{
            background: #1e1e2e;
            border-color: #3f3f4f;
            color: #f1f5f9;
        }}
        .chat-send {{
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 24px;
            padding: 8px 16px;
            cursor: pointer;
            font-size: 0.75rem;
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 0 16px; }}
            .header {{ padding: 30px 0 20px; }}
            .header h1 {{ font-size: 1.8rem; }}
            .navbar {{ flex-direction: column; padding: 12px 20px; border-radius: 24px; }}
            .nav-links {{ justify-content: center; gap: 12px; }}
            .tab-btn {{ padding: 8px 16px; font-size: 0.75rem; }}
            .search-card, .advanced-card {{ padding: 20px; }}
            .search-grid {{ grid-template-columns: 1fr; }}
            .search-row {{ flex-direction: column; }}
            .destinations-grid {{ grid-template-columns: 1fr; }}
            .near-card {{ flex-direction: column; text-align: center; }}
            .form-grid {{ grid-template-columns: 1fr; }}
            .chat-modal {{ width: 300px; }}
        }}
        @media (max-width: 480px) {{
            .header h1 {{ font-size: 1.5rem; }}
            .tab-btn {{ padding: 6px 12px; font-size: 0.7rem; }}
            .chat-modal {{ width: calc(100vw - 40px); right: 20px; bottom: 80px; }}
        }}
    </style>
</head>
<body>
    <div class="content-wrapper">
        <div class="container">
            <div class="navbar">
                <div class="logo"><span>✈️</span> SmartTravel</div>
                <div class="nav-links">
                    <a href="/">Главная</a>
                    <a href="/profile">Бронирования</a>
                    <button class="theme-btn" onclick="toggleTheme()" id="themeToggleBtn">Тёмная тема</button>
                    <div class="user-info" id="userInfo">
                        <span id="userName"></span>
                        <a href="/login" id="loginLink" class="btn-login">Войти</a>
                        <a href="/logout" id="logoutLink" class="btn-logout" style="display:none;">Выйти</a>
                    </div>
                </div>
            </div>
            <div class="header">
                <h1>Путешествуйте с <span>умом</span></h1>
                <p>Найдите идеальный тур за считанные минуты</p>
            </div>
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('simple')">Быстрый поиск</button>
                <button class="tab-btn" onclick="switchTab('advanced')">Расширенный поиск</button>
            </div>
            <div id="simpleTab" class="tab-content active">
                <div class="search-card">
                    <div class="search-header">
                        <h2>Начните планирование</h2>
                        <p>Заполните форму и получите лучшие предложения</p>
                    </div>
                    <form action="/search" method="POST" id="searchForm">
                        <div class="search-grid">
                            <div class="search-field">
                                <label>Город назначения</label>
                                <select name="destination" id="destinationSelect" required>
                                    <option value="">Выберите город</option>
                                    {CITY_OPTIONS}
                                </select>
                            </div>
                            <div class="search-field">
                                <label>Аэропорт вылета</label>
                                <select name="departure_airport">
                                    <option value="">Любой аэропорт</option>
                                    {AIRPORTS_OPTIONS}
                                </select>
                            </div>
                        </div>
                        <div class="search-row">
                            <div class="search-field half">
                                <label>Дата заезда</label>
                                <input type="date" name="start_date" id="startDate" required>
                            </div>
                            <div class="search-field half">
                                <label>Дата выезда</label>
                                <input type="date" name="end_date" id="endDate" required>
                            </div>
                            <div class="search-field half">
                                <label>Взрослых</label>
                                <input type="number" name="adults" value="2" min="1">
                            </div>
                            <div class="search-field half">
                                <label>Детей</label>
                                <input type="number" name="children" value="0" min="0">
                            </div>
                        </div>
                        <div class="search-row">
                            <div class="search-field half">
                                <label>Бюджет (₽)</label>
                                <input type="number" name="budget" placeholder="Не обязательно">
                            </div>
                            <div class="search-field half">
                                <label>Звездность</label>
                                <select name="hotel_stars">
                                    <option value="">Любая</option>
                                    <option value="5">5 звезд</option>
                                    <option value="4">4 звезды</option>
                                    <option value="3">3 звезды</option>
                                </select>
                            </div>
                            <div class="search-field half">
                                <label>Ваше имя</label>
                                <input type="text" name="user_name">
                            </div>
                            <div class="search-field half">
                                <label>Email</label>
                                <input type="email" name="user_email">
                            </div>
                        </div>
                        <button type="submit" class="search-btn">Найти отели</button>
                    </form>
                    <div class="interests-section">
                        <label>Ваши интересы</label>
                        <div class="interests-buttons" id="interestsButtons">
                            <button type="button" class="interest-btn" data-interest="пляж">Пляж</button>
                            <button type="button" class="interest-btn" data-interest="культура">Культура</button>
                            <button type="button" class="interest-btn" data-interest="приключения">Приключения</button>
                            <button type="button" class="interest-btn" data-interest="гастрономия">Гастрономия</button>
                            <button type="button" class="interest-btn" data-interest="шопинг">Шопинг</button>
                            <button type="button" class="interest-btn" data-interest="семья">Семья</button>
                        </div>
                        <input type="hidden" name="interests" id="interests" value="[]">
                    </div>
                    
                    <div class="popular-section">
                        <h3 class="section-title">Популярные направления</h3>
                        <p class="section-subtitle">Выберите одно из самых востребованных мест</p>
                        <div class="destinations-grid">
                            <button class="destination-card" onclick="searchCity('Сочи')">
                                <div class="destination-name">Сочи</div>
                                <div class="destination-attractions">
                                    <span class="attraction-tag">Олимпийский парк</span>
                                    <span class="attraction-tag">Красная Поляна</span>
                                </div>
                                <div class="destination-price">от 3 500 ₽</div>
                            </button>
                            <button class="destination-card" onclick="searchCity('Стамбул')">
                                <div class="destination-name">Стамбул</div>
                                <div class="destination-attractions">
                                    <span class="attraction-tag">Айя-София</span>
                                    <span class="attraction-tag">Босфор</span>
                                </div>
                                <div class="destination-price">от 12 500 ₽</div>
                            </button>
                            <button class="destination-card" onclick="searchCity('Дубай')">
                                <div class="destination-name">Дубай</div>
                                <div class="destination-attractions">
                                    <span class="attraction-tag">Бурдж Халифа</span>
                                    <span class="attraction-tag">Пальма Джумейра</span>
                                </div>
                                <div class="destination-price">от 18 500 ₽</div>
                            </button>
                            <button class="destination-card" onclick="searchCity('Санкт-Петербург')">
                                <div class="destination-name">Санкт-Петербург</div>
                                <div class="destination-attractions">
                                    <span class="attraction-tag">Эрмитаж</span>
                                    <span class="attraction-tag">Невский проспект</span>
                                </div>
                                <div class="destination-price">от 4 200 ₽</div>
                            </button>
                            <button class="destination-card" onclick="searchCity('Пхукет')">
                                <div class="destination-name">Пхукет</div>
                                <div class="destination-attractions">
                                    <span class="attraction-tag">Пхи Пхи</span>
                                    <span class="attraction-tag">Большой Будда</span>
                                </div>
                                <div class="destination-price">от 32 500 ₽</div>
                            </button>
                            <button class="destination-card" onclick="searchCity('Бангкок')">
                                <div class="destination-name">Бангкок</div>
                                <div class="destination-attractions">
                                    <span class="attraction-tag">Королевский дворец</span>
                                    <span class="attraction-tag">Плавучие рынки</span>
                                </div>
                                <div class="destination-price">от 28 500 ₽</div>
                            </button>
                        </div>
                    </div>
                    
                    <div class="near-card">
                        <div><div>Рядом с вами</div><div>Москва — откройте новые места в столице</div></div>
                        <button id="nearbyMapBtn">Исследовать</button>
                    </div>
                    
                    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--gray-light);">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; margin-bottom: 20px;">
                            <h3 style="font-size: 1.25rem; font-weight: 600;">Горячие билеты</h3>
                            <span style="font-size: 0.75rem; color: var(--gray);">Скоро разберут</span>
                        </div>
                        <div style="background: linear-gradient(135deg, #fef5e8 0%, #fae8d8 100%); border-radius: 24px; padding: 20px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 20px;">
                            <div style="display: flex; align-items: center; gap: 24px; flex-wrap: wrap;">
                                <div style="background: #e85d4a; border-radius: 40px; padding: 8px 20px; color: white; font-weight: 700; font-size: 1rem;">Суперскидка 62%</div>
                                <div style="display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 1.8rem; font-weight: 800; color: #e85d4a;">2 180 ₽</span><span style="font-size: 1rem; color: #999; text-decoration: line-through;">5 760 ₽</span></div>
                            </div>
                            <div style="background: white; border-radius: 20px; padding: 12px 20px;"><div style="font-weight: 700; font-size: 1rem;">Москва — Сочи</div><div style="font-size: 0.8rem; color: var(--gray);">10 апр, пт • 11:00 — 14:55 • 4ч в пути / Прямой</div></div>
                            <a href="#" onclick="searchCity('Сочи'); return false;" style="background: #e85d4a; color: white; padding: 12px 28px; border-radius: 40px; text-decoration: none; font-weight: 600; white-space: nowrap;">Больше жарких билетов →</a>
                        </div>
                    </div>
                </div>
            </div>
            <div id="advancedTab" class="tab-content">
                <div class="advanced-card">
                    <h2 style="margin-bottom: 24px; font-size: 1.25rem; font-weight: 600;">Расширенный поиск</h2>
                    <form action="/search" method="POST" id="advancedForm">
                        <div class="form-grid">
                            <div class="form-group"><label>Город назначения</label><select name="destination" required><option value="">Выберите город</option>{CITY_OPTIONS}</select></div>
                            <div class="form-group"><label>Аэропорт вылета</label><select name="departure_airport"><option value="">Любой аэропорт</option>{AIRPORTS_OPTIONS}</select></div>
                            <div class="form-group"><label>Дата заезда</label><input type="date" name="start_date" required></div>
                            <div class="form-group"><label>Дата выезда</label><input type="date" name="end_date" required></div>
                            <div class="form-group"><label>Взрослых</label><input type="number" name="adults" value="2" min="1"></div>
                            <div class="form-group"><label>Детей</label><input type="number" name="children" value="0" min="0"></div>
                            <div class="form-group"><label>Бюджет (₽)</label><input type="number" name="budget" placeholder="Не обязательно"></div>
                            <div class="form-group"><label>Звездность</label><select name="hotel_stars"><option value="">Любая</option><option value="5">5 звезд</option><option value="4">4 звезды</option><option value="3">3 звезды</option></select></div>
                            <div class="form-group">
                                <label>Интересы</label>
                                <div class="interests-buttons" id="interestsButtons2">
                                    <button type="button" class="interest-btn" data-interest="пляж">Пляж</button>
                                    <button type="button" class="interest-btn" data-interest="культура">Культура</button>
                                    <button type="button" class="interest-btn" data-interest="приключения">Приключения</button>
                                    <button type="button" class="interest-btn" data-interest="гастрономия">Гастрономия</button>
                                    <button type="button" class="interest-btn" data-interest="шопинг">Шопинг</button>
                                    <button type="button" class="interest-btn" data-interest="семья">Семья</button>
                                </div>
                                <input type="hidden" name="interests" id="interests2" value="[]">
                            </div>
                            <div class="form-group"><label>Ваше имя</label><input type="text" name="user_name"></div>
                            <div class="form-group"><label>Email</label><input type="email" name="user_email"></div>
                        </div>
                        <div class="filter-group">
                            <label>Дополнительные фильтры</label>
                            <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;"><button type="button" id="clearFilters" style="background: none; border: none; color: var(--primary); font-size: 0.75rem; cursor: pointer;">Сбросить все</button></div>
                            {FILTERS_OPTIONS}
                            <div id="activeFilters" class="active-filters" style="display: none;"></div>
                            <input type="hidden" name="filters" id="filters" value="{{}}">
                        </div>
                        <button type="submit" class="btn-submit">Найти варианты</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Кнопка чата поддержки с пульсацией -->
    <button class="chat-button" onclick="toggleChat()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
    </button>
    
    <!-- Модальное окно чата -->
    <div id="chatModal" class="chat-modal">
        <div class="chat-header">
            <span>Поддержка</span>
            <button class="chat-close" onclick="toggleChat()">✕</button>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="chat-message support">Здравствуйте! Чем могу помочь?</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="chatInput" class="chat-input" placeholder="Напишите сообщение...">
            <button class="chat-send" onclick="sendSupportMessage()">Отправить</button>
        </div>
    </div>

    <script>
        function toggleTheme() {{
            document.body.classList.toggle('dark-theme');
            localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
            const btn = document.getElementById('themeToggleBtn');
            if (btn) btn.innerHTML = document.body.classList.contains('dark-theme') ? 'Светлая тема' : 'Тёмная тема';
        }}
        if (localStorage.getItem('theme') === 'dark') document.body.classList.add('dark-theme');
        
        function switchTab(tab) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            if (tab === 'simple') {{
                document.querySelector('.tab-btn:first-child').classList.add('active');
                document.getElementById('simpleTab').classList.add('active');
            }} else {{
                document.querySelector('.tab-btn:last-child').classList.add('active');
                document.getElementById('advancedTab').classList.add('active');
            }}
        }}
        
        let interests = [];
        document.querySelectorAll('#interestsButtons .interest-btn, #interestsButtons2 .interest-btn').forEach(btn => {{
            btn.onclick = (e) => {{
                e.preventDefault();
                const val = btn.dataset.interest;
                if (interests.includes(val)) {{
                    interests = interests.filter(i => i !== val);
                    btn.classList.remove('active');
                }} else {{
                    interests.push(val);
                    btn.classList.add('active');
                }}
                document.getElementById('interests').value = JSON.stringify(interests);
                document.getElementById('interests2').value = JSON.stringify(interests);
            }};
        }});
        
        const today = new Date();
        const nextWeek = new Date(today);
        nextWeek.setDate(today.getDate() + 7);
        const startDateInput = document.getElementById('startDate');
        const endDateInput = document.getElementById('endDate');
        if (startDateInput) {{
            startDateInput.value = today.toISOString().split('T')[0];
            startDateInput.min = today.toISOString().split('T')[0];
            startDateInput.onchange = function() {{ if (endDateInput) endDateInput.min = this.value; }};
        }}
        if (endDateInput) {{
            endDateInput.value = nextWeek.toISOString().split('T')[0];
            endDateInput.min = today.toISOString().split('T')[0];
        }}
        
        let activeFilters = {{ meal_type: [], distance: [], amenity: [], rating: [], holiday: [] }};
        function updateActiveFiltersDisplay() {{
            const container = document.getElementById('activeFilters');
            let hasFilters = false;
            for (var key in activeFilters) if (activeFilters[key].length > 0) hasFilters = true;
            if (!hasFilters) {{ container.style.display = 'none'; return; }}
            container.style.display = 'flex';
            let html = '';
            const filterNames = {{
                meal_type: {{ "RO": "Без питания", "BB": "Завтрак", "HB": "Полупансион", "FB": "Полный пансион", "AI": "Всё включено" }},
                distance: {{ "0-100": "до 100 м", "100-500": "100-500 м", "500-1000": "500-1000 м", "1000+": "более 1 км" }},
                amenity: {{ "pool": "Бассейн", "spa": "СПА", "wifi": "Wi-Fi", "parking": "Парковка", "transfer": "Трансфер", "kids_club": "Детский клуб" }},
                rating: {{ "4.5": "Рейтинг 4.5+", "4.0": "Рейтинг 4.0+", "3.5": "Рейтинг 3.5+" }},
                holiday: {{ "family": "Семейный", "romantic": "Романтический", "youth": "Молодёжный", "sports": "Спортивный", "spa": "СПА-отдых" }}
            }};
            for (var type in activeFilters) {{
                for (var j = 0; j < activeFilters[type].length; j++) {{
                    var value = activeFilters[type][j];
                    var name = filterNames[type] ? filterNames[type][value] : value;
                    html += '<div class="active-filter">' + name + ' <span class="remove-filter" onclick="removeFilter(\\'' + type + '\\', \\'' + value + '\\')">✕</span></div>';
                }}
            }}
            container.innerHTML = html;
            document.getElementById('filters').value = JSON.stringify(activeFilters);
        }}
        function removeFilter(type, value) {{
            activeFilters[type] = activeFilters[type].filter(v => v !== value);
            document.querySelectorAll('.filter-btn[data-filter="' + type + '"][data-value="' + value + '"]').forEach(btn => btn.classList.remove('active'));
            updateActiveFiltersDisplay();
        }}
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                var filterType = this.dataset.filter;
                var filterValue = this.dataset.value;
                if (activeFilters[filterType].includes(filterValue)) {{
                    activeFilters[filterType] = activeFilters[filterType].filter(v => v !== filterValue);
                    this.classList.remove('active');
                }} else {{
                    activeFilters[filterType].push(filterValue);
                    this.classList.add('active');
                }}
                updateActiveFiltersDisplay();
            }});
        }});
        document.getElementById('clearFilters')?.addEventListener('click', () => {{
            activeFilters = {{ meal_type: [], distance: [], amenity: [], rating: [], holiday: [] }};
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            updateActiveFiltersDisplay();
        }});
        
        fetch('/api/check_auth').then(res => res.json()).then(data => {{
            if (data.logged_in) {{
                document.getElementById('userName').innerText = data.username;
                document.getElementById('loginLink').style.display = 'none';
                document.getElementById('logoutLink').style.display = 'inline-block';
            }}
        }});
        
        function searchCity(city) {{
            const destinationSelect = document.getElementById('destinationSelect');
            if (destinationSelect) destinationSelect.value = city;
            const searchForm = document.getElementById('searchForm');
            if (searchForm) searchForm.submit();
        }}
        
        const nearbyBtn = document.getElementById('nearbyMapBtn');
        if (nearbyBtn) {{
            nearbyBtn.addEventListener('click', function() {{
                window.open('https://yandex.ru/maps/?text=%D0%B4%D0%BE%D1%81%D1%82%D0%BE%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%87%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B&ll=37.6173,55.7558&z=12', '_blank');
            }});
        }}
        
        // Чат поддержки
        function toggleChat() {{
            document.getElementById('chatModal').classList.toggle('active');
        }}
        
        function sendSupportMessage() {{
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;
            
            const messagesContainer = document.getElementById('chatMessages');
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'chat-message user';
            userMessageDiv.textContent = message;
            messagesContainer.appendChild(userMessageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            input.value = '';
            
            fetch('/api/support_message', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: message }})
            }})
            .then(res => res.json())
            .then(data => {{
                const supportMessageDiv = document.createElement('div');
                supportMessageDiv.className = 'chat-message support';
                supportMessageDiv.textContent = data.reply;
                messagesContainer.appendChild(supportMessageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }});
        }}
        
        document.getElementById('chatInput')?.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') sendSupportMessage();
        }});
    </script>
</body>
</html>
'''

@app.get("/")
async def home():
    return HTMLResponse(content=MAIN_PAGE)

@app.get("/api/check_auth")
async def check_auth(session: str = Cookie(None)):
    username = get_current_user(session)
    return {"logged_in": username is not None, "username": username or ""}

@app.post("/api/support_message")
async def support_message(data: dict, session: str = Cookie(None)):
    """Автоответчик для чата поддержки"""
    message = data.get("message", "")
    username = get_current_user(session) or "Гость"
    
    message_lower = message.lower()
    if "привет" in message_lower or "здравствуй" in message_lower:
        reply = f"Здравствуйте, {username}! Чем могу помочь?"
    elif "отель" in message_lower or "отели" in message_lower:
        reply = "Вы можете найти отели через форму поиска на главной странице. Укажите город, даты и нажмите 'Найти отели'."
    elif "билет" in message_lower or "авиабилет" in message_lower:
        reply = "Авиабилеты доступны при поиске тура. Выберите направление и даты, и мы покажем все варианты."
    elif "экскурсия" in message_lower or "экскурсии" in message_lower:
        reply = "В результатах поиска есть вкладка 'Экскурсии' с самыми популярными местами и фотографиями."
    elif "оплата" in message_lower or "платеж" in message_lower:
        reply = "Оплата происходит в демо-режиме. Вы можете выбрать карту или СБП. Реальные деньги не списываются."
    elif "скидка" in message_lower:
        reply = "У нас есть горячие билеты со скидкой до 62%! Посмотрите блок 'Горячие билеты' на главной странице."
    elif "спасибо" in message_lower:
        reply = "Пожалуйста! Обращайтесь, если понадобится помощь."
    else:
        reply = "Спасибо за обращение! Наш специалист свяжется с вами в ближайшее время. А пока вы можете найти ответ в разделе 'Популярные направления'."
    
    return {"reply": reply}


@app.post("/search")
async def search(
    destination: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    adults: int = Form(2),
    children: int = Form(0),
    budget: float = Form(None),
    hotel_stars: int = Form(None),
    departure_airport: str = Form(""),
    filters: str = Form("{}"),
    session: str = Cookie(None)
):
    nights = calculate_nights(start_date, end_date)
    city_data = get_city_data(destination)
    hotels = get_hotels_for_city(destination)
    
    if hotel_stars:
        hotels = [h for h in hotels if h["stars"] == hotel_stars]
    if budget:
        max_price = budget / nights * 0.6
        hotels = [h for h in hotels if h["price"] <= max_price] or hotels
    
    distance_km = city_data.get("distance_km", 2000) if city_data else 2000
    flights_there, flights_back = get_flights(distance_km)
    attractions = get_attractions(destination)
    arrival_airport = city_data["airport"] if city_data else "Аэропорт назначения"
    weather = get_weather(destination, start_date)
    
    discount_info = {"Сочи": 62}
    
    hotels_html = ""
    for i, hotel in enumerate(hotels[:10]):
        hotel_total = hotel["price"] * nights
        stars_display = "★" * hotel["stars"] + "☆" * (5 - hotel["stars"])
        hotel_image = hotel.get("image", "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500")
        
        hotel_reviews = REVIEWS.get(str(i), [])
        avg_rating = 0
        if hotel_reviews:
            avg_rating = sum(r["rating"] for r in hotel_reviews) / len(hotel_reviews)
        
        reviews_html = ""
        if hotel_reviews:
            reviews_html = '<div class="hotel-reviews">'
            for review in hotel_reviews[:3]:
                stars_review = "★" * review["rating"] + "☆" * (5 - review["rating"])
                reviews_html += f'''
                <div class="review-item">
                    <div class="review-header">
                        <span class="review-author">{review["username"]}</span>
                        <span class="review-stars">{stars_review}</span>
                        <span class="review-date">{review["date"]}</span>
                    </div>
                    <div class="review-text">{review["text"]}</div>
                </div>'''
            if len(hotel_reviews) > 3:
                reviews_html += f'<div class="review-more" onclick="showAllReviews({i})">Показать все ({len(hotel_reviews)}) отзывы →</div>'
            reviews_html += '</div>'
        
        hotels_html += f"""
        <div class="hotel-card" onclick="selectHotel({i}, {hotel_total}, '{hotel['name'].replace("'", "\\'")}', {hotel['stars']})">
            <div class="hotel-image"><img src="{hotel_image}" style="width:100%; height:200px; object-fit:cover;"></div>
            <div class="hotel-info">
                <div class="hotel-name">{hotel['name']}</div>
                <div class="hotel-stars">{stars_display}</div>
                <div class="hotel-desc">{hotel['desc']}</div>
                <div class="hotel-price">{hotel_total:,} ₽ за {nights} {'ночь' if nights == 1 else 'ночей'}</div>
                <div class="hotel-rating">
                    <span class="rating-value">{avg_rating:.1f}</span>
                    <span class="rating-count">({len(hotel_reviews)} отзывов)</span>
                    <button class="review-btn" onclick="event.stopPropagation(); openReviewModal({i}, '{hotel['name'].replace("'", "\\'")}')">Оставить отзыв</button>
                </div>
                {reviews_html}
                <div class="hotel-actions">
                    <button class="select-btn" onclick="event.stopPropagation(); selectHotel({i}, {hotel_total}, '{hotel['name'].replace("'", "\\'")}', {hotel['stars']})">Выбрать</button>
                    <button class="favorite-btn" onclick="event.stopPropagation(); addToFavorites({i}, '{hotel['name'].replace("'", "\\'")}', '{destination}', {hotel['price']})">В избранное</button>
                </div>
            </div>
        </div>
"""
    
    flights_there_html = ""
    for i, flight in enumerate(flights_there):
        class_badge = f'<span class="class-badge {flight["class"]}">{flight["class_icon"]} {flight["class_name"]}</span>'
        stops_badge = f'<span class="stops-badge">✈️ {flight["stops_text"]}</span>' if flight["stops"] > 0 else '<span class="stops-badge direct">✈️ Прямой</span>'
        
        discount_percent = discount_info.get(destination, 0)
        discount_badge = f'<span class="discount-badge" style="background: #e85d4a; color: white; padding: 2px 8px; border-radius: 20px; font-size: 11px; margin-left: 10px;">-{discount_percent}%</span>' if discount_percent > 0 and i == 0 else ''
        
        flights_there_html += f"""
        <div class="flight-item" onclick="selectFlightThere({i}, {flight['price']}, '{flight['airline']} ({flight['class_name']})')">
            <div class="flight-row">
                <div class="flight-airline">✈️ {flight['airline']}</div>
                <div class="flight-number">{flight['flight_num']}</div>
                <div class="flight-class">{class_badge}</div>
                <div class="flight-time">{flight['time']}</div>
                <div class="flight-duration">{flight['duration']}</div>
                <div class="flight-stops">{stops_badge}</div>
                <div class="flight-baggage">{flight['baggage']}</div>
                <div class="flight-price">{flight['price']:,} ₽ {discount_badge}</div>
            </div>
        </div>"""
    
    flights_back_html = ""
    for i, flight in enumerate(flights_back):
        class_badge = f'<span class="class-badge {flight["class"]}">{flight["class_icon"]} {flight["class_name"]}</span>'
        stops_badge = f'<span class="stops-badge">✈️ {flight["stops_text"]}</span>' if flight["stops"] > 0 else '<span class="stops-badge direct">✈️ Прямой</span>'
        flights_back_html += f"""
        <div class="flight-item" onclick="selectFlightBack({i}, {flight['price']}, '{flight['airline']} ({flight['class_name']})')">
            <div class="flight-row">
                <div class="flight-airline">✈️ {flight['airline']}</div>
                <div class="flight-number">{flight['flight_num']}</div>
                <div class="flight-class">{class_badge}</div>
                <div class="flight-time">{flight['time']}</div>
                <div class="flight-duration">{flight['duration']}</div>
                <div class="flight-stops">{stops_badge}</div>
                <div class="flight-baggage">{flight['baggage']}</div>
                <div class="flight-price">{flight['price']:,} ₽</div>
            </div>
        </div>"""
    
    attractions_html = ""
    for idx, attr in enumerate(attractions):
        stars_display = "★" * int(attr["rating"]) + "☆" * (5 - int(attr["rating"]))
        images = attr.get("images", [])
        images_json = json.dumps(images)
        
        attractions_html += f"""
        <div class="attraction-card">
            <div class="attraction-icon">{attr['icon']}</div>
            <div class="attraction-info">
                <div class="attraction-name">{attr['name']}</div>
                <div class="attraction-stars">{stars_display}</div>
                <div class="attraction-desc">{attr['desc']}</div>
                <div class="attraction-details">
                    <span class="attraction-price">{attr['price']:,} ₽</span>
                    <span class="attraction-duration">{attr['duration']}</span>
                </div>
                <button class="photo-btn" onclick="openGallery({images_json}, {idx})">Смотреть фото ({len(images)})</button>
            </div>
        </div>"""
    
    map_html = get_map_script(city_data, hotels, attractions)
    
    weather_forecast_html = ""
    if weather.get("forecast"):
        weather_forecast_html = '<div class="weather-forecast"><h3>Прогноз на неделю</h3><div class="forecast-grid">'
        for day in weather["forecast"][:5]:
            weather_forecast_html += f'<div class="forecast-day"><div class="forecast-date">{day["date"]}</div><div class="forecast-icon">{day["icon"]}</div><div class="forecast-temp">{day["temp_min"]}°...{day["temp_max"]}°</div></div>'
        weather_forecast_html += '</div></div>'
    
    results_html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Выбор тура - {destination}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --bg-color: #f3f5f9;
            --card-bg: white;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --btn-bg: #7c8ea8;
        }}
        body.dark-theme {{
            --bg-color: #0f0f1a;
            --card-bg: #1e1e2e;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border-color: #2d2d44;
            --btn-bg: #4a5b7e;
        }}
        body.dark-theme select,
        body.dark-theme option {{
            background-color: #1e1e2e !important;
            color: #f1f5f9 !important;
        }}
        body.dark-theme .hotel-card,
        body.dark-theme .flight-item,
        body.dark-theme .attraction-card,
        body.dark-theme .flights-section,
        body.dark-theme .summary,
        body.dark-theme .weather-forecast,
        body.dark-theme .weather-card,
        body.dark-theme .total-bar,
        body.dark-theme .payment-modal-content,
        body.dark-theme .review-modal-content,
        body.dark-theme .payment-input,
        body.dark-theme .review-textarea {{
            background-color: #1e1e2e !important;
            color: #f1f5f9 !important;
        }}
        body.dark-theme .hotel-card .hotel-name,
        body.dark-theme .attraction-name,
        body.dark-theme .flight-airline,
        body.dark-theme .review-author,
        body.dark-theme .payment-title {{
            color: #f1f5f9 !important;
        }}
        body.dark-theme .hotel-desc,
        body.dark-theme .attraction-desc,
        body.dark-theme .review-text,
        body.dark-theme .payment-sbp-hint,
        body.dark-theme .payment-sbp-note {{
            color: #cbd5e1 !important;
        }}
        body.dark-theme .payment-input,
        body.dark-theme .review-textarea {{
            border-color: #3f3f4f !important;
        }}
        body.dark-theme .payment-input:focus,
        body.dark-theme .review-textarea:focus {{
            border-color: #3b82f6 !important;
        }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: var(--bg-color);
            padding: 20px;
            transition: all 0.3s;
        }}
        body, body * {{
            color: var(--text-primary);
        }}
        .hotel-stars, .attraction-stars {{ color: #ffc107 !important; }}
        .hotel-price, .attraction-price, .flight-price {{ color: #28a745 !important; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, var(--card-bg) 0%, #eef2f7 100%);
            padding: 24px 32px;
            border-radius: 24px;
            margin-bottom: 24px;
        }}
        body.dark-theme .header {{
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        }}
        .weather-card {{
            background: linear-gradient(135deg, #e8f0fe 0%, #d4e0f0 100%);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }}
        body.dark-theme .weather-card {{
            background: linear-gradient(135deg, #1e3a5f 0%, #1a2a4a 100%);
        }}
        .weather-icon {{ font-size: 3rem; }}
        .weather-temp {{ font-size: 2rem; font-weight: bold; }}
        .weather-forecast {{
            background: var(--card-bg);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 24px;
        }}
        .forecast-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 15px; }}
        .forecast-day {{ text-align: center; padding: 10px; background: #f8fafd; border-radius: 12px; }}
        body.dark-theme .forecast-day {{
            background: #2d2d44;
        }}
        .summary {{
            background: var(--card-bg);
            padding: 16px 20px;
            border-radius: 20px;
            margin-bottom: 24px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .result-tabs {{ display: flex; gap: 16px; margin-bottom: 30px; justify-content: center; flex-wrap: wrap; }}
        .result-tab-btn {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 14px 28px;
            background: white;
            border: none;
            border-radius: 60px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        body.dark-theme .result-tab-btn {{
            background: #2d2d44;
            color: #f1f5f9;
        }}
        .result-tab-btn.active {{
            background: linear-gradient(135deg, var(--btn-bg) 0%, #6a7c96 100%);
            color: white;
        }}
        .result-tab-content {{ display: none; }}
        .result-tab-content.active {{ display: block; }}
        .hotels-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; margin-bottom: 30px; }}
        .hotel-card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            cursor: pointer;
            border: 2px solid transparent;
        }}
        .hotel-card.selected {{ border-color: #28a745; background: #f0fff4; }}
        body.dark-theme .hotel-card.selected {{
            background: #1a3a2a;
        }}
        .hotel-image {{ height: 200px; overflow: hidden; }}
        .hotel-image img {{ width: 100%; height: 100%; object-fit: cover; }}
        .hotel-info {{ padding: 16px; }}
        .hotel-name {{ font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }}
        .hotel-stars {{ margin-bottom: 8px; }}
        .hotel-desc {{ font-size: 0.9rem; margin-bottom: 10px; }}
        .hotel-price {{ font-size: 1.2rem; font-weight: bold; margin-bottom: 12px; }}
        .hotel-rating {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}
        .rating-value {{
            font-weight: bold;
            color: #f59e0b;
        }}
        .rating-count {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        .review-btn {{
            background: #e2e8f0;
            border: 1px solid #cbd5e1;
            color: #1e293b;
            padding: 4px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.7rem;
            transition: all 0.2s;
        }}
        .review-btn:hover {{
            background: var(--primary);
            border-color: var(--primary);
            color: white;
        }}
        body.dark-theme .review-btn {{
            background: #334155;
            border-color: #475569;
            color: #f1f5f9;
        }}
        body.dark-theme .review-btn:hover {{
            background: var(--primary);
            color: white;
        }}
        .hotel-reviews {{
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid var(--border-color);
        }}
        .review-item {{
            margin-bottom: 10px;
            padding: 8px;
            background: var(--bg-color);
            border-radius: 8px;
        }}
        .review-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 5px;
            font-size: 0.75rem;
            flex-wrap: wrap;
        }}
        .review-author {{
            font-weight: bold;
        }}
        .review-stars {{
            color: #f59e0b;
        }}
        .review-date {{
            color: var(--text-secondary);
            font-size: 0.7rem;
        }}
        .review-text {{
            font-size: 0.8rem;
            line-height: 1.4;
        }}
        .review-more {{
            text-align: right;
            font-size: 0.7rem;
            color: var(--primary);
            cursor: pointer;
            margin-top: 5px;
        }}
        .review-more:hover {{
            text-decoration: underline;
        }}
        .hotel-actions {{
            display: flex;
            gap: 10px;
            margin-top: 12px;
        }}
        .select-btn, .favorite-btn {{ padding: 8px 16px; border: none; border-radius: 20px; cursor: pointer; flex: 1; }}
        .select-btn {{ background: #667eea; color: white; }}
        .favorite-btn {{ background: #fef3c7; border: 1px solid #fcd34d; }}
        body.dark-theme .favorite-btn {{
            background: #d97706;
            border-color: #d97706;
            color: white !important;
        }}
        .flights-section {{ background: white; border-radius: 20px; padding: 20px; margin-bottom: 20px; }}
        .flight-item {{
            background: #fafcff;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 12px;
            cursor: pointer;
            border: 1px solid #eef2f7;
        }}
        body.dark-theme .flight-item {{
            background: #2d2d44;
            border-color: #3f3f4f;
        }}
        .flight-item.selected-there, .flight-item.selected-back {{ border-color: #28a745; background: #e8f5e9; }}
        body.dark-theme .flight-item.selected-there,
        body.dark-theme .flight-item.selected-back {{
            background: #1a3a2a;
            border-color: #28a745;
        }}
        .flight-row {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
        .flight-airline {{ font-weight: bold; min-width: 100px; }}
        .class-badge {{ padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }}
        .class-badge.economy {{ background: #e3f2fd; color: #1976d2; }}
        .class-badge.business {{ background: #fff3e0; color: #ed6c02; }}
        .stops-badge {{ font-size: 12px; background: #f5f5f5; padding: 2px 8px; border-radius: 15px; }}
        .stops-badge.direct {{ background: #e8f5e9; color: #2e7d32; }}
        .flight-price {{ font-weight: bold; min-width: 100px; text-align: right; }}
        .attractions-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .attraction-card {{ background: #fafcff; padding: 20px; border-radius: 16px; display: flex; gap: 16px; border: 1px solid #eef2f7; }}
        body.dark-theme .attraction-card {{
            background: #2d2d44;
            border-color: #3f3f4f;
        }}
        .attraction-icon {{ font-size: 2.5rem; }}
        .attraction-info {{ flex: 1; }}
        .attraction-name {{ font-size: 1.1rem; font-weight: bold; }}
        .photo-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.75rem;
            margin-top: 10px;
        }}
        .total-bar {{
            position: sticky;
            bottom: 20px;
            background: white;
            border-radius: 60px;
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            box-shadow: 0 8px 28px rgba(0,0,0,0.1);
            margin-top: 20px;
        }}
        body.dark-theme .total-bar {{
            background: #1e1e2e;
        }}
        .btn-book {{ background: var(--btn-bg); padding: 10px 28px; border: none; border-radius: 40px; cursor: pointer; color: white; }}
        .btn-book:disabled {{ background: #cbd5e1; cursor: not-allowed; }}
        .back-link {{ display: inline-block; margin-top: 20px; text-decoration: none; color: var(--btn-bg); }}
        
        /* Стили для галереи */
        .gallery-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 10000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }}
        .gallery-modal.active {{ display: flex; }}
        .gallery-modal img {{
            max-width: 90%;
            max-height: 80%;
            border-radius: 12px;
        }}
        .gallery-close {{
            position: absolute;
            top: 20px;
            right: 40px;
            color: white;
            font-size: 40px;
            cursor: pointer;
            font-weight: bold;
        }}
        .gallery-close:hover {{ color: #ccc; }}
        .gallery-nav {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            font-size: 50px;
            color: white;
            cursor: pointer;
            background: rgba(0,0,0,0.5);
            padding: 10px 20px;
            border-radius: 50%;
            user-select: none;
        }}
        .gallery-nav.prev {{ left: 20px; }}
        .gallery-nav.next {{ right: 20px; }}
        .gallery-nav:hover {{ background: rgba(0,0,0,0.8); }}
        
        /* Стили для модального окна оплаты */
        .payment-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 10001;
            justify-content: center;
            align-items: center;
        }}
        .payment-modal.active {{ display: flex; }}
        .payment-modal-content {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 32px;
            max-width: 460px;
            width: 90%;
            position: relative;
            box-shadow: 0 20px 35px -8px rgba(0,0,0,0.2);
        }}
        .payment-close {{
            position: absolute;
            top: 20px;
            right: 24px;
            width: 24px;
            height: 24px;
            cursor: pointer;
            opacity: 0.6;
            transition: opacity 0.2s;
        }}
        .payment-close:hover {{ opacity: 1; }}
        .payment-close::before,
        .payment-close::after {{
            content: '';
            position: absolute;
            top: 10px;
            left: 0;
            width: 24px;
            height: 2px;
            background: var(--text-primary);
        }}
        .payment-close::before {{ transform: rotate(45deg); }}
        .payment-close::after {{ transform: rotate(-45deg); }}
        .payment-title {{ font-size: 1.25rem; font-weight: 600; margin-bottom: 8px; }}
        .payment-amount {{ font-size: 1.75rem; font-weight: 700; color: var(--primary); margin-bottom: 24px; }}
        .payment-methods {{ display: flex; gap: 12px; margin-bottom: 24px; }}
        .payment-method {{
            flex: 1;
            padding: 16px 12px;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            background: var(--card-bg);
        }}
        .payment-method:hover {{ border-color: var(--primary); background: rgba(37, 99, 235, 0.05); }}
        .payment-method.selected {{ border-color: var(--primary); background: rgba(37, 99, 235, 0.08); }}
        .payment-method-icon {{ width: 32px; height: 32px; margin: 0 auto 8px; color: var(--primary); }}
        .payment-method-icon svg {{ width: 100%; height: 100%; stroke: currentColor; }}
        .payment-method-title {{ font-weight: 500; font-size: 0.875rem; margin-bottom: 2px; }}
        .payment-method-subtitle {{ font-size: 0.7rem; color: var(--text-secondary); }}
        .payment-card-form {{ margin-bottom: 24px; }}
        .payment-field {{ margin-bottom: 16px; }}
        .payment-row {{ display: flex; gap: 12px; }}
        .payment-field.half {{ flex: 1; }}
        .payment-label {{ display: block; font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); margin-bottom: 6px; }}
        .payment-input {{
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background: var(--card-bg);
            font-size: 0.875rem;
            transition: all 0.2s;
        }}
        .payment-input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
        }}
        .payment-sbp-form {{ text-align: center; margin-bottom: 24px; }}
        .payment-sbp-hint {{ font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 16px; }}
        .payment-qr-container {{ display: inline-block; padding: 12px; background: white; border-radius: 16px; margin-bottom: 12px; }}
        .payment-qr-image {{ width: 180px; height: 180px; display: block; }}
        .payment-sbp-note {{ font-size: 0.7rem; color: var(--text-secondary); }}
        .payment-button {{
            width: 100%;
            padding: 14px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 40px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .payment-button:hover {{ background: var(--primary-dark); }}
        
        /* Стили для модального окна отзыва */
        .review-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 10002;
            justify-content: center;
            align-items: center;
        }}
        .review-modal.active {{ display: flex; }}
        .review-modal-content {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 24px;
            max-width: 450px;
            width: 90%;
            position: relative;
        }}
        .review-modal-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        .review-rating-select {{
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
        }}
        .review-star {{
            font-size: 2rem;
            cursor: pointer;
            color: #cbd5e1;
            transition: color 0.2s;
        }}
        .review-star.selected {{
            color: #f59e0b;
        }}
        .review-textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            background: var(--card-bg);
            font-family: inherit;
            font-size: 0.875rem;
            resize: vertical;
            margin-bottom: 16px;
        }}
        .review-textarea:focus {{
            outline: none;
            border-color: var(--primary);
        }}
        .review-submit {{
            width: 100%;
            padding: 12px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 40px;
            cursor: pointer;
            font-weight: 600;
        }}
        .review-close {{
            position: absolute;
            top: 12px;
            right: 16px;
            font-size: 24px;
            cursor: pointer;
            color: var(--text-secondary);
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 12px; }}
            .header h1 {{ font-size: 1.5rem; }}
            .result-tab-btn {{ padding: 8px 16px; font-size: 12px; }}
            .hotels-grid {{ grid-template-columns: 1fr; }}
            .attractions-grid {{ grid-template-columns: 1fr; }}
            .flight-row {{ flex-direction: column; align-items: flex-start; }}
            .flight-price {{ text-align: left; }}
            .hotel-actions {{ flex-direction: column; }}
            .total-bar {{ flex-direction: column; text-align: center; }}
            .forecast-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .payment-methods {{ flex-direction: column; gap: 8px; }}
            .payment-modal-content {{ padding: 24px; }}
        }}
        @media (max-width: 480px) {{
            .forecast-grid {{ grid-template-columns: 1fr; }}
            .payment-qr-image {{ width: 140px; height: 140px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{destination}</h1>
            <div class="airport-info">Аэропорт прилета: {arrival_airport}</div>
            <div style="margin-top: 12px;">{nights} {'ночь' if nights == 1 else 'ночей'} | {adults} взрослых, {children} детей</div>
        </div>
        
        <div class="weather-card">
            <div class="weather-icon">{weather["icon"]}</div>
            <div>
                <div class="weather-temp">{weather["avg"]}°C</div>
                <div>{weather["description"]}</div>
                <div style="font-size: 14px;">{weather["temp_min"]}°C - {weather["temp_max"]}°C</div>
            </div>
        </div>
        
        {weather_forecast_html}
        
        <div class="summary">
            <div>{budget if budget else "Не указан"} ₽</div>
            <div>{len(hotels)} отелей</div>
            <div>{len(flights_there)} вариантов туда</div>
            <div>{len(flights_back)} вариантов обратно</div>
            <div>{len(attractions)} экскурсий</div>
        </div>
        
        <div class="result-tabs">
            <button class="result-tab-btn active" onclick="switchResultTab('hotels')"><span class="tab-icon">🏨</span><span class="tab-text">Отели</span><span class="tab-count">{len(hotels[:10])}</span></button>
            <button class="result-tab-btn" onclick="switchResultTab('flights')"><span class="tab-icon">✈️</span><span class="tab-text">Билеты</span><span class="tab-count">{len(flights_there)}</span></button>
            <button class="result-tab-btn" onclick="switchResultTab('attractions')"><span class="tab-icon">🎯</span><span class="tab-text">Экскурсии</span><span class="tab-count">{len(attractions)}</span></button>
            <button class="result-tab-btn" onclick="switchResultTab('map')"><span class="tab-icon">🗺️</span><span class="tab-text">Карта</span></button>
        </div>
        
        <div id="hotelsTab" class="result-tab-content active">
            <h2 style="margin: 20px 0 15px;">Выберите отель</h2>
            <div class="hotels-grid">{hotels_html}</div>
        </div>
        
        <div id="flightsTab" class="result-tab-content">
            <div class="flights-section"><h3>Выберите билет туда (Москва → {destination}) - {len(flights_there)} вариантов</h3><div id="flightsThereList">{flights_there_html}</div></div>
            <div class="flights-section"><h3>Выберите билет обратно ({destination} → Москва) - {len(flights_back)} вариантов</h3><div id="flightsBackList">{flights_back_html}</div></div>
        </div>
        
        <div id="attractionsTab" class="result-tab-content">
            <h2 style="margin: 20px 0 15px;">Популярные экскурсии в {destination} - {len(attractions)} вариантов</h2>
            <div class="attractions-grid">{attractions_html}</div>
        </div>
        
        <div id="mapTab" class="result-tab-content">
            <h2 style="margin: 20px 0 15px;">Карта отелей и достопримечательностей</h2>
            {map_html}
        </div>
        
        <div class="total-bar">
            <div>Отель <strong id="selectedHotel">Не выбран</strong> | Билет туда <strong id="selectedThere">Не выбран</strong> | Билет обратно <strong id="selectedBack">Не выбран</strong></div>
            <div><span class="total-value highlight" id="totalPrice">0 ₽</span><button class="btn-book" id="bookBtn" onclick="bookTour()" disabled>Забронировать</button></div>
        </div>
        
        <a href="/" class="back-link">← Вернуться к поиску</a>
    </div>
    
    <!-- Модальное окно для галереи -->
    <div id="galleryModal" class="gallery-modal">
        <span class="gallery-close" onclick="closeGallery()">&times;</span>
        <span class="gallery-nav prev" onclick="changeImage(-1)">&#10094;</span>
        <img id="galleryImage" src="">
        <span class="gallery-nav next" onclick="changeImage(1)">&#10095;</span>
    </div>

    <!-- Модальное окно оплаты -->
    <div id="paymentModal" class="payment-modal">
        <div class="payment-modal-content">
            <div class="payment-close" onclick="closePaymentModal()"></div>
            <div class="payment-title">Оплата тура</div>
            <div id="paymentAmount" class="payment-amount"></div>
            
            <div class="payment-methods">
                <div class="payment-method" onclick="selectPaymentMethod('card')">
                    <div class="payment-method-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <rect x="2" y="5" width="20" height="14" rx="2" ry="2"></rect>
                            <line x1="2" y1="10" x2="22" y2="10"></line>
                        </svg>
                    </div>
                    <div class="payment-method-title">Банковская карта</div>
                    <div class="payment-method-subtitle">Visa, Mastercard, Мир</div>
                </div>
                <div class="payment-method" onclick="selectPaymentMethod('sbp')">
                    <div class="payment-method-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M21 12a9 9 0 0 1-9 9m9-9a9 9 0 0 0-9-9m9 9H3m9 9a9 9 0 0 1-9-9m9 9c1.66 0 3-4 3-9s-1.34-9-3-9m0 18c-1.66 0-3-4-3-9s1.34-9 3-9"/>
                        </svg>
                    </div>
                    <div class="payment-method-title">СБП</div>
                    <div class="payment-method-subtitle">Система быстрых платежей</div>
                </div>
            </div>
            
            <div id="cardForm" class="payment-card-form" style="display: none;">
                <div class="payment-field">
                    <label class="payment-label">Номер карты</label>
                    <input type="text" id="cardNumber" class="payment-input" placeholder="0000 0000 0000 0000" maxlength="19">
                </div>
                <div class="payment-row">
                    <div class="payment-field half">
                        <label class="payment-label">Срок действия</label>
                        <input type="text" id="cardExpiry" class="payment-input" placeholder="ММ/ГГ" maxlength="5">
                    </div>
                    <div class="payment-field half">
                        <label class="payment-label">CVV</label>
                        <input type="password" id="cardCvv" class="payment-input" placeholder="***" maxlength="3">
                    </div>
                </div>
                <div class="payment-field">
                    <label class="payment-label">Владелец карты</label>
                    <input type="text" id="cardName" class="payment-input" placeholder="IVAN IVANOV">
                </div>
            </div>
            
            <div id="sbpForm" class="payment-sbp-form" style="display: none;">
                <div class="payment-sbp-hint">Сканируйте QR-код в приложении вашего банка</div>
                <div class="payment-qr-container">
                    <img id="sbpQrCode" class="payment-qr-image" src="" alt="QR-код для оплаты">
                </div>
                <div class="payment-sbp-note">Демонстрационный режим</div>
            </div>
            
            <button id="payButton" class="payment-button" onclick="processPayment()">Подтвердить оплату</button>
        </div>
    </div>

    <!-- Модальное окно для отзыва -->
    <div id="reviewModal" class="review-modal">
        <div class="review-modal-content">
            <span class="review-close" onclick="closeReviewModal()">&times;</span>
            <div class="review-modal-title">Оставить отзыв</div>
            <div id="reviewHotelName" style="margin-bottom: 16px; font-weight: 500;"></div>
            <div class="review-rating-select" id="ratingStars">
                <span class="review-star" data-rating="1">☆</span>
                <span class="review-star" data-rating="2">☆</span>
                <span class="review-star" data-rating="3">☆</span>
                <span class="review-star" data-rating="4">☆</span>
                <span class="review-star" data-rating="5">☆</span>
            </div>
            <textarea id="reviewText" class="review-textarea" rows="4" placeholder="Поделитесь впечатлениями об отеле..."></textarea>
            <button class="review-submit" onclick="submitReview()">Отправить отзыв</button>
        </div>
    </div>

    <script>
        let selectedHotelPrice = 0, selectedHotelName = "", selectedHotelStars = 0;
        let selectedTherePrice = 0, selectedThereName = "";
        let selectedBackPrice = 0, selectedBackName = "";
        
        let currentImages = [];
        let currentImageIndex = 0;
        
        let currentPaymentAmount = 0;
        let currentPaymentMethod = null;
        let currentPaymentId = null;
        let currentBookingData = null;
        
        let currentReviewHotelId = null;
        let currentReviewHotelName = "";
        let selectedRating = 0;
        
        function switchResultTab(tab) {{
            document.querySelectorAll('.result-tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.result-tab-content').forEach(content => content.classList.remove('active'));
            if (tab === 'hotels') {{
                document.querySelector('.result-tab-btn:first-child').classList.add('active');
                document.getElementById('hotelsTab').classList.add('active');
            }} else if (tab === 'flights') {{
                document.querySelector('.result-tab-btn:nth-child(2)').classList.add('active');
                document.getElementById('flightsTab').classList.add('active');
            }} else if (tab === 'attractions') {{
                document.querySelector('.result-tab-btn:nth-child(3)').classList.add('active');
                document.getElementById('attractionsTab').classList.add('active');
            }} else if (tab === 'map') {{
                document.querySelector('.result-tab-btn:nth-child(4)').classList.add('active');
                document.getElementById('mapTab').classList.add('active');
                setTimeout(() => {{ if (window.map) window.map.invalidateSize(); }}, 100);
            }}
        }}
        
        function selectHotel(idx, price, name, stars) {{
            document.querySelectorAll('.hotel-card').forEach((el, i) => el.classList.toggle('selected', i === idx));
            selectedHotelPrice = price;
            selectedHotelName = name;
            selectedHotelStars = stars;
            document.getElementById('selectedHotel').innerHTML = name;
            updateTotal();
        }}
        
        function addToFavorites(id, name, city, price) {{
            fetch('/api/add_favorite', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{ hotel_id: id, hotel_name: name, city: city, price: price }})
            }}).then(() => alert('Отель добавлен в избранное'));
        }}
        
        function openReviewModal(hotelId, hotelName) {{
            currentReviewHotelId = hotelId;
            currentReviewHotelName = hotelName;
            selectedRating = 0;
            document.getElementById('reviewHotelName').innerHTML = hotelName;
            document.getElementById('reviewText').value = '';
            document.querySelectorAll('.review-star').forEach(star => {{
                star.classList.remove('selected');
                star.innerHTML = '☆';
            }});
            document.getElementById('reviewModal').classList.add('active');
        }}
        
        function closeReviewModal() {{
            document.getElementById('reviewModal').classList.remove('active');
        }}
        
        function submitReview() {{
            if (selectedRating === 0) {{
                alert('Поставьте оценку');
                return;
            }}
            const text = document.getElementById('reviewText').value;
            if (!text.trim()) {{
                alert('Напишите текст отзыва');
                return;
            }}
            
            fetch('/api/add_review', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    hotel_id: currentReviewHotelId,
                    rating: selectedRating,
                    text: text
                }})
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) {{
                    alert('Спасибо за отзыв');
                    location.reload();
                }} else {{
                    alert('Ошибка: ' + (data.error || 'Неизвестная ошибка'));
                }}
            }});
        }}
        
        document.querySelectorAll('.review-star').forEach(star => {{
            star.addEventListener('click', function() {{
                const rating = parseInt(this.dataset.rating);
                selectedRating = rating;
                document.querySelectorAll('.review-star').forEach((s, i) => {{
                    if (i < rating) {{
                        s.classList.add('selected');
                        s.innerHTML = '★';
                    }} else {{
                        s.classList.remove('selected');
                        s.innerHTML = '☆';
                    }}
                }});
            }});
        }});
        
        function showAllReviews(hotelId) {{
            const hotelCard = document.querySelectorAll('.hotel-card')[hotelId];
            if (hotelCard) {{
                hotelCard.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}
        }}
        
        function selectFlightThere(idx, price, name) {{
            document.querySelectorAll('#flightsThereList .flight-item').forEach((el, i) => el.classList.toggle('selected-there', i === idx));
            selectedTherePrice = price;
            selectedThereName = name;
            document.getElementById('selectedThere').innerHTML = name;
            updateTotal();
        }}
        
        function selectFlightBack(idx, price, name) {{
            document.querySelectorAll('#flightsBackList .flight-item').forEach((el, i) => el.classList.toggle('selected-back', i === idx));
            selectedBackPrice = price;
            selectedBackName = name;
            document.getElementById('selectedBack').innerHTML = name;
            updateTotal();
        }}
        
        function updateTotal() {{
            const total = selectedHotelPrice + selectedTherePrice + selectedBackPrice;
            document.getElementById('totalPrice').innerHTML = total.toLocaleString() + ' ₽';
            document.getElementById('bookBtn').disabled = !(selectedHotelPrice && selectedTherePrice && selectedBackPrice);
        }}
        
        function openPaymentModal(amount, bookingData) {{
            currentPaymentAmount = amount;
            currentBookingData = bookingData;
            document.getElementById('paymentAmount').innerHTML = amount.toLocaleString() + ' ₽';
            document.getElementById('paymentModal').classList.add('active');
            document.getElementById('cardForm').style.display = 'none';
            document.getElementById('sbpForm').style.display = 'none';
            currentPaymentMethod = null;
            document.querySelectorAll('.payment-method').forEach(m => m.classList.remove('selected'));
        }}
        
        function closePaymentModal() {{
            document.getElementById('paymentModal').classList.remove('active');
        }}
        
        function selectPaymentMethod(method) {{
            currentPaymentMethod = method;
            document.querySelectorAll('.payment-method').forEach(m => m.classList.remove('selected'));
            event.target.closest('.payment-method').classList.add('selected');
            
            if (method === 'card') {{
                document.getElementById('cardForm').style.display = 'block';
                document.getElementById('sbpForm').style.display = 'none';
            }} else {{
                document.getElementById('cardForm').style.display = 'none';
                document.getElementById('sbpForm').style.display = 'block';
                
                const qrImage = document.getElementById('sbpQrCode');
                if (qrImage) {{
                    qrImage.src = '/static/images/sbp_qr_demo.png';
                    qrImage.onerror = function() {{
                        this.src = 'https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg';
                    }};
                }}
                
                fetch('/api/initiate_payment', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        booking_id: currentBookingData?.id || 'demo',
                        amount: currentPaymentAmount,
                        method: 'sbp'
                    }})
                }})
                .then(res => res.json())
                .then(data => {{
                    if (data.success) {{
                        currentPaymentId = data.payment_id;
                    }}
                }})
                .catch(err => console.log('Init payment error:', err));
            }}
        }}
        
        function processPayment() {{
            if (!currentPaymentMethod) {{
                alert('Выберите способ оплаты');
                return;
            }}
            
            if (currentPaymentMethod === 'card') {{
                const cardNum = document.getElementById('cardNumber').value.replace(/\\s/g, '');
                const expiry = document.getElementById('cardExpiry').value;
                const cvv = document.getElementById('cardCvv').value;
                
                if (cardNum.length < 16) {{
                    alert('Введите номер карты (16 цифр)');
                    return;
                }}
                if (expiry.length < 5) {{
                    alert('Введите срок действия (ММ/ГГ)');
                    return;
                }}
                if (cvv.length < 3) {{
                    alert('Введите CVV код');
                    return;
                }}
            }}
            
            fetch('/api/initiate_payment', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    booking_id: currentBookingData?.id || 'demo',
                    amount: currentPaymentAmount,
                    method: currentPaymentMethod
                }})
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) {{
                    return fetch('/api/confirm_payment', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            payment_id: data.payment_id,
                            booking_id: currentBookingData?.id || 'demo',
                            destination: currentBookingData?.destination,
                            nights: currentBookingData?.nights,
                            hotel: currentBookingData?.hotel,
                            flight_there: currentBookingData?.flight_there,
                            flight_back: currentBookingData?.flight_back
                        }})
                    }});
                }}
                throw new Error('Init payment failed');
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) {{
                    alert('Оплата успешно проведена');
                    closePaymentModal();
                    document.getElementById('bookBtn').disabled = true;
                    document.getElementById('bookBtn').innerHTML = 'Оплачено';
                }} else {{
                    alert('Ошибка оплаты: ' + (data.error || 'Неизвестная ошибка'));
                }}
            }})
            .catch(err => {{
                alert('Ошибка соединения: ' + err.message);
            }});
        }}
        
        document.getElementById('cardNumber')?.addEventListener('input', function(e) {{
            let value = e.target.value.replace(/\\D/g, '');
            value = value.replace(/(\\d{{4}})(?=\\d)/g, '$1 ');
            e.target.value = value.slice(0, 19);
        }});
        
        document.getElementById('cardExpiry')?.addEventListener('input', function(e) {{
            let value = e.target.value.replace(/\\D/g, '');
            if (value.length >= 2) {{
                value = value.slice(0,2) + '/' + value.slice(2,4);
            }}
            e.target.value = value.slice(0,5);
        }});
        
        document.getElementById('cardCvv')?.addEventListener('input', function(e) {{
            e.target.value = e.target.value.replace(/\\D/g, '').slice(0,3);
        }});
        
        function bookTour() {{
            if (!selectedHotelPrice || !selectedTherePrice || !selectedBackPrice) {{
                alert('Выберите отель и билеты');
                return;
            }}
            const total = selectedHotelPrice + selectedTherePrice + selectedBackPrice;
            
            openPaymentModal(total, {{
                id: Date.now(),
                destination: '{destination}',
                nights: {nights},
                hotel: selectedHotelName,
                flight_there: selectedThereName,
                flight_back: selectedBackName,
                total_price: total
            }});
        }}
        
        function openGallery(images, index) {{
            if (!images || images.length === 0) {{
                alert('Фотографии временно недоступны');
                return;
            }}
            currentImages = images;
            currentImageIndex = 0;
            const modal = document.getElementById('galleryModal');
            const img = document.getElementById('galleryImage');
            if (modal && img) {{
                img.src = images[0];
                modal.classList.add('active');
            }}
        }}
        
        function closeGallery() {{
            document.getElementById('galleryModal').classList.remove('active');
        }}
        
        function changeImage(direction) {{
            if (!currentImages || currentImages.length === 0) return;
            currentImageIndex += direction;
            if (currentImageIndex < 0) currentImageIndex = currentImages.length - 1;
            if (currentImageIndex >= currentImages.length) currentImageIndex = 0;
            document.getElementById('galleryImage').src = currentImages[currentImageIndex];
        }}
        
        document.addEventListener('keydown', function(e) {{
            if (document.getElementById('galleryModal').classList.contains('active')) {{
                if (e.key === 'ArrowLeft') changeImage(-1);
                if (e.key === 'ArrowRight') changeImage(1);
                if (e.key === 'Escape') closeGallery();
            }}
            if (document.getElementById('paymentModal').classList.contains('active')) {{
                if (e.key === 'Escape') closePaymentModal();
            }}
            if (document.getElementById('reviewModal').classList.contains('active')) {{
                if (e.key === 'Escape') closeReviewModal();
            }}
        }});
        
        function toggleTheme() {{
            document.body.classList.toggle('dark-theme');
            localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
        }}
        if (localStorage.getItem('theme') === 'dark') document.body.classList.add('dark-theme');
    </script>
</body>
</html>
"""
    return HTMLResponse(content=results_html)
# ============= API ДЛЯ ОТЗЫВОВ =============

@app.post("/api/add_review")
async def add_review(data: dict, session: str = Cookie(None)):
    """Добавление отзыва об отеле"""
    username = get_current_user(session)
    if not username:
        return {"success": False, "error": "Не авторизован"}
    
    hotel_id = data.get("hotel_id")
    rating = data.get("rating")
    text = data.get("text")
    
    if hotel_id is None or not rating or not text:
        return {"success": False, "error": "Заполните все поля"}
    
    if rating < 1 or rating > 5:
        return {"success": False, "error": "Оценка должна быть от 1 до 5"}
    
    hotel_id_str = str(hotel_id)
    
    if hotel_id_str not in REVIEWS:
        REVIEWS[hotel_id_str] = []
    
    REVIEWS[hotel_id_str].append({
        "username": username,
        "rating": rating,
        "text": text,
        "date": datetime.now().strftime("%d.%m.%Y")
    })
    
    return {"success": True}


@app.get("/api/get_reviews/{hotel_id}")
async def get_reviews(hotel_id: str):
    """Получение отзывов об отеле"""
    hotel_reviews = REVIEWS.get(hotel_id, [])
    return {"success": True, "reviews": hotel_reviews}


# ============= ПРОФИЛЬ И ОСТАЛЬНЫЕ API =============

@app.get("/profile")
async def profile(session: str = Cookie(None)):
    username = get_current_user(session)
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    user_data = USERS.get(username, {})
    avatar = user_data.get("avatar", "👤")
    full_name = user_data.get("full_name", username)
    email = user_data.get("email", "")
    phone = user_data.get("phone", "")
    bookings = BOOKINGS.get(username, [])
    favorites = FAVORITES.get(username, [])
    notifications = NOTIFICATIONS.get(username, [])
    balance = USER_BALANCES.get(username, 0)
    referral_link = get_referral_link(username)
    bookings.reverse()
    
    bookings_html = "".join(f'<div class="booking"><div><strong>✈️ {b["destination"]}</strong> | 📅 {b["nights"]} ночей | 💰 {b["total_price"]:,} ₽</div><div>🏨 {b["hotel"]} | ✈️ {b["flight_there"]} → {b["flight_back"]}</div><div>📅 {b["start_date"]} - {b["end_date"]}</div><div class="status">Подтверждено</div></div>' for b in bookings) or "<p>Нет бронирований</p>"
    favorites_html = "".join(f'<div class="fav"><div><strong>🏨 {fav["hotel_name"]}</strong> ({fav["city"]}) - 💰 {fav["price"]:,} ₽/ночь</div><button onclick="removeFavorite({fav["hotel_id"]})">Удалить</button></div>' for fav in favorites) or "<p>Нет избранных</p>"
    notifications_html = "".join(f'<div class="notif {"" if n.get("read") else "unread"}" onclick="markAsRead({n["id"]})"><div>{n["icon"]}</div><div><div>{n["title"]}</div><div>{n["text"]}</div><div>{n["date"]}</div></div></div>' for n in notifications[:5]) or "<p>Нет уведомлений</p>"
    
    return HTMLResponse(content=f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Личный кабинет</title>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        :root{{--bg:#f3f5f9;--card:white;--text:#5a6e8a;--border:#eef2f7}}
        body.dark{{--bg:#1a1a2e;--card:#1e1e2e;--text:#e0e0e0}}
        body{{font-family:Segoe UI;background:var(--bg);padding:20px;transition:.3s}}
        .container{{max-width:1200px;margin:0 auto}}
        .navbar{{background:var(--card);padding:15px 30px;border-radius:60px;margin-bottom:30px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:15px}}
        .profile-grid{{display:grid;grid-template-columns:280px 1fr;gap:24px}}
        .sidebar{{background:var(--card);border-radius:24px;padding:24px}}
        .avatar{{width:100px;height:100px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:3rem;margin:0 auto 15px;cursor:pointer}}
        .menu-item{{padding:12px 15px;cursor:pointer;border-radius:12px;margin-bottom:5px;color:var(--text)}}
        .menu-item:hover,.menu-item.active{{background:var(--border)}}
        .main-content{{background:var(--card);border-radius:24px;padding:30px}}
        .tab{{display:none}}
        .tab.active{{display:block}}
        .booking,.fav,.notif{{background:var(--border);border-radius:16px;padding:15px;margin-bottom:15px}}
        .status{{background:#e8f5e9;color:#2e7d32;padding:4px 12px;border-radius:20px;display:inline-block;margin-top:10px}}
        .unread{{background:#eef2ff;border-left:4px solid #667eea}}
        .referral-box{{background:linear-gradient(135deg,#667eea20 0%,#764ba220 100%);border-radius:16px;padding:15px;margin-top:15px;text-align:center}}
        .referral-code{{background:var(--card);padding:10px;border-radius:12px;font-family:monospace;font-size:1.2rem;margin:10px 0;word-break:break-all}}
        .copy-btn{{background:#667eea;color:white;border:none;padding:8px 20px;border-radius:40px;cursor:pointer}}
        .balance{{background:#e8f5e9;padding:10px;border-radius:12px;text-align:center;margin-bottom:15px;color:#2e7d32;font-weight:bold}}
        
        @media (max-width: 768px) {{
            .profile-grid{{grid-template-columns:1fr;gap:16px}}
            .navbar{{flex-direction:column;text-align:center}}
            .sidebar{{padding:16px}}
            .main-content{{padding:20px}}
            .avatar{{width:80px;height:80px;font-size:2.5rem}}
            .menu-item{{padding:10px 12px;font-size:0.9rem}}
            .booking,.fav,.notif{{padding:12px;font-size:0.85rem}}
        }}
        @media (max-width: 480px) {{
            body{{padding:12px}}
            .navbar{{padding:12px 20px}}
            .main-content{{padding:16px}}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="navbar">
        <div>SmartTravel</div>
        <div>
            <button onclick="toggleTheme()">Тёмная</button>
            <a href="/" style="margin-left:15px;">Главная</a>
            <a href="/logout" style="margin-left:15px;color:#dc2626">Выйти</a>
        </div>
    </div>
    <div class="profile-grid">
        <div class="sidebar">
            <div class="avatar" onclick="showAvatar()">{avatar}</div>
            <div><div>{full_name}</div><div>{email}</div></div>
            <div class="balance">Баланс бонусов: {balance} ₽</div>
            <div class="menu">
                <div class="menu-item active" onclick="switchTab('bookings')">Бронирования</div>
                <div class="menu-item" onclick="switchTab('favorites')">Избранное</div>
                <div class="menu-item" onclick="switchTab('notifications')">Уведомления</div>
                <div class="menu-item" onclick="switchTab('referral')">Реферальная система</div>
                <div class="menu-item" onclick="switchTab('profile')">Настройки</div>
            </div>
        </div>
        <div class="main-content">
            <div id="bookingsTab" class="tab active"><h2>Бронирования</h2>{bookings_html}</div>
            <div id="favoritesTab" class="tab"><h2>Избранное</h2>{favorites_html}</div>
            <div id="notificationsTab" class="tab"><h2>Уведомления</h2>{notifications_html}</div>
            <div id="referralTab" class="tab">
                <h2>Реферальная система</h2>
                <div class="referral-box">
                    <p>Приглашайте друзей и получайте бонусы</p>
                    <p><strong>За каждого приглашённого друга вы получите {REFERRAL_BONUS} ₽</strong></p>
                    <p>Друг получит {REGISTRATION_BONUS} ₽ при регистрации</p>
                    <div class="referral-code">{referral_link}</div>
                    <button class="copy-btn" onclick="copyReferralLink()">Скопировать ссылку</button>
                </div>
            </div>
            <div id="profileTab" class="tab">
                <h2>Настройки</h2>
                <form action="/api/update_profile" method="POST">
                    <div style="margin-bottom:15px;"><label>Имя</label><input type="text" name="full_name" value="{full_name}" style="width:100%;padding:8px;border-radius:8px;border:1px solid #ddd;"></div>
                    <div style="margin-bottom:15px;"><label>Email</label><input type="email" name="email" value="{email}" style="width:100%;padding:8px;border-radius:8px;border:1px solid #ddd;"></div>
                    <div style="margin-bottom:15px;"><label>Телефон</label><input type="tel" name="phone" value="{phone}" style="width:100%;padding:8px;border-radius:8px;border:1px solid #ddd;"></div>
                    <button type="submit" style="background:#667eea;color:white;padding:10px 20px;border:none;border-radius:40px;cursor:pointer;">Сохранить</button>
                </form>
            </div>
        </div>
    </div>
</div>
<div id="avatarModal" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);justify-content:center;align-items:center;z-index:1000">
    <div style="background:white;border-radius:24px;padding:30px;max-width:90%;margin:20px;">
        <h3>Выберите аватар</h3>
        <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin:20px 0;">
            {"".join(f'<div style="font-size:2rem;cursor:pointer;padding:8px;text-align:center" onclick="selectAvatar(\'{a}\')">{a}</div>' for a in AVATARS)}
        </div>
        <button onclick="closeAvatar()" style="width:100%;padding:10px;background:#667eea;color:white;border:none;border-radius:40px;">Закрыть</button>
    </div>
</div>
<script>
function switchTab(t){{
    document.querySelectorAll('.menu-item').forEach(i=>i.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(c=>c.classList.remove('active'));
    if(t==='bookings'){{document.getElementById('bookingsTab').classList.add('active');}}
    else if(t==='favorites'){{document.getElementById('favoritesTab').classList.add('active');}}
    else if(t==='notifications'){{document.getElementById('notificationsTab').classList.add('active');}}
    else if(t==='referral'){{document.getElementById('referralTab').classList.add('active');}}
    else{{document.getElementById('profileTab').classList.add('active');}}
}}
function showAvatar(){{document.getElementById('avatarModal').style.display='flex'}}
function closeAvatar(){{document.getElementById('avatarModal').style.display='none'}}
function selectAvatar(a){{fetch('/api/update_avatar',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{avatar:a}})}}).then(()=>location.reload())}}
function removeFavorite(id){{fetch('/api/remove_favorite',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{hotel_id:id}})}}).then(()=>location.reload())}}
function markAsRead(id){{fetch('/api/mark_notification_read',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{notification_id:id}})}}).then(()=>location.reload())}}
function copyReferralLink() {{
    const link = document.querySelector('.referral-code').innerText;
    navigator.clipboard.writeText(window.location.origin + link);
    alert('Ссылка скопирована');
}}
function toggleTheme(){{document.body.classList.toggle('dark');localStorage.setItem('theme',document.body.classList.contains('dark')?'dark':'light')}}
if(localStorage.getItem('theme')==='dark')document.body.classList.add('dark')
</script>
</body>
</html>
''')


@app.post("/api/update_profile")
async def update_profile(full_name: str = Form(""), email: str = Form(""), phone: str = Form(""), session: str = Cookie(None)):
    username = get_current_user(session)
    if username and username in USERS:
        USERS[username]["full_name"] = full_name
        USERS[username]["email"] = email
        USERS[username]["phone"] = phone
    return RedirectResponse(url="/profile", status_code=303)


@app.post("/api/update_avatar")
async def update_avatar(data: dict, session: str = Cookie(None)):
    username = get_current_user(session)
    if username and username in USERS:
        USERS[username]["avatar"] = data.get("avatar", "👤")
    return {"success": True}


@app.post("/api/add_favorite")
async def add_favorite(data: dict, session: str = Cookie(None)):
    username = get_current_user(session)
    if username:
        if username not in FAVORITES:
            FAVORITES[username] = []
        FAVORITES[username].append({"hotel_id": data.get("hotel_id"), "hotel_name": data.get("hotel_name"), "city": data.get("city"), "price": data.get("price")})
    return {"success": True}


@app.post("/api/remove_favorite")
async def remove_favorite(data: dict, session: str = Cookie(None)):
    username = get_current_user(session)
    if username and username in FAVORITES:
        FAVORITES[username] = [f for f in FAVORITES[username] if f["hotel_id"] != data.get("hotel_id")]
    return {"success": True}


@app.post("/api/mark_notification_read")
async def mark_notification_read(data: dict, session: str = Cookie(None)):
    username = get_current_user(session)
    if username and username in NOTIFICATIONS:
        for n in NOTIFICATIONS[username]:
            if n["id"] == data.get("notification_id"):
                n["read"] = True
    return {"success": True}


@app.post("/api/save_booking")
async def save_booking(data: dict, session: str = Cookie(None)):
    username = get_current_user(session)
    if username:
        if username not in BOOKINGS:
            BOOKINGS[username] = []
        BOOKINGS[username].append(data)
        if username not in NOTIFICATIONS:
            NOTIFICATIONS[username] = []
        NOTIFICATIONS[username].append({"id": len(NOTIFICATIONS[username]) + 1, "icon": "✅", "title": "Тур успешно забронирован", "text": f"Ваш тур в {data['destination']} на {data['nights']} ночей подтвержден.", "date": datetime.now().strftime("%d.%m.%Y %H:%M"), "read": False})
    return {"success": True}


# ============= ПЛАТЁЖНАЯ СИСТЕМА (ДЕМО-РЕЖИМ) =============

@app.post("/api/initiate_payment")
async def initiate_payment(data: dict, session: str = Cookie(None)):
    """Имитация инициализации платежа"""
    username = get_current_user(session)
    if not username:
        return {"success": False, "error": "Не авторизован"}
    
    booking_id = data.get("booking_id")
    amount = data.get("amount")
    method = data.get("method")
    
    if not booking_id or not amount:
        return {"success": False, "error": "Не указаны данные платежа"}
    
    payment_id = secrets.token_hex(8)
    
    PAYMENTS[payment_id] = {
        "booking_id": booking_id,
        "amount": amount,
        "method": method,
        "status": "pending",
        "username": username,
        "created_at": datetime.now().isoformat()
    }
    
    return {"success": True, "payment_id": payment_id, "method": method}


@app.post("/api/confirm_payment")
async def confirm_payment(data: dict, session: str = Cookie(None)):
    """Подтверждение оплаты (демо-режим)"""
    username = get_current_user(session)
    if not username:
        return {"success": False, "error": "Не авторизован"}
    
    payment_id = data.get("payment_id")
    
    if not payment_id or payment_id not in PAYMENTS:
        return {"success": False, "error": "Платёж не найден"}
    
    payment = PAYMENTS[payment_id]
    payment["status"] = "completed"
    payment["completed_at"] = datetime.now().isoformat()
    
    if username not in NOTIFICATIONS:
        NOTIFICATIONS[username] = []
    NOTIFICATIONS[username].append({
        "id": len(NOTIFICATIONS[username]) + 1,
        "icon": "💳",
        "title": "Оплата прошла успешно",
        "text": f"Оплата тура на сумму {payment['amount']:,} ₽ подтверждена. Демо-режим.",
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "read": False
    })
    
    if username not in BOOKINGS:
        BOOKINGS[username] = []
    BOOKINGS[username].append({
        "destination": data.get("destination", ""),
        "nights": data.get("nights", 0),
        "start_date": data.get("start_date", ""),
        "end_date": data.get("end_date", ""),
        "hotel": data.get("hotel", ""),
        "flight_there": data.get("flight_there", ""),
        "flight_back": data.get("flight_back", ""),
        "total_price": payment["amount"],
        "payment_id": payment_id,
        "payment_status": "completed"
    })
    
    return {"success": True, "message": "Оплата успешно завершена (демо-режим)"}


@app.get("/api/get_payment_status/{payment_id}")
async def get_payment_status(payment_id: str, session: str = Cookie(None)):
    username = get_current_user(session)
    if not username:
        return {"success": False, "error": "Не авторизован"}
    
    if payment_id not in PAYMENTS:
        return {"success": False, "error": "Платёж не найден"}
    
    payment = PAYMENTS[payment_id]
    if payment["username"] != username:
        return {"success": False, "error": "Нет доступа"}
    
    return {"success": True, "status": payment["status"]}


# ============= АВТОРИЗАЦИЯ =============

@app.get("/login")
async def login_page():
    return HTMLResponse('''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Вход | SmartTravel</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .auth-card {
            background: white;
            border-radius: 32px;
            padding: 48px 40px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            transition: transform 0.2s;
        }
        .auth-card:hover { transform: translateY(-4px); }
        .auth-card h2 { font-size: 1.75rem; font-weight: 700; margin-bottom: 8px; color: #0f172a; }
        .auth-card .subtitle { color: #64748b; margin-bottom: 32px; font-size: 0.875rem; }
        .input-group { margin-bottom: 24px; }
        .input-group label { display: block; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; margin-bottom: 8px; }
        .input-group input { width: 100%; padding: 12px 16px; border: 1.5px solid #e2e8f0; border-radius: 16px; font-size: 0.875rem; transition: all 0.2s; outline: none; font-family: inherit; }
        .input-group input:focus { border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        .btn-auth { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 40px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; margin-top: 8px; }
        .btn-auth:hover { transform: translateY(-1px); box-shadow: 0 10px 20px -5px rgba(102,126,234,0.4); }
        .auth-footer { text-align: center; margin-top: 28px; font-size: 0.875rem; color: #64748b; }
        .auth-footer a { color: #667eea; text-decoration: none; font-weight: 600; }
        @media (max-width: 480px) { .auth-card { padding: 32px 24px; } .auth-card h2 { font-size: 1.5rem; } }
    </style>
</head>
<body>
    <div class="auth-card">
        <h2>Добро пожаловать</h2>
        <div class="subtitle">Войдите в свой аккаунт</div>
        <form action="/login" method="POST">
            <div class="input-group"><label>Имя пользователя</label><input type="text" name="username" placeholder="Введите имя" required></div>
            <div class="input-group"><label>Пароль</label><input type="password" name="password" placeholder="••••••••" required></div>
            <button type="submit" class="btn-auth">Войти</button>
        </form>
        <div class="auth-footer">Нет аккаунта? <a href="/register">Зарегистрироваться</a></div>
    </div>
</body>
</html>
''')


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    hashed = hash_password(password)
    if username in USERS and USERS[username]["password"] == hashed:
        token = create_session_token(username)
        resp = RedirectResponse(url="/", status_code=303)
        resp.set_cookie(key="session", value=token, httponly=True, max_age=86400)
        return resp
    return HTMLResponse('''
<!DOCTYPE html>
<html><head><title>Ошибка входа</title><style>
body{font-family:Segoe UI;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;justify-content:center;align-items:center;min-height:100vh}
.card{background:white;padding:40px;border-radius:24px;text-align:center}
a{color:#667eea;text-decoration:none}
</style></head>
<body><div class="card"><h2>Неверный логин или пароль</h2><a href="/login">Попробовать снова</a></div></body></html>
''')


@app.get("/register")
async def register_page():
    return HTMLResponse('''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Регистрация | SmartTravel</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .auth-card {
            background: white;
            border-radius: 32px;
            padding: 48px 40px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        }
        .auth-card h2 { font-size: 1.75rem; font-weight: 700; margin-bottom: 8px; color: #0f172a; }
        .auth-card .subtitle { color: #64748b; margin-bottom: 32px; font-size: 0.875rem; }
        .input-group { margin-bottom: 24px; }
        .input-group label { display: block; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; margin-bottom: 8px; }
        .input-group input { width: 100%; padding: 12px 16px; border: 1.5px solid #e2e8f0; border-radius: 16px; font-size: 0.875rem; outline: none; }
        .input-group input:focus { border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        .btn-auth { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 40px; font-size: 0.875rem; font-weight: 600; cursor: pointer; margin-top: 8px; }
        .auth-footer { text-align: center; margin-top: 28px; font-size: 0.875rem; color: #64748b; }
        .auth-footer a { color: #667eea; text-decoration: none; font-weight: 600; }
        @media (max-width: 480px) { .auth-card { padding: 32px 24px; } }
    </style>
</head>
<body>
    <div class="auth-card">
        <h2>Создать аккаунт</h2>
        <div class="subtitle">Начните планировать путешествия</div>
        <form action="/register" method="POST" id="registerForm">
            <input type="hidden" name="ref" id="refCode" value="">
            <div class="input-group"><label>Имя пользователя</label><input type="text" name="username" placeholder="Придумайте имя" required></div>
            <div class="input-group"><label>Email</label><input type="email" name="email" placeholder="your@email.com" required></div>
            <div class="input-group"><label>Пароль</label><input type="password" name="password" placeholder="••••••••" required></div>
            <button type="submit" class="btn-auth">Зарегистрироваться</button>
        </form>
        <div class="auth-footer">Уже есть аккаунт? <a href="/login">Войти</a></div>
    </div>
    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const refCode = urlParams.get('ref');
        if (refCode) {{
            document.getElementById('refCode').value = refCode;
        }}
    </script>
</body>
</html>
''')


@app.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...), ref: str = Form("")):
    if username in USERS:
        return HTMLResponse('''
<!DOCTYPE html>
<html><head><title>Ошибка</title><style>
body{font-family:Segoe UI;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;justify-content:center;align-items:center;min-height:100vh}
.card{background:white;padding:40px;border-radius:24px;text-align:center}
a{color:#667eea;text-decoration:none}
</style></head>
<body><div class="card"><h2>Пользователь уже существует</h2><a href="/register">Попробовать другое имя</a></div></body></html>
''')
    
    inviter = REFERRAL_LINKS.get(ref)
    if inviter and inviter in USERS:
        USER_BALANCES[inviter] = USER_BALANCES.get(inviter, 0) + REFERRAL_BONUS
        if inviter not in NOTIFICATIONS:
            NOTIFICATIONS[inviter] = []
        NOTIFICATIONS[inviter].append({
            "id": len(NOTIFICATIONS[inviter]) + 1,
            "icon": "🎁",
            "title": "Реферальный бонус",
            "text": f"Пользователь {username} зарегистрировался по вашей ссылке. +{REFERRAL_BONUS} бонусов",
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "read": False
        })
    
    USERS[username] = {
        "email": email,
        "password": hash_password(password),
        "full_name": username,
        "phone": "",
        "avatar": random.choice(AVATARS),
        "role": "user"
    }
    
    USER_BALANCES[username] = USER_BALANCES.get(username, 0) + REGISTRATION_BONUS
    REFERRAL_CODES[username] = generate_referral_code(username)
    REFERRAL_LINKS[REFERRAL_CODES[username]] = username
    
    token = create_session_token(username)
    resp = RedirectResponse(url="/", status_code=303)
    resp.set_cookie(key="session", value=token, httponly=True, max_age=86400)
    return resp


@app.get("/logout")
async def logout(session: str = Cookie(None)):
    remove_session(session)
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("session")
    return resp


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("SmartTravel Builder запущен")
    print("http://127.0.0.1:8000")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)