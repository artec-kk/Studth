# coding:utf-8
from time import sleep, time
from controller import *
import tkinter as tk
import tkinter.ttk as ttk


class Calibration(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.target = -1
        with open('./calib.txt') as f:
            s = f.read()
        cd = s.split(',')
        self.calib_data = [ tk.IntVar(value=int(cd[i])) for i in range(8) ]
        for i, val in enumerate(cd):
            self.set_servomotor(i, int(val))

    def create_widgets(self):
        location = ['1', '2', '3', '4']
        # parts = ['ROT', 'GRB']
        # rot = ['D9', 'D7', 'D11', 'D2']
        # grb = ['D10', 'D8', 'D12', 'D4']
        parts = [['D9', 'D10'], ['D2', 'D4'], ['D11', 'D12'], ['D7', 'D8']]
        calib_rng = [[-30, 0], [-30, 30]]

        frm_calib = ttk.Frame(self.master)
        frm_button = ttk.Frame(self.master)
        frm_calib.grid(column=0, row=0)
        frm_button.grid(column=0, row=1)

        for l in range(4):
            frame = ttk.LabelFrame(frm_calib, text=location[l])
            part = parts[l]
            for p in range(2):
                self.scale = tk.Scale(frame,
                    variable=self.calib_data[l*2+p],
                    command=self.send_degree, name=str(l*2+p),
                    orient=tk.HORIZONTAL, label=part[p],
                    from_=calib_rng[p][0], to=calib_rng[p][1],
                    resolution=1, tickinterval=0)
                self.scale.bind(sequence='<1>', func=self.set_target)
                self.scale.grid(column=0, row=p)
            frame.grid(column=l, row=0)

        frame = ttk.Frame(frm_button)
        self.btn_ok = tk.Button(frame, text='OK', command=self.set_calib)
        self.btn_cancel = tk.Button(frame, text='Cancel', command=self.cancel)
        self.btn_ok.grid(column=0, row=1)
        self.btn_cancel.grid(column=1, row=1)
        frame.grid(column=0, row=0)

    def set_calib(self):
        result = [str(val.get()) for val in self.calib_data]
        with open('./calib.txt', mode='w') as f:
            s = f.writelines(','.join(result))
        self.master.destroy()

    def cancel(self):
        self.master.destroy()

    def set_target(self, event):
        self.target = int(str(event.widget).split('.')[-1])

    def send_degree(self, val):
        self.set_servomotor(self.target, val)

    def set_servomotor(self, num, val):
        calib_id = 10000
        # num = int(str(event.widget).split('.')[-1])
        delta = int(val)
        base = 180
        if num % 2 == 1:    # GRG
            base = 90

        send_command([num, calib_id + base + delta])


root = tk.Tk()
root.title('Servomotor calibration application')
root.resizable(width=False, height=False)
app = Calibration(root)
app.create_widgets()
app.mainloop()
