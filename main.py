import tkinter as tk
import threading
import time

class TextEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Editor")

        self.text = tk.Text(self.root)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.bind('<FocusIn>', self.reset_timer)

        self.timer_label = tk.Label(self.root, text="Timer: 10")
        self.timer_label.pack()

        self.timer_thread = None
        self.timer_running = False
        self.total_time = 10

        self.root.bind('<Key>', self.reset_timer)

        self.root.mainloop()

    def start_timer(self):
        self.timer_running = True
        while self.total_time > 0:
            time.sleep(1)
            if time.time() - self.last_typing_time >= 10:
                self.total_time -= 1
                self.timer_label.config(text=f"Timer: {self.total_time}")
            else:
                self.total_time = 10  # Reset to initial value when typing occurs
                self.timer_label.config(text=f"Timer: {self.total_time}")
        if self.total_time == 0:
            self.delete_text()
        self.timer_running = False  # Reset timer running flag

    def reset_timer(self, event=None):
        self.last_typing_time = time.time()
        if not self.timer_running:
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join()  # Ensure the previous thread is finished
            self.total_time = 10  # Reset the timer countdown
            self.timer_thread = threading.Thread(target=self.start_timer)
            self.timer_thread.start()

    def delete_text(self):
        self.text.delete('1.0', 'end')
        # Directly manipulate timer in UI reset
        self.timer_label.config(text="Timer: 10")
        self.timer_running = False  # Ensure flag is reset
        self.reset_timer()  # Restart timer after clearing text

if __name__ == "__main__":
    app = TextEditorApp()
