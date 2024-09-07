import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import json

# Определение структуры запроса
class RequestModel(BaseModel):
    query: str  # Поле "query" для системного промпта

# Создание FastAPI приложения
app = FastAPI()

# Загрузка модели и LoRA-адаптера
model_name = "AnatoliiPotapov/T-lite-instruct-0.1"
peft_model_path = "USSR-POWER/T-lite-instruct-0.1-flashteam-finetuned"  # Путь к вашему LoRA адаптеру

# Настройка для 4-битной модели
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# Загрузка модели и токенайзера
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Применение LoRA адаптера к модели
model = PeftModel.from_pretrained(model, peft_model_path)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Эндпоинт для обработки запросов
@app.post("/assist")
async def assist(request: RequestModel):
    # Получаем системный промпт из запроса (поле "query")
    system_prompt = request.query

    # Подготовка сообщений для модели
    messages = [{"role": "system", "content": system_prompt}]

    # Применение шаблона чата для ввода
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    # Определение терминаторов для завершения текста
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    # Генерация ответа
    outputs = model.generate(
        input_ids,
        max_new_tokens=512,
        eos_token_id=terminators 
    )

    # Декодирование и вывод сгенерированного ответа
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Убираем часть до слова "assistant", если оно присутствует
    if "assistant" in generated_text:
        generated_text = generated_text.split("assistant", 1)[-1]

    # Попытка распарсить текст как JSON
    try:
        response_json = json.loads(generated_text)
    except json.JSONDecodeError:
        # Если текст невалиден как JSON, выводим его для отладки
        return {"error": "Невозможно распарсить JSON", "generated_text": generated_text}

    # Возвращаем JSON объект
    return response_json

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
