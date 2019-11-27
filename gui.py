# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 23:25:23 2019

@author: monic
"""


import tkinter as tk
import pandas as pd

file_path = r'D:\All Docs\Masters\CS425 Database Organization\Project\Code\Login_details.csv'
 

import os
 
def delete2():
  screen3.destroy()
 
def delete3():
  screen4.destroy()
 
def delete4():
  screen5.destroy()
   
def login_sucess():
  global screen3
  screen3 = tk.Toplevel(screen)
  screen3.title("Success")
  screen3.geometry("150x100")
  tk.Label(screen3, text = "Login Sucess").pack()
  tk.Button(screen3, text = "OK", command =delete2).pack()
 
def password_not_recognised():
  global screen4
  screen4 = tk.Toplevel(screen)
  screen4.title("Success")
  screen4.geometry("150x100")
  tk.Label(screen4, text = "Password Error").pack()
  tk.Button(screen4, text = "OK", command =delete3).pack()
 
def user_not_found():
  global screen5
  screen5 = tk.Toplevel(screen)
  screen5.title("Success")
  screen5.geometry("150x100")
  tk.Label(screen5, text = "User Not Found").pack()
  tk.Button(screen5, text = "OK", command =delete4).pack()
 
   
def register_user():
   
  username_info = username.get()
  password_info = password.get()
 
  df = pd.read_csv(file_path)
  temp_dp = pd.DataFrame(columns = ['username', 'password'])
  df.reset_index(drop = True)
  df = df.append({'username': username_info, 'password': password_info}, ignore_index=True)
  temp_dp['username'] = df['username']
  temp_dp['password'] = df['password']
  temp_dp.to_csv(file_path)
   
  username_entry.delete(0, tk.END)
  password_entry.delete(0, tk.END)
  firstname_entry.delete(0, tk.END)
  lastname_entry.delete(0, tk.END)
 
  tk.Label(screen1, text = "Registration Sucess", fg = "green" ,font = ("calibri", 11)).pack()
 
def login_verify():
   
  username1 = username_verify.get()
  password1 = password_verify.get()
  username_entry1.delete(0, tk.END)
  password_entry1.delete(0, tk.END)
 
  list_of_files = os.listdir()
  if username1 in list_of_files:
    file1 = open(username1, "r")
    verify = file1.read().splitlines()
    if password1 in verify:
        login_sucess()
    else:
        password_not_recognised()
 
  else:
        user_not_found()
   
 
 
def register():
  global screen1
  screen1 = tk.Toplevel(screen)
  screen1.title("Register")
  screen1.geometry("400x350")
   
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
 
def login():
  global screen2
  screen2 = tk.Toplevel(screen)
  screen2.title("Login")
  screen2.geometry("300x250")
  tk.Label(screen2, text = "Please enter details below to login").pack()
  tk.Label(screen2, text = "").pack()
 
  global username_verify
  global password_verify
   
  username_verify = tk.StringVar()
  password_verify = tk.StringVar()
 
  global username_entry1
  global password_entry1
   
  tk.Label(screen2, text = "Username * ").pack()
  username_entry1 = tk.Entry(screen2, textvariable = username_verify)
  username_entry1.pack()
  tk.Label(screen2, text = "").pack()
  tk.Label(screen2, text = "Password * ").pack()
  password_entry1 = tk.Entry(screen2, textvariable = password_verify)
  password_entry1.pack()
  tk.Label(screen2, text = "").pack()
  tk.Button(screen2, text = "Login", width = 10, height = 1, command = login_verify).pack()
   
   
def main_screen():
  global screen
  screen = tk.Tk()
  screen.geometry("300x250")
  screen.title("Notes 1.0")
  tk.Label(text = "Application Started", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
  tk.Label(text = "").pack()
  tk.Button(text = "Login", height = "2", width = "30", command = login).pack()
  tk.Label(text = "").pack()
  tk.Button(text = "Register",height = "2", width = "30", command = register).pack()
 
  screen.mainloop()
 
main_screen()