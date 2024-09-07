# Проект: Согласование модели T-Lite с пользовательскими запросами

## Основные цели проекта

1. **Согласование модели T-Lite с пользовательскими запросами** — дообучение модели для эффективного сопоставления запросов с командами и параметрами.
2. **Генерация команд для выполнения задач и их аргументация** — модель создает команды для выполнения задач, аргументируя свои решения в формате JSON.
3. **Работа с ограниченным контекстом** — обучение модели для работы в условиях ограничения на объем данных, передаваемых в один запрос.
4. **Интеграция модели с агентскими системами** — интеграция модели с системами, такими как шоп-ассистенты, тревел-ассистенты и другие агенты.

## Используемые технологии и библиотеки

- **Python** — язык программирования для разработки всего проекта.
- **Transformers (Hugging Face)** — библиотека для работы с моделями естественного языка.
- **PEFT (LoRA)** — для эффективного дообучения моделей с использованием низкоранговой аппроксимации.
- **BitsAndBytes** — библиотека для 4-битного квантования, что позволяет экономить ресурсы.
- **FastAPI** — для разработки и развертывания API.
- **Kaggle** — платформа для выполнения вычислений и дообучения модели на мощностях GPU.

## Ссылка на Kaggle блокнот

[FlashTeam Alignment T-Lite на Kaggle](https://www.kaggle.com/code/ussrpower/flashteam-aligment-tlite)

## Запуск проекта

1. **Клонирование репозитория:**
    ```bash
    git clone https://github.com/USSR-POWER/FlashTeam_T-lite_aligment
    cd FlashTeam_T-lite_aligment
    ```

2. **Установка зависимостей:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Создание файла `.env`:**

    Для корректной работы Telegram-бота необходимо создать файл `.env` в корне проекта и добавить токен бота в следующем формате:
    
    ```
    TOKEN="<токен бота>"
    ```

4. **Запуск FastAPI сервера:**
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

5. **Запуск Telegram-бота:**
    ```bash
    python bot.py
    ```

## Контактная информация

По всем вопросам, связанным с проектом, вы можете обратиться через Telegram: [ProgressNeuro](https://t.me/ProgressNeuro).
