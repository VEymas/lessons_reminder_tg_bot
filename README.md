# Телеграмм бот, оповещающий о занятиях

Описание
-------------------------

Я постоянно забываю в какой аудитории у меня будет пара, поэтому каждый раз приходится открывать расписание. Этот бот призван решить эту проблему. Незадолго до пары он оповещает о том, какая пара предстоит и в какой аудитории.

TODO 21.03.24
-------------------------

Пока бот никуда не сохраняет данные о парах, полученных через /add_lesson(пока даже эта команда не добавлена в описание бота) и имеет слабенький интерфейс.
Первое время бот будет сохранять данные просто в json файл, в дальнейшем возможно придётся прикрутить БД.
Необходимо добавить взаимодействие с json файлом, прикрутить оповещения о парах.