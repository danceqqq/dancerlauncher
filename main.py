import tkinter as tk
from tkinter import filedialog
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

        self.launch_button = tk.Button(root, text="Запустить", command=self.launch)
        self.launch_button.pack()

        self.file_label = tk.Label(root, text="Файл:")
        self.file_label.pack()

        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.pack()

        self.browse_button = tk.Button(root, text="Обзор", command=self.browse_file)
        self.browse_button.pack()

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
        response = requests.get("https://github.com/danceqqq/dancerlauncher/archive/refs/tags/latest.zip", stream=True)
        if response.status_code == 200:
            with open("update.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall()
            shutil.rmtree("your_repo-latest")
            os.rename("your_repo-latest", "your_repo")
            os.remove("update.zip")
            self.version_label.config(text="Обновление успешно")
            self.update_button.config(state=tk.DISABLED)
        else:
            self.version_label.config(text="Ошибка при обновлении")

    def launch(self):
        file_path = self.file_entry.get()
        if file_path:
            os.startfile(file_path)
        else:
            self.file_label.config(text="Выберите файл")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

if __name__ == "__main__":
    root = tk.Tk()
    launcher = Launcher(root)
    root.mainloop()