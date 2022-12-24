<h1>проект для тестового задания
</h1>

<h2>Вводная часть</h2>
В SQL базе данных есть продукты и категории. Одному продукту может соответствовать много категорий, 
в одной категории может быть много продуктов.

HTTP API через которое можно получить:

* список всех продуктов с их категориями,
* список категорий с продуктами,
* список всех пар «Имя продукта – Имя категории».

Если у продукта нет категорий, то он все равно должен выводиться. Если у категории нет продуктов, то она все равно должна выводиться

<h2>Установка</h2>
Проект на DRF. Подразумевается что вы знаете как это установить и запустить, или у вас уже все установлено и запущено

Для сборки и запуска выполните:  
`docker-compose up`

Для заполнения тестовыми данными и создания тестовых пользователей выполните:  
`docker-compose run web python manage.py fill_db`
 
Вход в админку:  
пользователь `django`  
пароль `12345`

Если не заполнять тестовыми данными при первом запуске нужно будет вручную создать учетную запись админа:</p>
`docker-compose run web python manage.py createsuperuser`

Xтобы остановить работу выполните
`docker-compose down`

<h2>Авторизация</h2>
Для доспупа в админку нужно зайти по 
https://your_url_here/admin и аутентифицироваться под учеткой имеющей права админа.

Для доступа к функциям API нужно авторизоваться с правами пользователя  
https://your_url_here/api-auth/login/

<h2>API</h2>

Ссылка  в API  https://your_url_here/api

`GET game/{int:game}/level/` - все уровни игры game  
`GET game/{int:game}/level/{int:id}` - уровень игры с заданым номером  
`GET game/{int:game}/level/{int:id}/promt/{int:num}`  - подсказка num, для уровня id, игры game  
`POST /answer/` - отправить ответ: 

```
content : {
    "game": id,     - id игры
    "level": id,    - id уровня   
    "answer": ""    - ответ
}
   ```

`GET /stat/` - статистика уровней



