# *название в разработке*

## СУТЬ ПРОЕКТА

Данный проект выступает в роли приложения для публикации фотографий и видео.
***
Приложение будет обладать следущими возможностями:
* публикация фото, видео
* отмечать фотографию как понравившуюся или не понравившуюся
* комментирование публикаций и других комментариев
* чат
* добавление в друзья
* просмотр уведомлений
* установка собственного заднего фона страницы

  > он может быть выбран из списка или загружен пользователем
* другие интересные фичи :)

## СУЩНОСТИ
> Сущности, получаемые при авторизации обозначаются, как **@сущность**. Они являются приватными.
1. **@self_data** - Список данных пользователя, обладает следущими полями:
    * login
    * description - описание профиля, максимальная длина: 150 символов
    * avatar
    * phone_number
    * subscribers - список подписчков
    * subscriprions - список подписок
    * publications - список публикаций пользователя
    * like_data - лайки пользователя
    * dislike_data - дизлайки пользователя
    * settings - настройки профиля
    * notifications - список уведомлений
    * comments_data - комментарии пользователя
    * bg_theme - картинка background'а пользователя
    * registration_date - дата регистрации пользователя
2. **user_data** - Список данных любого пользователя. Он обладает всеми полями **self_data**, за исключением 5 последних и phone_number
3. **demo_user** - Демо-лист пользователя, для списка подписок или подписчиков, содержащий:
    * login
    * avatar
    * user_ref - ссылка на профиль
4. **subscribers** - Список подписчиков. Выдаётся пользователю при авторизации или посещении страницы любого другого пользователя. Данная сущность имеет следущие поля:
    * count
    * users_ref - словарь содержащий **demo_user** всех подписчиков
5. **subscriptions** - Список подписок. Выдаётся пользователю при авторизации или посещении страницы любого другого пользователя. Данная сущность имеет следущие поля:
    * count
    * users_ref - словарь содержащий **demo_user** всех подписок
    > Данная сущность может быть скрыта пользователем от других через настройки
6. **publication** - Данные конкретной публикации, такие как:
    * id
    * content - видео или фотография
    * likes - Список содержащий **demo_user** пользователей, отметивших эту фотографию, как понравившуюся
    * dislikes - Список, содержащий **demo_user** пользователей, отметивших эту фотографию, как НЕ понравившуюся
    * comments - Список коментариев.
      > Это отдельная сущность, содержащая **demo_user**, коментарий и список собственных коментариев 
6. **publications** - Сущность, содержащая все публикации пользователя
    * count
    * data - список всех сущностей **publications** пользователя
7. **@like_data** - Сущность, cодерджащая список всех лайков. Поля:
    * data - список, элементы которого хранят id публикации
8. **@dislike_data** - Сущность, идентичная **like_data**.
9. **@settings** - Сущность, описывающая все настройки профиля конкретного пользователя. Поля:
    > Поля в разработке :)
10. **@notifications** - Сущность, содержащая список всех уведомлений пользователя. Поля:     
    > Поля в разработке :)
11. **@comments_data** - Сущность, содержащая список всех комментариев пользователя.
    > Поля в разработке :)
12. **@notification** - Данные о конкретном уведомлении, такие как:
    * notification_type - Тип уведомления. Сообщение/Лайк/Дизлайк/Коммент/Сторис?/Публикация
    * notification_time - Дата создания уведомления
13. **@comment** - Данные о конкретном комментарии, такие как:
    * publication_id - id публикации под которой оставлен коммент
    * author - создатель коммента
    * comment_time - время создания комментария
    * likes - список, содержащий данные о пользователях лайкнувших коммент
    * dislike - аналог поля выше
    * answer - указывает на то, является ли комментарии ответом на другой комментарии или нет
