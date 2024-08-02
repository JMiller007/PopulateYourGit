import os
import requests
from git import Repo
import tkinter as tk
from tkinter import messagebox, filedialog

# Replace with your GitHub username and personal access token
GITHUB_USERNAME = 'JMiller007'
GITHUB_TOKEN = ''
GITHUB_API_URL = 'https://api.github.com'

README_CONTENT = """# Project Title

A brief description of what this project does and who it's for.
"""

LICENSE_CONTENT = """MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

GITIGNORE_CONTENT = """# Compiled source #
###################
*.com
*.class
*.dll
*.exe
*.o
*.so

# Packages #
############
# it's better to unpack these files and commit the raw source
# git has its own built in compression methods
*.7z
*.dmg
*.gz
*.iso
*.jar
*.rar
*.tar
*.zip

# Logs and databases #
######################
*.log

# OS generated files #
######################
.DS_Store
Thumbs.db
"""

def github_repo_exists(repo_name):
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    return response.status_code == 200

def create_github_repo(repo_name):
    url = f"{GITHUB_API_URL}/user/repos"
    data = {
        "name": repo_name,
        "private": False
    }
    response = requests.post(url, json=data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()

def add_files_to_repo(path):
    readme_path = os.path.join(path, "README.md")
    license_path = os.path.join(path, "LICENSE")
    gitignore_path = os.path.join(path, ".gitignore")

    with open(readme_path, "w") as readme_file:
        readme_file.write(README_CONTENT)
    
    with open(license_path, "w") as license_file:
        license_file.write(LICENSE_CONTENT)
    
    with open(gitignore_path, "w") as gitignore_file:
        gitignore_file.write(GITIGNORE_CONTENT)

def initialize_git_repo(path, repo_name):
    add_files_to_repo(path)
    repo = Repo.init(path)
    repo.git.add(A=True)
    repo.index.commit('Initial commit')
    remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git"
    origin = repo.create_remote('origin', remote_url)
    origin.push('master')

def process_projects(parent_folder):
    for project in os.listdir(parent_folder):
        project_path = os.path.join(parent_folder, project)
        if os.path.isdir(project_path):
            repo_name = project.replace(" ", "-")  # Replace spaces with hyphens for URL compatibility
            if not github_repo_exists(repo_name):
                create_github_repo(repo_name)
                initialize_git_repo(project_path, repo_name)
            else:
                print(f"Repository for {project} already exists.")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_projects(folder_path)
        messagebox.showinfo("Success", "Projects processed successfully.")

def create_gui():
    root = tk.Tk()
    root.title("GitHub Repository Creator")

    canvas = tk.Canvas(root, height=300, width=400)
    canvas.pack()

    frame = tk.Frame(root, bg='#f7f7f7')
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    label = tk.Label(frame, text="Select the folder containing your CS projects", bg='#f7f7f7')
    label.pack(pady=20)

    button = tk.Button(frame, text="Browse", padx=10, pady=5, fg="white", bg="#263D42", command=select_folder)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
