from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk,Image

import client_side


def bag_screen(window):
    bag_frame = Frame(window)
    bag_frame.pack()

    # Heading   
    Label(bag_frame, text="Products in your Basket", font='bold 20').pack(pady=20)

    # Making the heading of treeview as bold
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Bold"))

    headings = ["Product Id","Product Category", "Product Name", "Price", "Quantity"]

    # initiallising treeview, show =  heading - shows only heading otherwise it is having one more column by default
    # selectmode = browse , allows user to select only one product at a time, (as multi select will create invalid input for increase decrease and remove buttons)
    bag_products_tree = ttk.Treeview(bag_frame, columns=headings, show="headings", selectmode='browse')

    # clear all the previous data in treeview widget
    bag_products_tree.delete(*bag_products_tree.get_children())

    # setting or creating the heading of treeview
    for head in headings:
        bag_products_tree.heading(head, text=head)

    # displaying selected columns, hiding product category
    bag_products_tree.config(displaycolumns=(0,2,3,4))

    # setting width of treeview columns
    bag_products_tree.column("Product Id", width=120, stretch='no')
    bag_products_tree.column("Product Name", width=200, stretch='no')
    bag_products_tree.column("Price", width=120, stretch='no')
    bag_products_tree.column("Quantity", width=120, stretch='no')

    # setting the values of treeview
    for selected_row in client_side.selected_products:
        bag_products_tree.insert('', 'end', values=selected_row)


    # aligning values inside product_tree at center
    for col in bag_products_tree["column"]:
        bag_products_tree.column(col, anchor='center')

    bag_products_tree.pack(padx=40)
    # padding done to increase the frame width so that increase decrease buttons can be in the frame

    # increment button
    increment_image = Image.open("resources/add.png")
    increment_image = increment_image.resize((25, 25),  Image.ANTIALIAS)
    increment_image = ImageTk.PhotoImage(increment_image)

    increment_button = Button(bag_frame, image=increment_image, activebackground="grey", command= lambda: increase_quantity(window, bag_frame, bag_products_tree) , borderwidth=0)
    increment_button.image = increment_image # the reason we did it is, Tk interface doesn't handle it properly and python garbage collecter removes the object, which remove the image(partially), something like that....... so we need to keep a reference to the tkinter object, by attaching it to widget attribute....
    # other ways to do it: type "global increment_button" before starting, or use self... (google: Why does Tkinter image not show up if created in a function?)
    increment_button.place(x=610, y=150)

    # decrement button
    decrement_image = Image.open("resources/minus.png")
    decrement_image = decrement_image.resize((25, 25),  Image.ANTIALIAS)
    decrement_image = ImageTk.PhotoImage(decrement_image)

    decrement_button = Button(bag_frame, image=decrement_image, activebackground="grey", command= lambda: decrease_quantity(window, bag_frame, bag_products_tree), borderwidth=0)
    decrement_button.image = decrement_image 
    decrement_button.place(x=610, y=190)

    # remove button
    remove_image = Image.open("resources/delete.png")
    remove_image = remove_image.resize((25, 25),  Image.ANTIALIAS)
    remove_image = ImageTk.PhotoImage(remove_image)

    remove_button = Button(bag_frame, image=remove_image, activebackground="grey", command= lambda: remove_product(window, bag_frame, bag_products_tree), borderwidth=0)
    remove_button.image = remove_image 
    remove_button.place(x=610, y=230)



    def find_total():
        total_price = 0
        for row in bag_products_tree.get_children():
            row_values = bag_products_tree.item(row, 'values')
            # add the product of price and quantity
            total_price += int(row_values[3])*int(row_values[4])
        
        return total_price
    

    total_price = find_total()

    Label(bag_frame, text=f'Total Price = {total_price}', font='bold 15').pack(pady=30)

    Button(bag_frame, text='Proceed to pay', font='15').pack(pady=10)

    Button(bag_frame, text='Add more items', font='15', command= lambda: add_more_items(window, bag_frame)).pack(pady=20)

def add_more_items(window, bag_frame):
    bag_frame.destroy()
    client_side.main_screen(window) #goes to client side

def increase_quantity(window, bag_frame, bag_products_tree):
    row = bag_products_tree.item(bag_products_tree.focus(), 'values')
    row = list(row)
    row[4] = int(row[4])
    
    for i in range(len(client_side.selected_products)):
        if client_side.selected_products[i] == row:
            client_side.selected_products[i][4] += 1
    
    bag_frame.destroy()
    bag_screen(window)

def decrease_quantity(window, bag_frame, bag_products_tree):
    row = bag_products_tree.item(bag_products_tree.focus(), 'values')
    row = list(row)
    row[4] = int(row[4])
    
    for i in range(len(client_side.selected_products)):
        if client_side.selected_products[i] == row:
            client_side.selected_products[i][4] -= 1
            if client_side.selected_products[i][4] == 0:
                client_side.selected_products.pop(i)
                client_side.selected_products_id.pop(i)
    
    bag_frame.destroy()
    bag_screen(window)

def remove_product(window, bag_frame, bag_products_tree):
    row = bag_products_tree.item(bag_products_tree.focus(), 'values')
    row = list(row)
    row[4] = int(row[4])
    
    client_side.selected_products.remove(row)
    client_side.selected_products_id.remove(row[0])
            
    bag_frame.destroy()
    bag_screen(window)