from src.entities import Order, User
o1 = Order()
u1 = User()

# o1.user_id = 123456789
# print(f'Создн ордер с id: {o1.createOrder()}')
# print(f'Ссылка на оплату: {o1.getPaymentLink("Курс по саморазвитию", 300)}')

# user_id = u1.getInnerID(859711206)

print(o1.checkOrderPayed(1, u1.getInnerID(859711206)))