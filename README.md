# Без броні | Про людину, війну та віру

Сайт подкасту «Без броні» — статичний сайт для GitHub Pages, без збірки.

## Структура

```
index.html               головна сторінка
assets/style.css         стилі (світла й темна тема)
assets/app.js            рендер епізодів і посилань
assets/favicon.svg       іконка
episodes/episodes.json   платформи, контакти, список епізодів
episodes/_template.md    шаблон нотаток до епізоду
```

## Як додати епізод

Додайте об'єкт у масив `episodes` у `episodes/episodes.json`:

```json
{
  "number": 1,
  "title": "Назва епізоду",
  "guest": "Ім'я гостя",
  "date": "2026-11-01",
  "duration": "48 хв",
  "summary": "Короткий опис розмови.",
  "audio": "",
  "links": { "YouTube": "https://...", "Spotify": "https://..." }
}
```

Порожні поля просто не показуються. Посилання на платформи й контакти — там само, у `platforms` і `contacts`.

## Публікація

Settings → Pages → Source: *Deploy from a branch*, гілка `main`, папка `/ (root)`.
Сайт буде доступний за адресою `https://<користувач>.github.io/bez-broni/`.

## Локальний перегляд

```
python3 -m http.server 8000
```
