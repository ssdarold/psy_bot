from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.storage import FSMContextProxy
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from src.entities import Order, User, Settings, Guide, Product, Course, Meditaion
from aiogram.types import InputFile
from dotenv import load_dotenv
import os

load_dotenv()

# Инициализация бота
bot = Bot(token=os.getenv("BOT_API_KEY"))
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализируем экземпляры классов
instOrder = Order()
instUser = User()
instSettings = Settings()
instGuide = Guide()
instCourse = Course()

prodGuide = Product(1)
prodCourse = Product(2)

meditation = Meditaion(1)


# Иницилизируем кнопки

guide_button = types.InlineKeyboardButton(text="Получить гайд", callback_data="check_payment_1")
course_button = types.InlineKeyboardButton(text="Получить курс", callback_data="check_payment_2")
get_guide_button = types.InlineKeyboardButton(text="Купить гайд", callback_data="get_product_1")
unsubscribe_button = types.InlineKeyboardButton(text="Отписаться от уведомлений", callback_data="unsubscribe")
get_meditation_button = types.InlineKeyboardButton(text="Бесплатная медитация", callback_data="get_meditation")
get_course_button = types.InlineKeyboardButton(text="Купить курс", callback_data="get_product_2")


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    orderExist = instOrder.checkOrderExist(instUser.getInnerID(message.from_user.id))

    if orderExist:

        pre_pay_markup = types.InlineKeyboardMarkup()
        generate_link_button = types.InlineKeyboardButton(f"Перейти к оплате", url=instOrder.getPaymentLink(orderExist.get("item_name"), orderExist.get("amount")))
        check_payment_button = types.InlineKeyboardButton(f"Проверить оплату", callback_data=f"check_payment_{orderExist.get('item_id')}")
        cancel_payment_button = types.InlineKeyboardButton(f"Отказаться от оплаты", callback_data=f"cancel_payment_{orderExist.get('item_id')}")

        pre_pay_markup.add(generate_link_button)
        pre_pay_markup.add(check_payment_button)
        pre_pay_markup.add(cancel_payment_button)

        await bot.send_message(message.from_user.id, f"""У вас есть счет, ожидающий оплаты: \n\n
<b>{orderExist.get("item_name")}</b> на сумму {orderExist.get("amount")} руб.\n\n""", parse_mode="HTML", reply_markup=pre_pay_markup)

    else:
        welcome_markup = types.InlineKeyboardMarkup()
        
        # Если пользователь существует
        if not instUser.checkUserExist(message.from_user.id):

            # Заносим пользователя в систему
            instUser.tg_id = message.from_user.id
            instUser.saveUser()

            # Формируем кнопки
            welcome_markup.add(get_guide_button)
            welcome_markup.add(get_course_button)

            # welcome_markup.add(unsubscribe_button)
            welcome_markup.add(get_meditation_button)
            await bot.send_message(message.from_user.id, instSettings.start_message, parse_mode="HTML", reply_markup=welcome_markup)

        else:
            # Формируем кнопки
            welcome_markup.add(guide_button)
            welcome_markup.add(course_button)

            # welcome_markup.add(unsubscribe_button)
            welcome_markup.add(get_meditation_button)
            await bot.send_message(message.from_user.id, instSettings.start_message, parse_mode="HTML", reply_markup=welcome_markup)




@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("get_product"))
async def cmd_get_product(query: types.CallbackQuery):

    pre_product_id = query.data.split("_")
    product_id = pre_product_id[2]

    if int(product_id) == 1:
        product = prodGuide

    elif int(product_id) == 2:
        product = prodCourse

    product_markup = types.InlineKeyboardMarkup()
    buy_product_button = types.InlineKeyboardButton(f"Купить за {product.price} руб.", callback_data=f"pre_process_payment_{product_id}")
    product_markup.add(buy_product_button)
    await bot.send_message(query.from_user.id, f"{product.name} за <b>{product.price}</b> руб.", reply_markup=product_markup, parse_mode="HTML")


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("pre_process_payment"))
async def cmd_process_payment(query: types.CallbackQuery):

    pre_product_id = query.data.split("_")
    product_id = int(pre_product_id[3])

    if product_id == 1:
        product = prodGuide

    elif product_id == 2:
        product = prodCourse

    instOrder.amount = product.price
    instOrder.user_id = instUser.getInnerID(query.from_user.id)

    instOrder.createOrder(product_id)

    pre_pay_markup = types.InlineKeyboardMarkup()
    generate_link_button = types.InlineKeyboardButton(f"Перейти к оплате", url=instOrder.getPaymentLink(product.name, instOrder.amount))
    check_payment_button = types.InlineKeyboardButton(f"Проверить оплату", callback_data=f"check_payment_{product_id}")
    cancel_payment_button = types.InlineKeyboardButton(f"Отказаться от оплаты", callback_data=f"cancel_payment_{product_id}")

    pre_pay_markup.add(generate_link_button)
    pre_pay_markup.add(check_payment_button)
    pre_pay_markup.add(cancel_payment_button)

    await bot.send_message(query.from_user.id, f"Для вас сформирована уникальная ссылка на оплату", reply_markup=pre_pay_markup, parse_mode="HTML")



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("check_payment"))
async def cmd_check_payment(query: types.CallbackQuery):

    pre_product_id = query.data.split("_")
    product_id = pre_product_id[2]


    if instOrder.checkOrderPayed(product_id, instUser.getInnerID(query.from_user.id)):

        if int(product_id) == 1:
            # Возвращаем pdf
            guideRes = instGuide.getGuide()
            file_url = InputFile(f'psy_admin/{guideRes.get("file")}')
            await bot.send_document(query.from_user.id, file_url, caption=guideRes.get("name"))
            await bot.answer_callback_query(query.id)

        elif int(product_id) == 2:
            # Возвращаем видео из курса
            courseRes = instCourse.getCourse()
            await bot.send_message(query.from_user.id, f"Ссылка на загрузку видеокурса: {courseRes}")
            await bot.answer_callback_query(query.id)


    else:
        if product_id == 1:
            nopay_guides_markup = types.InlineKeyboardMarkup()
            nopay_guides_markup.add(get_guide_button)
            await bot.send_message(query.from_user.id, "У вас нет оплаченных гайдов", reply_markup=nopay_guides_markup)

        elif product_id == 2:
            nopay_courses_markup = types.InlineKeyboardMarkup()
            nopay_courses_markup.add(get_guide_button)
            await bot.send_message(query.from_user.id, "У вас нет оплаченных курсов", reply_markup=nopay_courses_markup)



@dp.callback_query_handler(lambda callback_query: callback_query.data == "get_meditation")
async def cmd_get_meditaion(query: types.CallbackQuery):

    meditation_url = InputFile(f'psy_admin/{meditation.file}')
    await bot.send_audio(query.from_user.id, audio=meditation_url, caption=instSettings.start_message, parse_mode="HTML")

# Удалить ордер на оплату
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("cancel_payment"))
async def cmd_delete_payment(query: types.CallbackQuery):

    product_id = query.data.split("_")[2]

    user_id = instUser.getInnerID(query.from_user.id)

    if instOrder.checkOrderExist(user_id):
        instOrder.deleteOrder(user_id, product_id)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)