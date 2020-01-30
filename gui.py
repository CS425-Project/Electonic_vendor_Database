import os
import pandas as pd
import tkinter as tk
import pyodbc
import random
import datetime
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-UL1030M\SQLEXPRESS;'
                      'Database=Electronic_vendor;'
                      'Trusted_Connection=yes;')

tbl = conn.cursor()

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


def add_to_cart(data):
 
    temp_dp = pd.DataFrame(columns = ['productID', 'productName', 'companyName', 'price'])
    global cart_df1
    cart_df1 = cart_df1.append({'productID': data.iloc[1], 'productName': data.iloc[0], 'companyName': data['companyName'], 'price' : data['price']}, ignore_index=True)
    temp_dp['productName'] = cart_df1['productName']
    temp_dp['companyName'] = cart_df1['companyName']
    temp_dp['price'] = cart_df1['price']
    temp_dp['productID'] = cart_df1['productID']
    
    cart_df1 = temp_dp

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
    global screen6
    screen6 = tk.Toplevel(screen)
    screen6.title("Dashboard")
    screen6.geometry("10000x800")
    
    global cart_df1
    
    cart_df1 = pd.DataFrame(columns = ['productID', 'productName', 'price'])
    
    logo = tk.Label(screen6, text = "TRIDENT",font=("Chiller", 32))
    logo.place(relx = 0, rely = 0)
    display_name = tk.Label(screen6, text = "Welcome " + username1 ,font=("Arial", 16))
    display_name.place(relx = 0.875, rely = 0)
    
    cart_but = tk.Button(screen6, text = "Cart" ,command = cart)
    cart_but.place(relx = 0.775, rely = 0)

    
    product_tables = pd.read_sql_query('select productType from products',conn)
    prod_types_df = pd.DataFrame(product_tables,columns=['productType'])
    
    company_tables = pd.read_sql_query('select companyName from company',conn)
    comp_name_df = pd.DataFrame(company_tables,columns=['companyName'])
    
    list_1 = tk.Label(screen6, text = "Product Types",font=("Ariel", 12))
    list_1.place(relx = 0.13, rely = 0)
    list_2 = tk.Label(screen6, text = "Brands",font=("Ariel", 12))
    list_2.place(relx = 0.24, rely = 0)
    list_3 = tk.Label(screen6, text = "My Account",font=("Ariel", 12))
    list_3.place(relx = 0.875, rely = 0.05)
    
    global dd1_option
    global dd2_option
    global dd3_option
    
    dd1_option = tk.StringVar()
    dd2_option = tk.StringVar()
    dd3_option = tk.StringVar()
    
    dd1_option.trace('w', option1)
    dd2_option.trace('w', option2)
    dd3_option.trace('w', option3)
    
    
    my_acc = ['My Address', 'Payment Options', 'Orders', 'Sign out']
    dd1 = tk.OptionMenu(screen6, dd1_option, *list(prod_types_df['productType']))
    dd1.place(relx = 0.13, rely = 0.1)
    
    dd2 = tk.OptionMenu(screen6, dd2_option, *list(comp_name_df['companyName']))
    dd2.place(relx = 0.24, rely = 0.1)
    
    dd3 = tk.OptionMenu(screen6, dd3_option, *my_acc)
    dd3.place(relx = 0.875, rely = 0.1)
    

def myapp():
    screen18 = tk.Toplevel(screen)
    screen18.title("Products")
    screen18.geometry("10000x800")
    
    prod_list = []    
    global prod_type_df
    phone = pd.read_sql_query('select * from phone_spec', conn)
    laptop = pd.read_sql_query('select * from laptop_spec', conn)
    tablet = pd.read_sql_query('select * from tablet_spec', conn)

    if (dd1_option.get()) == 'Laptop':
        prod_type_df = pd.DataFrame(laptop,columns=['lapName', 'productID' ,'companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    elif (dd1_option.get()) == 'Phone':
        prod_type_df = pd.DataFrame(phone,columns=['phoneName', 'productID','companyName','phoneStorage','color','frontcampixel','backcampixel','processor','extStoragecapacity','phoneOS','phoneOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    else:   
        prod_type_df = pd.DataFrame(tablet,columns=['tabName', 'productID','companyName','screenResolution','processor','RAM','tabStorage','tabOS','tabOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    
    
    cart_but = tk.Button(screen18, text = "Cart" ,command = cart)
    cart_but.place(relx = 0.875, rely = 0.05)
    
    dic = {}
    
    row_val = 0
    for x in list(prod_type_df.iloc[:,0]):
        tk.Label(screen18, text = x).grid(row = row_val, column = 3)
        dic[x] = tk.Button(screen18, text = str(x), command = lambda a = x :data1(a))
        dic[x].grid(row = row_val, column = 9)
        row_val = row_val + 1

def myapp1():
    screen19 = tk.Toplevel(screen)
    screen19.title("Products")
    screen19.geometry("10000x800")
    
    global prod_type_df
    global prod_type_df1
    global prod_type_df2
    
    
    Apple = pd.read_sql_query("select * from phone_spec where companyName = 'Apple'", conn)
    AppleLap = pd.read_sql_query("select * from laptop_spec where companyName = 'Apple'", conn)
    AppleTab = pd.read_sql_query("select * from tablet_spec where companyName = 'Apple'", conn)
    Dell = pd.read_sql_query("select * from laptop_spec where companyName = 'Dell'", conn)
    HP = pd.read_sql_query("select * from laptop_spec where companyName = 'Hewlett Packard'", conn)
    Lenovo = pd.read_sql_query("select * from laptop_spec where companyName = 'Lenovo'", conn)
    Microsoft = pd.read_sql_query("select * from laptop_spec where companyName = 'Microsoft'", conn)
    MSI = pd.read_sql_query("select * from laptop_spec where companyName = 'MSI'", conn)
    Razor = pd.read_sql_query("select * from laptop_spec where companyName = 'Razor'", conn)
    Samsung = pd.read_sql_query("select * from phone_spec where companyName = 'Samsung'", conn)
    Samsung2 = pd.read_sql_query("select * from tablet_spec where companyName = 'Samsung'", conn)
    Xiaomi = pd.read_sql_query("select * from phone_spec where companyName = 'Xiaomi'", conn)
    
    prod_list = []
    
    if (dd2_option.get()) == 'Apple':
         prod_type_df = pd.DataFrame(Apple,columns=['phoneName', 'productID','companyName','phoneStorage','color','frontcampixel','backcampixel','processor','extStoragecapacity','phoneOS','phoneOS_version','price'])
         prod_type_df1 = pd.DataFrame(AppleLap,columns=['lapName', 'productID','companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
         prod_type_df2 = pd.DataFrame(AppleTab,columns=['tabName', 'productID','companyName','screenResolution','processor','RAM','tabStorage','tabOS','tabOS_version','price'])
         prod_list.extend(list(prod_type_df.iloc[:,0]))
         prod_list.extend(list(prod_type_df1.iloc[:,0]))
         prod_list.extend(list(prod_type_df2.iloc[:,0]))
    elif (dd2_option.get()) == 'Dell':
        prod_type_df = pd.DataFrame(Dell,columns=['lapName', 'productID','companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    elif (dd2_option.get()) == 'Hewlett Packard':
        prod_type_df = pd.DataFrame(HP,columns=['lapName', 'productID','companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    elif (dd2_option.get()) == 'Lenovo':
        prod_type_df = pd.DataFrame(Lenovo,columns=['lapName', 'productID','companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    elif (dd2_option.get()) == 'Microsoft':
        prod_type_df = pd.DataFrame(Microsoft,columns=['lapName', 'productID','companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    elif (dd2_option.get()) == 'Samsung':
        prod_type_df = pd.DataFrame(Samsung,columns=['phoneName', 'productID','companyName','phoneStorage','color','frontcampixel','backcampixel','processor','extStoragecapacity','phoneOS','phoneOS_version','price'])
        prod_type_df1 = pd.DataFrame(Samsung2,columns=['tabName', 'productID','companyName','screenResolution','processor','RAM','tabStorage','tabOS','tabOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
        prod_list.extend(list(prod_type_df1.iloc[:,0]))
    elif (dd2_option.get()) == 'Xiaomi':
        prod_type_df = pd.DataFrame(Xiaomi,columns=['phoneName', 'productID','companyName','phoneStorage','color','frontcampixel','backcampixel','processor','extStoragecapacity','phoneOS','phoneOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    elif (dd2_option.get()) == 'MSI':
        prod_type_df = pd.DataFrame(MSI,columns=['lapName', 'productID','companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    else:
        prod_type_df = pd.DataFrame(Razor,columns=['lapName', 'productID','companyName','screenresolution','processor','RAM','GPU','internalStorage','lapOS','lapOS_version','price'])
        prod_list.extend(list(prod_type_df.iloc[:,0]))
    
    cart_but = tk.Button(screen19, text = "Cart" ,command = cart)
    cart_but.place(relx = 0.875, rely = 0.05)
    
    dic1 = {}

    row_val = 0
    for x in list(prod_list):
        tk.Label(screen19, text = x).grid(row = row_val, column = 3)
        dic1[x] = tk.Button(screen19, text = str(x), command = lambda a = x :data1(a))
        dic1[x].grid(row = row_val, column = 9)
        row_val = row_val + 1
        

def data1(item):
    screen17 = tk.Toplevel(screen)
    screen17.title("Data")
    screen17.geometry("800x800")
    
    cart_but = tk.Button(screen17, text = "Cart" ,command = cart)
    cart_but.place(relx = 0.875, rely = 0.05)
    
    if (item in list(prod_type_df.iloc[:,0])):
        details = prod_type_df.loc[prod_type_df.iloc[:,0] == item].iloc[0]
    elif (item in list(prod_type_df1.iloc[:,0])):
        details = prod_type_df1.loc[prod_type_df1.iloc[:,0] == item].iloc[0]
    elif (item in list(prod_type_df2.iloc[:,0])):
        details = prod_type_df2.loc[prod_type_df2.iloc[:,0] == item].iloc[0]

    
    tk.Label(screen17, text = details).pack()
    
    add_cart_but = tk.Button(screen17, text = "Add to Cart" ,command = lambda a = details :add_to_cart(a))
    add_cart_but.pack()
    

def add_address():
    screen23 = tk.Toplevel(screen)
    screen23.title("Edit Address")
    screen23.geometry("1000x900")
    
    global address_line_1
    global address_line_2
    global city
    global state
    global zipcode
    
    address_line_1 = tk.StringVar()
    address_line_2 = tk.StringVar()
    city = tk.StringVar()
    state = tk.StringVar()
    zipcode = tk.StringVar()
    
    addr_list = []
    addr = pd.read_sql_query("select * from address_table",conn)
    addr_df = pd.DataFrame(addr,columns=['addrID','addressLine1','addressLine2','zipcode','city','state_a'])
    for i in range(len(addr_df)):
        addr_list.append(list(addr_df.iloc[i]))
    
    
    tk.Label(screen23, text = 'Shipping Address', font=("Ariel", 18)).pack()
    tk.Label(screen23).pack()
    tk.Label(screen23, text = 'Address Line 1', font=("Ariel", 18)).pack()
    tk.Label(screen23).pack()
    tk.Entry(screen23, textvariable = address_line_1).pack()
    tk.Label(screen23).pack()
    tk.Label(screen23, text = 'Address Line 2', font=("Ariel", 18)).pack()
    tk.Label(screen23).pack()
    tk.Entry(screen23, textvariable = address_line_2).pack()
    tk.Label(screen23).pack()
    tk.Label(screen23, text = 'City', font=("Ariel", 18)).pack()
    tk.Label(screen23).pack()
    tk.Entry(screen23, textvariable = city).pack()
    tk.Label(screen23).pack()
    tk.Label(screen23, text = 'State', font=("Ariel", 18)).pack()
    tk.Label(screen23).pack()
    tk.Entry(screen23, textvariable = state).pack()
    tk.Label(screen23).pack()
    tk.Label(screen23, text = 'Zipcode', font=("Ariel", 18)).pack()
    tk.Label(screen23).pack()
    tk.Entry(screen23, textvariable = zipcode).pack()
    tk.Label(screen23).pack()
    
    tk.Button(screen23, text = "Save" ,command = addr_save).pack()

def addr_save():
    addressLine1 = address_line_1.get()
    addressLine2 = address_line_2.get()
    ZipCode = zipcode.get() 
    City = city.get()
    State = state.get()
    
    done()
    tbl.execute("INSERT INTO address_table (addressLine1,addressLine2,zipcode,city,state_a) VALUES (?,?,?,?,?)",addressLine1,addressLine2,ZipCode,City,State)
    conn.commit()
    ''' Save the address to the database'''
    

def edit_save():
    addrLine1 = address_line_1.get()
    addrLine2 = address_line_2.get()
    Zip = zipcode.get() 
    Ci = city.get()
    St = state.get()
    addr1 = address_1[0]
    done() 
    tbl.execute('update address_table set addressLine1 = ?, addressLine2 = ?,zipcode=?,city=?,state_a=? where addrID = ?',addrLine1,addrLine2,Zip,Ci,St,addr1)
    conn.commit()

    
    
def edit_address1(*args):
    screen22 = tk.Toplevel(screen)
    screen22.title("Edit Address")
    screen22.geometry("1000x900")
    
    
    global address_line_1
    global address_line_2
    global city
    global state
    global zipcode
    
    address_line_1 = tk.StringVar()
    address_line_2 = tk.StringVar()
    city = tk.StringVar()
    state = tk.StringVar()
    zipcode = tk.StringVar()
    
    global address_1

    address_1 = addr_edit_option.get().split("', '")
    address_1[0] = address_1[0][2:]
    address_1[-1] = address_1[-1][:-2]
    
    tk.Label(screen22, text = 'Address Line 1', font=("Ariel", 18)).pack()
    tk.Label(screen22).pack()
    ent = tk.Entry(screen22, textvariable = address_line_1)
    ent.insert(0, address_1[1])
    ent.pack()
    tk.Label(screen22).pack()
    tk.Label(screen22, text = 'Address Line 2', font=("Ariel", 18)).pack()
    tk.Label(screen22).pack()
    ent = tk.Entry(screen22, textvariable = address_line_2)
    ent.insert(0, address_1[2])
    ent.pack()
    tk.Label(screen22).pack()
    tk.Label(screen22, text = 'City', font=("Ariel", 18)).pack()
    tk.Label(screen22).pack()
    ent = tk.Entry(screen22, textvariable = city)
    ent.insert(0, address_1[3])
    ent.pack()
    tk.Label(screen22).pack()
    tk.Label(screen22, text = 'State', font=("Ariel", 18)).pack()
    tk.Label(screen22).pack()
    ent = tk.Entry(screen22, textvariable = state)
    ent.insert(0, address_1[4])
    ent.pack()
    tk.Label(screen22).pack()
    tk.Label(screen22, text = 'Zipcode', font=("Ariel", 18)).pack()
    tk.Label(screen22).pack()
    ent = tk.Entry(screen22, textvariable = zipcode)
    ent.insert(0, address_1[5])
    ent.pack()
    tk.Label(screen22).pack()
    tk.Button(screen22, text = 'Save' ,command = edit_save).pack()
    

def edit_address():
    screen21 = tk.Toplevel(screen)
    screen21.title("Edit Address")
    screen21.geometry("1000x900")
    
    addr_list = []
    addr = pd.read_sql_query("select * from address_table",conn)
    addr_df = pd.DataFrame(addr,columns=['addrID','addressLine1','addressLine2','zipcode','city','state_a'])
    for i in range(len(addr_df)):
        addr_list.append(list(addr_df.iloc[i]))
        
    
    global addr_edit_option
    addr_edit_option = tk.StringVar()
    
    addr_edit_option.trace('w', edit_address1)
        
    tk.OptionMenu(screen21, addr_edit_option, *addr_list).pack()

def delete_address1(*args):
    address_1 = addr_delete_option.get().split("', '")
    address_1[0] = address_1[0][2:]
    address_1[-1] = address_1[-1][:-2]
    
    text = 'Address deleted succfully  ' + address_1[0] 
    tk.Label(screen24, text = text , font=("Ariel", 18)).pack()

def delete_address():
    global screen24
    add = address_1[0]
    screen24 = tk.Toplevel(screen)
    screen24.title("Delete Address")
    screen24.geometry("1000x900")
    
#    print(add)
    addr_list = []
    addr = pd.read_sql_query("select * from address_table",conn)
    addr_df = pd.DataFrame(addr,columns=['addrID','addressLine1','addressLine2','zipcode','city','state_a'])
    for i in range(len(addr_df)):
        addr_list.append(list(addr_df.iloc[i]))
    
    tbl.execute('delete from address_table where addrID = ?',add)
        
    
    global addr_delete_option
    addr_delete_option = tk.StringVar()
    
    addr_delete_option.trace('w', delete_address1)
        
    tk.OptionMenu(screen24, addr_delete_option, *addr_list).pack()

    
def option1(*args):
    myapp()
    
def option2(*args):
    myapp1()


def address():
    screen20 = tk.Toplevel(screen)
    screen20.title("Address")
    screen20.geometry("400x400")
    tk.Button(screen20, text = "Add" ,command = add_address).pack()
    tk.Button(screen20, text = "Edit" ,command = edit_address).pack()
    tk.Button(screen20, text = "Delete" ,command = delete_address).pack()

def add_payment_save():
    ACCNumber = account_number.get()
    CCNum=card_number.get()
    exp_date=expiry_date.get()
    Name = name_card.get()
    
    tbl.execute("INSERT INTO payment_details (AccountNumber,CCNumber,ExpiryDate,NameonCard) VALUES (?,?,?,?)",ACCNumber,CCNum,exp_date,Name)
    conn.commit()
    
    done()

   
def add_paymnet():
    screen26 = tk.Toplevel(screen)
    screen26.title("Payment")
    screen26.geometry("1500x850")
    
    global account_number
    global card_number
    global name_card
    global expiry_date

    
    account_number = tk.StringVar()
    card_number = tk.StringVar()
    name_card = tk.StringVar()
    expiry_date = tk.StringVar()
   
    
    card_list = []
    global card_df
    card = pd.read_sql_query("select * from payment_details",conn)
    card_df = pd.DataFrame(card,columns=['AccountNumber','CCNumber','ExpiryDate','NameonCard'])
    
    for i in range(len(card_df)):
        card_list.append(list(card_df.iloc[i])

    tk.Label(screen26, text = 'Enter the Payment Details', font=("Ariel", 18)).pack()
    tk.Label(screen26).pack()
    tk.Label(screen26, text = 'Account Number', font=("Ariel", 18)).pack()
    tk.Label(screen26).pack()
    tk.Entry(screen26, textvariable = account_number).pack()
    tk.Label(screen26).pack()
    tk.Label(screen26, text = 'Card Number', font=("Ariel", 18)).pack()
    tk.Label(screen26).pack()
    tk.Entry(screen26, textvariable = card_number).pack()
    tk.Label(screen26).pack()
    tk.Label(screen26, text = 'Name on the Card', font=("Ariel", 18)).pack()
    tk.Label(screen26).pack()
    tk.Entry(screen26, textvariable = name_card).pack()
    tk.Label(screen26).pack()
    tk.Label(screen26, text = 'Expiry', font=("Ariel", 18)).pack()
    tk.Label(screen26).pack()
    tk.Entry(screen26, textvariable = expiry_date).pack()
    tk.Label(screen26).pack()
    tk.Button(screen26, text = "Save" ,command = add_payment_save).pack()


def edit_payment_save():
    AccNumber = account_number.get()
    Exp = expiry_date.get()
    Name = name_card.get()
    cc = card_number.get()
   
    payment1 = payment_1[1]
    bl.execute('update payment_details set AccountNumber = ?, ExpiryDate = ?, NameonCard = ? where CCNumber = ?',AccNumber,Exp,Name,cc)
    conn.commit()
    done()
    


def edit_payment1(*args):
#    global screen27
    screen27 = tk.Toplevel(screen)
    screen27.title("Payment")
    screen27.geometry("1500x850")
    global card_number
    global account_number
    global name_card
    global account_number
    account_number = tk.StringVar()
    card_number = tk.StringVar()
    name_card = tk.StringVar()
    expiry_date = tk.StringVar()
    
    
    global payment_1
    

    
    payment_1 = pay_edit_option.get().split("', '")
    payment_1[0] = payment_1[0][2:]
    payment_1[-1] = payment_1[-1][:-2]
    print(payment_1)

    tk.Label(screen27, text = 'Enter the Payment Details', font=("Ariel", 18)).pack()
    tk.Label(screen27).pack()
    tk.Label(screen27, text = 'Account Number', font=("Ariel", 18)).pack()
    tk.Label(screen27).pack()
    ent = tk.Entry(screen27, textvariable = account_number)
    ent.insert(0, payment_1[0])
    ent.pack()
    tk.Label(screen27).pack()
    tk.Label(screen27, text = 'Card Number', font=("Ariel", 18)).pack()
    tk.Label(screen27).pack()
    ent = tk.Entry(screen27, textvariable = card_number)
    ent.insert(0, payment_1[1])
    ent.pack()
    tk.Label(screen27).pack()
    tk.Label(screen27, text = 'Name on the Card', font=("Ariel", 18)).pack()
    tk.Label(screen27).pack()
    ent = tk.Entry(screen27, textvariable = name_card)
    ent.insert(0, payment_1[2])
    ent.pack()
    tk.Label(screen27).pack()
    tk.Label(screen27, text = 'Expiry', font=("Ariel", 18)).pack()
    tk.Label(screen27).pack()
    ent = tk.Entry(screen27, textvariable = expiry_date)
    ent.insert(0, payment_1[3])
    ent.pack()
    tk.Button(screen27, text = "Save" ,command = edit_payment_save).pack()

def edit_payment():
    screen27 = tk.Toplevel(screen)
    screen27.title("Edit Payment")
    screen27.geometry("1000x900")
    
    card_list = []
    card = pd.read_sql_query("select * from payment_details",conn)
    card_df = pd.DataFrame(card,columns=['AccountNumber','CCNumber','ExpiryDate','NameonCard'])

    for i in range(len(card_df)):
        card_list.append(list(card_df.iloc[i]))
    global pay_edit_option
    pay_edit_option = tk.StringVar()
    
    pay_edit_option.trace('w', edit_payment1)
        
    tk.OptionMenu(screen27, pay_edit_option, *card_list).pack()

def delete_pay1(*args):
    pay_1 = pay_delete_option.get().split("', '")
    pay_1[0] = pay_1[0][2:]
    pay_1[-1] = pay_1[-1][:-2]
    pay = payment_1[1]
    
    text = 'Payment deleted succfully  ' + pay_1[0] 
    tk.Label(screen28, text = text , font=("Ariel", 18)).pack()
    tbl.execute('Delete from payment_details where CCNumber = ?',pay)

def delete_payment():
    global screen28
    screen28 = tk.Toplevel(screen)
    screen28.title("Delete Address")
    screen28.geometry("1000x900")
    
    card_list = []
    card = pd.read_sql_query("select * from payment_details",conn)
    card_df = pd.DataFrame(card,columns=['AccountNumber','CCNumber','ExpiryDate','NameonCard'])
    for i in range(len(card_df)):
        card_list.append(list(card_df.iloc[i]))
    global pay_delete_option
    pay_delete_option = tk.StringVar()
    
    pay_delete_option.trace('w', delete_pay1)
        
    tk.OptionMenu(screen28, pay_delete_option, *card_list).pack()


def pay_options():
    screen25 = tk.Toplevel(screen)
    screen25.title("Payment Options")
    screen25.geometry("400x400")
    
    
    
    tk.Button(screen25, text = "Add" ,command = add_paymnet).pack()
    tk.Button(screen25, text = "Edit" ,command = edit_payment).pack()
    tk.Button(screen25, text = "Delete" ,command = delete_payment).pack()

def cancel_order(order_1):
    '''cancel the order order_1'''
    

def order_details(order_1):
    screen30 = tk.Toplevel(screen)
    screen30.title("Data")
    screen30.geometry("800x800")
    order_df = pd.DataFrame()
    details = order_df.loc[order_df.iloc[:,0] == order_1].iloc[0]
    
    tk.Label(screen30, text = details).pack()
    
    tk.Button(screen30, text = "Cancel Order" ,command = lambda a = details :cancel_order(a)).pack()
    


def my_orders():
    screen29 = tk.Toplevel(screen)
    screen29.title("Orders")
    screen29.geometry("1000x1000")
    
    dic = {}
    
    order = pd.read_sql_query('select * from orders_prod',conn)
    
    orders_df = pd.DataFrame(order,columns=['orderID','orderDate','orderTime','orderQty','transactionID'])
    row_val = 0
    for x in list(orders_df.iloc[:,0]):
        tk.Label(screen29, text = x).grid(row = row_val, column = 3)
        dic[x] = tk.Button(screen29, text = str(x), command = lambda a = x :order_details(a))
        dic[x].grid(row = row_val, column = 9)
        row_val = row_val + 1
    
    

def option3(*args):
    if dd3_option.get() == 'My Address':
        address()
    elif dd3_option.get() == 'Payment Options':
        pay_options()
    elif dd3_option.get() == 'Orders':
        my_orders()
    else:
        screen6.destroy()

def cust_search():
    
    global username1
    
    login_details_df = pd.read_csv(login_file)
    if employee.get() in list(login_details_df['username']):
        username1 = employee.get()
        session()
    else:
        print(list(login_details_df['username']))
    
def empl_session():
    screen_e = tk.Toplevel(screen)
    screen_e.title("Employee Login")
    screen_e.geometry("2000x800")
    global employee
    employee = tk.StringVar()

    logo = tk.Label(screen_e, text = "TRIDENT",font=("Chiller", 32))
    logo.place(relx = 0, rely = 0)
    display_name = tk.Label(screen_e, text = "Welcome " + username2 ,font=("Arial", 16))
    display_name.place(relx = 0.875, rely = 0)
    
    tk.Label(screen_e, text = 'Enter Employe Details', font=("Ariel", 18)).pack()
    tk.Entry(screen_e, textvariable = employee).pack()
    
    tk.Button(screen_e, text = "Search" ,command = cust_search).pack()



  
def login_success():
    session()
    
def login_success1():
    empl_session()
    
def cart():
    global screen14
    global qty_list
    global cart_df
    screen14 = tk.Toplevel(screen)
    screen14.title("Cart")
    screen14.geometry("800x600")
    
    cart_df = cart_df1

    qty_list = []
    
    for i in range(len(cart_df)):
        qty_list.append(tk.StringVar())
        tk.Label(screen14, text = cart_df['productName'][i]).place(x = 10, y = (i * 25))
        tk.Label(screen14, text = cart_df['price'][i]).place(x = 200, y = (i * 25))
        tk.Entry(screen14, textvariable = qty_list[i]).place(x = 350, y = (i * 25))
        
    tk.Button(screen14, text = "Procees to Payment" ,command = checkout).pack(side='bottom')
    

def checkout():
    global screen13
    global amount
    global address_line_1
    global address_line_2
    global city
    global state
    global zipcode
    global addr_option
    screen13 = tk.Toplevel(screen14)
    screen13.title("Check Out")
    screen13.geometry("2000x800")
    address_line_1 = tk.StringVar()
    address_line_2 = tk.StringVar()
    city = tk.StringVar()
    state = tk.StringVar()
    zipcode = tk.StringVar()
    addr_option = tk.StringVar()
        
    addr_list = []
    addr = pd.read_sql_query("select * from address_table",conn)
    addr_df = pd.DataFrame(addr,columns=['addressLine1','addressLine2','city','state_a','zipcode'])
    
    amount = 0
    
    for i in range(len(addr_df)):
        addr_list.append(list(addr_df.iloc[i][1:5]))
    
    for i in range(len(qty_list)):
        amount = amount + (float(cart_df['price'][i][1:]) * int(qty_list[i].get()))
    
    tk.Button(screen13, text = "Proceed to Payment",height = "2", width = "30", command = payment).pack(side = 'right')
    tk.Label(screen13, text = 'Select Address', font=("Ariel", 18)).pack()
    tk.Label(screen13).pack()
    tk.Label(screen13, text = 'Total Amount', font=("Ariel", 18)).pack()
    tk.Label(screen13).pack()
    tk.Label(screen13, text = amount, font=("Ariel", 18)).pack()
    tk.Label(screen13).pack()
    tk.OptionMenu(screen13, addr_option, *addr_list).pack()
    tk.Label(screen13).pack()
     


def payment():
    global screen15
    screen15 = tk.Toplevel(screen)
    screen15.title("Payment")
    screen15.geometry("1500x850")
    global account_number
    global card_number
    global expiry_date
    
    
    add_2 = addr_option.get().split("', '")
    add_2[0] = add_2[0][2:]
    add_2[-1] = add_2[-1][:-2]

    '''if (add_2[0] != ''):'''

    global card_option
    card_option = tk.StringVar()

    tk.Button(screen15, text = "Pay",height = "2", width = "30", command = order).pack(side = 'right')
    #card_df = pd.read_excel(file, sheet_name = "cards")
    
  
    
    card_list = []
    card = pd.read_sql_query("select * from payment_details",conn)
    card_df = pd.DataFrame(card,columns=['AccountNumber','CCNumber','ExpiryDate'])
    
    for i in range(len(card_df)):
        card_list.append(list(card_df.iloc[i]))
      
    tk.Label(screen15, text = 'Total Amount', font=("Ariel", 18)).pack()
    tk.Label(screen15).pack()
    tk.Label(screen15, text = amount, font=("Ariel", 18)).pack()
    tk.Label(screen15).pack()
    tk.OptionMenu(screen15, card_option, *card_list).pack()
    tk.Label(screen15).pack()



def order():
    global screen16
    screen16 = tk.Toplevel(screen)
    screen16.title("Payment")
    screen16.geometry("1500x850")
    

    card_2 = card_option.get().split("', '")
    card_2[0] = card_2[0][2:]
    card_2[-1] = card_2[-1][:-2]
    
#    print(cart_df.iloc[0, 0])
    
    productId = cart_df.iloc[0, 0]
    
    orderQty = qty_list[0].get()
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time(),
    temp = float(1)
    
    
    tk.Label(screen16, text = 'Order Details', font=("Ariel", 18)).pack()
    
    tk.Label(screen16, text = 'Yor order has been placed Thank you Trident.', font=("Ariel", 18)).pack()
    
def done():
    global screen32
    screen32 = tk.Toplevel(screen)
    screen32.title("Success")
    screen32.geometry("300x250")
    
    tk.Label(screen32, text = "Success").pack()
    

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
    name_info = firstname.get()
    
    tbl.execute("INSERT INTO customer (CustName, Email,pass) VALUES (?,?,?)",name_info,username_info,password_info)
    conn.commit()
    df = pd.read_csv(login_file)
    temp_dp = pd.DataFrame(columns = ['username', 'password'])
    df.reset_index(drop = True)
    df = df.append({'username': username_info, 'password': password_info}, ignore_index=True)
    temp_dp['username'] = df['username']
    temp_dp['password'] = df['password']

   
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
    global firstname
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

    x = pd.read_sql_query('select * from customer',conn)
    login_details_df = pd.DataFrame(x,columns=['custID','CustName','Email','pass'])
    if username1 in list(login_details_df['Email']):
        a = login_details_df.loc[login_details_df['Email'] == username1, 'pass'].iloc[0]
        if password1 == a:
            login_success()
        else:
            incorrect_password()
    else:
        user_not_found()
    

def login_verify1():
    global username_verify
    global username2
    username2 = username_verify.get()
    password2 = password_verify.get()
    username_entry1.delete(0, tk.END)
    password_entry1.delete(0, tk.END)

    login_details_df = pd.read_csv(login_file)
    
    if username2 in list(login_details_df['username']):
        a = login_details_df.loc[login_details_df['username'] == username2, 'password'].iloc[0]
        if password2 == a:
            login_success1()
        else:
            incorrect_password()
    else:
        user_not_found()


    
def cust_login():
    global screen2
    screen2 = tk.Toplevel(screen)
    screen2.title("Customer Login")
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


def emp_login():
    global screen2
    screen2 = tk.Toplevel(screen)
    screen2.title("Employee Login")
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
    tk.Button(screen2, text = "Login", width = 10, height = 1, command = login_verify1).pack()
    tk.Button(screen2, text = "Back", width = 10, height = 1, command = back2).pack()
    
def guest():
    global username1
    global password1
    username1 = 'guest'
    password1 = 'guest'
    login_success()
    

def login():
    global screen0
    screen0 = tk.Toplevel(screen)
    screen0.title("Login")
    screen0.geometry("300x250")
    tk.Label(screen0, text = "Please enter details below to log in").pack()
    tk.Label(screen0).pack()
    screen.resizable(False,False)
    tk.Label(screen0).pack()
    tk.Button(screen0, text = "Customer Login", height = "2", width = "30", command = cust_login).pack()
    tk.Label(screen0).pack()
    tk.Button(screen0, text= "Employee login", height = "2", width = "30", command = emp_login).pack()
    tk.Label(screen0).pack()
    tk.Button(screen0, text= "Guest", height = "2", width = "30", command = guest).pack()
  


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











