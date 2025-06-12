# MerchStore - FastAPI + PostgreSQL в Docker

Это веб-приложение для управления магазином мерча. Использует FastAPI, PostgreSQL и всё запускается через Docker.

---

## Требования

- Установленный [Docker](https://www.docker.com/)
- Установленный [Docker Compose](https://docs.docker.com/compose/)

---

## Запуск проекта

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Tqgeng/merchShop.git
cd merchShop
```

2. Соберите и запустите контейнеры:
```bash
docker compose up --build -d
```

3. Приложение будет доступно по адресу:

API: http://localhost:8000/docs

pgAdmin: http://localhost:5050 (пароль: admin) (пароль от бд: 123)

APP: http://localhost:8000/

#### Доступ к админ-панели

Email: admin@mail.ru

Пароль: admin