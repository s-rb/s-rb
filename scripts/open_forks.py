import requests
import os
import re

# Параметры
GITHUB_USERNAME = 's-rb'

def get_forked_repositories(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        forked_repos = [
            {
                'name': repo['name'],
                'html_url': repo['html_url'],
                'description': repo['description'] or "No description provided"
            }
            for repo in repos if repo['fork']
        ]
        return forked_repos
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return []

def update_open_md(forked_repos):
    open_md_content = """<div style="background-color: #212830; color: white; padding: 20px; border-radius: 10px;">
<h2 align="center">👨‍💻OPEN SOURCED FORKS 👨‍💻</h2>
<div align="center">
"""

    for i, repo in enumerate(forked_repos):
        if i % 2 == 0 and i != 0:
            open_md_content += "</div><div align=\"center\">\n"

        open_md_content += f"""
        <a align="center" href="{repo['html_url']}" title="{repo['description']}">
        <img align="center" style="margin: 10px" src="https://github-readme-stats.vercel.app/api/pin/?username={GITHUB_USERNAME}&repo={repo['name']}&theme=react&border_color=61dafb&border_radius=10"></a>
        """

    open_md_content += "</div>\n</div>"

    with open("OPEN.md", "w", encoding="utf-8") as file:
        file.write(open_md_content)

def main():
    token = os.environ['GH_TOKEN_1']

    forked_repos = get_forked_repositories({GITHUB_USERNAME}, token)
    if forked_repos:
        update_open_md(forked_repos)
    else:
        print("No forked repositories found.")

if __name__ == "__main__":
    main()
