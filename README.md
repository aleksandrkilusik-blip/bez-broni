# Без броні | Про людину, війну та віру

Статичний сайт подкасту: чистий HTML + один CSS-файл, без фреймворків і збирачів. Єдиний JS — кілька рядків у `index.html` для кнопок ← → каруселі (без нього карусель гортається свайпом).

```
index.html              головна: постер, опис, платформи, карусель епізодів, ведучі
episodes.html           усі епізоди картками
about.html              про подкаст і ведучих
episodes/ep-01.html …   сторінки епізодів (лонгрід із повним текстом розмови)
en/                     англійська версія: та сама структура (en/index.html, en/episodes/ep-01.html …)
assets/css/style.css    усі стилі; кольори — CSS-змінні в :root (+ темна тема)
assets/img/             фото, іконка, лапки-мазок
```

Усе, що треба дописати, позначено жовтим `[ЗАПОВНИТИ: …]` — знайдіть пошуком по файлах.

## Публікація на GitHub Pages

Settings → Pages → Build and deployment → Source: **Deploy from a branch** → гілка **main**, папка **/ (root)** → Save.
Сайт: `https://aleksandrkilusik-blip.github.io/bez-broni/`. Усі посилання відносні, тому підшлях `/bez-broni/` працює.

## Як додати новий епізод (на прикладі №8)

1. **Сторінка.** Скопіюйте `episodes/ep-07.html` → `episodes/ep-08.html` і змініть у ній:
   - `<title>` і `<meta name="description">` / `og:*` у `<head>`;
   - рядок `Епізод 7` → `Епізод 8` і дату;
   - `<h1>` — «Ім'я Прізвище: «Головна цитата»»;
   - `Ведучі:`;
   - у `<figure class="cover">`: клас `photo--ep-07` → `photo--ep-08`, `aria-label` і підпис `<figcaption>`;
   - `<p class="lead">` — 2–3 речення про гостя (виходить жирним, як лід статті);
   - у `<div class="player">` — вставте iframe YouTube (зразок у коментарі там же) і видаліть заглушку;
   - вміст `<div class="prose">` — текст розмови:
     - розділи — `<h2>Заголовок</h2>`;
     - репліки — `<p><strong class="speaker">Надя:</strong> Текст…</p>`;
     - велика цитата — `<blockquote class="pullquote"><p>Цитата.</p><footer>Ім'я Прізвище</footer></blockquote>`;
     - виділення маркером — `<mark class="marker">ключова фраза</mark>` (помірно, 1 на сторінку);
   - наприкінці `<div class="prose">` залиште дисклеймер `<hr>` + `<p class="note">Текстова версія не є дослівною розшифровкою…</p>` (в англійській — «The text version is not a verbatim transcript…»);
   - у `<aside class="others">` приберіть пункт 8 (себе) і додайте пункт 7.
2. **Списки епізодів.**
   - `episodes.html` — скопіюйте верхню `<article class="card">…</article>` і поставте над нею з новими даними (номер, дата, назва, гість, 1–2 речення, посилання `episodes/ep-08.html`).
   - `index.html` — те саме в каруселі «Останні епізоди» (`<div class="cards cards--carousel">`); старі картки не видаляйте.
   - В усіх інших `episodes/ep-*.html` додайте пункт 8 у бокову колонку «Інші епізоди» (скопіюйте будь-який `<li>`).
3. **Обкладинка.** Збережіть обкладинку 16:9 у двох розмірах: `assets/img/ep-08.jpg` (1600×900) і `assets/img/ep-08-thumb.jpg` (640×360).
   - На сторінці епізоду замініть `<div class="photo …">…</div>` у `<figure class="cover">` на
     `<img class="cover-img" src="../assets/img/ep-08.jpg" width="1600" height="900" alt="Обкладинка епізоду: Ім'я. «Цитата з обкладинки»">`
     і в `<head>` поставте `og:image` на `…/assets/img/ep-08.jpg` (це прев'ю в Telegram і соцмережах).
   - У картці замініть `<span class="card-thumb card-thumb--empty" …></span>` на
     `<img class="card-thumb" src="assets/img/ep-08-thumb.jpg" width="640" height="360" alt="" loading="lazy">`.

## Англійська версія (en/)

Англійські сторінки лежать у `en/` і повторюють українські: `en/index.html`, `en/episodes.html`, `en/about.html`, `en/episodes/ep-NN.html`. Тексти перенесено з Notion (сторінка «Подкасти» → «EN»). Картинки спільні — з `assets/`.

У шапці кожної сторінки є перемикач **UA / EN** (`<li class="lang-switch">` в кінці меню). Він веде на ту саму сторінку іншою мовою, тому при додаванні епізоду:
- в українській `episodes/ep-08.html` посилання EN має вести на `../en/episodes/ep-08.html`, в англійській — UA на `../../episodes/ep-08.html`;
- так само оновіть два рядки `<link rel="alternate" hreflang=…>` у `<head>`;
- повторіть кроки «Як додати новий епізод» для `en/` (картки в `en/index.html` і `en/episodes.html`, «Other episodes» у `en/episodes/`). Підписи англійською: `Episode 8 · <time …>Month D, YYYY</time>`, `Guest:`, `Read the conversation →`, репліки — `<strong class="speaker">Nadia:</strong>`.

## Обкладинки і фото

Обкладинки є для всіх 7 епізодів (показуються в кольорі, як зроблені дизайнером).
`og-default.jpg` — прев'ю для головної, «Епізодів» і «Про подкаст» (зараз копія обкладинки 5-го епізоду з обома ведучими).

Фото на постері головної — `poster.jpg` (1600×900, кадр із запису в студії). Фото ведучих — `oleksandr.jpg` і `nadiia.jpg` (ширина 640 px, висота довільна): показуються повністю, без обрізання, у кольорі. Щоб замінити — покладіть нові файли з тими самими назвами й оновіть `width`/`height` в `<img class="host-photo">` на головній і в «Про подкаст».

## Платформи

Подкаст поки є тільки на YouTube. Кнопка на головній і в «Про подкаст» веде на плейлист усіх епізодів: `https://www.youtube.com/playlist?list=PLF7PYvFUKJXKWFEcvs6UVisVNEZm91Sbm`. На сторінці кожного епізоду — вбудований плеєр і кнопка на конкретне відео.

## Кеш браузера

Стилі підключені як `style.css?v=7`. Після змін у `assets/css/style.css` збільште номер (`?v=8` …) в усіх HTML-файлах — інакше браузери можуть показувати старий CSS.

## Перегляд локально

```
cd ..   # тека, де лежить bez-broni
python3 -m http.server 8000
# відкрийте http://localhost:8000/bez-broni/
```

Тексти епізодів перенесено з Notion (сторінка «Подкасти») дослівно, разом із редакторськими примітками в кінці.
