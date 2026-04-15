"""
flights.py - Данные о билетах
"""

import random

AIRLINES = ["Аэрофлот", "S7 Airlines", "Turkish Airlines", "Emirates", "Qatar Airways"]

def generate_flights(distance_km):
    """Генерирует 5 вариантов билетов (Эконом/Бизнес/Первый)"""
    flights = []
    base_price = max(3000, int(distance_km * 1.5))
    
    for i in range(5):
        airline = AIRLINES[i % len(AIRLINES)]
        price = int(base_price * random.uniform(0.8, 1.2))
        hour = random.randint(6, 23)
        minute = random.choice([0, 30])
        duration_h = max(1, int(distance_km / 800) + random.randint(-1, 2))
        duration_h = max(1, min(12, duration_h))
        duration_m = random.choice([0, 30])
        stops = random.choice([0, 1, 2])
        flight_num = f"{airline[:2].upper()}{random.randint(100, 999)}"
        
        FLIGHT_CLASSES = [
            {"id": "economy", "name": "Эконом", "multiplier": 1.0, "baggage": "23 кг", "hand_luggage": "10 кг", "icon": "💺"},
            {"id": "business", "name": "Бизнес", "multiplier": 2.5, "baggage": "2 × 32 кг", "hand_luggage": "15 кг", "icon": "💼"},
            {"id": "first", "name": "Первый", "multiplier": 4.0, "baggage": "3 × 32 кг", "hand_luggage": "20 кг", "icon": "👑"}
        ]
        
        for flight_class in FLIGHT_CLASSES:
            class_price = int(price * flight_class["multiplier"])
            flights.append({
                "airline": airline,
                "flight_num": flight_num,
                "price": class_price,
                "time": f"{hour:02d}:{minute:02d}",
                "duration": f"{duration_h}ч {duration_m:02d}м",
                "stops": stops,
                "stops_text": "прямой" if stops == 0 else f"{stops} пересадк{'а' if stops == 1 else 'и'}",
                "class": flight_class["id"],
                "class_name": flight_class["name"],
                "class_icon": flight_class["icon"],
                "baggage": flight_class["baggage"],
                "hand_luggage": flight_class["hand_luggage"]
            })
    
    flights.sort(key=lambda x: x["price"])
    return flights[:15]  # 5 вариантов × 3 класса = 15


def get_flights(distance_km):
    """Получить билеты туда и обратно"""
    there = generate_flights(distance_km)
    back = generate_flights(int(distance_km * 0.9))
    return there, back