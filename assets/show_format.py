import customtkinter
import json
def show_format():
    root=customtkinter.CTk()
    root.geometry("250x500")
    with open("assets/format.json","r") as file:
        text=file.read()
    lbl=customtkinter.CTkLabel(root,text=text,compound="left")
    lbl.pack(side="top",anchor="center")
    root.mainloop()