# 📊 Настройка Codacy для проекта

## Что такое Codacy?

Codacy — это платформа для автоматического анализа качества кода и отслеживания покрытия тестами. Она доступна в России и предоставляет:
- Автоматический анализ качества кода
- Отслеживание покрытия тестами
- Обнаружение дублирования кода
- Анализ безопасности
- Интеграцию с GitHub PR

## ✨ Преимущества Codacy

- ✅ **Доступен в РФ** - работает без VPN
- ✅ **Бесплатно для open-source** проектов
- ✅ **Автоматический анализ** при каждом коммите
- ✅ **Интеграция с GitHub** - комментарии в PR
- ✅ **Анализ качества кода** + покрытие тестами в одном месте
- ✅ **Поддержка Python** и Django

## 🚀 Настройка

### Шаг 1: Регистрация на Codacy

1. Перейдите на [app.codacy.com](https://app.codacy.com)
2. Нажмите **"Sign up with GitHub"**
3. Авторизуйте Codacy для доступа к GitHub
4. Выберите организацию/пользователя `yv0vaa`

### Шаг 2: Добавление репозитория

1. На главной странице Codacy нажмите **"Add repository"**
2. Найдите репозиторий `SE-XP` в списке
3. Нажмите **"Add repository"**
4. Дождитесь первого анализа кода (занимает 1-2 минуты)

### Шаг 3: Получение токена проекта

1. Откройте проект `SE-XP` в Codacy
2. Перейдите в **Settings** → **Integrations** → **Project API**
3. Скопируйте **Project Token**

### Шаг 4: Добавление токена в GitHub

1. Откройте GitHub репозиторий `yv0vaa/SE-XP`
2. Перейдите в **Settings** → **Secrets and variables** → **Actions**
3. Нажмите **New repository secret**
4. Заполните:
   - **Name**: `CODACY_PROJECT_TOKEN`
   - **Secret**: вставьте скопированный токен
5. Нажмите **Add secret**

### Шаг 5: Обновление badge в README

1. В Codacy откройте проект `SE-XP`
2. Перейдите в **Settings** → **Integrations** → **Badges**
3. Скопируйте **Project ID** из URL badge
4. Замените `PROJECT_ID` в `README.md` на ваш реальный Project ID:

```markdown
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ВАШ_PROJECT_ID)](https://app.codacy.com/gh/yv0vaa/SE-XP/dashboard)
[![Codacy Coverage](https://app.codacy.com/project/badge/Coverage/ВАШ_PROJECT_ID)](https://app.codacy.com/gh/yv0vaa/SE-XP/dashboard)
```

### Шаг 6: Готово! ✅

Теперь при каждом push в `main` или создании PR:
- Codacy автоматически проанализирует код
- Загрузится отчёт о покрытии тестами
- В PR появятся комментарии с найденными проблемами
- Обновятся badges в README

## 📈 Использование

### Локальный запуск с coverage

```bash
cd hw_checker
source ../venv/bin/activate

# Установить зависимости
pip install -r ../requirements-dev.txt

# Запустить тесты с покрытием
pytest --cov=assignments --cov-report=xml --cov-report=html --cov-report=term-missing

# Открыть HTML отчёт
open htmlcov/index.html  # macOS
# или
xdg-open htmlcov/index.html  # Linux
```

### Просмотр анализа на Codacy

1. Откройте [app.codacy.com](https://app.codacy.com)
2. Выберите проект `SE-XP`
3. Просмотрите:
   - **Dashboard**: общая оценка качества кода (A-F)
   - **Issues**: найденные проблемы с приоритетами
   - **Coverage**: покрытие тестами по файлам
   - **Duplication**: дублирование кода
   - **Commits**: анализ по коммитам

## 🎯 Оценки качества

Codacy использует шкалу от A до F:
- **A**: Отличное качество (0-5 проблем на 1000 строк)
- **B**: Хорошее качество (6-10 проблем)
- **C**: Среднее качество (11-20 проблем)
- **D**: Плохое качество (21-50 проблем)
- **E**: Очень плохое (51-100 проблем)
- **F**: Критическое (100+ проблем)

**Цель проекта**: поддерживать оценку A или B

## 📁 Файлы конфигурации

### `.codacy.yml`
Основная конфигурация Codacy:
- Включение/отключение проверок
- Исключения (миграции, тесты)
- Настройки анализа

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

## 📊 Интеграция с GitHub PR

Codacy автоматически:
- ✅ Комментирует новые проблемы в PR
- ✅ Показывает изменение покрытия
- ✅ Блокирует merge при критических проблемах (опционально)
- ✅ Обновляет статус проверок

### Настройка PR комментариев

1. В Codacy откройте **Settings** → **Integrations** → **GitHub**
2. Включите опции:
   - ✅ **Comment on pull requests**
   - ✅ **Block pull requests with quality issues**
   - ✅ **Show coverage diff**

## 🎨 Что анализируется

### Анализ кода:
- ✅ **Code Style**: соответствие PEP 8
- ✅ **Error Prone**: потенциальные ошибки
- ✅ **Performance**: проблемы производительности
- ✅ **Security**: уязвимости безопасности
- ✅ **Compatibility**: совместимость версий
- ✅ **Documentation**: отсутствие docstrings
- ✅ **Complexity**: сложность функций

### Покрытие тестами:
- ✅ **Overall coverage**: общее покрытие
- ✅ **File coverage**: покрытие по файлам
- ✅ **Diff coverage**: покрытие изменений в PR

### Дублирование:
- ✅ **Duplicate code blocks**
- ✅ **Similar code patterns**

## 🎯 Игнорирование проблем

### В коде:

```python
# Игнорировать проблему для одной строки
result = eval(user_input)  # codacy: ignore[E701]

# Игнорировать для блока
# codacy: disable=line-too-long
def very_long_function_with_many_parameters(param1, param2, param3, param4):
    pass
# codacy: enable=line-too-long
```

### В конфигурации (`.codacy.yml`):

```yaml
exclude_paths:
  - "path/to/ignore/**"
```

## 🚨 Troubleshooting

### Проблема: Coverage не загружается

**Решение**: 
1. Проверьте, что токен `CODACY_PROJECT_TOKEN` добавлен в GitHub Secrets
2. Убедитесь, что файл `coverage.xml` генерируется
3. Проверьте логи GitHub Actions

### Проблема: Слишком много false-positive

**Решение**: Настройте паттерны в `.codacy.yml`:

```yaml
engines:
  pylint:
    enabled: false  # Отключить конкретный анализатор
```

### Проблема: Badge не показывает данные

**Решение**: 
1. Убедитесь, что заменили `PROJECT_ID` на реальный
2. Дождитесь завершения первого анализа
3. Проверьте, что репозиторий публичный

### Проблема: Анализ не запускается

**Решение**:
1. Проверьте интеграцию GitHub в настройках Codacy
2. Убедитесь, что Codacy имеет доступ к репозиторию
3. Попробуйте переподключить интеграцию

## 📚 Дополнительные ресурсы

- [Codacy Documentation](https://docs.codacy.com/)
- [Python Patterns Guide](https://docs.codacy.com/repositories-configure/codacy-configuration-file/)
- [GitHub Integration](https://docs.codacy.com/repositories-configure/integrations/github-integration/)
- [Coverage Configuration](https://docs.codacy.com/coverage-reporter/)

## ✨ Лучшие практики

1. **Стремитесь к Grade A или B** для качества кода
2. **Поддерживайте 80%+ покрытие** основного кода
3. **Исправляйте критические проблемы** перед merge
4. **Используйте Codacy Issues** как To-Do список
5. **Мониторьте тренды** качества во времени
6. **Настройте блокировку PR** при критических проблемах
7. **Регулярно проверяйте дублирование** кода

## 🌟 Отличия от Codecov

| Функция | Codacy | Codecov |
|---------|--------|---------|
| Доступность в РФ | ✅ Да | ❌ Нет (требует VPN) |
| Анализ качества кода | ✅ Да | ❌ Нет |
| Покрытие тестами | ✅ Да | ✅ Да |
| Дублирование кода | ✅ Да | ❌ Нет |
| Анализ безопасности | ✅ Да | ❌ Нет |
| Цена для open-source | ✅ Бесплатно | ✅ Бесплатно |

---

**Настроено для проекта HW Checker** 🎉  
**Полностью работает в РФ без VPN!** 🇷🇺

