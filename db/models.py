from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base


class DBConfig():
    # Создаем соединение с базой данных
    engine = create_engine('sqlite:///psy_admin/db.sqlite3')
    # Создаем базовый класс для объявления моделей
    Base = declarative_base()

# Модель пользователя
class User(DBConfig.Base):
    __tablename__ = 'main_user'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    user_name = Column(String)
    signup_date = Column(DateTime)
    funnel_step = Column(Integer)

# Модель заказов
class Order(DBConfig.Base):
    __tablename__ = 'main_order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    item_id = Column(String)
    system_id = Column(Integer)
    creation_date = Column(DateTime)
    status = Column(String)
    amount = Column(Integer)


# Модель настроек
class Settings(DBConfig.Base):
    __tablename__ = 'main_settings'

    id = Column(Integer, primary_key=True)
    start_message = Column(Text)
    start_audio_file = Column(String)
    help_message = Column(Text)
    promocode = Column(String)
    guide_cost = Column(Integer)
    course_cost = Column(Integer)


# Модель курсов
class Product(DBConfig.Base):
    __tablename__ = 'main_product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    price = Column(String)


# Модель гайдов
class Guide(DBConfig.Base):
    __tablename__ = 'main_guide'

    id = Column(Integer, primary_key=True)
    guide_name = Column(String)
    guide_description = Column(Text)
    guide_file = Column(String)


# Модель курсов
class Course(DBConfig.Base):
    __tablename__ = 'main_course'

    id = Column(Integer, primary_key=True)
    course_video_name = Column(String)
    course_link = Column(String)


# Модель курсов
class Meditation(DBConfig.Base):
    __tablename__ = 'main_meditation'

    id = Column(Integer, primary_key=True)
    meditation_name = Column(String)
    meditation_description = Column(Text)
    meditation_file = Column(String)