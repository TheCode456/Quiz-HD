from files_check import checking

if not checking():
    quit()
    #it is above all to save cpu power loading all stuff without need as it may crash
import sys
import traceback
from tkinter import messagebox,filedialog

def global_exception_handler(exc_type, exc_value, exc_traceback):#global error handler
    err = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    messagebox.showerror("Unexpected Error", err)
def tkinter_exception_handler(exc, val, tb):
    err = "".join(traceback.format_exception(exc, val, tb))
    messagebox.showerror("Application Error", err)

sys.excepthook = global_exception_handler
import json
import os
from xpCalculator import convert_level,actual_xp,required_xp,xp_required
import customtkinter as ctk
from login import login
from Quiz import Quiz
from PIL import Image
from add_questions import add,upload
from assets.leaderboard import show_leaderboard


# ---------- BASIC CONFIG ----------
ctk.set_appearance_mode("dark")       
ctk.set_default_color_theme("dark-blue")  

# ---------- ROOT WINDOW ----------
root = ctk.CTk()
root.title("My App")
root.geometry("1080x720")              # width x height
root.minsize(810,540)                # minimum size
root.resizable(False, False)       
root.configure(bg="#16213E")
root.report_callback_exception = tkinter_exception_handler #check for any error and show properly.

#  Center window on screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (500 // 2)
root.geometry(f"900x500+{x}+{y}")

# ---------- START ----------
def clear_content(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def Quiz_Window(username,window):
    clear_content(window)
    completed_frame=ctk.CTkScrollableFrame(window,width=(window.winfo_width()-30),corner_radius=10,fg_color="#1E293B",height=225)
    completed_frame.pack(side="bottom",pady=10,padx=10)
    uncompleted_frame=ctk.CTkScrollableFrame(window,width=(window.winfo_width()-30),corner_radius=10,fg_color="#1E293B",height=225)
    uncompleted_frame.pack(side="top",pady=10,padx=10)
    ctk.CTkLabel(completed_frame,text="Completed Quizzes",text_color="#F1F5F9",font=("Arial",20,"bold")).pack(anchor="nw",padx=5,pady=5)
    ctk.CTkLabel(uncompleted_frame,text="Pending Quizzes",text_color="#F1F5F9",font=("Arial",20,"bold")).pack(anchor="nw",padx=5,pady=5)
    with open(f"users/{username}.json","r") as file:
        data=json.load(file)
        completed=data["quizzes_completed"]

    files=os.listdir("assets/questions")

    # clear old widgets
    for widget in completed_frame.winfo_children():
        widget.destroy()

    for widget in uncompleted_frame.winfo_children():
        widget.destroy()

    for f in files:

        if f in completed:
            ctk.CTkLabel(completed_frame,text=f.replace(".json",""),text_color="#94A3B8",font=("Arial",16,"bold")).pack(pady=3)

        else:
            frame=ctk.CTkFrame(uncompleted_frame)
            frame.pack(pady=5, padx=5)

            ctk.CTkButton(frame,text=f.replace(".json",""),text_color="#94A3B8",font=("Arial",16,"bold"),command=lambda x=f: Quiz(username,x,window)).pack()

    # empty messages
    if len(completed_frame.winfo_children()) == 0:
        ctk.CTkLabel(completed_frame,text="No Quiz Completed").pack(pady=10)

    if len(uncompleted_frame.winfo_children()) == 0:
        ctk.CTkLabel(uncompleted_frame,text="No Pending Quiz").pack(pady=10)
            


def info():
    window=ctk.CTkToplevel(root)
    window.title("Information")
    with open("assets/info.txt","r") as file:
        txt=str(file.read())
    text=ctk.CTkTextbox(window,width=1000,height=320,wrap="word")
    text.pack(expand=True,fill="both",padx=20,pady=20)
    text.insert("1.0",txt)
    text.focus_displayof()

def fill_in(username,quiz_played_lbl,correct_lbl,wrong_lbl,left_lbl,total_lbl,accuracy_lbl,overall_xp_lbl):

    path="users/"+username+".json"
    with open(path,"r") as file:
        data=json.load(file)
    quiz_played=data.get("quizzes_played",0)
    stats=data.get("stats", {}) or {}
    correct=stats.get("correct",0)
    wrong=stats.get("wrong",0)
    left=stats.get("skipped",0)
    total=correct+wrong+left
    if total==0:
        accuracy="0%"
    else:
        accuracy=str(round((correct/total)*100))+"%"
    overall_xp=data.get("xp",0)
    
    quiz_played_lbl.configure(text=quiz_played)
    correct_lbl.configure(text=correct)
    wrong_lbl.configure(text=wrong)
    left_lbl.configure(text=left)
    total_lbl.configure(text=total)
    accuracy_lbl.configure(text=accuracy)
    overall_xp_lbl.configure(text=overall_xp)

def fill_past(username,quiz_name_lbl,correct_lbl,wrong_lbl,left_lbl,accuracy_lbl,overall_xp_lbl):
    path="users/"+username+".json"
    with open(path,"r") as file:
        data=json.load(file)
    past_quiz = data.get("last_quiz")
    if not past_quiz:
        quiz_name_lbl.configure(text="No Quiz Played Yet")
        correct_lbl.configure(text="-")
        wrong_lbl.configure(text="-")
        left_lbl.configure(text="-")
        accuracy_lbl.configure(text="-")
        overall_xp_lbl.configure(text="-")
        return
    try:
        if past_quiz.get("quiz_name"):
            quiz_name = past_quiz.get("quiz_name").replace(".json","" ).replace("assets/questions/","")
        else:
            quiz_name = "No Quiz Played"
        correct = past_quiz.get("correct", 0)
        wrong = past_quiz.get("wrong", 0)
        left = past_quiz.get("skipped", 0)
        total = correct + wrong + left
        if total == 0:
            accuracy = "0%"
        else:
            accuracy = str(round((correct/total)*100)) + "%"
        overall_xp = past_quiz.get("xp", 0)
    except Exception:
        quiz_name = "No Quiz Played"
        correct = "-"
        wrong = "-"
        left = "-"
        accuracy = "-"
        overall_xp = "-"

    quiz_name_lbl.configure(text=quiz_name)
    correct_lbl.configure(text=correct)
    wrong_lbl.configure(text=wrong)
    left_lbl.configure(text=left)
    accuracy_lbl.configure(text=accuracy)
    overall_xp_lbl.configure(text=overall_xp)

def dashboard(username,frame):
    clear_content(frame)
    text=str(username).capitalize()
    ctk.CTkLabel(frame,text=f"{text}'s Dashboard",font=("Arial", 34,"bold"),bg_color="transparent",fg_color="transparent",text_color="#F1F5F9").pack(pady=20,anchor="n")
    framew=int((frame.winfo_width())*0.8)
    framey=int((frame.winfo_height())*0.2)
    stats=ctk.CTkFrame(frame,width=framew,height=framey,fg_color="#0F172A",corner_radius=20)
    stats.pack(side="right",fill="both")


    with open(f"users/{username}.json", "r") as f:
        data=json.load(f)
        level=data["level"]
        xp=data["xp"]
    
    simple_container=ctk.CTkFrame(stats,fg_color="#1F2A3A",corner_radius=10)
    simple_container.pack(expand=True,anchor="ne",pady=10,padx=20)
    level_lbl=ctk.CTkLabel(simple_container,text=f"Level: {level}",font=("Arial", 19),bg_color="transparent",text_color="#F59E0B",corner_radius=20)
    xp_lbl=ctk.CTkLabel(simple_container,text=f"XP: {actual_xp(xp)}",font=("Arial", 19),bg_color="transparent",text_color="#84CC16",corner_radius=20)#,text_color="#0F172A"
    level_lbl.pack(pady=10,padx=20)
    xp_lbl.pack(pady=10,padx=20)
    # horizontal row container for question controls
    row = ctk.CTkFrame(frame, fg_color="transparent")
    row.pack(pady=20)

    ctk.CTkLabel(row, text="Questions:", font=("Arial", 20), bg_color="transparent").pack(side="left")
    
    values=os.listdir("assets/questions/")
    if not values:
        values=["No Questions Available"]
    else:
        for i in range(len(values)):
            values[i]=values[i][:-5]

    def go():
        if questions.get():
            question=questions.get()
            Quiz(username,(question+".json"),frame)
        else:
            messagebox.showerror("No Questions","Please select question set from the dropdown menu")

    questions=ctk.CTkOptionMenu(row,values=values,font=("Arial",20),width=200,fg_color="#1F2A3A",button_color="#3B82F6",button_hover_color="#2563EB",text_color="#F1F5F9",text_color_disabled="#6B7280",dropdown_fg_color="#1F2A3A",dropdown_text_color="#F1F5F9",dropdown_hover_color="#374151")
    questions.pack(side="left",padx=10)

    go_btn=ctk.CTkButton(row,text="GO!",font=("Arial",20),width=50,fg_color="#3b82f6",hover_color="#2563eb",command=go)
    go_btn.pack(side="left",padx=10)
    if not os.listdir("assets/questions/"):
        go_btn.configure(state="disabled") # turn off button funtionality if no question set avl

    ctk.CTkButton(frame,bg_color="transparent",fg_color="transparent",text_color="white",hover_color="#1c2b50",text="To know more about the xp calculation and levels algorithm. Click Here",command=info).pack(side="top",pady=8)

    total_stats=ctk.CTkFrame(frame,fg_color="#1f2a3a",bg_color="transparent",corner_radius=20)
    total_stats.pack(side="left",anchor="sw",pady=20,padx=20)
    ctk.CTkLabel(total_stats,text="Overall Statistics",font=("Arial",25,"bold"),fg_color="transparent",text_color="#f1f5f9").pack(side="top",pady=(15,0),padx=10)#first is top padding and 2nd is  bottom

    f=ctk.CTkFrame(total_stats,fg_color="#1E293B")
    f.pack(side="bottom",expand=True)
    
    quiz_played_title=ctk.CTkLabel(f,text="No of Quiz Played: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    quiz_played_title.grid(padx=5,pady=5,column=0,row=0)
    correct_title=ctk.CTkLabel(f,text="Correct: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    correct_title.grid(padx=5,pady=5,column=0,row=1)
    wrong_title=ctk.CTkLabel(f,text="Wrong: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    wrong_title.grid(padx=5,pady=5,column=0,row=2)
    left_title=ctk.CTkLabel(f,text="Skipped: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    left_title.grid(padx=5,pady=5,column=0,row=3)
    total_title=ctk.CTkLabel(f,text=f"Total Questions:",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    total_title.grid(padx=5,pady=5,column=0,row=4)
    accuracy_title=ctk.CTkLabel(f,text=f"Accuracy: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    accuracy_title.grid(padx=5,pady=5,column=0,row=5)
    overall_xp_title=ctk.CTkLabel(f,text=f"Score(total xp): ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    overall_xp_title.grid(padx=5,pady=5,column=0,row=6)

    quiz_played=ctk.CTkLabel(f,text="No of Quiz Played: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    quiz_played.grid(padx=5,pady=5,column=2,row=0)
    correct=ctk.CTkLabel(f,text="Correct: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    correct.grid(padx=5,pady=5,column=2,row=1)
    wrong=ctk.CTkLabel(f,text="Wrong: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    wrong.grid(padx=5,pady=5,column=2,row=2)
    left=ctk.CTkLabel(f,text="Skipped: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    left.grid(padx=5,pady=5,column=2,row=3)
    total=ctk.CTkLabel(f,text=f"Total Questions:",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    total.grid(padx=5,pady=5,column=2,row=4)
    accuracy=ctk.CTkLabel(f,text=f"Accuracy: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    accuracy.grid(padx=5,pady=5,column=2,row=5)
    overall_xp=ctk.CTkLabel(f,text=f"total xp: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    overall_xp.grid(padx=5,pady=5,column=2,row=6)

    fill_in(username,quiz_played,correct,wrong,left,total,accuracy,overall_xp)

    last_frame = ctk.CTkFrame(frame, fg_color="#1E293B", corner_radius=20, width=500, height=700)
    last_frame.pack(pady=20)
    last_frame.pack_propagate(False)
    last_frame.grid_propagate(False)
    last_frame.grid_columnconfigure(0, weight=1)
    last_frame.grid_columnconfigure(1, weight=1)
    title = ctk.CTkLabel(last_frame,text="Last Quiz Statistics",font=("Arial",25,"bold"),wraplength=450,fg_color="transparent",text_color="#f1f5f9")
    title.grid(row=0, column=0, columnspan=2, pady=(10,15))
    quiz_name_title=ctk.CTkLabel(last_frame,text="Quiz Played: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    correct_titl=ctk.CTkLabel(last_frame,text="Correct: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    wrong_titl=ctk.CTkLabel(last_frame,text="Wrong: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    left_titl=ctk.CTkLabel(last_frame,text="Skipped: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    accuracy_titl=ctk.CTkLabel(last_frame,text="Accuracy: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    overall_xp_titl=ctk.CTkLabel(last_frame,text="Score(total xp): ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    quiz_name_title.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    correct_titl.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    wrong_titl.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    left_titl.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    accuracy_titl.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    overall_xp_titl.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    quiz_name=ctk.CTkLabel(last_frame,text="Quiz Played: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    quiz_name.grid(padx=5,pady=5,column=1,row=1, sticky="w")

    correct_past=ctk.CTkLabel(last_frame,text="Correct: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    correct_past.grid(padx=5,pady=5,column=1,row=2, sticky="w")

    wrong_past=ctk.CTkLabel(last_frame,text="Wrong: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    wrong_past.grid(padx=5,pady=5,column=1,row=3, sticky="w")

    left_past=ctk.CTkLabel(last_frame,text="Skipped: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    left_past.grid(padx=5,pady=5,column=1,row=4, sticky="w")

    accuracy_past=ctk.CTkLabel(last_frame,text="Accuracy: ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    accuracy_past.grid(padx=5,pady=5,column=1,row=5, sticky="w")

    overall_xp_past=ctk.CTkLabel(last_frame,text="Score(total xp): ",font=("Arial",15),fg_color="transparent",text_color="#f1f5f9")
    overall_xp_past.grid(padx=5,pady=5,column=1,row=6, sticky="w")

    fill_past(username,quiz_name,correct_past,wrong_past,left_past,accuracy_past,overall_xp_past)

    lvl_frame=ctk.CTkFrame(frame,fg_color="#1E293B",corner_radius=20,height=300,width=150)
    lvl_frame.place(relx=0.975,rely=0.95,anchor="se")
    lvl_frame.pack_propagate(False)

    lvl_progress=ctk.CTkProgressBar(lvl_frame,orientation="vertical",width=20,progress_color="#22c55e",fg_color="#334155",height=200)
    lvl_progress.pack(anchor="n",padx=20,pady=20,expand=True)
    lvl_progress.set(required_xp(username))
    xp_needed_title=ctk.CTkLabel(lvl_frame,text="XP to next level",font=("Arial",10),bg_color="transparent",text_color="#f1f5f9")
    xp_needed_title.pack(pady=(0,5))
    xp_needed=ctk.CTkLabel(lvl_frame,font=("Arial",15,"bold"),bg_color="transparent",text_color="#f1f5f9")
    xp_needed.pack(pady=(0,10))
    xp_needed.configure(text=xp_required(username))


        
def update_pic(user,lbl):
    file_path = filedialog.askopenfilename(
        title="Select Profile Picture",
        filetypes=[("Image Files",["*.png","*.jpg"])]
    )

    if not file_path:
        return  # user cancelled

    # Open image using PIL
    img = Image.open(file_path)

    # Resize to consistent size
    img = img.resize((120, 120))

    # Save as PNG
    img.save(f"users/imgs/{user}.png")
    lbl.configure(image=open_profile_image(user))

def delete_user(username):
    statement="Are you sure you want to delete all your data.\nEverything including your quiz history,xp,stats and profile data will be cleared from our database and you will no longer able to recover them.\nClick yes to continue and no to cancel"
    cnf=messagebox.askyesno("Confirm",statement)
    if cnf:
        ask=ctk.CTkInputDialog(text="Enter your password to confirm")
        password=ask.get_input()
        with open(f"users/{username}.json","r") as file:
            data=json.load(file)
        if data["password"]==password:
            os.remove(f"users/{username}.json")
            try:
                os.remove(f"users/imgs/{username}.png")
                os.remove("remember.txt")
            except:
                pass
            root.destroy()
        else:
            messagebox.showerror("Wrong Password","To delete your account please enter the correct password of your account")

def Profile(frame,userid,lbl):
    clear_content(frame)
    
    ctk.CTkLabel(frame,text="User Settings",font=("Arial", 34, "bold"),bg_color="transparent",fg_color="transparent").pack(pady=20,anchor="n")
    ctk.CTkLabel(frame,text="Change Profile Picture",font=("Arial", 20),bg_color="transparent",fg_color="transparent").pack(pady=10,anchor="n")
    ctk.CTkButton(frame,text="Upload New Picture",font=("Arial", 15),fg_color="#3B82F6",hover_color="#2563EB",command=lambda:update_pic(userid,lbl)).pack(pady=10,anchor="n")
    with open(f"users/{userid}.json", "r") as f:
        data=json.load(f)
        passw=data["password"]
    pass_entry=ctk.CTkEntry(frame,placeholder_text=passw,width=200)
    pass_entry.pack(pady=10,anchor="n")
    ctk.CTkButton(frame,text="Change Password",font=("Roboto", 15),fg_color="#3B82F6",hover_color="#2563EB",command=lambda: change_password(userid,pass_entry.get())).pack(pady=10,anchor="n")
    ctk.CTkButton(frame,text="Delete User",font=("Roboto", 15),fg_color="#A41919",hover_color="#6A1010",command=lambda: delete_user(userid)).pack(pady=10,side="bottom")
    ctk.CTkButton(frame,text="Remove Auto Login(remember me)",font=("Roboto", 15),fg_color="#3B82F6",hover_color="#2563EB",command=lambda: [os.remove("remember.txt"), messagebox.showinfo("Success", "Auto Login Removed Successfully")]).pack(pady=10,side="top")

def change_password(userid,new_password):
    with open(f"users/{userid}.json", "r") as f:
        data=json.load(f)
    data["password"]=new_password
    if not new_password:
        messagebox.showerror("Error","Password cannot be empty")
        return
    with open(f"users/{userid}.json", "w") as f:
        json.dump(data,f,indent=4)#indent ncreases readability by adding newlines and indentation to the JSON data.
        messagebox.showinfo("Success", "Password changed successfully")

def delete_question_set(q):
    statement="Are you sure you want to delete this question set.\nThis action cannot be undone.\nClick yes to continue and no to cancel"
    cnf=messagebox.askyesno("Conform",statement)
    if cnf:
        try:
            os.remove(f"assets/questions/{q}")
            messagebox.showinfo("Deleted",f"{q.replace('.json','')} question set has been deleted successfully")
            root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error",f"Failed to delete question set: {e}")
####################################################################################################
resize_job = None
def show_question_set(frame,user):
    clear_content(frame)

    questions=[]
    number=0
    for file in os.listdir("assets/questions/"):
        questions.append(file)
        number+=1
    add_button_frame=ctk.CTkFrame(frame,width=frame.winfo_width(),height=50,fg_color="#16213e")
    add_button_frame.pack(pady=5,side="top",padx=10)
    add_button_frame.pack_propagate(False)
    upload_btn=ctk.CTkButton(add_button_frame,text="Upload Questions(json)",text_color="#f1f5f9",corner_radius=5,command=upload)
    manual_btn=ctk.CTkButton(add_button_frame,text="Add Questions Manually",text_color="#f1f5f9",corner_radius=5,command=add)
    upload_btn.pack(side="left",padx=100)
    manual_btn.pack(side="right",padx=100)

    if number>3:
        question_frame=ctk.CTkScrollableFrame(frame,fg_color="#0F172A")
        question_frame.pack(fill="both",expand=True)
    else:
        question_frame=ctk.CTkFrame(frame,fg_color="#0F172A")
        question_frame.pack(fill="both",expand=True)

    frame.update_idletasks()
    frame_width = frame.winfo_width()

    cols = max(1, frame_width // 240)  # Calculate number of columns based on frame width and desired card width (220 + padding)
    for set in range(number):
        row = set // cols
        col = set % cols
        f=ctk.CTkFrame(question_frame,width=220,height=150,fg_color="#1E293B",corner_radius=12)
        f.grid(row=row, column=col, padx=20, pady=20) # pack stacks widget up to down but grid allows you to place widgets in a 2D grid.
        f.grid_propagate(False) # propogate means that the frame will adjust its size to fit the content inside it. By setting grid_propagate(False), you are telling the frame to maintain its specified width and height (220x150 in this case) regardless of the size of the widgets inside it. 
        with open(f"assets/questions/{questions[set]}","r") as file:
            data=json.load(file)
        info=data["set_info"]
        title=info["title"]
        difficulty="Difficulty: "+info["level"]
        genere="Genre: "+info["genre"]
        if info["level"]=="easy":
            font_color="#84CC16"
        elif info["level"]=="medium":
            font_color="#F59E0B"
        else:
            font_color="#F87171"
        ctk.CTkLabel(f,text=title,font=("Roboto", 17, "bold")).pack(pady=15,padx=15)
        ctk.CTkLabel(f,text=difficulty,font=("Roboto", 15),text_color=font_color).pack(pady=15,padx=15)
        ctk.CTkLabel(f,text=genere,font=("Roboto", 15)).pack(pady=15,padx=15)
        ctk.CTkButton(f,text="Start Quiz",font=("Roboto", 15),fg_color="#3B82F6",hover_color="#2563EB",command=lambda q=questions[set]:[ Quiz(user,q,frame)]).pack(pady=10)
        ctk.CTkButton(f,text="Delete Set",font=("Roboto", 15),fg_color="#A41919",hover_color="#6A1010",command=lambda q=questions[set]:[delete_question_set(q),show_question_set(frame,user)]).pack(pady=10)

    
def open_profile_image(username):
    try:
        pic=Image.open(f"users/imgs/{username}.png")
    except:
        pic=Image.open("assets/default.png")
    return ctk.CTkImage(light_image=pic,dark_image=pic,size=(120, 120))

def open_dashboard(username):
    show_main(username)

def show_main(username):
    # Clear entire window
    for widget in root.winfo_children():
        widget.destroy()

    convert_level(username)

    root.configure(fg_color="#0F172A")
    sidebar = ctk.CTkFrame(root, fg_color="#1E293B")
    sidebar.pack(side="left", fill="y")

    content_frame = ctk.CTkFrame(root, fg_color="#0F172A")
    content_frame.pack(side="right", fill="both", expand=True)
    ctk.CTkLabel(sidebar,text="Settings",font=("Arial",34,"bold"),bg_color="transparent",fg_color="transparent",corner_radius=20).pack(side="top",pady=10)
    

    profile_image = open_profile_image(username)
    img_lbl=ctk.CTkLabel(sidebar, image=profile_image, text="",corner_radius=50)
    img_lbl.pack(side="top",pady=20)
    ctk.CTkButton(sidebar,text="Logout",font=("Arial", 15, "bold"),fg_color="transparent",text_color="#F87171",hover_color="#7F1D1D",border_width=1,border_color="#7F1D1D",command=lambda:root.destroy()).pack(side="bottom",pady=10)

    user_settings=ctk.CTkButton(sidebar,text="User Settings",font=("Arial", 15, "bold"),text_color="#F1F5F9",fg_color="#3B82F6",hover_color="#2563EB",cursor="hand2",command=lambda:[Profile(content_frame,username,img_lbl)])
    user_settings.pack(pady=10,side="bottom")

    dashboard_txt=ctk.CTkButton(sidebar,text="Dashboard",font=("Arial", 15, "bold"),text_color="#F1F5F9",fg_color="#3B82F6",hover_color="#2563EB",cursor="hand2",command=lambda:dashboard(username,content_frame))
    dashboard_txt.pack(side="top",pady=10)

    dashboard(username,content_frame)

    quiz_btn=ctk.CTkButton(sidebar,text="Quiz",font=("Arial", 15, "bold"),text_color="#F1F5F9",fg_color="#3B82F6",hover_color="#2563EB",command=lambda:Quiz_Window(username,content_frame))
    quiz_btn.pack(side="top",pady=10)

    question_set_btn=ctk.CTkButton(sidebar,text="Question Set",font=("Arial", 15, "bold"),text_color="#F1F5F9",fg_color="#3B82F6",hover_color="#2563EB",command=lambda:show_question_set(content_frame,username))
    question_set_btn.pack(side="top",pady=10)

    leader_btn=ctk.CTkButton(sidebar,text="Leaderboard",font=("Arial", 15, "bold"),text_color="#F1F5F9",fg_color="#3B82F6",hover_color="#2563EB",command=lambda:show_leaderboard(content_frame))
    leader_btn.pack(side="top",pady=10)
root.after(100, lambda: login(root, open_dashboard))

root.mainloop()