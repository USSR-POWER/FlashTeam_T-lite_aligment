Основные цели проекта:
Согласование модели T-Lite с пользовательскими запросами.
Генерация команд для выполнения задач и их аргументация.
Работа с ограниченным контекстом и интеграция модели с агентскими системами.
Используемые технологии и библиотеки
Технологии:

Python
Transformers (Hugging Face)
PEFT (LoRA) для дообучения модели
BitsAndBytes (для 4-битного квантования)
FastAPI (для реализации API)
Kaggle (для дообучения модели)
Ссылки на Kaggle блокнот: https://www.kaggle.com/code/ussrpower/flashteam-aligment-tlite

Запуск проекта
Клонирование репозитория:
bash
git clone <your-repo-link>
cd <your-repo-folder>
Установка зависимостей:
bash
pip install -r requirements.txt
Запуск FastAPI сервера:
bash
uvicorn app:app --host 0.0.0.0 --port 8000
Запуск Телеграм-бота:
bash
python bot.py
