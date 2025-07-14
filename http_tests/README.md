# HTTP Tests

Файлы для тестирования API через JetBrains HTTP Client или VS Code REST Client.

## Использование

1. Убедитесь, что Django сервер запущен: `python manage.py runserver`
2. Откройте `.http` файл в IDE
3. Нажмите на кнопку "Run" рядом с запросом

## Файлы

- `auth.http` - тесты для аутентификации

## Переменные

- `@baseUrl` - базовый URL API (по умолчанию http://localhost:8000)
- `@contentType` - тип контента (application/json)
- `@token` - JWT токен для авторизованных запросов

## Альтернативы

Также можно использовать:
- Postman
- Insomnia
- curl
- httpie
