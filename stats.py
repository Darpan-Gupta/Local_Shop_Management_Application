import os
import pickle
import main


class variables:
    shopkeeper_registered = False
    shop_name = ""
    window_width = 700
    window_height = 600
    user_name = ""
    user_password = ""
    file_path = ''

object_variable = variables()

# checking if app_data file exist, if exist then read the variables from it, if doesn't exist then create a new one, as it will store the value of variables that user has set, hence user won't need to register itselt again everytime the application is run.
if os.path.isfile('./app_data.pickle'):
    with open("./app_data.pickle", 'rb') as file:
        object_variable = pickle.load(file)
        
else:
    with open("./app_data.pickle", 'wb') as file:
        pickle.dump(obj=object_variable, file=file)

# saving the variable in file, this function is called every time some shop variable is changed.
def save_variables():
    with open("./app_data.pickle", 'wb') as file:
        pickle.dump(obj=object_variable, file=file)


# this function is called when user want to reset the application, all the shop variables are changed to default and app_data file is overwritten  
def delete_stored_variables(window):
    window.destroy()
    object_variable.shopkeeper_registered = False
    object_variable.shop_name = ""
    object_variable.window_width = 700
    object_variable.window_height = 600
    object_variable.user_name = ""
    object_variable.user_password = ""
    object_variable.file_path = ''

    save_variables()
    main.main()