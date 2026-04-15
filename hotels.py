"""
hotels.py - Данные об отелях с локальными изображениями
"""

import random

# Аэропорты вылета
AIRPORTS_DEPARTURE = [
    {"code": "SVO", "name": "Шереметьево (SVO)"},
    {"code": "DME", "name": "Домодедово (DME)"},
    {"code": "VKO", "name": "Внуково (VKO)"},
    {"code": "ZIA", "name": "Жуковский (ZIA)"}
]

# Реальные отели с координатами
REAL_HOTELS = {
    "Москва": [
        {"name": "Ararat Park Hyatt Moscow", "price": 48000, "stars": 5, "desc": "Роскошный отель в центре Москвы. Вид на Большой театр.", "lat": 55.7602, "lng": 37.6098},
        {"name": "Four Seasons Moscow", "price": 55000, "stars": 5, "desc": "Отель на Манежной площади. Историческое здание.", "lat": 55.7560, "lng": 37.6175},
        {"name": "Lotte Hotel Moscow", "price": 52000, "stars": 5, "desc": "Премиальный отель. Лучший СПА в городе.", "lat": 55.7584, "lng": 37.5850},
        {"name": "St. Regis Moscow", "price": 48000, "stars": 5, "desc": "Элегантный отель на Патриарших прудах.", "lat": 55.7648, "lng": 37.5896},
        {"name": "Moscow Marriott Grand", "price": 18000, "stars": 4, "desc": "Отель на Тверской. Рядом метро.", "lat": 55.7664, "lng": 37.6025},
        {"name": "Hilton Moscow Leningradskaya", "price": 16000, "stars": 4, "desc": "Отель в сталинской высотке.", "lat": 55.7742, "lng": 37.6533},
        {"name": "Radisson Blu Belorusskaya", "price": 14000, "stars": 4, "desc": "Отель рядом с Белорусским вокзалом.", "lat": 55.7762, "lng": 37.5808},
        {"name": "Ibis Moscow Centre", "price": 6500, "stars": 3, "desc": "Бюджетный отель в центре.", "lat": 55.7625, "lng": 37.6275},
        {"name": "Izmailovo Hotel", "price": 3500, "stars": 3, "desc": "Крупнейший отель Европы.", "lat": 55.7915, "lng": 37.7496},
        {"name": "Novotel Moscow City", "price": 12000, "stars": 4, "desc": "Отель в деловом центре Москва-Сити.", "lat": 55.7493, "lng": 37.5404}
    ],
    "Санкт-Петербург": [
        {"name": "Four Seasons Lion Palace", "price": 50000, "stars": 5, "desc": "Роскошный отель в историческом здании у Исаакиевского собора.", "lat": 59.9343, "lng": 30.3092},
        {"name": "Belmond Grand Hotel Europe", "price": 45000, "stars": 5, "desc": "Знаменитый отель на Невском проспекте. Исторический люкс.", "lat": 59.9360, "lng": 30.3315},
        {"name": "W Hotel St. Petersburg", "price": 32000, "stars": 5, "desc": "Современный дизайн-отель на Вознесенском проспекте.", "lat": 59.9296, "lng": 30.3119},
        {"name": "Sofitel St. Petersburg", "price": 25000, "stars": 5, "desc": "Элегантный отель французского бренда.", "lat": 59.9285, "lng": 30.3289},
        {"name": "Corinthia Hotel St. Petersburg", "price": 22000, "stars": 5, "desc": "Отель класса люкс на Невском проспекте.", "lat": 59.9324, "lng": 30.3494},
        {"name": "Angleterre Hotel", "price": 18000, "stars": 4, "desc": "Знаменитый отель с видом на Исаакиевский собор.", "lat": 59.9328, "lng": 30.3081},
        {"name": "Astoria Hotel", "price": 28000, "stars": 5, "desc": "Легендарный отель, историческое здание.", "lat": 59.9325, "lng": 30.3095},
        {"name": "Sokos Hotel Vasilievsky", "price": 12000, "stars": 4, "desc": "Уютный отель на Васильевском острове.", "lat": 59.9442, "lng": 30.2758},
        {"name": "Park Inn by Radisson Nevsky", "price": 11000, "stars": 4, "desc": "Отель на Невском проспекте, рядом с Московским вокзалом.", "lat": 59.9303, "lng": 30.3617},
        {"name": "Indigo St. Petersburg", "price": 13000, "stars": 4, "desc": "Стильный отель на Невском проспекте.", "lat": 59.9325, "lng": 30.3417}
    ],
    "Казань": [
        {"name": "Riviera Kazan", "price": 21000, "stars": 5, "desc": "Отель с аквапарком на берегу реки Казанки.", "lat": 55.8052, "lng": 49.1024},
        {"name": "Mirage Hotel Kazan", "price": 19000, "stars": 5, "desc": "Роскошный отель в центре города.", "lat": 55.7932, "lng": 49.1203},
        {"name": "Kazan Palace by Tasigo", "price": 18000, "stars": 5, "desc": "Отель в центре, недалеко от Кремля.", "lat": 55.7985, "lng": 49.1064},
        {"name": "Ramada Kazan City Centre", "price": 12000, "stars": 4, "desc": "Отель в историческом центре города.", "lat": 55.7908, "lng": 49.1220},
        {"name": "Courtyard by Marriott Kazan", "price": 13000, "stars": 4, "desc": "Современный отель в деловом центре.", "lat": 55.8021, "lng": 49.1272},
        {"name": "Ibis Kazan", "price": 7000, "stars": 3, "desc": "Бюджетный отель в центре города.", "lat": 55.7993, "lng": 49.1054},
        {"name": "Shalyapin Palace Hotel", "price": 15000, "stars": 4, "desc": "Отель в стиле сталинского ампира.", "lat": 55.7955, "lng": 49.1078},
        {"name": "Hayal Hotel", "price": 11000, "stars": 4, "desc": "Отель в центре, удобное расположение.", "lat": 55.7942, "lng": 49.1147},
        {"name": "Bilyar Palace", "price": 10000, "stars": 4, "desc": "Отель с восточным колоритом.", "lat": 55.8025, "lng": 49.1403},
        {"name": "Tatarstan Hotel", "price": 8000, "stars": 3, "desc": "Отель в центре, рядом с Кремлем.", "lat": 55.7981, "lng": 49.1102}
    ],
    "Сочи": [
        {"name": "Grand Hotel Polyana", "price": 25000, "stars": 5, "desc": "Роскошный отель в горах Красной Поляны.", "lat": 43.6789, "lng": 40.2123},
        {"name": "Bridge Resort", "price": 22000, "stars": 5, "desc": "Отель с собственным пляжем и аквапарком.", "lat": 43.5850, "lng": 39.7245},
        {"name": "Mercure Sochi Center", "price": 11000, "stars": 4, "desc": "Современный отель в центре Сочи.", "lat": 43.5855, "lng": 39.7235},
        {"name": "Sea Galaxy Hotel", "price": 9500, "stars": 4, "desc": "Отель на первой линии у моря.", "lat": 43.5902, "lng": 39.7250},
        {"name": "Radisson Blu Resort", "price": 22000, "stars": 5, "desc": "Премиальный курорт.", "lat": 43.4240, "lng": 39.9269},
        {"name": "Hyatt Regency Sochi", "price": 20000, "stars": 5, "desc": "Элегантный отель на берегу моря.", "lat": 43.4196, "lng": 39.9331},
        {"name": "Park Inn by Radisson", "price": 8500, "stars": 4, "desc": "Уютный отель рядом с парком.", "lat": 43.5878, "lng": 39.7220},
        {"name": "Boutique Hotel Sochi", "price": 3800, "stars": 3, "desc": "Мини-отель в тихом центре.", "lat": 43.5801, "lng": 39.7275},
        {"name": "Zhemchuzhina Hotel", "price": 4500, "stars": 3, "desc": "Бюджетный вариант в центре.", "lat": 43.5835, "lng": 39.7200},
        {"name": "Rosa Khutor Grand Hotel", "price": 28000, "stars": 5, "desc": "Отель в Красной Поляне.", "lat": 43.6792, "lng": 40.2058}
    ],
    "Дубай": [
        {"name": "Burj Al Arab Jumeirah", "price": 120000, "stars": 5, "desc": "Самый роскошный отель мира. Форма паруса.", "lat": 25.1410, "lng": 55.1850},
        {"name": "Atlantis The Palm", "price": 55000, "stars": 5, "desc": "Отель на острове Пальма. Аквапарк.", "lat": 25.1308, "lng": 55.1163},
        {"name": "Armani Hotel Dubai", "price": 48000, "stars": 5, "desc": "Отель в Бурдж Халифа.", "lat": 25.1972, "lng": 55.2744},
        {"name": "Jumeirah Beach Hotel", "price": 42000, "stars": 5, "desc": "Отель в форме волны.", "lat": 25.1400, "lng": 55.1910},
        {"name": "Address Downtown", "price": 38000, "stars": 5, "desc": "Отель рядом с фонтанами.", "lat": 25.1954, "lng": 55.2794},
        {"name": "Rove Downtown", "price": 15000, "stars": 4, "desc": "Современный отель.", "lat": 25.1930, "lng": 55.2740},
        {"name": "Ibis Dubai", "price": 8000, "stars": 3, "desc": "Бюджетный вариант.", "lat": 25.2522, "lng": 55.2978},
        {"name": "Premier Inn Dubai", "price": 9000, "stars": 3, "desc": "Хороший бюджетный отель.", "lat": 25.2560, "lng": 55.3050},
        {"name": "Hilton Dubai Jumeirah", "price": 35000, "stars": 5, "desc": "Отель на пляже.", "lat": 25.0760, "lng": 55.1390},
        {"name": "Park Hyatt Dubai", "price": 40000, "stars": 5, "desc": "Роскошный курорт.", "lat": 25.2420, "lng": 55.3290}
    ],
    "Стамбул": [
        {"name": "Ciragan Palace Kempinski", "price": 55000, "stars": 5, "desc": "Бывший дворец султана.", "lat": 41.0440, "lng": 29.0210},
        {"name": "Four Seasons Bosphorus", "price": 48000, "stars": 5, "desc": "Роскошный отель с видом на пролив.", "lat": 41.0389, "lng": 29.0006},
        {"name": "Hagia Sophia Mansions", "price": 35000, "stars": 5, "desc": "Отель с видом на Айя-Софию.", "lat": 41.0082, "lng": 28.9784},
        {"name": "Swissotel The Bosphorus", "price": 32000, "stars": 5, "desc": "Современный отель с видом на Босфор.", "lat": 41.0520, "lng": 29.0100},
        {"name": "InterContinental Istanbul", "price": 28000, "stars": 5, "desc": "Отель в центре города.", "lat": 41.0660, "lng": 28.9950},
        {"name": "Sultanhan Hotel", "price": 15000, "stars": 4, "desc": "Уютный отель в историческом районе.", "lat": 41.0100, "lng": 28.9740},
        {"name": "DoubleTree by Hilton", "price": 12000, "stars": 4, "desc": "Современный отель.", "lat": 41.0220, "lng": 28.9700},
        {"name": "Holiday Inn Istanbul", "price": 10000, "stars": 4, "desc": "Бюджетный вариант.", "lat": 41.0180, "lng": 28.9750},
        {"name": "Istanbul Golden City", "price": 6000, "stars": 3, "desc": "Бюджетный отель в центре.", "lat": 41.0150, "lng": 28.9600},
        {"name": "Hotel Amira Istanbul", "price": 11000, "stars": 4, "desc": "Отель в османском стиле.", "lat": 41.0090, "lng": 28.9770}
    ],
    "Пхукет": [
        {"name": "Anantara Phuket", "price": 35000, "stars": 5, "desc": "Роскошный курорт на пляже.", "lat": 7.9964, "lng": 98.2973},
        {"name": "Rosewood Phuket", "price": 48000, "stars": 5, "desc": "Ультра-роскошный отель.", "lat": 7.9429, "lng": 98.2934},
        {"name": "The Shore at Katathani", "price": 32000, "stars": 5, "desc": "Виллы с частным бассейном.", "lat": 7.8225, "lng": 98.3713},
        {"name": "Holiday Inn Resort", "price": 18000, "stars": 4, "desc": "Идеально для семей с детьми.", "lat": 7.8915, "lng": 98.3040},
        {"name": "Centara Grand Beach", "price": 28000, "stars": 5, "desc": "Премиальный курорт.", "lat": 7.8456, "lng": 98.2932},
        {"name": "Amari Phuket", "price": 20000, "stars": 4, "desc": "Вид на море.", "lat": 7.8842, "lng": 98.3812},
        {"name": "Novotel Phuket", "price": 12000, "stars": 4, "desc": "Современный отель.", "lat": 7.8952, "lng": 98.3123},
        {"name": "Patong Beach Hotel", "price": 10000, "stars": 4, "desc": "Отель на пляже.", "lat": 7.8962, "lng": 98.2987},
        {"name": "Baan Laimai Beach Resort", "price": 9000, "stars": 4, "desc": "Бюджетный курорт.", "lat": 7.8945, "lng": 98.3012},
        {"name": "Andaman Embrace", "price": 11000, "stars": 4, "desc": "Уютный отель.", "lat": 7.8968, "lng": 98.2995}
    ]
}


def get_hotels_for_city(city_name):
    """Получить отели для города с реальными координатами"""
    city_mapping = {
        "Москва": "Москва",
        "Санкт-Петербург": "Санкт-Петербург",
        "Казань": "Казань",
        "Сочи": "Сочи",
        "Стамбул": "Стамбул",
        "Дубай": "Дубай",
        "Пхукет": "Пхукет",
        "Бангкок": "Пхукет",
        "Турция": "Стамбул",
        "ОАЭ": "Дубай",
        "Таиланд": "Пхукет"
    }
    
    city_key = city_mapping.get(city_name, city_name)
    
    if city_key in REAL_HOTELS:
        hotels = REAL_HOTELS[city_key]
        # Добавляем путь к локальному изображению
        for hotel in hotels:
            filename = hotel['name'].replace(' ', '_').replace('★', '').replace('⭐', '').strip()
            hotel["image"] = f"/static/images/hotels/{filename}.jpg"
        return hotels
    
    # Если город не найден, генерируем отели со случайными координатами
    hotels = []
    center_lat = 55.7558
    center_lng = 37.6173
    for i in range(10):
        stars = random.choice([3, 4, 5])
        price = random.randint(3000, 50000)
        name = f"{['Бюджетный', 'Комфортный', 'Премиальный'][stars-3]} {city_name} Hotel"
        
        hotels.append({
            "name": name,
            "price": price,
            "stars": stars,
            "desc": f"{['Бюджетный', 'Комфортабельный', 'Роскошный'][stars-3]} отель в центре {city_name}",
            "image": f"/static/images/hotels/default_{stars}_star.jpg",
            "lat": center_lat + random.uniform(-0.05, 0.05),
            "lng": center_lng + random.uniform(-0.05, 0.05)
        })
    
    return hotels