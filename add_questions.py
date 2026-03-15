import customtkinter as ctk
import json
from tkinter import filedialog,messagebox
def get_data(entries,title,lvl,gnr):
    json_format=[]
    for r in range(len(entries)):
        row=[e.get() for e in entries[r]]
        options=[]
        options.append(row[1])
        options.append(row[2])
        options.append(row[3])
        options.append(row[4])
        q={
            "question":row[0],
            "options":options,
            "correct_index": int(row[5])
        }
        json_format.append(q)
    set_info={
        "title":title,
        "level":lvl,
        "genre":gnr
    }
    with open(f"assets/questions/{title}.json","w")as file:
            data={
                "set_info":set_info,
                "questions":json_format
            }
            if title==None or title=="":
                return
            json.dump(data,file,indent=4)
            print("done")
        

def add():
    app = ctk.CTk()
    app.geometry("900x500")
    ti=ctk.CTkInputDialog(text="Title")
    title=ti.get_input()
    lvl=ctk.CTkInputDialog(text="level")
    level=lvl.get_input()
    genr=ctk.CTkInputDialog(text="Genre")
    genre=genr.get_input()
    row=ctk.CTkInputDialog(text="No of questions")
    try:
        rows=int(row.get_input())
    except:#user cancelled
        rows=10
    

    frame = ctk.CTkScrollableFrame(app)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    headers = [
        "SlNo",
        "Question",
        "Option1",
        "Option2",
        "Option3",
        "Option4",
        "Correct Index"
    ]

    # Create header row
    for col, text in enumerate(headers):
        label = ctk.CTkLabel(frame, text=text)
        label.grid(row=0, column=col, padx=5, pady=5)


    entries = []   # this will store all entry widgets

    for r in range(rows):

        row_entries = []   # store entries for this row

        # SlNo
        ctk.CTkLabel(frame, text=str(r+1)).grid(row=r+1, column=0, padx=5, pady=5)

        # Question
        q = ctk.CTkEntry(frame, width=200)
        q.grid(row=r+1, column=1, padx=5, pady=5)
        row_entries.append(q)

        # Options
        for c in range(2, 6):
            opt = ctk.CTkEntry(frame, width=120)
            opt.grid(row=r+1, column=c, padx=5, pady=5)
            row_entries.append(opt)

        # Correct Index
        correct = ctk.CTkOptionMenu(frame,values=["0","1","2","3"],width=70)
        correct.set("0")
        correct.grid(row=r+1, column=6, padx=5, pady=5)
        row_entries.append(correct)

        entries.append(row_entries)
    button=ctk.CTkButton(app,text="Save",command=lambda:get_data(entries,title,level,genre))
    button.pack(side="bottom")

    app.mainloop()

def check_quiz_file(path):

    try:
        with open(str(path), "r") as f:
            data = json.load(f)
    except Exception as e:
        return str(e)

    # check set_info
    if "set_info" not in data:
        return "no set info"

    set_info = data["set_info"]

    for key in ["title", "level", "genre"]:
        if key not in set_info:
            return f"Missing '{key}' in set_info"

    # check questions
    if "questions" not in data:
        return "Missing 'questions' section"

    if not isinstance(data["questions"], list):
        return "'questions' must be a list"

    for i, q in enumerate(data["questions"], start=1):

        if "question" not in q:
            return f"Question {i} missing 'question'"

        if "options" not in q:
            return f"Question {i} missing 'options'"

        if "answer_index" not in q:
            return f"Question {i} missing 'answer_index'"

        # check options
        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            return f"Question {i} must contain exactly 4 options"

        # check answer_index
        if not isinstance(q["answer_index"], int) or q["answer_index"] not in [0,1,2,3]:
            return f"Question {i} has invalid answer_index (must be 0-3)"

    return True
def upload():
    import assets.show_format as s
    path=filedialog.askopenfile(title="Select Quiz JSON",filetypes=[("JSON Files","*.json")])
    json_data=check_quiz_file(path.name)
    if json_data:
        json_data=json.load(path)
    if json_data!=True:
        messagebox.showerror("Not correct",str(json_data))
        s.show_format()
        return

    f=ctk.CTkInputDialog(text="Filename")
    try:
        with open(f"assets/questions/{f.get_input()}.json","w")as file:
            json.dump(json_data,file,indent=4)
    except Exception as e:
        messagebox.showerror("Error",str(e))
        s.show_format()