import requests
import base64
import math
import re
import os

# Параметры API
API_KEY = os.environ['WAKATIME_API_KEY']
USER = 'surkoff'
RANGE_7_DAYS = 'last_7_days'
WAKA_STATS_URL = f'https://wakatime.com/api/v1/users/{USER}/stats/{RANGE_7_DAYS}'

# Функция для рисования прогресса в виде блока
def draw_progress_bar(percentage, bar_length=30):
    filled_length = math.ceil(bar_length * percentage / 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    return bar

def get_wakatime_stats():
    # Кодируем API ключ в base64
    encoded_api_key = base64.b64encode(API_KEY.encode()).decode('utf-8')

    # Заголовки для авторизации
    headers = {
        'Authorization': f'Basic {encoded_api_key}'
    }

    # Отправляем запрос
    response = requests.get(WAKA_STATS_URL, headers=headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        data = response.json()

        # Извлекаем языки программирования
        languages = data.get('data', {}).get('languages', [])
        results = []

        # Печатаем каждый язык с его временем, если процент >= 0.5
        for language in languages:
            name = language.get('name')
            time_spent = language.get('text')
            percent = language.get('percent', 0)

            # Округляем процент до ближайших 1%
            rounded_percent = round(percent)

            # Если процент меньше 1, пропускаем этот язык
            if rounded_percent < 1:
                continue

            bar = draw_progress_bar(rounded_percent)
            formatted = f'{name:15} {time_spent:15} {bar}   {rounded_percent:6.2f} %'
            print(formatted)
            results.append(formatted)
        return "\n".join(results)
    else:
        print(f"Ошибка при запросе данных: {response.status_code}")
        return None

def update_readme(new_content):
    readme_path = '../README.md'

    # Читаем содержимое README.md
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Удаляем старый блок и вставляем новый
    updated_content = re.sub(
        r'<!--START_SECTION:waka-->.*?<!--END_SECTION:waka-->',
        f'<!--START_SECTION:waka-->\n```text\n{new_content}\n```\n<!--END_SECTION:waka-->',
        content,
        flags=re.DOTALL
    )

    # Записываем обновленное содержимое обратно в README.md
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


def main():
    stats = get_wakatime_stats()
    if stats:
        update_readme(stats)


# Запуск основной функции
if __name__ == "__main__":
    main()