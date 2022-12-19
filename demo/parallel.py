""" To demonstrate multitasking GUI """
import time
import tkinter as tk


def greet_user():
    name = input('Enter your name: ')
    print(f'Good morning {name}')


def tk_updating():
    ws = tk.Tk()
    ws.title('PyGUI - Tk')
    ws.geometry('300x200')
    ws.config(bg='#4a7a8c')

    lbl_time = tk.Label(
        ws,
        text=time.strftime('%d%m%Y %A %H:%M:%S'),
        font=(21),
        padx=10,
        pady=6,
        bg='#d9d8d7'
    )
    lbl_time.pack(expand=True)
    ws.update()

    while True:
        time.sleep(1)
        txt_time = time.strftime('%d%m%Y %A %H:%M:%S')
        lbl_time.config(text=txt_time)
        ws.update()

    # ws.mainloop()


def mt_after():
    """ run a non-blocking multi-tasking GUI using the method of after() """
    ws = tk.Tk()
    ws.title('PyGUI - Tk')
    ws.geometry('300x200')
    ws.config(bg='#4a7a8c')

    tk.Button(
        ws,
        text='Exit',
        command=lambda: ws.destroy()
    ).pack(expand=True)

    ws.after(0, greet_user)
    ws.mainloop()


if __name__ == '__main__':
    # tk_updating()
    mt_after()
