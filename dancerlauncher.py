import tkinter as tk
from tkinter import ttk
import requests
import os
import zipfile
import shutil

class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Мой Лаунчер")
        self.root.geometry("400x300")

        self.version_label = tk.Label(root, text="Версия: 1.0")
        self.version_label.pack()

        self.check_button = tk.Button(root, text="Проверить обновления", command=self.check_updates)
        self.check_button.pack()

        self.update_button = tk.Button(root, text="Обновить", command=self.update, state=tk.DISABLED)
        self.update_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

    def check_updates(self):
        response = requests.get("https://api.github.com/repos/danceqqq/dancerlauncher/releases/latest")
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            if latest_version > "1.0":
                self.update_button.config(state=tk.NORMAL)
                self.version_label.config(text=f"Доступна новая версия: {latest_version}")
            else:
                self.version_label.config(text="Вы используете последнюю версию")
        else:
            self.version_label.config(text="Ошибка при проверке обновлений")

    def update(self):
        self.status_label.config(text="Обновление...")
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = 100
        response = requests.get("https://github.com/danceqqq/dancerlauncher/archive/refs/heads/master.zip", stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 1))
            with open("update.zip", "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                    self.progress_bar['value'] = (f.tell() / total_size) * 100
                    self.root.update_idletasks()
            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall()
            files_and_folders = os.listdir()
            for item in files_and_folders:
                if os.path.isdir(item):
                    folder_name = item
                    break
            if os.path.exists(os.path.join(os.getcwd(), "dancerlauncher.py")):
                os.remove("dancerlauncher.py")
            shutil.move(folder_name, "dancerlauncher.py")
            os.remove("update.zip")
            self.status_label.config(text="Обновление успешно")
            self.update_button.config(state=tk.DISABLED)
        else:
            self.status_label.config(text="Ошибка при обновлении")

if __name__ == "__main__":
    root = tk.Tk()
    launcher = Launcher(root)
    root.mainloop()