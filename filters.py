"""
filters.py - Данные для фильтров
"""

MEAL_TYPES = [
    {"id": "RO", "name": "Без питания", "icon": "🍽️"},
    {"id": "BB", "name": "Завтрак", "icon": "🥐"},
    {"id": "HB", "name": "Полупансион", "icon": "🍳"},
    {"id": "FB", "name": "Полный пансион", "icon": "🍽️🍽️"},
    {"id": "AI", "name": "Всё включено", "icon": "🍹"}
]

DISTANCE_TO_SEA = [
    {"id": "0-100", "name": "до 100 м", "icon": "🏖️"},
    {"id": "100-500", "name": "100-500 м", "icon": "🏖️🚶"},
    {"id": "500-1000", "name": "500-1000 м", "icon": "🚶"},
    {"id": "1000+", "name": "более 1 км", "icon": "🚗"}
]

AMENITIES = [
    {"id": "pool", "name": "Бассейн", "icon": "🏊"},
    {"id": "spa", "name": "СПА", "icon": "💆"},
    {"id": "wifi", "name": "Wi-Fi", "icon": "📶"},
    {"id": "parking", "name": "Парковка", "icon": "🅿️"},
    {"id": "transfer", "name": "Трансфер", "icon": "🚌"},
    {"id": "kids_club", "name": "Детский клуб", "icon": "🧸"}
]

RATINGS = [
    {"id": "4.5", "name": "4.5+", "icon": "⭐"},
    {"id": "4.0", "name": "4.0+", "icon": "⭐"},
    {"id": "3.5", "name": "3.5+", "icon": "⭐"}
]

HOLIDAY_TYPES = [
    {"id": "family", "name": "Семейный", "icon": "👨‍👩‍👧"},
    {"id": "romantic", "name": "Романтический", "icon": "💕"},
    {"id": "youth", "name": "Молодёжный", "icon": "🎉"},
    {"id": "sports", "name": "Спортивный", "icon": "⚽"},
    {"id": "spa", "name": "СПА-отдых", "icon": "💆‍♀️"}
]


def get_filter_options():
    """Генерация HTML для фильтров"""
    
    meal_html = '<div class="filter-group"><label>🍽️ Тип питания</label><div class="filter-buttons">'
    for meal in MEAL_TYPES:
        meal_html += f'<button type="button" class="filter-btn" data-filter="meal_type" data-value="{meal["id"]}">{meal["icon"]} {meal["name"]}</button>'
    meal_html += '</div></div>'
    
    distance_html = '<div class="filter-group"><label>🏖️ Расстояние до моря</label><div class="filter-buttons">'
    for dist in DISTANCE_TO_SEA:
        distance_html += f'<button type="button" class="filter-btn" data-filter="distance" data-value="{dist["id"]}">{dist["icon"]} {dist["name"]}</button>'
    distance_html += '</div></div>'
    
    amenities_html = '<div class="filter-group"><label>✨ Удобства</label><div class="filter-buttons">'
    for amenity in AMENITIES:
        amenities_html += f'<button type="button" class="filter-btn" data-filter="amenity" data-value="{amenity["id"]}">{amenity["icon"]} {amenity["name"]}</button>'
    amenities_html += '</div></div>'
    
    rating_html = '<div class="filter-group"><label>⭐ Рейтинг</label><div class="filter-buttons">'
    for rating in RATINGS:
        rating_html += f'<button type="button" class="filter-btn" data-filter="rating" data-value="{rating["id"]}">{rating["icon"]} {rating["name"]}</button>'
    rating_html += '</div></div>'
    
    holiday_html = '<div class="filter-group"><label>🎯 Тип отдыха</label><div class="filter-buttons">'
    for holiday in HOLIDAY_TYPES:
        holiday_html += f'<button type="button" class="filter-btn" data-filter="holiday" data-value="{holiday["id"]}">{holiday["icon"]} {holiday["name"]}</button>'
    holiday_html += '</div></div>'
    
    return meal_html + distance_html + amenities_html + rating_html + holiday_html