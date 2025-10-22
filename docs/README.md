# Документация проекта HW Checker

Эта папка содержит документацию проекта, автоматически генерируемую из docstrings с помощью Sphinx.

## Установка зависимостей

```bash
pip install -r ../requirements.txt
```

## Сборка документации

### HTML версия

```bash
make html
```

Документация будет доступна в `_build/html/index.html`

Открыть в браузере:
```bash
open _build/html/index.html  # MacOS
xdg-open _build/html/index.html  # Linux
start _build/html/index.html  # Windows
```

### PDF версия

```bash
make latexpdf
```

### Другие форматы

```bash
make epub      # EPUB книга
make text      # Текстовая версия
make man       # Man страница
make texinfo   # Texinfo файлы
```

## Просмотр доступных команд

```bash
make help
```

## Очистка сгенерированных файлов

```bash
make clean
```

## Структура документации

- `conf.py` - конфигурация Sphinx
- `index.rst` - главная страница документации
- `overview.rst` - обзор проекта
- `installation.rst` - инструкции по установке
- `usage.rst` - руководство пользователя
- `api/` - автоматически генерируемая документация API
  - `models.rst` - документация моделей
  - `views.rst` - документация представлений
  - `forms.rst` - документация форм
  - `decorators.rst` - документация декораторов
- `changelog.rst` - история изменений
- `contributing.rst` - руководство для разработчиков

## Обновление документации

После изменения docstrings в коде просто пересоберите документацию:

```bash
make clean
make html
```

## Автоматическая пересборка

Для автоматической пересборки при изменении файлов установите sphinx-autobuild:

```bash
pip install sphinx-autobuild
sphinx-autobuild . _build/html
```

Документация будет доступна на http://127.0.0.1:8000 и автоматически обновляться при изменениях.

