import tkinter
import datetime

def uptime():
    global label
    labeltext=datetime.datetime.now()
    label.config(text=labeltext,)
    app.after(1000,uptime)

if __name__=='__main__':
    app=tkinter.Tk()
    app.geometry("300x200")
    label=tkinter.Label(
            app,
            width=30,
            height=1
        )
    label.pack()
    app.after(1000,uptime)
    app.mainloop()
    
