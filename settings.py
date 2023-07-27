from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk,Image
import pandas as pd

import stats
import os
import shopkeeper
import main


def setting(window):

    # greetings
    greeting_frame = Frame(window)
    greeting_frame.pack()
    Label(greeting_frame, text=f"Hello {stats.object_variable.user_name}", font="comicsansms 35 bold", justify="center", pady=50).pack()


    settings_frame = Frame(window)
    settings_frame.pack()


    # set shop name
    Label(settings_frame, text="Name of Shop:", font="comicsansms 16", justify="center").grid(row=1, column=0, pady=15)
    shopname_entry = Entry(settings_frame, font="comicsansms 16", justify="center", textvariable=StringVar(value=f'{stats.object_variable.shop_name}'))
    shopname_entry.grid(row=1, column=1)


    # file path
    Label(settings_frame, text="File path containg Products info\nin format: C:\example.xlsx", font="comicsansms 16", justify="center", padx=10).grid(row=2, column=0, pady=15)
    file_entry = Entry(settings_frame, font="comicsansms 16", justify="center",  textvariable=StringVar(value=f'{stats.object_variable.file_path}'))
    file_entry.grid(row=2, column=1)

    # file browse button
    Button(settings_frame, text='Browse',font="comicsansms 13", command= lambda: open_file(file_entry)).grid(row=2, column=2, pady=0)

    def show_file_info():
        messagebox.showinfo(title='File Format Information', message="Only Excel files(.xlsx) are supported\nExcel file should contain 4 columns, with first row as headings in the order: Product Id, Product Category, Product Name, Price")

    # file information button
    info_image = Image.open("resources/info.png")
    info_image = info_image.resize((25, 25),  Image.ANTIALIAS)
    info_image = ImageTk.PhotoImage(info_image)

    increment_button = Button(settings_frame, image=info_image, activebackground="grey", command=show_file_info , borderwidth=0)
    increment_button.image = info_image 
    increment_button.grid(row=2, column=3, padx=3)



    # save and continue button
    Button(settings_frame, text="Save and continue to\nClient Mode", font="comicsansms 15 bold", command= lambda: save_and_continue_func(window, greeting_frame, settings_frame, shopname_entry, file_entry), background="#5bcf7c").grid(row=3, column=1, pady=20)

    # update username password
    Label(settings_frame, text="Change username or password", font="comicsansms 16", justify="center", padx=10).grid(row=4, column=0, pady=15)
    Button(settings_frame, text="Change", font="consolas 15 bold", command=lambda: verify_user(window, greeting_frame, settings_frame ), activebackground="grey").grid(row=4, column=1)
    
    
    # reset app
    Label(settings_frame, text="Reset Everything / New User", font="comicsansms 16", justify="center", padx=10).grid(row=5, column=0, pady=15)
    Button(settings_frame, text="Reset", font="consolas 15 bold", command=lambda:reset(window), activebackground="grey").grid(row=5, column=1)

    
def open_file(file_entry):
   filename = filedialog.askopenfilename(title="Open a File", filetype=(("xlxs files", ".*xlsx"),
("All Files", "*.")))
   file_entry.config(textvariable=StringVar(value=f'{filename}'))
   

def save_and_continue_func(window, greeting_frame, settings_frame, shopname_entry, file_entry):
    # destroy label frame, settings frame
    if len(shopname_entry.get()) == 0:
        messagebox.showerror("Error", "Shop Name not filled!\nPlease fill and try again.")
        greeting_frame.destroy()
        settings_frame.destroy()
        setting(window)
    
    else:
        stats.object_variable.shop_name = shopname_entry.get()

    if len(file_entry.get()) == 0:
        messagebox.showerror("Error", "File path not filled!\nPlease fill and try again.")
        greeting_frame.destroy()
        settings_frame.destroy()
        setting(window)
    
    else:
        if os.path.isfile(file_entry.get()) == False:
            messagebox.showerror("Error", "Given file path does not exist!\nPlease try again.")
            greeting_frame.destroy()
            settings_frame.destroy()
            setting(window)

        else:
            try:
                products_df = pd.read_excel(file_entry.get())
            except ValueError:
                messagebox.showerror(title='Error', message='File could not be opened!')
                greeting_frame.destroy()
                settings_frame.destroy()
                setting(window)
            if len(products_df.columns) != 4:
                messagebox.showerror(title='Error', message='File in wrong format.\nRefer info(i) for more detail.')
                greeting_frame.destroy()
                settings_frame.destroy()
                setting(window)
                
            stats.object_variable.file_path = file_entry.get()
            
    
    if (len(shopname_entry.get()) != 0) and (len(file_entry.get()) != 0):
        messagebox.showinfo(title='Changes saved', message='All changes are saved.\nYour shop is all set')
        stats.save_variables()
        window.destroy()
        main.main()

    
def verify_user(window, greeting_frame, settings_frame):
    verification_window = Tk()

    Label(verification_window, text = "Please verify your account",font=('consolas', 22), justify="center", pady=50).pack()

    Label(verification_window, text = "Enter current Username:",font=('consolas', 13), justify="center", padx=100, pady=10).pack()

    username_entry = Entry(verification_window, font=('consolas', 13), justify="center")
    username_entry.pack()

    Label(verification_window, text = "Enter current Password:",font=('consolas', 13), justify="center", padx=100, pady=10).pack()

    password_entry = Entry(verification_window, font=('consolas', 13), justify="center", show='*')
    password_entry.pack()

    def show_and_hide():
        if password_entry['show'] == '*':
            password_entry['show'] = ''
        else:
            password_entry['show'] = '*'
    
    Checkbutton(verification_window, text="show password", 
                                    font=('verdana',11), command=show_and_hide).pack(pady=5)


    Button(verification_window, text="Verify", font=('consolas', 15), cursor="circle", command = lambda: verify_button(window, greeting_frame, settings_frame, verification_window, username_entry, password_entry)).pack(pady=20)


def verify_button(window, greeting_frame, settings_frame, verification_window, username_entry, password_entry):
    if(username_entry.get()==stats.object_variable.user_name) and (password_entry.get() == stats.object_variable.user_password):
        messagebox.showinfo(title='Verified', message='You can now update your username and/or password')
        greeting_frame.destroy()
        settings_frame.destroy()
        verification_window.destroy()
        shopkeeper.register_shopkeeper(window)
    else:
        messagebox.showerror(title='Error', message='Invalid username or password\nPlease try again')
        verification_window.destroy()
        verify_user(window)


def reset(window):
    stats.delete_stored_variables(window)