import requests
import os

# Параметры
USER = 's-rb'
GH_TOKEN = os.environ['GITHUB_TOKEN']
OUTPUT_FILE = 'OPEN.md'

# Заголовки авторизации
headers = {
    'Authorization': f'token {GH_TOKEN}'
}

# Функция для получения всех форкнутых репозиториев с учётом постраничной загрузки и фильтрации
def fetch_forked_repositories():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USER}/repos?type=forks&per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Поднимает исключение при ошибке HTTP
        data = response.json()

        if not data:  # Прерываем цикл, если нет данных
            break

        # Фильтрация отключённых репозиториев
        enabled_repos = [repo for repo in data if not repo.get('disabled', False)]
        repos.extend(enabled_repos)
        page += 1

    return repos

# Функция для генерации контента в формате Markdown
def generate_open_md(forked_repos):
    content = (
        '<div style="background-color: #212830; color: white; padding: 20px; border-radius: 10px;">\n'
        '<h2 align="center">👨‍💻&nbsp;OPEN SOURCED FORKS&nbsp;👨‍💻</h2>\n<div align="center">\n'
    )

    for i, repo in enumerate(forked_repos, start=1):
        # Проверка и формирование описания
        description = repo.get('description', '') or ''
        description = description.replace('"', "'")  # Замена кавычек
        title = description if description else repo['html_url'].split('/')[-1]

        # Формирование блока для каждого репозитория
        repo_md = (
            f'<a align="center" href="{repo["html_url"]}" title="{title}">\n'
            f'<img align="center" style="margin: 10px" '
            f'src="https://github-readme-stats.vercel.app/api/pin/?username={USER}&repo={repo["name"]}&theme=react&border_color=61dafb&border_radius=10"></a>\n'
        )
        content += repo_md

    content += '</div>\n</div>'
    return content

# Основная логика
if __name__ == "__main__":
    forked_repos = fetch_forked_repositories()
    open_md_content = generate_open_md(forked_repos)

    with open(OUTPUT_FILE, "w", encoding='utf-8') as file:
        file.write(open_md_content)

    print(f"{OUTPUT_FILE} успешно обновлён!")