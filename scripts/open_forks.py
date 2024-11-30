import requests
import os
import re

# Параметры
USER = 's-rb'
GH_TOKEN = os.environ['GITHUB_TOKEN']
OUTPUT_FILE = 'OPEN.md'

# Заголовки авторизации
headers = {
    'Authorization': f'token {GH_TOKEN}'
}

# Базовый URL для API
repos_url = 'https://api.github.com/user/repos'
params = {'per_page': 100, 'page': 1}

# Функция для получения всех репозиториев
def fetch_all_repositories():
    all_repos = []
    while True:
        response = requests.get(repos_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code}")
            break
        repos = response.json()
        if not repos:
            break
        all_repos.extend(repos)
        params['page'] += 1
    return all_repos

# Функция для фильтрации форков
def filter_forks(repositories):
    return [repo for repo in repositories if repo.get('fork')]

# Функция для генерации контента
def generate_open_md(forked_repos):
    content = (
        '<div style="background-color: #212830; color: white; padding: 20px; border-radius: 10px;">\n'
        '<h2 align="center">👨‍💻OPEN SOURCED FORKS 👨‍💻</h2>\n<div align="center">\n'
    )

    for i, repo in enumerate(forked_repos, start=1):
        # Получаем описание или название репозитория
        description = repo.get('description', '') or ''
        description = description.replace('"', "'")  # Заменяем двойные кавычки на одинарные
        title = description if description else repo['html_url'].split('/')[-1]

        # Формируем блок для репозитория
        repo_md = (
            f'<a align="center" href="{repo["html_url"]}" title="{title}">\n'
            f'<img align="center" style="margin: 10px" '
            f'src="https://github-readme-stats.vercel.app/api/pin/?username={USER}&repo={repo["name"]}&theme=react&border_color=61dafb&border_radius=10"></a>\n'
        )
        content += repo_md

        if i % 2 == 0:  # Закрываем строку после двух элементов
            content += '</div>\n<div align="center">\n'

    content += '</div>\n</div>'
    return content

# Функция для записи в файл
def write_to_file(content):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write(content)

# Основная логика
def main():
    repositories = fetch_all_repositories()
    if not repositories:
        print("No repositories found.")
        return

    forks = filter_forks(repositories)
    if not forks:
        print("No forks found.")
        return

    open_md_content = generate_open_md(forks)
    write_to_file(open_md_content)
    print(f"Updated {OUTPUT_FILE} successfully.")

if __name__ == "__main__":
    main()