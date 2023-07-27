from tkinter import *
import stats
import shopkeeper
import client_side
import os



# basic flow of this application:
# main function runs, creates a main window, if shopkeeper haven't register before it goes to 'shopkeeper.py' to registeration window to set username and password and then to settings window funciton in 'settings.py' to set shop name and file path for products, it all this is successfull, then flow is transfered to 'client_side.py' where all the products are displayed then last is proceed to bag button, which leads to 'shoping_bag.py' which displays the item in bag and bill.



# check if the file path entered by user was currupted or not, if currupt or user closed the application before complete registeration, delete the app_data file
def check_data(window):
    if os.path.isfile(stats.object_variable.file_path) == False or stats.object_variable.shopkeeper_registered == False:
        os.remove("./app_data.pickle")
        window.destroy()
    else:
        window.destroy()    


def main():
    # creating main tkinter window
    window = Tk()
    window.title(stats.object_variable.shop_name)

    # accessing the screen width and height to find the center of screen to display tkinter window at center
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - stats.object_variable.window_width) // 2
    y = (screen_height - stats.object_variable.window_height) // 2

    window.geometry(f"{stats.object_variable.window_width}x{stats.object_variable.window_height}+{x}+{y}")

    # displaying client side window if user has allredy registered otherwise registeration window
    if(stats.object_variable.shopkeeper_registered == False):
        shopkeeper.register_shopkeeper(window)
    else:
        client_side.main_screen(window)
    
    # function to run at the closing of main window, to check for any error in stored data(in file path and registeration) and delete app_data file if any
    window.protocol("WM_DELETE_WINDOW", lambda: check_data(window)) 
    
    window.mainloop()

# to run the main function only when this file(main.py) is run
if __name__ == "__main__":
    main()



