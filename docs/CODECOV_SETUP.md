# 📊 Настройка Codecov для проекта

## Что такое Codecov?

Codecov — это сервис для отслеживания покрытия кода тестами. Он интегрируется с CI/CD и показывает:
- Процент покрытия кода
- Изменения покрытия в PR
- Непокрытые строки кода
- Тренды покрытия во времени

## 🚀 Настройка

### Шаг 1: Регистрация на Codecov

1. Перейдите на [codecov.io](https://codecov.io)
2. Войдите через GitHub
3. Выберите организацию/пользователя `yv0vaa`
4. Найдите репозиторий `SE-XP` и активируйте его

### Шаг 2: Получение токена

1. В Codecov откройте репозиторий `SE-XP`
2. Перейдите в **Settings** → **General**
3. Скопируйте **Upload Token** (Repository Upload Token)

### Шаг 3: Добавление токена в GitHub

1. Откройте GitHub репозиторий
2. Перейдите в **Settings** → **Secrets and variables** → **Actions**
3. Нажмите **New repository secret**
4. Заполните:
   - **Name**: `CODECOV_TOKEN`
   - **Secret**: вставьте скопированный токен
5. Нажмите **Add secret**

### Шаг 4: Готово! ✅

Теперь при каждом push в `main` или создании PR:
- Запустятся тесты с измерением покрытия
- Отчёт автоматически загрузится в Codecov
- В PR появится комментарий с изменениями покрытия

## 📈 Использование

### Локальный запуск с coverage

```bash
cd hw_checker
source ../venv/bin/activate

# Установить зависимости
pip install -r ../requirements-dev.txt

# Запустить тесты с покрытием
pytest --cov=assignments --cov-report=html --cov-report=term-missing

# Открыть HTML отчёт
open htmlcov/index.html  # macOS
# или
xdg-open htmlcov/index.html  # Linux
```

### Просмотр отчётов на Codecov

1. Откройте [codecov.io/gh/yv0vaa/SE-XP](https://codecov.io/gh/yv0vaa/SE-XP)
2. Выберите ветку или commit
3. Просмотрите:
   - **Coverage**: общий процент покрытия
   - **Files**: покрытие по файлам
   - **Flags**: покрытие по категориям (unittests, integration, и т.д.)
   - **Commits**: история изменений покрытия

## 🎯 Целевые показатели

Согласно `codecov.yml`:
- **Минимум**: 70% покрытия
- **Цель**: 100% покрытия
- **Допустимое снижение**: не более 1% на PR

## 📁 Файлы конфигурации

### `codecov.yml`
Основная конфигурация Codecov:
- Пороги покрытия
- Исключения (миграции, тесты)
- Настройки комментариев в PR

### `.coveragerc`
Конфигурация coverage.py:
- Какие файлы включать/исключать
- Какие строки игнорировать
- Формат отчётов

### `pytest.ini`
Конфигурация pytest:
- Django settings
- Пути к тестам
- Маркеры тестов

## 🔧 Команды

```bash
# Запустить тесты
pytest

# Запустить с coverage
pytest --cov=assignments

# Запустить с детальным отчётом
pytest --cov=assignments --cov-report=term-missing

# Только HTML отчёт
pytest --cov=assignments --cov-report=html

# XML отчёт (для CI)
pytest --cov=assignments --cov-report=xml

# Запустить только быстрые тесты
pytest -m "not slow"

# Запустить только unit-тесты
pytest -m unit
```

## 📊 Badge в README

Badge автоматически показывает текущее покрытие:

```markdown
[![codecov](https://codecov.io/gh/yv0vaa/SE-XP/branch/main/graph/badge.svg)](https://codecov.io/gh/yv0vaa/SE-XP)
```

## 🎨 Что исключено из покрытия

Согласно `.coveragerc` и `codecov.yml`:
- ✅ Миграции Django (`*/migrations/*`)
- ✅ Тестовые файлы (`test_*.py`, `tests.py`)
- ✅ Служебные файлы (`manage.py`, `wsgi.py`, `asgi.py`)
- ✅ Виртуальное окружение (`venv/`)
- ✅ Абстрактные методы и магические методы
- ✅ Debug-код (`if settings.DEBUG`)

## 🚨 Troubleshooting

### Ошибка: "Missing coverage data"

**Решение**: Убедитесь, что pytest-cov установлен:
```bash
pip install pytest-cov
```

### Ошибка: "No token provided"

**Решение**: Проверьте, что `CODECOV_TOKEN` добавлен в GitHub Secrets.

### Coverage показывает 0%

**Решение**: 
1. Убедитесь, что тесты запускаются
2. Проверьте пути в `.coveragerc`
3. Запустите локально: `pytest --cov=assignments -v`

### Отчёт не загружается в Codecov

**Решение**:
1. Проверьте логи CI в GitHub Actions
2. Убедитесь, что файл `coverage.xml` создаётся
3. Проверьте, что токен корректный

## 📚 Дополнительные ресурсы

- [Codecov Documentation](https://docs.codecov.com/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Best Practices for Code Coverage](https://docs.codecov.com/docs/common-recipe-list)

## ✨ Лучшие практики

1. **Стремитесь к 80%+ покрытию** основного кода
2. **Пишите тесты для критичных функций** (проверка прав, работа с данными)
3. **Не гонитесь за 100%** - некоторый код не требует тестов
4. **Используйте маркеры** для разделения быстрых и медленных тестов
5. **Проверяйте покрытие локально** перед push
6. **Не снижайте покрытие** в новых PR

---

**Настроено для проекта HW Checker** 🎉

