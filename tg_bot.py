import sys
import asyncio
import os
import logging
import aiohttp  
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import json

load_dotenv()

bot = Bot(os.environ.get('TOKEN'))  
FASTAPI_URL = "<URL вашего FastAPI сервера>"  # 

dp = Dispatcher(parse_mode=ParseMode.MARKDOWN)


@dp.message(Command("start"))
async def start(message: types.Message):
    start_message_1 = (
        "👋 Привет! Я — бот команды <b>FlashTeam</b>, работающий на дообученной модели <b>T-lite-instruct-0.1</b>. "
        "Я помогу решить задачи, связанные с интерпретацией и выполнением пользовательских запросов."
    )

    start_message_2 = (
        "⚠️ ВАЖНО: Отправь мне свой системный промпт с указанием задачи для модели. Пример:\n\n"
        "You are {{ai-name}}, {{user-provided AI bot description}}.\n"
        "Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM "
        "and pursue simple strategies with no legal complications.\n\n"
        "GOALS:\n"
        "1. {{user-provided goal 1}}\n"
        "2. {{user-provided goal 2}}\n"
        "3. ...\n"
        "4. ...\n"
        "5. ...\n\n"
        "Constraints:\n"
        "1. ~4000 word limit for short-term memory. Your short-term memory is short, so immediately save important information to files.\n"
        "2. If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.\n"
        "3. No user assistance.\n"
        "4. Exclusively use the commands listed in double quotes, e.g., 'command name'.\n"
        "5. Use subprocesses for commands that will not terminate within a few minutes.\n\n"
        "Commands:\n"
        "1. Google Search: 'google', args: 'input': '<поисковый запрос>'\n"
        "2. Browse Website: 'browse_website', args: 'url': '<url>', 'question': '<что вы хотите найти на сайте>'\n"
        "3. Start GPT Agent: 'start_agent', args: 'name': '<имя>', 'task': '<описание задачи>', 'prompt': '<промпт>'\n"
        "4. Message GPT Agent: 'message_agent', args: 'key': '<ключ>', 'message': '<сообщение>'\n"
        "5. List GPT Agents: 'list_agents', args: ...\n"
        "6. Delete GPT Agent: 'delete_agent', args: 'key': '<ключ>'\n"
        "7. Clone Repository: 'clone_repository', args: 'repository_url': '<url>', 'clone_path': '<путь для клонирования>'\n"
        "8. Write to File: 'write_to_file', args: 'file': '<файл>', 'text': '<текст>'\n"
        "9. Read File: 'read_file', args: 'file': '<файл>'\n"
        "10. Append to File: 'append_to_file', args: 'file': '<файл>', 'text': '<текст>'\n"
        "11. Delete File: 'delete_file', args: 'file': '<файл>'\n"
        "12. Search Files: 'search_files', args: 'directory': '<директория>'\n"
        "13. Analyze Code: 'analyze_code', args: 'code': '<полный код>'\n"
        "14. Get Improved Code: 'improve_code', args: 'suggestions': '<список предложений>', 'code': '<полный код>'\n"
        "15. Write Tests: 'write_tests', args: 'code': '<полный код>', 'focus': '<ключевые моменты>'\n"
        "16. Execute Python File: 'execute_python_file', args: 'file': '<файл>'\n"
        "17. Generate Image: 'generate_image', args: 'prompt': '<промпт>'\n"
        "18. Send Tweet: 'send_tweet', args: 'text': '<текст>'\n"
        "19. Do Nothing: 'do_nothing', args: ...\n"
        "20. Task Complete (Shutdown): 'task_complete', args: 'reason': '<причина>'\n\n"
        "Resources:\n"
        "1. Internet access for searches and information gathering.\n"
        "2. Long-term memory management.\n"
        "3. GPT-3.5-powered Agents for delegation of simple tasks.\n"
        "4. File output.\n\n"
        "Performance Evaluation:\n"
        "1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.\n"
        "2. Constructively self-criticize your big-picture behavior constantly.\n"
        "3. Reflect on past decisions and strategies to refine your approach.\n"
        "4. Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.\n\n"
        "Response Format:\n"
        "{\n"
        "    'thoughts': {\n"
        "        'text': 'thought',\n"
        "        'reasoning': 'reasoning',\n"
        "        'plan': '- short bulleted\\n- list that conveys\\n- long-term plan',\n"
        "        'criticism': 'constructive self-criticism',\n"
        "        'speak': 'thoughts summary to say to user'\n"
        "    },\n"
        "    'command': {\n"
        "        'name': 'command name',\n"
        "        'args': {\n"
        "            'arg name': 'value'\n"
        "        }\n"
        "    }\n"
        "}\n"
        "Убедитесь, что ответ может быть распознан json.loads."
    )

    await message.answer(start_message_1, parse_mode=ParseMode.HTML)
    await message.answer(start_message_2)


@dp.message(F.text)
async def handle_message(message: types.Message):
    user_message = message.text

    # Формируем запрос к FastAPI (системный промпт передается через поле "query")
    async with aiohttp.ClientSession() as session:
        async with session.post(
                FASTAPI_URL,
                json={"query": user_message}
        ) as response:
            if response.status == 200:
                # Получаем JSON-ответ от FastAPI
                result = await response.json()

                # Преобразуем JSON в строку для отправки в Telegram
                response_text = json.dumps(result, ensure_ascii=False, indent=2)

                # Отправляем JSON-ответ пользователю как есть
                await message.reply(response_text)
            else:
                await message.reply("Ошибка при обращении к серверу.")

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot, parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
