<?php

header('Content-type:text/plain;charset=utf-8');

require_once __DIR__ . '/Hmac.php';

$linktoform = 'https://konsa.payform.ru/';

// Секретный ключ. Можно найти на странице настроек, 
// в личном кабинете платежной формы.
$secret_key = '900f52586149e0aa93f8cf2d4138c08941180cad25ebae88aba70595db8c676b';

$data = [
	// хххх - номер заказ в системе интернет-магазина
	'order_id' => $argv[1],

	// +7хххххххххх - мобильный телефон клиента
	'customer_phone' => '+79991234567',

	// ИМЯ@prodamus.ru - e-mail адрес клиента
	'customer_email' => 'name@prodamus.ru',

	// перечень товаров заказа
	'products' => [
		[
			// id товара в системе интернет-магазина 
			//    (не обязательно) - при необходимоти прописать 
			'sku' => 321654,

			// название товара - необходимо прописать название вашего товара 
			//          (обязательный параметр)
			'name' => $argv[2],

			// цена за единицу товара, 123 - значение, которое нужно прописать
			//      (обязательный параметр)
			'price' => $argv[3],

			// количество товара, х - значение, которое нужно прописать
			//           (обязательный параметр)
			'quantity' => '1',

			// данные о налоге
			// (не обязательно, если не указано будет взято из настроек Магазина 
			//  на стороне системы)
			'tax' => [
				
			  // ставка НДС, с возможными значениями (при необходимоти заменить):
			  //	0 – без НДС;
			  //	1 – НДС по ставке 0%;
			  //	2 – НДС чека по ставке 10%;
			  //	3 – НДС чека по ставке 18%;
			  //	4 – НДС чека по расчетной ставке 10/110;
			  //	5 – НДС чека по расчетной ставке 18/118.
			  //	6 - НДС чека по ставке 20%;
			  //	7 - НДС чека по расчётной ставке 20/120.
			  'tax_type' => 0,

			  // (не обязательно) сумма налога, хх - при необходимости заменить
			//   'tax_sum' => хх,
			
			],

			// Тип оплаты, с возможными значениями (при необходимости заменить):
			//	1 - полная предварительная оплата до момента передачи предмета расчёта;
			//	2 - частичная предварительная оплата до момента передачи 
			//      предмета расчёта;
			//	3 - аванс;
			//	4 - полная оплата в момент передачи предмета расчёта;
			//	5 - частичная оплата предмета расчёта в момент его передачи 
			//      с последующей оплатой в кредит;
			//	6 - передача предмета расчёта без его оплаты в момент 
			//      его передачи с последующей оплатой в кредит;
			//	7 - оплата предмета расчёта после его передачи с оплатой в кредит.
			// (не обязательно, если не указано будет взято из настроек 
			//     Магазина на стороне системы)
			// 'paymentMethod' => х,

			// Тип оплачиваемой позиции, с возможными 
			//     значениями (при необходимости заменить):
			//	1 - товар;
			//	2 - подакцизный товар;
			//	3 - работа;
			//	4 - услуга;
			//	5 - ставка азартной игры;
			//	6 - выигрыш азартной игры;
			//	7 - лотерейный билет;
			//	8 - выигрыш лотереи;
			//	9 - предоставление РИД;
			//	10 - платёж;
			//	11 - агентское вознаграждение;
			//	12 - составной предмет расчёта;
			//	13 - иной предмет расчёта.
			// (не обязательно, если не указано будет взято из настроек Магазина на стороне системы)
			// 'paymentObject' => х,

		],
	],
	
	// id подписки (при необходимости прописать)
	// актуально и обязательно только для рекуррентных платежей, 
	//           передается вместо параметра products
	// 'subscription' => 123,
	
	// вк id пользователя (при необходимости прописать)
	// 'vk_user_id' => 123,
	
	// фио пользователя в ВК (при необходимости прописать)
	// 'vk_user_name' => 'Фамилия Имя Отчество',

	// дополнительные данные
	'customer_extra' => $argv[1],

	// для интернет-магазинов доступно только действие "Оплата"
	'do' => 'pay',

	// url-адрес для возврата пользователя без оплаты 
	//           (при необходимости прописать свой адрес)
	'urlReturn' => 'https://demo.payform.ru/demo-return',

	// url-адрес для возврата пользователя при успешной оплате 
	//           (при необходимости прописать свой адрес)
	'urlSuccess' => 'https://demo.payform.ru/demo-success',

	// служебный url-адрес для уведомления интернет-магазина 
	//           о поступлении оплаты по заказу
	// 	         пока реализован только для Advantshop, 
	//           формат данных настроен под систему интернет-магазина
	//           (при необходимости прописать свой адрес)
	'urlNotification' => 'https://demo.payform.ru/demo-notification',

	// код системы интернет-магазина, запросить у поддержки, 
	//     для самописных систем можно оставлять пустым полем
	//     (при необходимости прописать свой код)
	'sys' => 'senler',

	// метод оплаты, выбранный клиентом
	// 	     если есть возможность выбора на стороне интернет-магазина,
	// 	     иначе клиент выбирает метод оплаты на стороне платежной формы
	//       варианты (при необходимости прописать значение):
	// 	AC - банковская карта
	// 	PC - Яндекс.Деньги
	// 	QW - Qiwi Wallet
	// 	WM - Webmoney
	// 	GP - платежный терминал
	'payment_method' => 'AC',

	// сумма скидки на заказ
	// 	     указывается только в том случае, если скидка 
	//       не прменена к товарным позициям на стороне интернет-магазина
	// 	     алгоритм распределения скидки по товарам 
	//       настраивается на стороне пейформы
	'discount_value' => 0.00,
	
	// тип плательщика, с возможными значениями:
	//     FROM_INDIVIDUAL - Физическое лицо
	//     FROM_LEGAL_ENTITY - Юридическое лицо
	//     FROM_FOREIGN_AGENCY - Иностранная организация
	//     (не обязательно. если форма работает в режиме самозанятого 
	//      значение по умолчанию: FROM_INDIVIDUAL)
	'npd_income_type' => 'FROM_INDIVIDUAL',
	
	// инн плательщика (при необходимости прописат)
	//     (обязательно, если форма в режиме самозанятого 
	//      и тип плательщика FROM_LEGAL_ENTITY)
	'npd_income_inn' => 1234567890,
	
	// название компании плательщика (при необходимости прописать название)
	//          (обязательно, если форма в режиме самозанятого 
	//           и тип плательщика FROM_LEGAL_ENTITY или FROM_FOREIGN_AGENCY)
	'npd_income_company' => 'Название компании плательщика',
	
	// срок действия ссылки в формате: дд.мм.гггг чч:мм или гггг-мм-дд чч:мм
	//      при необходимости добавить дату
	//      (не обязательно, по умолчанию срок действия ссылки не ограничен)
	// 'link_expired' => 'дд.мм.гггг чч:мм',
	
	// дата начала подписки в формате: дд.мм.гггг чч:мм или гггг-мм-дд чч:мм
	//      при необходимости добавить дату
	//      (не обязательно, актуально только для рекуррентных платежей, 
	//       по умолчанию текущая дата/время)
	// 'subscription_date_start' => 'дд.мм.гггг чч:мм',
	
	// текст который будет показан пользователю после совершения оплаты
	//       (не обязательно)
	'paid_content' => 'Оплата успешно получена'
];


$data['signature'] = Hmac::create($data, $secret_key);

$link = sprintf('%s?%s', $linktoform, http_build_query($data));

echo $link;