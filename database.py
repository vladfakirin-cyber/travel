"""
database.py - Работа с базой данных SQLite
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

# Создаём подключение к БД (файл travel.db в папке проекта)
engine = create_engine('sqlite:///travel.db', echo=False, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# ============= МОДЕЛИ БАЗЫ ДАННЫХ =============

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, default="")
    phone = Column(String, default="")
    avatar = Column(String, default="👤")
    role = Column(String, default="user")
    balance = Column(Integer, default=0)
    referral_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Связи
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    destination = Column(String, nullable=False)
    nights = Column(Integer, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    hotel = Column(String, nullable=False)
    flight_there = Column(String, nullable=False)
    flight_back = Column(String, nullable=False)
    total_price = Column(Integer, nullable=False)
    booking_date = Column(DateTime, default=datetime.now)
    status = Column(String, default="confirmed")
    
    user = relationship("User", back_populates="bookings")


class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    hotel_id = Column(String, nullable=False)
    hotel_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    user = relationship("User", back_populates="favorites")


class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    icon = Column(String, default="✅")
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    date = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="notifications")


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    hotel_id = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    date = Column(String, nullable=False)
    
    user = relationship("User", back_populates="reviews")


class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    payment_id = Column(String, unique=True, index=True)
    booking_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    method = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="payments")


class SupportTicket(Base):
    __tablename__ = 'support_tickets'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    reply = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now)
    is_resolved = Column(Boolean, default=False)


# ============= ФУНКЦИИ ДЛЯ РАБОТЫ С БД =============

def init_db():
    """Создаёт все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Возвращает сессию БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============= ФУНКЦИИ-ОБЁРТКИ ДЛЯ ИСПОЛЬЗОВАНИЯ В main.py =============

def create_user(db, username, email, password_hash, referral_code, avatar="👤"):
    """Создаёт нового пользователя"""
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        referral_code=referral_code,
        avatar=avatar,
        balance=300  # Приветственный бонус
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db, username):
    """Получает пользователя по имени"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_referral_code(db, code):
    """Получает пользователя по реферальному коду"""
    return db.query(User).filter(User.referral_code == code).first()


def create_booking(db, user_id, booking_data):
    """Создаёт бронирование"""
    booking = Booking(
        user_id=user_id,
        destination=booking_data["destination"],
        nights=booking_data["nights"],
        start_date=booking_data["start_date"],
        end_date=booking_data["end_date"],
        hotel=booking_data["hotel"],
        flight_there=booking_data["flight_there"],
        flight_back=booking_data["flight_back"],
        total_price=booking_data["total_price"]
    )
    db.add(booking)
    db.commit()
    return booking


def get_user_bookings(db, user_id):
    """Получает все бронирования пользователя"""
    return db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.booking_date.desc()).all()


def add_favorite(db, user_id, hotel_id, hotel_name, city, price):
    """Добавляет отель в избранное"""
    favorite = Favorite(
        user_id=user_id,
        hotel_id=hotel_id,
        hotel_name=hotel_name,
        city=city,
        price=price
    )
    db.add(favorite)
    db.commit()
    return favorite


def get_user_favorites(db, user_id):
    """Получает избранное пользователя"""
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


def remove_favorite(db, user_id, hotel_id):
    """Удаляет отель из избранного"""
    db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.hotel_id == hotel_id).delete()
    db.commit()


def add_notification(db, user_id, icon, title, text):
    """Добавляет уведомление пользователю"""
    notification = Notification(
        user_id=user_id,
        icon=icon,
        title=title,
        text=text,
        date=datetime.now().strftime("%d.%m.%Y %H:%M")
    )
    db.add(notification)
    db.commit()
    return notification


def get_user_notifications(db, user_id, limit=10):
    """Получает уведомления пользователя"""
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.id.desc()).limit(limit).all()


def mark_notification_read(db, notification_id):
    """Отмечает уведомление как прочитанное"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.read = True
        db.commit()


def add_review(db, user_id, hotel_id, rating, text):
    """Добавляет отзыв об отеле"""
    review = Review(
        user_id=user_id,
        hotel_id=hotel_id,
        rating=rating,
        text=text,
        date=datetime.now().strftime("%d.%m.%Y")
    )
    db.add(review)
    db.commit()
    return review


def get_hotel_reviews(db, hotel_id):
    """Получает отзывы об отеле"""
    return db.query(Review).filter(Review.hotel_id == hotel_id).order_by(Review.id.desc()).all()


def update_user_balance(db, user_id, amount):
    """Обновляет баланс пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.balance += amount
        db.commit()
        return user.balance
    return 0


def create_payment(db, user_id, payment_id, booking_id, amount, method):
    """Создаёт запись о платеже"""
    payment = Payment(
        user_id=user_id,
        payment_id=payment_id,
        booking_id=booking_id,
        amount=amount,
        method=method
    )
    db.add(payment)
    db.commit()
    return payment


def update_payment_status(db, payment_id, status):
    """Обновляет статус платежа"""
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if payment:
        payment.status = status
        if status == "completed":
            payment.completed_at = datetime.now()
        db.commit()