"""
cities.py - Данные о городах
"""

CITIES = {
    "Россия": {
        "Сочи": {"code": "AER", "airport": "Международный аэропорт Сочи (AER)", "lat": 43.5855, "lng": 39.7231, "zoom": 12, "has_sea": True, "distance_km": 1500},
        "Москва": {"code": "MOW", "airport": "Шереметьево, Домодедово, Внуково (MOW)", "lat": 55.7558, "lng": 37.6173, "zoom": 10, "has_sea": False, "distance_km": 0},
        "Санкт-Петербург": {"code": "LED", "airport": "Пулково (LED)", "lat": 59.9343, "lng": 30.3351, "zoom": 10, "has_sea": True, "distance_km": 700},
        "Казань": {"code": "KZN", "airport": "Международный аэропорт Казань (KZN)", "lat": 55.7887, "lng": 49.1221, "zoom": 10, "has_sea": False, "distance_km": 800},
        "Калининград": {"code": "KGD", "airport": "Храброво (KGD)", "lat": 54.7104, "lng": 20.4522, "zoom": 10, "has_sea": True, "distance_km": 1100}
    },
    "Турция": {
        "Стамбул": {"code": "IST", "airport": "Аэропорт Стамбул (IST)", "lat": 41.0082, "lng": 28.9784, "zoom": 10, "has_sea": True, "distance_km": 2200},
        "Анталья": {"code": "AYT", "airport": "Аэропорт Анталья (AYT)", "lat": 36.8969, "lng": 30.7133, "zoom": 10, "has_sea": True, "distance_km": 2400},
        "Аланья": {"code": "GZP", "airport": "Аэропорт Газипаша (GZP)", "lat": 36.5442, "lng": 31.9948, "zoom": 10, "has_sea": True, "distance_km": 2450},
        "Бодрум": {"code": "BJV", "airport": "Аэропорт Милас-Бодрум (BJV)", "lat": 37.0344, "lng": 27.4305, "zoom": 10, "has_sea": True, "distance_km": 2350},
        "Каппадокия": {"code": "NAV", "airport": "Аэропорт Невшехир (NAV)", "lat": 38.6436, "lng": 34.8291, "zoom": 9, "has_sea": False, "distance_km": 2300}
    },
    "Мальдивы": {
        "Мале": {"code": "MLE", "airport": "Международный аэропорт Мале (MLE)", "lat": 4.1755, "lng": 73.5093, "zoom": 10, "has_sea": True, "distance_km": 6500},
        "Ари Атолл": {"code": "MLE", "airport": "Трансфер на гидросамолете", "lat": 3.8642, "lng": 72.8342, "zoom": 9, "has_sea": True, "distance_km": 6600},
        "Баа Атолл": {"code": "MLE", "airport": "Трансфер на гидросамолете", "lat": 5.0875, "lng": 72.9431, "zoom": 9, "has_sea": True, "distance_km": 6650},
        "Нуну Атолл": {"code": "MLE", "airport": "Трансфер на гидросамолете", "lat": 5.9647, "lng": 73.3561, "zoom": 9, "has_sea": True, "distance_km": 6700},
        "Южный Мале": {"code": "MLE", "airport": "Трансфер на катере", "lat": 3.9431, "lng": 73.4567, "zoom": 10, "has_sea": True, "distance_km": 6550}
    },
    "Таиланд": {
        "Пхукет": {"code": "HKT", "airport": "Международный аэропорт Пхукет (HKT)", "lat": 7.8804, "lng": 98.3923, "zoom": 10, "has_sea": True, "distance_km": 7500},
        "Бангкок": {"code": "BKK", "airport": "Суварнабхуми (BKK)", "lat": 13.7563, "lng": 100.5018, "zoom": 10, "has_sea": False, "distance_km": 7300},
        "Паттайя": {"code": "UTP", "airport": "Утапао (UTP)", "lat": 12.9276, "lng": 100.8771, "zoom": 10, "has_sea": True, "distance_km": 7400},
        "Самуи": {"code": "USM", "airport": "Аэропорт Самуи (USM)", "lat": 9.5120, "lng": 100.0136, "zoom": 10, "has_sea": True, "distance_km": 7600},
        "Краби": {"code": "KBV", "airport": "Аэропорт Краби (KBV)", "lat": 8.0863, "lng": 98.9066, "zoom": 10, "has_sea": True, "distance_km": 7550}
    },
    "Египет": {
        "Хургада": {"code": "HRG", "airport": "Международный аэропорт Хургада (HRG)", "lat": 27.2579, "lng": 33.8126, "zoom": 10, "has_sea": True, "distance_km": 3200},
        "Шарм-эль-Шейх": {"code": "SSH", "airport": "Шарм-эль-Шейх (SSH)", "lat": 27.9158, "lng": 34.3299, "zoom": 10, "has_sea": True, "distance_km": 3300},
        "Каир": {"code": "CAI", "airport": "Международный аэропорт Каир (CAI)", "lat": 30.0444, "lng": 31.2357, "zoom": 10, "has_sea": False, "distance_km": 3000},
        "Луксор": {"code": "LXR", "airport": "Международный аэропорт Луксор (LXR)", "lat": 25.6833, "lng": 32.6500, "zoom": 10, "has_sea": False, "distance_km": 3100},
        "Марса-Алам": {"code": "RMF", "airport": "Марса-Алам (RMF)", "lat": 25.5567, "lng": 34.5889, "zoom": 10, "has_sea": True, "distance_km": 3400}
    },
    "ОАЭ": {
        "Дубай": {"code": "DXB", "airport": "Международный аэропорт Дубай (DXB)", "lat": 25.2048, "lng": 55.2708, "zoom": 10, "has_sea": True, "distance_km": 3800},
        "Абу-Даби": {"code": "AUH", "airport": "Абу-Даби (AUH)", "lat": 24.4539, "lng": 54.3773, "zoom": 10, "has_sea": True, "distance_km": 3900},
        "Шарджа": {"code": "SHJ", "airport": "Шарджа (SHJ)", "lat": 25.3463, "lng": 55.4209, "zoom": 10, "has_sea": True, "distance_km": 3850},
        "Рас-эль-Хайма": {"code": "RKT", "airport": "Рас-эль-Хайма (RKT)", "lat": 25.7915, "lng": 55.9432, "zoom": 10, "has_sea": True, "distance_km": 3950},
        "Фуджейра": {"code": "FJR", "airport": "Фуджейра (FJR)", "lat": 25.1288, "lng": 56.3265, "zoom": 10, "has_sea": True, "distance_km": 4000}
    },
    "Италия": {
        "Рим": {"code": "FCO", "airport": "Леонардо да Винчи (FCO)", "lat": 41.9028, "lng": 12.4964, "zoom": 10, "has_sea": True, "distance_km": 2400},
        "Венеция": {"code": "VCE", "airport": "Марко Поло (VCE)", "lat": 45.4408, "lng": 12.3155, "zoom": 10, "has_sea": True, "distance_km": 2300},
        "Флоренция": {"code": "FLR", "airport": "Перетола (FLR)", "lat": 43.7719, "lng": 11.2554, "zoom": 10, "has_sea": False, "distance_km": 2350},
        "Милан": {"code": "MXP", "airport": "Мальпенса (MXP)", "lat": 45.4642, "lng": 9.1900, "zoom": 10, "has_sea": False, "distance_km": 2250},
        "Неаполь": {"code": "NAP", "airport": "Неаполь (NAP)", "lat": 40.8518, "lng": 14.2681, "zoom": 10, "has_sea": True, "distance_km": 2450}
    },
    "Испания": {
        "Барселона": {"code": "BCN", "airport": "Эль-Прат (BCN)", "lat": 41.3851, "lng": 2.1734, "zoom": 10, "has_sea": True, "distance_km": 2800},
        "Мадрид": {"code": "MAD", "airport": "Барахас (MAD)", "lat": 40.4168, "lng": -3.7038, "zoom": 10, "has_sea": False, "distance_km": 2900},
        "Валенсия": {"code": "VLC", "airport": "Валенсия (VLC)", "lat": 39.4699, "lng": -0.3763, "zoom": 10, "has_sea": True, "distance_km": 2850},
        "Севилья": {"code": "SVQ", "airport": "Севилья (SVQ)", "lat": 37.3891, "lng": -5.9845, "zoom": 10, "has_sea": False, "distance_km": 2950},
        "Малага": {"code": "AGP", "airport": "Малага (AGP)", "lat": 36.7213, "lng": -4.4214, "zoom": 10, "has_sea": True, "distance_km": 3000}
    },
    "Греция": {
        "Афины": {"code": "ATH", "airport": "Элефтериос Венизелос (ATH)", "lat": 37.9838, "lng": 23.7275, "zoom": 10, "has_sea": True, "distance_km": 2300},
        "Санторини": {"code": "JTR", "airport": "Санторини (JTR)", "lat": 36.3932, "lng": 25.4615, "zoom": 10, "has_sea": True, "distance_km": 2400},
        "Крит (Ираклион)": {"code": "HER", "airport": "Ираклион (HER)", "lat": 35.3387, "lng": 25.1442, "zoom": 10, "has_sea": True, "distance_km": 2450},
        "Родос": {"code": "RHO", "airport": "Родос (RHO)", "lat": 36.4349, "lng": 28.2177, "zoom": 10, "has_sea": True, "distance_km": 2500},
        "Корфу": {"code": "CFU", "airport": "Корфу (CFU)", "lat": 39.6243, "lng": 19.9217, "zoom": 10, "has_sea": True, "distance_km": 2200}
    },
    "Кипр": {
        "Ларнака": {"code": "LCA", "airport": "Ларнака (LCA)", "lat": 34.9000, "lng": 33.6333, "zoom": 10, "has_sea": True, "distance_km": 2300},
        "Пафос": {"code": "PFO", "airport": "Пафос (PFO)", "lat": 34.7751, "lng": 32.4211, "zoom": 10, "has_sea": True, "distance_km": 2350},
        "Айя-Напа": {"code": "LCA", "airport": "Трансфер из Ларнаки", "lat": 34.9880, "lng": 34.0095, "zoom": 10, "has_sea": True, "distance_km": 2320},
        "Лимассол": {"code": "LCA", "airport": "Трансфер из Ларнаки", "lat": 34.6786, "lng": 33.0443, "zoom": 10, "has_sea": True, "distance_km": 2340},
        "Протарас": {"code": "LCA", "airport": "Трансфер из Ларнаки", "lat": 35.0085, "lng": 34.0581, "zoom": 10, "has_sea": True, "distance_km": 2330}
    }
}


def get_city_options():
    """Генерирует HTML для выбора города"""
    options = ""
    for country, cities in CITIES.items():
        options += f'<optgroup label="{country}">'
        for city in cities.keys():
            options += f'<option value="{city}">{city}</option>'
        options += '</optgroup>'
    return options


def get_city_data(city_name):
    """Возвращает данные о городе по названию"""
    for country, cities in CITIES.items():
        if city_name in cities:
            return cities[city_name]
    return None