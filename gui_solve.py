# coding:utf-8
from controller import set_status, send_command
from cube_main import solve, shuffle
import tkinter as tk
import threading


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.protocol("WM_DELETE_WINDOW", self.exit)

        with open('./calib.txt') as f:
            s = f.read()
        c = s.split(',')
        for i, val in enumerate(c):
            send_command([i, 12100+int(val)])

        self.status = 2

    def create_widgets(self):
        self.start_btn = tk.Button(self.master, text='Solve', font=('', 16))
        self.shuffle_btn = tk.Button(self.master, text='Shuffle', font=('', 16))
        self.stop_btn = tk.Button(self.master, text='Stop', font=('', 16), state='disabled')
        self.start_btn.configure(width=15, height=3, command=self.start)
        self.shuffle_btn.configure(width=15, height=3, command=self.shuffle)
        self.stop_btn.configure(width=15, height=3, command=self.stop)
        self.start_btn.grid(column=0, row=0)
        self.shuffle_btn.grid(column=0, row=1)
        self.stop_btn.grid(column=0, row=2)

    def finish(self):
        print('finish')
        if self.status == 1:
            self.start_btn['state'] = 'active'
            self.shuffle_btn['state'] = 'active'
            self.stop_btn['state'] = 'disabled'
            self.status = 2

    def start(self):
        print('solve!!!')

        self.start_btn['state'] = 'disabled'
        self.shuffle_btn['state'] = 'disabled'
        self.stop_btn['state'] = 'active'

        self.status = 1
        set_status(self.status)
        self.cube_thread = threading.Thread(target=solve, args=(self.finish,))
        self.cube_thread.start()

    def shuffle(self):
        print('shuffle!!!')

        self.start_btn['state'] = 'disabled'
        self.shuffle_btn['state'] = 'disabled'
        self.stop_btn['state'] = 'active'

        self.status = 1
        set_status(self.status)
        self.cube_thread = threading.Thread(target=shuffle, args=(self.finish,))
        self.cube_thread.start()

    def stop(self):
        print('stop!!!')
        self.status = 0
        set_status(self.status)
        self.cube_thread.join()
        print('cube end')
        self.status = 2
        
        self.start_btn['state'] = 'active'
        self.shuffle_btn['state'] = 'active'
        self.stop_btn['state'] = 'disabled'

    def exit(self):
        print(self.status)
        if self.status == 2:
            self.master.destroy()
        else:
            print('dummy function')


root = tk.Tk()
root.title('Cube solver application')
root.resizable(width=False, height=False)
app = Application(root)
app.create_widgets()
app.mainloop()
