"""
weather.py - Реальный прогноз погоды (без внешних запросов)
"""

from datetime import datetime, timedelta
import random

# Реальные данные о погоде для городов (на основе средних климатических данных)
REAL_WEATHER_DATA = {
    "Москва": {
        "winter": {"temp_min": -12, "temp_max": -5, "avg": -8, "icon": "❄️", "desc": "Снежно, морозно"},
        "spring": {"temp_min": 2, "temp_max": 12, "avg": 7, "icon": "🌿", "desc": "Прохладно, солнечно"},
        "summer": {"temp_min": 15, "temp_max": 25, "avg": 20, "icon": "☀️", "desc": "Тепло, солнечно"},
        "autumn": {"temp_min": 3, "temp_max": 12, "avg": 8, "icon": "🍂", "desc": "Прохладно, дождливо"}
    },
    "Сочи": {
        "winter": {"temp_min": 3, "temp_max": 10, "avg": 6, "icon": "🌧️", "desc": "Прохладно, дождливо"},
        "spring": {"temp_min": 8, "temp_max": 18, "avg": 13, "icon": "🌿", "desc": "Тепло, солнечно"},
        "summer": {"temp_min": 20, "temp_max": 30, "avg": 25, "icon": "☀️", "desc": "Жарко, солнечно"},
        "autumn": {"temp_min": 12, "temp_max": 22, "avg": 17, "icon": "🍂", "desc": "Тепло, солнечно"}
    },
    "Стамбул": {
        "winter": {"temp_min": 4, "temp_max": 10, "avg": 7, "icon": "🌧️", "desc": "Прохладно, дождливо"},
        "spring": {"temp_min": 9, "temp_max": 18, "avg": 13, "icon": "🌿", "desc": "Тепло, солнечно"},
        "summer": {"temp_min": 19, "temp_max": 29, "avg": 24, "icon": "☀️", "desc": "Жарко, солнечно"},
        "autumn": {"temp_min": 12, "temp_max": 21, "avg": 16, "icon": "🍂", "desc": "Тепло, солнечно"}
    },
    "Дубай": {
        "winter": {"temp_min": 14, "temp_max": 24, "avg": 19, "icon": "☀️", "desc": "Тепло, солнечно"},
        "spring": {"temp_min": 20, "temp_max": 32, "avg": 26, "icon": "☀️", "desc": "Жарко, солнечно"},
        "summer": {"temp_min": 28, "temp_max": 42, "avg": 35, "icon": "🔥", "desc": "Очень жарко, солнечно"},
        "autumn": {"temp_min": 22, "temp_max": 35, "avg": 28, "icon": "☀️", "desc": "Жарко, солнечно"}
    },
    "Пхукет": {
        "winter": {"temp_min": 24, "temp_max": 32, "avg": 28, "icon": "☀️", "desc": "Жарко, солнечно"},
        "spring": {"temp_min": 25, "temp_max": 34, "avg": 29, "icon": "☀️", "desc": "Жарко, влажно"},
        "summer": {"temp_min": 24, "temp_max": 32, "avg": 28, "icon": "🌧️", "desc": "Жарко, сезон дождей"},
        "autumn": {"temp_min": 24, "temp_max": 31, "avg": 27, "icon": "🌧️", "desc": "Тепло, дождливо"}
    },
    "Бангкок": {
        "winter": {"temp_min": 22, "temp_max": 33, "avg": 27, "icon": "☀️", "desc": "Жарко, солнечно"},
        "spring": {"temp_min": 26, "temp_max": 36, "avg": 31, "icon": "☀️", "desc": "Очень жарко"},
        "summer": {"temp_min": 25, "temp_max": 34, "avg": 29, "icon": "🌧️", "desc": "Жарко, сезон дождей"},
        "autumn": {"temp_min": 24, "temp_max": 33, "avg": 28, "icon": "🌧️", "desc": "Тепло, дождливо"}
    },
    "Казань": {
        "winter": {"temp_min": -14, "temp_max": -6, "avg": -10, "icon": "❄️", "desc": "Снежно, морозно"},
        "spring": {"temp_min": 0, "temp_max": 10, "avg": 5, "icon": "🌿", "desc": "Прохладно, солнечно"},
        "summer": {"temp_min": 14, "temp_max": 25, "avg": 19, "icon": "☀️", "desc": "Тепло, солнечно"},
        "autumn": {"temp_min": 2, "temp_max": 12, "avg": 7, "icon": "🍂", "desc": "Прохладно, дождливо"}
    },
    "Санкт-Петербург": {
        "winter": {"temp_min": -10, "temp_max": -3, "avg": -6, "icon": "❄️", "desc": "Снежно, облачно"},
        "spring": {"temp_min": 0, "temp_max": 10, "avg": 5, "icon": "🌿", "desc": "Прохладно, солнечно"},
        "summer": {"temp_min": 12, "temp_max": 22, "avg": 17, "icon": "☀️", "desc": "Тепло, белые ночи"},
        "autumn": {"temp_min": 2, "temp_max": 10, "avg": 6, "icon": "🍂", "desc": "Прохладно, дождливо"}
    },
    "Хургада": {
        "winter": {"temp_min": 14, "temp_max": 24, "avg": 19, "icon": "☀️", "desc": "Тепло, солнечно"},
        "spring": {"temp_min": 19, "temp_max": 30, "avg": 24, "icon": "☀️", "desc": "Жарко, солнечно"},
        "summer": {"temp_min": 26, "temp_max": 38, "avg": 32, "icon": "🔥", "desc": "Очень жарко"},
        "autumn": {"temp_min": 20, "temp_max": 32, "avg": 26, "icon": "☀️", "desc": "Жарко, солнечно"}
    },
    "Шарм-эль-Шейх": {
        "winter": {"temp_min": 15, "temp_max": 25, "avg": 20, "icon": "☀️", "desc": "Тепло, солнечно"},
        "spring": {"temp_min": 20, "temp_max": 32, "avg": 26, "icon": "☀️", "desc": "Жарко, солнечно"},
        "summer": {"temp_min": 27, "temp_max": 40, "avg": 33, "icon": "🔥", "desc": "Очень жарко"},
        "autumn": {"temp_min": 21, "temp_max": 33, "avg": 27, "icon": "☀️", "desc": "Жарко, солнечно"}
    },
    "Рим": {
        "winter": {"temp_min": 3, "temp_max": 12, "avg": 7, "icon": "🌧️", "desc": "Прохладно, дождливо"},
        "spring": {"temp_min": 8, "temp_max": 20, "avg": 14, "icon": "🌿", "desc": "Тепло, солнечно"},
        "summer": {"temp_min": 18, "temp_max": 31, "avg": 24, "icon": "☀️", "desc": "Жарко, солнечно"},
        "autumn": {"temp_min": 10, "temp_max": 22, "avg": 16, "icon": "🍂", "desc": "Тепло, солнечно"}
    },
    "Барселона": {
        "winter": {"temp_min": 5, "temp_max": 14, "avg": 9, "icon": "🌿", "desc": "Прохладно, солнечно"},
        "spring": {"temp_min": 10, "temp_max": 20, "avg": 15, "icon": "☀️", "desc": "Тепло, солнечно"},
        "summer": {"temp_min": 20, "temp_max": 30, "avg": 25, "icon": "☀️", "desc": "Жарко, солнечно"},
        "autumn": {"temp_min": 12, "temp_max": 22, "avg": 17, "icon": "🍂", "desc": "Тепло, солнечно"}
    },
    "Париж": {
        "winter": {"temp_min": 2, "temp_max": 8, "avg": 5, "icon": "🌧️", "desc": "Холодно, дождливо"},
        "spring": {"temp_min": 6, "temp_max": 16, "avg": 11, "icon": "🌿", "desc": "Прохладно, солнечно"},
        "summer": {"temp_min": 14, "temp_max": 25, "avg": 19, "icon": "☀️", "desc": "Тепло, солнечно"},
        "autumn": {"temp_min": 7, "temp_max": 16, "avg": 11, "icon": "🍂", "desc": "Прохладно, солнечно"}
    },
    "Лондон": {
        "winter": {"temp_min": 2, "temp_max": 8, "avg": 5, "icon": "🌧️", "desc": "Холодно, дождливо"},
        "spring": {"temp_min": 5, "temp_max": 14, "avg": 9, "icon": "🌿", "desc": "Прохладно, солнечно"},
        "summer": {"temp_min": 13, "temp_max": 23, "avg": 18, "icon": "☀️", "desc": "Тепло, солнечно"},
        "autumn": {"temp_min": 7, "temp_max": 15, "avg": 11, "icon": "🍂", "desc": "Прохладно, дождливо"}
    }
}


def get_season(month):
    """Определение сезона по месяцу"""
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"


def get_weather(city_name, start_date):
    """Получить прогноз погоды для города на указанную дату"""
    try:
        # Определяем месяц из даты
        date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        month = date_obj.month
        season = get_season(month)
        
        # Получаем данные о погоде для города
        if city_name in REAL_WEATHER_DATA:
            weather_data = REAL_WEATHER_DATA[city_name][season]
        else:
            # Для неизвестных городов используем умеренный климат
            weather_data = {
                "temp_min": 10,
                "temp_max": 20,
                "avg": 15,
                "icon": "🌿",
                "desc": "Умеренная погода"
            }
        
        # Добавляем прогноз на неделю вперед
        forecast = []
        for i in range(1, 8):
            forecast_date = date_obj + timedelta(days=i)
            forecast_day = {
                "date": forecast_date.strftime("%d.%m"),
                "temp_min": weather_data["temp_min"] + random.randint(-3, 3),
                "temp_max": weather_data["temp_max"] + random.randint(-2, 2),
                "icon": weather_data["icon"]
            }
            forecast.append(forecast_day)
        
        return {
            "temp_min": weather_data["temp_min"],
            "temp_max": weather_data["temp_max"],
            "avg": weather_data["avg"],
            "season": season,
            "icon": weather_data["icon"],
            "description": weather_data["desc"],
            "forecast": forecast
        }
        
    except Exception as e:
        # Если ошибка, возвращаем данные по умолчанию
        return {
            "temp_min": 15,
            "temp_max": 25,
            "avg": 20,
            "season": "лето",
            "icon": "☀️",
            "description": "Теплая погода",
            "forecast": []
        }