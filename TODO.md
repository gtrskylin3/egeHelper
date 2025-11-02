# ЕГЭ Study Tracker — MVP 

## 1. Цель

Сделать простой и полезный инструмент для систематизации подготовки к ЕГЭ:

* выбрать предметы,
* фиксировать, что изучил сегодня (заметки),
* планировать дальнейшую подготовку (план/таски),
* отслеживать время занятий (сессии) и суммарную статистику.

MVP должен быть минимально функциональным, но расширяемым.

---

## 2. MVP-фичи (минимальный набор)

1. Регистрация / логин (JWT)
2. CRUD предметов (subjects)
3. Добавление "сессии" — когда и сколько занимался (duration, timestamp, subject, notes)
4. Ежедневные заметки / что изучил (notes) — привязка к дате и предмету
5. План (tasks) — простые задачи с дедлайном и статусом (todo/done)
6. Просмотр статистики: суммарное время по предмету/дате
7. Экспорт дневных записей (CSV) — опция


## 4. API спецификация (основные эндпоинты)

**Auth**

* `POST /auth/register` — {email, password} -> user
* `POST /auth/token` — OAuth2 password (email/password) -> access_token (JWT)

**Subjects**

* `GET /subjects` — list user's subjects
* `POST /subjects` — create
* `PUT /subjects/{id}` — update
* `DELETE /subjects/{id}` — delete

**Study sessions**

* `GET /sessions?date=YYYY-MM-DD` — получить сессии за дату
* `POST /sessions` — {subject_id, started_at, duration_minutes, note}
* `DELETE /sessions/{id}`

**Notes**

* `GET /notes?date=YYYY-MM-DD`
* `POST /notes` — {subject_id, date, content}

**Tasks**

* `GET /tasks` — фильтры: subject_id, status, due_date
* `POST /tasks`
* `PUT /tasks/{id}`

**Stats**

* `GET /stats/summary?from=YYYY-MM-DD&to=YYYY-MM-DD` — возвращает суммарное время по предмету и день

Все эндпоинты защищены JWT (кроме /auth/*).

---

## Frontend (Vue 3) — структура

```
frontend/
  ├─ src/
  │   ├─ main.js
  │   ├─ App.vue
  │   ├─ api/axios.js
  │   ├─ stores/user.js (Pinia)
  │   ├─ components/SubjectSelector.vue
  │   ├─ components/StudySessionTracker.vue
  │   ├─ components/DailyNotes.vue
  │   └─ pages/Dashboard.vue
  └─ index.html
```

### Примеры

* `api/axios.js` — создаёт экземпляр axios с базовым URL и вставляет Authorization header из хранилища.
* `StudySessionTracker.vue` — кнопки start/stop, автоматически считает duration и отправляет `POST /sessions`.
* `SubjectSelector.vue` — список предметов и возможность добавить новый предмет (POST /subjects).

---

## UX-заметки и идеи для улучшения

* Таймер для сессий (start/stop) + автозаполнение времени
* Теги/метки для заметок (темы) — позже можно фильтровать
* Интеграция с календарём (Google Calendar) — опция позже
* Рекомендации по графику занятий (на основе статистики) — ML-фича на будущее

