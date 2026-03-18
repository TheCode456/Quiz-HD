import json
import os
import customtkinter as ctk
def leaderboard_cal(user):
    with open(f"users/{user}","r") as file:
        data=json.load(file)
    xp=data.get("xp",0)
    stats=data["stats"]
    correct=stats.get("correct",0)
    wrong=stats.get("wrong",0)
    skip=stats.get("skipped",0)
    point=xp
    point=point-(10*wrong)
    repeat=stats.get("repeat",0)
    point=point-(repeat*15)
    point=point+(correct*5)
    point=point-(skip*2)
    quizzes_played=data["quizzes_played"]
    point=point+(quizzes_played*5)
    if point<0:
        point=0
    return point

def clear_content(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def showFormula():
    wind=ctk.CTkToplevel()
    wind.geometry(f"900x500")
    wind.resizable(False,False)

    with open("assets/lead.txt","r") as f:
        txt=f.read()
    txt_bx=ctk.CTkTextbox(wind,font=("Arial",16),wrap="word",height=500)
    txt_bx.pack(fill="both")
    txt_bx.insert(1.0,txt)
    txt_bx['state']="disabled"
    wind.mainloop()

def show_leaderboard(frame):
    usernames=os.listdir("users/")
    usernames.remove("imgs")
    unsorted_points=[]
    clear_content(frame)
    
    for users in usernames:
        d=leaderboard_cal(users)
        unsorted_points.append(d)

    rows=len(usernames)
    cols=3
    ctk.CTkLabel(frame,text="Leaderboard",font=("Airal",18,"bold")).pack(side="top",pady=20)
    content_frame=ctk.CTkScrollableFrame(frame,width=600,height=400,fg_color="#1E293B",scrollbar_button_hover_color="#2563EB")
    content_frame.pack()
    content_frame.pack_propagate()
    content_frame.grid_columnconfigure(cols)
    content_frame.grid_rowconfigure(rows)
    content_frame.grid_anchor("center")
    title_rank=ctk.CTkLabel(content_frame,text="Rank",font=("Airal",16,"bold"))
    title_player=ctk.CTkLabel(content_frame,text="User",font=("Airal",16,"bold"))
    title_score=ctk.CTkLabel(content_frame,text="Score",font=("Airal",16,"bold"))
    title_rank.grid(column=0,row=0,padx=50,pady=30)
    title_player.grid(column=1,row=0,padx=50,pady=30)
    title_score.grid(column=2,row=0,padx=50,pady=30)
    
    for i in range(1,len(usernames)+1):
        rank=i
        point=max(unsorted_points)
        username=usernames[unsorted_points.index(point)][:-5]
        ctk.CTkLabel(content_frame,text=rank,font=("Airal",14)).grid(column=0,row=i,padx=50,pady=30)
        ctk.CTkLabel(content_frame,text=username,font=("Airal",14)).grid(column=1,row=i,padx=50,pady=30)
        ctk.CTkLabel(content_frame,text=point,font=("Airal",14)).grid(column=2,row=i,padx=50,pady=30)
        usernames.remove(usernames[unsorted_points.index(point)])
        unsorted_points.remove(point)
    info_btn=ctk.CTkButton(frame,text="i",width=5,font=("Arial",15,"italic"),fg_color="#1e293b",hover_color="#2563EB",text_color="#94A3B8",command=showFormula)
    info_btn.pack(side="bottom",anchor="se",padx=20,pady=5)
