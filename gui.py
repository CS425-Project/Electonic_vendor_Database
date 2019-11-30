import os
import pandas as pd
import tkinter as tk

login_file = r'D:\All Docs\Masters\CS425 Database Organization\Project\Code\Login_details.csv'
details_file = r'D:\All Docs\Masters\CS425 Database Organization\Project\Code\Details.xlsx'


def back1():
    screen1.destroy()


def back2():
    screen2.destroy()
    
    

def exit():
    screen.destroy()


def saved():
    saved = tk.Label(screen7, text = "Note saved", fg = "green", font = ("Calibri", 11))
    saved.pack()
    screen7.after(1500, saved.destroy)

def save():
    filename = raw_filename.get()
    notes = raw_notes.get()

    data = open(filename, "w")
    data.write(notes)
    data.close()

    saved()


def create_note():
    global raw_filename
    global raw_notes
    global screen7
    raw_filename = tk.StringVar()
    raw_notes = tk.StringVar()

    screen7 = tk.Toplevel(screen)
    screen7.title("Info")
    screen7.geometry("300x250")
    tk.Label(screen7, text = "Please enter a filename for the note below:").pack()
    tk.Entry(screen7, textvariable = raw_filename).pack()
    tk.Label(screen7, text = "Please enter the notes for the file below:").pack()
    tk.Entry(screen7, textvariable = raw_notes).pack()
    tk.Button (screen7, text = "Save", command = save).pack()


def view_notes1():
    filename1 = tk.raw_filename1.get()
    data = open(filename1, "r")
    data1 = data.read()
    screen9 = tk.Toplevel(screen)
    screen9.title("Notes")
    screen9.geometry("400x400")
    tk.Label(screen9, text = data1).pack()


def view_notes():
    screen8 = tk.Toplevel(screen)
    screen8.title("Notes")
    screen8.geometry("250x250")
    all_files = os.listdir()
    tk.Label(screen8, text = "Please use one of the file names below").pack()
    tk.Label(screen8, text = all_files).pack()
    global raw_filename1
    raw_filename1 = tk.StringVar()
    tk.Entry(screen8, textvariable=raw_filename1).pack()
    tk.Button(screen8, text = "OK", command = view_notes1).pack()


def delete_note1():
    filename3 = raw_filename2.get()
    os.remove(filename3)
    dn1 = tk.Label(screen10, text = "File removed", fg = "green", font = ("Calibri", 11))
    dn1.pack()
    screen10.after(1500, dn1.destroy)


def delete_note():
    global screen10
    screen10 = tk.Toplevel(screen)
    screen10.title("Delete Note(s)")
    screen10.geometry("250x250")
    all_files = os.listdir()
    tk.Label(screen10, text = "Please enter the name of the file you wish to delete").pack()
    tk.Label(screen10, text = all_files).pack()
    global raw_filename2
    raw_filename2 = tk.StringVar()
    tk.Entry(screen10, textvariable=raw_filename2).pack()
    tk.Button(screen10, text = "OK", command = delete_note1).pack()


def session():
    screen2.destroy()
    screen6 = tk.Toplevel(screen)
    screen6.title("Dashboard")
    screen6.geometry("10000x800")
    logo = tk.Label(screen6, text = "TRIDENT",font=("Chiller", 32))
    logo.place(relx = 0, rely = 0)
    display_name = tk.Label(screen6, text = "Welcome " + username1 ,font=("Arial", 16))
    display_name.place(relx = 0.875, rely = 0)
    
    
    file = pd.ExcelFile(details_file)
    prod_types_df = file.parse(0)
    comp_name_df = file.parse(1)
    
    list_1 = tk.Label(screen6, text = "Product Types",font=("Ariel", 12))
    list_1.place(relx = 0.13, rely = 0)
    list_2 = tk.Label(screen6, text = "Brands",font=("Ariel", 12))
    list_2.place(relx = 0.24, rely = 0)
    global dd1_option
    global dd2_option
    dd1_option = tk.StringVar()
    dd2_option = tk.StringVar()
    
    dd1_option.trace('w', option1)
    dd2_option.trace('w', option2)
    
    dd1 = tk.OptionMenu(screen6, dd1_option, *list(prod_types_df['Product Types']))
    dd1.place(relx = 0.13, rely = 0.1)
    
    dd2 = tk.OptionMenu(screen6, dd2_option, *list(comp_name_df['Brand']))
    dd2.place(relx = 0.24, rely = 0.1)

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Products')
        self.geometry("10000x800")
        container = tk.Frame(self)
#        container.geometry("10000x800")
        container.pack()

        self.frames = {}

        self.dict = {}

        for F in (StartPage, Data):
            frame = F(container, self, self.dict)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.show_window(StartPage)
        
    def show_window(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, d):
        tk.Frame.__init__(self, parent)

        file = pd.ExcelFile(details_file)
        prod_type_df = pd.read_excel(file, sheet_name = dd1_option.get())
        
        row_val = 0
        for x in list(prod_type_df[dd1_option.get()]):
            tk.Label(self, text = x).grid(row = row_val, column = 3)
            d[x] = tk.Button(self, text = 'Select',
                   command = lambda:controller.show_window(Data))
            d[x].grid(row = row_val, column = 9)
            row_val = row_val + 1
            
#            '''In this part, we create buttons by incrementing the table names in a dictionary.'''
            
class Data(tk.Frame):
    def __init__(self, parent, controller, d):
        tk.Frame.__init__(self, parent)
        
        label = 'Sample Data for testing'
        tk.Label(self, text=label).pack()
            
        tk.Button(self, text = 'Go to Start Page',
                command = lambda:controller.show_window(StartPage)).pack()

class MyApp1(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Products')
        self.geometry("10000x800")
        container1 = tk.Frame(self)
        container1.pack()

        self.frames1 = {}

        self.dict1 = {}

        for F in (StartPage1, Data1):
            frame = F(container1, self, self.dict1)
            self.frames1[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.show_window1(StartPage1)
        
    def show_window1(self, cont):
        frame1 = self.frames1[cont]
        frame1.tkraise()


class StartPage1(tk.Frame):
    def __init__(self, parent, controller, d1):
        tk.Frame.__init__(self, parent)

        file = pd.ExcelFile(details_file)
        comp_name_df = pd.read_excel(file, sheet_name = dd2_option.get())
        
        row_val = 0
        for x in list(comp_name_df[dd2_option.get()]):
            tk.Label(self, text = x).grid(row = row_val, column = 3)
            d1[x] = tk.Button(self, text = 'Select',
                   command = lambda:controller.show_window1(Data1))
            d1[x].grid(row = row_val, column = 9)
            
#            '''In this part, we create buttons by incrementing the table names in a dictionary.'''
            
class Data1(tk.Frame):
    def __init__(self, parent, controller, d):
        tk.Frame.__init__(self, parent)
        
        label = 'Sample Data for testing'
        tk.Label(self, text=label).pack()
            
        return_but = tk.Button(self, text = 'Go to Start Page',
                command = lambda:controller.show_window1(StartPage1))
        return_but.pack(side='left')


def option1(*args):
#    screen11 = tk.Toplevel(screen)
#    screen11.title(dd1_option.get())
#    screen11.geometry("600x600")
    app = MyApp()
    app.mainloop()
#    file = pd.ExcelFile(details_file)
#    prod_type_df = pd.read_excel(file, sheet_name = dd1_option.get())
#    prod_type_df.reset_index(drop = True)
#    var = prod_type_df[dd1_option.get()]
#    tk.Label(screen11, text = var.to_string(index=False)).pack()
    
def option2(*args):
    app1 = MyApp1()
    app1.mainloop()
#    screen12 = tk.Toplevel(screen)
#    screen12.title(dd2_option.get())
#    screen12.geometry("600x600")
#    file = pd.ExcelFile(details_file)
#    comp_name_df = pd.read_excel(file, sheet_name = dd2_option.get())
#    var = comp_name_df[dd2_option.get()]
#    tk.Label(screen12, text = var.to_string(index=False)).pack()

def login_success():
    session()


def incorrect_password():
    ip = tk.Label(screen2, text = "Incorrect password!", fg = "red", font = ("Calibri", 11))
    ip.pack()
    screen2.after(1500, ip.destroy)


def user_not_found():
    unf = tk.Label(screen2, text = "User not found!", fg = "red", font = ("Calibri", 11))
    unf.pack()
    screen2.after(1500, unf.destroy)

def register_user():

    username_info = username.get()
    password_info = password.get()
 
    df = pd.read_csv(login_file)
    temp_dp = pd.DataFrame(columns = ['username', 'password'])
    df.reset_index(drop = True)
    df = df.append({'username': username_info, 'password': password_info}, ignore_index=True)
    temp_dp['username'] = df['username']
    temp_dp['password'] = df['password']
    temp_dp.to_csv(login_file)
   
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    firstname_entry.delete(0, tk.END)
    lastname_entry.delete(0, tk.END)
 
    rs = tk.Label(screen1, text = "Registration Sucess", fg = "green" ,font = ("calibri", 11))
    rs.pack()
    screen1.after(1500, rs.destroy)


def clear_label(rs):
    print ("label cleared")
    rs.place_forget()

def register():
    global screen1
    screen1 = tk.Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    global firstname_entry
    global lastname_entry
    firstname = tk.StringVar()
    lastname = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label(screen1, text = "Please enter details below").pack()
    tk.Label(screen1, text = "").pack()
    tk.Label(screen1, text = "First Name * ").pack()
    firstname_entry = tk.Entry(screen1, textvariable = firstname)
    firstname_entry.pack()
    tk.Label(screen1, text = "Last Name * ").pack()
    lastname_entry = tk.Entry(screen1, textvariable = lastname)
    lastname_entry.pack()
    tk.Label(screen1, text = "Username * ").pack()
  
    username_entry = tk.Entry(screen1, textvariable = username)
    username_entry.pack()
    tk.Label(screen1, text = "Password * ").pack()
    password_entry =  tk.Entry(screen1, textvariable = password)
    password_entry.pack()
    tk.Label(screen1, text = "").pack()
    tk.Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()


def login_verify():
    global username_verify
    global username1
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_entry1.delete(0, tk.END)
    password_entry1.delete(0, tk.END)

    login_details_df = pd.read_csv(login_file)
    
    if username1 in list(login_details_df['username']):
        a = login_details_df.loc[login_details_df['username'] == username1, 'password'].iloc[0]
        if password1 == a:
            login_success()
        else:
            incorrect_password()
    else:
        user_not_found()
    

def login():
    global screen2
    screen2 = tk.Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x250")
    tk.Label(screen2, text = "Please enter details below to log in").pack()
    tk.Label(screen2, text = "").pack()

    global username_verify
    global password_verify

    username_verify = tk.StringVar()
    password_verify = tk.StringVar()

    global username_entry1
    global password_entry1

    tk.Label(screen2, text = "Username *").pack()
    username_entry1 = tk.Entry(screen2, textvariable = username_verify)
    username_entry1.pack()
    tk.Label(screen2, text = "Password *").pack()
    password_entry1 = tk.Entry(screen2, textvariable = password_verify)
    password_entry1.pack()
    tk.Label(screen2, text = "").pack()
    tk.Button(screen2, text = "Login", width = 10, height = 1, command = login_verify).pack()
    tk.Button(screen2, text = "Back", width = 10, height = 1, command = back2).pack()
    


def main_screen():
    global screen
    screen = tk.Tk()
    screen.title ("jjOS")
    screen.geometry ("300x250")
    screen.resizable(False,False)
    tk.Label(text = "Welcome to Trident Login Page", bg="grey", width="300", height ="2", font = ("Calibri", 13)).pack()
    tk.Label(text = "").pack()
    tk.Button(text = "Login", height = "2", width = "30", command = login).pack()
    tk.Label(text="").pack()
    tk.Button(text= "Register", height = "2", width = "30", command = register).pack()
    tk.Label(text="").pack()
    tk.Button(text= "Exit", height = "2", width = "30", command = exit).pack()

    screen.mainloop()

main_screen()