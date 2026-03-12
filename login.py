import customtkinter as ct
from tkinter import messagebox
from tkinter import PhotoImage
import json
import os
from autocorrect import ensure_user_structure

def adduser():
    # prompt for username/password and validate
    username_dialog = ct.CTkInputDialog(text="Username")
    user = username_dialog.get_input()

    # if the user cancelled or entered nothing, abort
    if not user:
        return

    passw_dialog = ct.CTkInputDialog(text="Password")
    password = passw_dialog.get_input()
    if not password:
        return

    usernames = get_users()
    if user in usernames:
        messagebox.showerror("Error", "Username already exists")
        return

    database = {
        "username": user,
        "password": password,
    }
    path_to_json = f"users/{user}.json"
    with open(path_to_json, "w") as j:
        json.dump(database, j)

    # ensure future reads have the full structure so the UI doesn't crash
    try:
        ensure_user_structure(path_to_json)
    except Exception:
        # if something goes wrong, delete the file to avoid a half-baked user
        os.remove(path_to_json)
        messagebox.showerror("Error", "Failed to create user")
        return

def get_users():
    usernames = []

    for file in os.listdir("users"):
        if file.endswith(".json"):
            username = file[:-5]   # remove ".json"
            usernames.append(username)

    return usernames

def openuser(username):
    filename="users/"+username+".json"
    with open(filename,"r") as j:
        data=json.load(j)
        dialogue=ct.CTkInputDialog(text="Password")
        var1=dialogue.get_input()
        realpass=data["password"]
        if realpass==var1:
            statement=("User Verified")
            return True,username

        else:
            statement=("Invalid Credentials")
            return False,None
        
def verify_password(username, entered_pass, frame, window, on_success, add_button, pass_entry):

    filename = f"users/{username}.json"

    try:
        with open(filename, "r") as j:
            data = json.load(j)

        if data["password"] == entered_pass:
            frame.destroy()
            on_success(username)

        else:
            messagebox.showerror("Error", "Wrong Password")
            pass_entry.configure(border_color="#EF4444")
            window.after(800, lambda: pass_entry.configure(border_color="#3B82F6"))

            # Clear entry and refocus
            pass_entry.delete(0, "end")
            pass_entry.focus()

    except FileNotFoundError:
        messagebox.showerror("Login Error", "User does not exist")

    except json.JSONDecodeError:
        messagebox.showerror("Login Error", "User file corrupted")

    except Exception as e:
        messagebox.showerror("Login Error", f"Unexpected error:\n{e}")
def handle_login(username, frame, window, on_success, add_button):

    # Remove old password widgets
    for widget in frame.winfo_children():
        if hasattr(widget, "is_password_widget"):
            widget.destroy()

    pass_label = ct.CTkLabel(
        frame,
        text=f"Enter password for {username}",
        text_color="#F1F5F9"
    )
    pass_label.pack(pady=(10, 5))
    pass_label.is_password_widget = True

    pass_entry = ct.CTkEntry(
        frame,
        placeholder_text="Password",
        show="*",
        width=200
    )
    pass_entry.pack(pady=5)
    pass_entry.is_password_widget = True

    pass_entry.focus()

    # Change Add User → Confirm Password
    add_button.configure(text="Confirm Password",fg_color="#10B981",hover_color="#059669",command=lambda: verify_password(username,pass_entry.get(),frame,window,on_success,add_button,pass_entry))
def login(window,on_success):
    usernames=get_users()
    for username in usernames:
        ensure_user_structure("users/" + username + ".json")
    frame_log=ct.CTkScrollableFrame(window,width=250,height=200,fg_color="#334155")
    ct.CTkLabel(frame_log,text="Users",bg_color="transparent",fg_color="transparent",corner_radius=25,text_color="#F1F5F9",font=("Arial", 20)).pack(side="top",pady=20)
    frame_log.place(relx=0.35,rely=0.3)

    button_frame=ct.CTkFrame(frame_log,width=500,height=100,bg_color='transparent',fg_color='transparent')
    button_frame.pack(side="bottom",pady=20)
    def refresh_users():
        # clear old buttons
        for widget in button_frame.winfo_children():
            widget.destroy()

        usernames = get_users()
        for i in usernames:
            ct.CTkButton(button_frame,text=i,fg_color="#3B82F6",hover_color="#2563EB",command=lambda u=i: handle_login(u,frame_log,window,on_success,add_button)).pack(pady=5)

    add_button = ct.CTkButton(window,text="Add User",fg_color="#3B82F6",hover_color="#2563EB",command=lambda: [adduser(), refresh_users()])
    add_button.pack(pady=50, side='bottom')

    refresh_users()

        