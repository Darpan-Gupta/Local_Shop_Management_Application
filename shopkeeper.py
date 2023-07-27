from tkinter import *
from tkinter import messagebox 
import stats
import settings

def register_shopkeeper(window):
    register_frame = Frame(window)
    register_frame.pack()

    Label(register_frame, text = "Please register yourself as shopkeeper",font=('consolas', 22), justify="center", pady=100).pack()

    Label(register_frame, text = "Username:",font=('consolas', 13), justify="center", padx=100, pady=10).pack()

    # can't pack this variable here without a variable name, because it is needed later in code and also because otherwise we will get error for accessing the value user will enter because python has this thing in which we can use multiple function by putting a dot like func().func1().func2()... and the return type of the variable will be the return type of end funtion and since return type of pack,grid or place is none we will get error.
    username_entry = Entry(register_frame, font=('consolas', 13), justify="center")
    username_entry.pack()

    Label(register_frame, text = "Password:",font=('consolas', 13), justify="center", padx=100, pady=10).pack()

    password_entry = Entry(register_frame, font=('consolas', 13), justify="center",show='*')
    password_entry.pack()

    def show_and_hide():
        if password_entry['show'] == '*':
            password_entry['show'] = ''
        else:
            password_entry['show'] = '*'
    
    Checkbutton(register_frame, text="show password", 
                                    font=('verdana',11), command=show_and_hide).pack(pady=5)

    Label(register_frame, text="", pady=20).pack()

    Button(register_frame, text="Register", font=('consolas', 15), cursor="circle", command= lambda: check_and_set_registeration(window, register_frame, username_entry, password_entry)).pack()
    # we need to use lambda in command if we want to use a function having parameter

def check_and_set_registeration(window, register_frame, username_entry, password_entry):
    if len(username_entry.get()) == 0:
        messagebox.showerror("Error", "Username not filled!\nPlease fill and try again.")
        register_frame.destroy()
        register_shopkeeper(window)
    
    else:
        stats.object_variable.user_name = username_entry.get()

    if len(password_entry.get()) == 0:
        messagebox.showerror("Error", "Password not filled!\nPlease fill and try again.")
        register_frame.destroy()
        register_shopkeeper(window)
    
    else:
        stats.object_variable.user_password = password_entry.get()
    
    if (len(username_entry.get()) != 0) and (len(password_entry.get()) != 0):
        stats.object_variable.shopkeeper_registered = True
        messagebox.showinfo(title='Registration Successfull', message=f'You are successfully registered as {stats.object_variable.user_name}! \nClick "ok" to fill out further details.')
        stats.save_variables()
        register_frame.destroy()
        settings.setting(window)


