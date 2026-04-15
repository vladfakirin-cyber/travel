"""
attractions.py - Данные об экскурсиях с реальными координатами и фотографиями
"""

ATTRACTIONS_DB = {
    "Москва": [
        {"name": "Красная площадь", "desc": "Главная площадь страны", "price": 0, "duration": "1-2ч", "icon": "🏛️", "rating": 4.9, "lat": 55.7537, "lng": 37.6213, "image_folder": "krasnaya_ploshad", "images_count": 3},
        {"name": "Большой театр", "desc": "Знаменитый театр оперы и балета", "price": 1500, "duration": "2-3ч", "icon": "🎭", "rating": 4.8, "lat": 55.7602, "lng": 37.6185, "image_folder": "bolshoy_teatr", "images_count": 2},
        {"name": "Московский Кремль", "desc": "Древняя крепость", "price": 700, "duration": "2-3ч", "icon": "🏰", "rating": 4.9, "lat": 55.7516, "lng": 37.6178, "image_folder": "kremlin", "images_count": 3},
        {"name": "Третьяковская галерея", "desc": "Музей русского искусства", "price": 600, "duration": "3-4ч", "icon": "🖼️", "rating": 4.8, "lat": 55.7411, "lng": 37.6208, "image_folder": "tretyakovka", "images_count": 2},
        {"name": "Парк Горького", "desc": "Центральный парк", "price": 0, "duration": "2-3ч", "icon": "🌳", "rating": 4.7, "lat": 55.7285, "lng": 37.6015, "image_folder": "gorky_park", "images_count": 2}
    ],
    "Сочи": [
        {"name": "Олимпийский парк", "desc": "Главная спортивная арена", "price": 500, "duration": "2-3ч", "icon": "🏟️", "rating": 4.9, "lat": 43.4017, "lng": 39.9558, "image_folder": "olympic_park", "images_count": 3},
        {"name": "Сочи Парк", "desc": "Тематический парк", "price": 2500, "duration": "Весь день", "icon": "🎢", "rating": 4.8, "lat": 43.4100, "lng": 39.9630, "image_folder": "sochi_park", "images_count": 3},
        {"name": "Красная Поляна", "desc": "Горный курорт", "price": 1500, "duration": "Весь день", "icon": "⛰️", "rating": 4.9, "lat": 43.6789, "lng": 40.2123, "image_folder": "krasnaya_polyana", "images_count": 3},
        {"name": "Дендрарий", "desc": "Ботанический сад", "price": 300, "duration": "2-3ч", "icon": "🌳", "rating": 4.7, "lat": 43.5825, "lng": 39.7240, "image_folder": "dendrarium", "images_count": 2},
        {"name": "Морской порт", "desc": "Набережная и яхты", "price": 0, "duration": "1-2ч", "icon": "⛴️", "rating": 4.6, "lat": 43.5800, "lng": 39.7180, "image_folder": "sea_port", "images_count": 2}
    ],
    "Санкт-Петербург": [
        {"name": "Эрмитаж", "desc": "Знаменитый музей", "price": 700, "duration": "3-4ч", "icon": "🏛️", "rating": 4.9, "lat": 59.9410, "lng": 30.3130, "image_folder": "hermitage", "images_count": 3},
        {"name": "Петропавловская крепость", "desc": "Историческая крепость", "price": 500, "duration": "2-3ч", "icon": "🏰", "rating": 4.8, "lat": 59.9500, "lng": 30.3160, "image_folder": "petropavlovsk", "images_count": 3},
        {"name": "Невский проспект", "desc": "Главная улица", "price": 0, "duration": "2-3ч", "icon": "🚶", "rating": 4.7, "lat": 59.9360, "lng": 30.3310, "image_folder": "nevsky", "images_count": 2},
        {"name": "Исаакиевский собор", "desc": "Величественный собор", "price": 400, "duration": "1-2ч", "icon": "⛪", "rating": 4.8, "lat": 59.9340, "lng": 30.3060, "image_folder": "isaac", "images_count": 2},
        {"name": "Дворцовая площадь", "desc": "Главная площадь", "price": 0, "duration": "1-2ч", "icon": "🏛️", "rating": 4.9, "lat": 59.9390, "lng": 30.3160, "image_folder": "palace_square", "images_count": 2}
    ],
    "Казань": [
        {"name": "Казанский Кремль", "desc": "Главная достопримечательность", "price": 500, "duration": "2-3ч", "icon": "🏰", "rating": 4.9, "lat": 55.7990, "lng": 49.1050, "image_folder": "kazan_kremlin", "images_count": 3},
        {"name": "Кул-Шариф", "desc": "Главная мечеть", "price": 0, "duration": "1-2ч", "icon": "🕌", "rating": 4.8, "lat": 55.7980, "lng": 49.1040, "image_folder": "kul_sharif", "images_count": 2},
        {"name": "Баумана", "desc": "Пешеходная улица", "price": 0, "duration": "1-2ч", "icon": "🚶", "rating": 4.7, "lat": 55.7950, "lng": 49.1080, "image_folder": "baumana", "images_count": 2},
        {"name": "Старо-Татарская слобода", "desc": "Исторический район", "price": 0, "duration": "2-3ч", "icon": "🏘️", "rating": 4.6, "lat": 55.7830, "lng": 49.1150, "image_folder": "sloboda", "images_count": 2}
    ],
    "Стамбул": [
        {"name": "Айя-София", "desc": "Византийский собор", "price": 1500, "duration": "2-3ч", "icon": "⛪", "rating": 4.9, "lat": 41.0085, "lng": 28.9798, "image_folder": "hagia_sophia", "images_count": 3},
        {"name": "Голубая мечеть", "desc": "Действующая мечеть", "price": 0, "duration": "1-2ч", "icon": "🕌", "rating": 4.8, "lat": 41.0052, "lng": 28.9770, "image_folder": "blue_mosque", "images_count": 3},
        {"name": "Дворец Топкапы", "desc": "Резиденция султанов", "price": 1200, "duration": "3-4ч", "icon": "🏰", "rating": 4.9, "lat": 41.0125, "lng": 28.9838, "image_folder": "topkapi", "images_count": 3},
        {"name": "Гранд-Базар", "desc": "Старейший крытый рынок", "price": 0, "duration": "2-3ч", "icon": "🛍️", "rating": 4.7, "lat": 41.0110, "lng": 28.9685, "image_folder": "grand_bazaar", "images_count": 2},
        {"name": "Босфор", "desc": "Круиз на корабле", "price": 800, "duration": "2ч", "icon": "🚢", "rating": 4.8, "lat": 41.0380, "lng": 29.0040, "image_folder": "bosphorus", "images_count": 2}
    ],
    "Дубай": [
        {"name": "Бурдж Халифа", "desc": "Самое высокое здание", "price": 2000, "duration": "2ч", "icon": "🏙️", "rating": 4.9, "lat": 25.1972, "lng": 55.2744, "image_folder": "burj_khalifa", "images_count": 3},
        {"name": "Дубай Молл", "desc": "Крупнейший ТЦ", "price": 0, "duration": "3-4ч", "icon": "🛍️", "rating": 4.8, "lat": 25.1962, "lng": 55.2797, "image_folder": "dubai_mall", "images_count": 2},
        {"name": "Пальма Джумейра", "desc": "Искусственный остров", "price": 3000, "duration": "3ч", "icon": "🌴", "rating": 4.8, "lat": 25.1150, "lng": 55.1380, "image_folder": "palm_jumeirah", "images_count": 2},
        {"name": "Фонтан Дубая", "desc": "Танцующий фонтан", "price": 0, "duration": "30 мин", "icon": "💧", "rating": 4.9, "lat": 25.1947, "lng": 55.2736, "image_folder": "dubai_fountain", "images_count": 2}
    ],
    "Пхукет": [
        {"name": "Большой Будда", "desc": "45-метровая статуя", "price": 0, "duration": "1-2ч", "icon": "🙏", "rating": 4.7, "lat": 7.8277, "lng": 98.3127, "image_folder": "big_buddha", "images_count": 3},
        {"name": "Старый Пхукет", "desc": "Китайско-португальская архитектура", "price": 0, "duration": "2-3ч", "icon": "🏘️", "rating": 4.6, "lat": 7.8860, "lng": 98.3895, "image_folder": "old_phuket", "images_count": 2},
        {"name": "Пляж Патонг", "desc": "Главный пляж", "price": 0, "duration": "2-3ч", "icon": "🏖️", "rating": 4.5, "lat": 7.8962, "lng": 98.2987, "image_folder": "patong_beach", "images_count": 2}
    ]
}


def get_attractions(city_name):
    """Получить экскурсии для города с локальными фотографиями"""
    if city_name in ATTRACTIONS_DB:
        attractions = ATTRACTIONS_DB[city_name]
        # Добавляем пути к локальным изображениям
        for attr in attractions:
            folder = attr["image_folder"]
            count = attr.get("images_count", 3)
            attr["images"] = [f"/static/images/attractions/{folder}/{i}.jpg" for i in range(1, count + 1)]
        return attractions
    
    # Если город не найден, возвращаем пустой список
    return []