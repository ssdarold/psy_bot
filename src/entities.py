from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from db import models
from datetime import datetime
import random
import subprocess


Session = sessionmaker(bind=models.DBConfig.engine)
session = Session()


class User():

    """ Класс для описания пользователя """

    def __init__(self, tg_id=None, username=None, id=None, funnel_step=None):
        self.tg_id = tg_id
        self.username = username
        self.id = id
        self.funnel_step = funnel_step
        self.signup_date = datetime.now()

    def saveUser(self):
        new_user = models.User(tg_id=self.tg_id, user_name=self.username, signup_date=self.signup_date, funnel_step=0)
        session.add(new_user)
        session.commit()

        self.id = new_user.id

        return new_user.id
    

    def getFunnelStep(self, user_tg_id):
        existUser = session.query(models.User).filter(models.User.tg_id == user_tg_id).first()

        return existUser.funnel_step
    

    def setFunnelStep(self, user_tg_id, funnel_step):
        session.query(models.User).filter(models.User.tg_id == user_tg_id).update({'funnel_step': funnel_step})

        return "Текущий шаг воронки успешно обновлен!"


    def checkUserExist(self, user_tg_id):
        existUser = session.query(models.User).filter(models.User.tg_id == user_tg_id).first()

        if existUser:
            return True
        else:
            return False
        
    def getInnerID(self, user_tg_id):
        existUser = session.query(models.User).filter(models.User.tg_id == user_tg_id).first()

        return existUser.id
    

    def getTgID(self, user_inner_id):
        existUser = session.query(models.User).filter(models.User.tg_id == user_inner_id).first()

        return existUser.tg_id
    
    def deleteUser(self, user_tg_id):
        session.query(models.User).filter(models.User.tg_id == user_tg_id).delete()
        session.commit()
    


class Order():

    """ Класс для описания заказа """

    def __init__(self, user_id=None, status=None, id=None, amount=None, system_id=None):
        self.user_id = user_id
        self.status = status
        self.id = id
        self.system_id = system_id
        self.creation_date = datetime.now()
        self.amount = amount

    def generateSystemId(self):
        while True:
            order_id = random.randint(1000, 9000000)
            existing_order = session.query(models.Order).filter_by(system_id=order_id).first()
            if not existing_order:
                return order_id

    def createOrder(self, item):

        self.system_id=self.generateSystemId()

        new_order = models.Order(user_id=self.user_id, item_id=item, creation_date=self.creation_date, status='pending', system_id=self.system_id, amount=self.amount)
        session.add(new_order)
        session.commit()

        self.id = new_order.id

        return new_order.id
    

    def checkOrderExist(self, inner_user_id):
        existOrder = session.query(models.Order).filter(models.Order.user_id == inner_user_id).filter(models.Order.status == "pending").first()

        if existOrder:
            product_query = session.query(models.Product).filter(models.Product.id == existOrder.item_id).first()
            orderInfo = {"item_name": product_query.name, "amount": existOrder.amount, "item_id": product_query.id}
            return orderInfo
        else:
            return False

    def checkOrderPayed(self, product_id, user_id):
        existOrder = session.query(models.Order).filter(models.Order.item_id == product_id).filter(models.Order.user_id == user_id).first()
        return True if existOrder and existOrder.status == "completed" else False

    def checkOrderStatus(self, inner_user_id):
        existOrder = session.query(models.Order).filter(models.Order.user_id == inner_user_id).first()
        return existOrder.status
    
    def getPaymentLink(self, product_name_arg, product_price_arg):
        order_id = str(self.system_id)
        product_name = str(product_name_arg)
        product_price = str(product_price_arg)

        result = subprocess.check_output(['php', 'genLink.php', order_id, product_name, product_price], shell=True)

        return result.decode('utf-8', errors='ignore')

    def doOrderComplete(self, inner_user_id):
        session.query(models.Order).filter(models.Order.user_id == inner_user_id).update({'status': 'completed'})
        session.commit()
        return "Status changed on completed!"
    
    def deleteOrder(self, user_id, product_id):
        session.query(models.Order).filter(models.Order.user_id == user_id).filter(models.Order.item_id == product_id).delete()
        session.commit()
    


class Settings():

    """ Класс для описания модели настроек """

    def __init__(self):
        settings_query = session.query(models.Settings).first()

        self.start_message = settings_query.start_message
        self.help_message = settings_query.help_message
        self.promocode = settings_query.promocode
        self.guide_cost = settings_query.guide_cost
        self.course_cost = settings_query.course_cost


class Guide():

    """ Класс для описания модели гайдов """

    def __init__(self):
        self.guide_query = session.query(models.Guide).first()

    def getGuide(self):
        resDict = {"name": self.guide_query.guide_name, "file": self.guide_query.guide_file}
        return resDict
    

class Course():

    """ Класс для описания модели курсов """

    def __init__(self):
        self.course_query = session.query(models.Course).first()

    def getCourse(self):
        return self.course_query.course_link


class Product():

    """ Класс для описания модели товаров """

    def __init__(self, product_id):
        try:
            product = session.query(models.Product).filter(models.Product.id == product_id).first()

            self.price = product.price
            self.name = product.name
            self.description = product.description
            self.id = product_id

        except exc.SQLAlchemyError:
            return "Не удалось найти продукт по указанному ID"
            

class Meditaion():

    """ Класс для описания модели медитации """

    def __init__(self, meditation_id):
        try:
            meditaion = session.query(models.Meditation).filter(models.Meditation.id == meditation_id).first()

            self.name = meditaion.meditation_name
            self.description = meditaion.meditation_description
            self.file = meditaion.meditation_file

        except exc.SQLAlchemyError:
            return "Не удалось найти медитацию по указанному ID"