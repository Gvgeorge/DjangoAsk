Учебный проект сайта с вопросами и ответами на основе Django и bootstrap.
Запускать как любой Джанго проект, предварительно добавив в PATH переменную `DJANGO_ASK_SECRET_KEY`
Чтобы запустить функциональные тесты нужно скачать geckodriver mozilla firefox, распаковать и положить в папку  /usr/local/bin/,
Также должна быть установлена сама Mozilla Firefox.
Seed.py - заполняет базу данных рыбой, запускать через shell:
`import seed`
`seed.seeder.execute()`