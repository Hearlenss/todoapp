import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox

class menemen:
    def __init__(self, root):
        self.root = root
        self.root.title("Uygulamaya Hoşgelmişsen")

        self.conn = sqlite3.connect('deneme1.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT,
                description TEXT, 
                done BOOLEAN,
                created_at TEXT
            )
        ''')
        self.conn.commit()

        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.pack(pady=10)

        self.description_entry = tk.Entry(root, width=30)  
        self.description_entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Ekle", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(root, width=40)
        self.task_listbox.pack(pady=10)

        self.list_button = tk.Button(root, text="Listele", command=self.list_tasks)
        self.list_button.pack()

        self.done_button = tk.Button(root, text="Tamamlandı olarak işaretle", command=self.mark_done)
        self.done_button.pack()

        self.delete_button = tk.Button(root, text="Görevi Sil", command=self.delete_task)
        self.delete_button.pack()

        self.quit_button = tk.Button(root, text="Çıkış", command=root.destroy)
        self.quit_button.pack()
 # bu üst menemen clasın içerdikleri : Butonlar ne yapacakları , görev yazma açıklama yazma kutusu.

    def add_task(self):
        task = self.task_entry.get()
        description = self.description_entry.get() 
        if task:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('INSERT INTO tasks (task, description, done, created_at) VALUES (?, ?, ?, ?)',
                                (task, description, False, current_time))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END) 
            messagebox.showinfo("Başarı", "Hadi başlayalım görevin eklendi sıra sende")
        else:
            messagebox.showwarning("Uyarı", "Görevi yazmayı unuttun.")

    def list_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.cursor.execute('SELECT id, task, description, done, created_at FROM tasks WHERE done = ?', (False,))
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task[0]}. [ ] {task[1]} - Açıklama: {task[2]} - Oluşturulma Tarihi: {task[4]}")

        self.cursor.execute('SELECT id, task, description, done, created_at FROM tasks WHERE done = ?', (True,))
        completed_tasks = self.cursor.fetchall()
        for task in completed_tasks:
            self.task_listbox.insert(tk.END, f"{task[0]}. [✔] {task[1]} - Açıklama: {task[2]} - Oluşturulma Tarihi: {task[4]}")

    def mark_done(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_id = int(selected_task.split(".")[0])
            self.cursor.execute('UPDATE tasks SET done = ? WHERE id = ?', (True, task_id))
            self.conn.commit()
            self.list_tasks()
            messagebox.showinfo("Başarı", "Aferin görevini tamamladın")
        else:
            messagebox.showwarning("Uyarı", "Tamamlamak istediğiğinizi maus ile seçin")

    def delete_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_id = int(selected_task.split(".")[0])
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            self.list_tasks()
            messagebox.showinfo("Başarı", "Sildim Giti")
        else:
            messagebox.showwarning("Uyarı", "Görev seçmedin.")
# burasıda butonlara bsınca ne yapacakları sil = sil basınca hem listden siliyor hemde db de 0 olarak günelliyo gerisi aynı mantık.
if __name__ == "__main__":
    root = tk.Tk()
    app = menemen(root) 
    root.mainloop()
