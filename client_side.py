from tkinter import *
from PIL import ImageTk,Image
import stats
import settings
import shoping_bag
import pandas as pd
from tkinter import ttk, messagebox

# to keep the data about selected products, all the values of columns in excel and quantity of that product. It is used in shoping_bag.py for making bag_products_treeview.
global selected_products
selected_products = []

# contain the id of selected products, used for keeping check for if a product is selected or not, so that if selected that product can't be selected again. 
global selected_products_id
selected_products_id = []


# don't do it as defining treeview here will create a new tkinter window
# global products_tree
# products_tree = ttk.Treeview()

# to keep the record of frame used, so that it they can be destroyed while not in use or while switching window(or view)
frames_used = []

def main_screen(window):
    
    main_frame = Frame(window,height=150, width=stats.object_variable.window_width)
    main_frame.pack()
    frames_used.append(main_frame)
    main_frame.pack_propagate(0)  # needed to set dimentions of frame, because by default frame takes size according to widgets present in it, so this is needed to override this feature


    settings_image = Image.open("./resources/settings_image.png")
    settings_image = settings_image.resize((30, 30),  Image.ANTIALIAS)
    settings_image = ImageTk.PhotoImage(image=settings_image, master=main_frame)


    # Button(main_frame, image=settings_image).pack()

    button = Button(main_frame, image=settings_image, activebackground="grey", command= lambda: proceed_to_settings(window))
    button.image = settings_image # the reason we did it is, Tk interface doesn't handle it properly and python garbage collecter removes the object, which remove the image(partially), something like that....... so we need to keep a reference to the tkinter object, by attaching it to widget attribute....
    # other ways to do it: type "global settings_image" before starting, or use self... (google: Why does Tkinter image not show up if created in a function?)
    button.pack(anchor='ne', pady=10, padx=10)

    # greet customer
    Label(main_frame, text=f"Hello, Dear Customer\nWelcome to {stats.object_variable.shop_name}!\nWhat would you like to buy today!", font="comicsansms 15").pack()


    display_products(window, main_frame)




def display_products(window, main_frame):

    utility_frame = Frame(window)
    utility_frame.pack()
    
    frames_used.append(utility_frame)
    
    # adding a search bar
    Label(utility_frame, text='Search Box : ').grid(row=0, column=1, pady=15)
    search_box_entry = Entry(utility_frame)
    search_box_entry.grid(column=2, row=0)

    # pending task: add a product category filter... 

    def search(self):
        # Get the search text from the entry widget
        search_text = search_box_entry.get()
        # Clear the treeview
        products_tree.delete(*products_tree.get_children())

        # Iterate over the data and only show the items that match the search text
        for row in products_df_rows:
            name = row[2]
            if search_text.lower() in name.lower():
                products_tree.insert("", "end", values=row)

    search_box_entry.bind('<KeyRelease>', search)  # it binds the key release function(when key is pressed and released), with search function


    products_frame = Frame(window)
    products_frame.pack()

    frames_used.append(products_frame)

    # making heading of treeview bold
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Bold"))

    
    headings = ["Product Id", "Product Category", "Product Name", "Price"]
    
    # selectmode = browse , allows user to select only one product at a time, (as multi select will create invalid input for add_To_bag button)
    products_tree = ttk.Treeview(products_frame, selectmode='browse', columns=headings)

    # reading excel file
    if stats.object_variable.file_path:
        try:
            products_df = pd.read_excel(stats.object_variable.file_path)
        except ValueError:
            messagebox.showerror(title='Error', message='File could not be opened!')


    # clear all the previous data in treeview widget
    products_tree.delete(*products_tree.get_children())


    products_tree['show'] = 'headings'  # this is used to show only the heading portion, if not used by default, it shows all the tree nodes, and there is one extra column that we don't need.

    # assigning product_tree headings
    for col_head in products_tree['column']:
        products_tree.heading(col_head, text=col_head)

    # creating a list data type of rows 
    products_df_rows = products_df.to_numpy().tolist()

    # adding rows data to products treeview
    for row in products_df_rows:
        products_tree.insert("", "end", values=row)
    
    # hiding product category by making its width zero
    # products_tree.column("Product Category", width=0, stretch='no')
    # products_tree.heading("Product Category", text="")

    # hiding product category by not displaying it
    products_tree.config(displaycolumns=(0,2,3))

    # setting width of columns in treeview
    products_tree.column("Product Id", width=150, stretch='no')
    products_tree.column("Product Name", width=250, stretch='no')
    products_tree.column("Price", width=150, stretch='no')

    # aligning values inside product_tree at center
    for col in products_tree["column"]:
        products_tree.column(col, anchor='center')

    # adding a scrollbar
    scrollbar = Scrollbar(products_frame, command=products_tree.yview, width=30)
    products_tree.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    products_tree.pack()

    display_buttons(window, products_tree)


def display_buttons(window, products_tree):
    buttons_frame = Frame(window)
    buttons_frame.pack()

    frames_used.append(buttons_frame)

    

    def add_to_bag():
        if products_tree.focus() == '':   #works when item is not selected in treeview
            return
        
        # making selected row in treeview as list, and is used as input for selected_products
        row = products_tree.item(products_tree.focus(), 'values')
        row = list(row)
        row.append(1)  # used to initailise quantity of product as 1

        # row[0] is the product id, data type of it is string
        if row[0] not in selected_products_id:
            selected_products_id.append(row[0])
            selected_products.append(row)
            item_count_label.config(text = f'Items in Bag = {len(selected_products)}') #updating the value of count label 
            
        
        
    # add to bag button
    Button(buttons_frame, text='Add to Bag', command=add_to_bag).grid(row=0, column=0, padx=(0, 100), pady=30, sticky='nsew')

    # label to show the number of products in bag
    item_count_label = Label(buttons_frame, text=f'Items in Bag = {len(selected_products)}', font="12")
    item_count_label.grid(row=0, column=1)

    # proceed to bag button
    Button(buttons_frame, text='Proceed to Bag', command= lambda: proceed_to_bag(window)).grid(sticky='se')


def proceed_to_bag(window):
    # deleting/forgeting the frames used
    for frame in frames_used:
        frame.forget()
    frames_used.clear()

    # switching to shoping bag screen
    shoping_bag.bag_screen(window)

def proceed_to_settings(window):
    # verifing if owner is accessing the settings
    verify_user(window)
    

def verify_user(window):
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
    
    # checkbox for making password hidden
    Checkbutton(verification_window, text="show password", 
                                    font=('verdana',11), command=show_and_hide).pack(pady=5)


    Button(verification_window, text="Verify", font=('consolas', 15), cursor="circle", command = lambda: verify_button(window, verification_window, username_entry, password_entry)).pack(pady=20)


def verify_button(window, verification_window, username_entry, password_entry):
    if(username_entry.get()==stats.object_variable.user_name) and (password_entry.get() == stats.object_variable.user_password):
        messagebox.showinfo(title='Verified', message='You can now proceed to settings')
        verification_window.destroy()
        for frame in frames_used:
            frame.forget()
        frames_used.clear()
        settings.setting(window)
    else:
        messagebox.showerror(title='Error', message='Invalid username or password\nPlease try again')
        verification_window.destroy()
        verify_user(window)