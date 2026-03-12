import json
import random
from customtkinter import *
import autocorrect
from xpCalculator import difficulty_multiplier,convert_level

import os

def save_progress(username, gained_xp, quizname, correct, wrong, skip):
    file_path = f"users/{username}.json"
    # if the file does not exist or is empty, start from a sane default
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        data = {
            "xp": 0,
            "quizzes_played": 0,
            "stats": {"correct": 0, "wrong": 0, "skipped": 0},
            "last_quiz": {}
        }
    else:
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            # corrupted or empty file – reset to defaults
            data = {
                "xp": 0,
                "quizzes_played": 0,
                "stats": {"correct": 0, "wrong": 0, "skipped": 0},
                "last_quiz": {}
            }

    # update the progress values
    xp = data.get("xp", 0) + gained_xp
    quiz_no = data.get("quizzes_played", 0) + 1
    stats = data.get("stats", {"correct": 0, "wrong": 0, "skipped": 0})
    quiz_name = quizname
    last_correct = correct
    last_wrong = wrong
    last_skip = skip
    last_xp = gained_xp
    total_correct = stats.get("correct", 0) + last_correct
    total_wrong = stats.get("wrong", 0) + last_wrong
    total_skip = stats.get("skipped", 0) + last_skip
    # ensure we have a list and strip out any None entries before updating
    done = data.get("quizzes_completed", [])
    # filter out None values 
    done = [q for q in done if q is not None]
    if quizname not in done:
        quiz=quizname.replace(".json","") and quizname.replace("assets/questions/","")
        done.append(quizname)
        for i in range(len(done)):
            done[i]=done[i].replace("assets/questions/","")
    data["quizzes_completed"]=done
    if xp<0:
        xp=0
        if data["level"]>0:
            data["level"]=data["level"]-1

    data["xp"] = xp
    data["quizzes_played"] = quiz_no
    stats["correct"] = total_correct
    stats["wrong"] = total_wrong
    stats["skipped"] = total_skip
    data["stats"] = stats
    last = data.get("last_quiz", {})
    last["quiz_name"] = quiz_name
    last["xp"] = last_xp
    last["correct"] = last_correct
    last["wrong"] = last_wrong
    last["skip"] = last_skip
    data["last_quiz"] = last
    convert_level(username)

    # write the updated structure back out
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        


def Quiz(username, questions, window):
    for widget in window.winfo_children():
        widget.destroy()

    path = "assets/questions/" + questions

    with open(path, "r") as file:
        data = json.load(file)

    all_questions = data["questions"]
    total = len(all_questions)

    index = 0

    progressbar=CTkProgressBar(window,width=700,progress_color="#3B82F6",height=12)
    progressbar.pack(side="top")
    progress = CTkLabel(window, font=("Roboto", 20))
    progress.pack(pady=(40,20))
    question_card = CTkFrame(window,fg_color="#17223B",corner_radius=14)
    text = CTkLabel(question_card, font=("Roboto", 22), wraplength=700)#wraplength is used to wrap the text after a certain length to prevent it from going out of the window
    text.pack(pady=20,padx=30)
    question_card.pack(pady=25)
    timer_text = CTkLabel(window, font=("Roboto", 18))
    timer_text.pack(pady=10,side="bottom")
    timer_bar = CTkProgressBar(window, width=400, height=10)
    timer_bar.pack(side="bottom",pady=10)
    optionFrame=CTkFrame(window,fg_color="transparent",corner_radius=14)
    optionFrame.pack(side="top",pady=20)
    option1=CTkButton(optionFrame,fg_color="#16213E",hover_color="#3B82F6",width=220,height=45,corner_radius=10)
    option2=CTkButton(optionFrame,fg_color="#16213E",hover_color="#3B82F6",width=220,height=45,corner_radius=10)
    option3=CTkButton(optionFrame,fg_color="#16213E",hover_color="#3B82F6",width=220,height=45,corner_radius=10)
    option4=CTkButton(optionFrame,fg_color="#16213E",hover_color="#3B82F6",width=220,height=45,corner_radius=10)
    option1.grid(column=0,row=0,pady=10,padx=10)
    option2.grid(column=0,row=1,pady=10,padx=10)
    option3.grid(column=1,row=0,pady=10,padx=10)
    option4.grid(column=1,row=1,pady=10,padx=10)

    time_left = 10
    gained_xp = 0
    questions_solved = 0
    questions_correct = 0
    questions_wrong = 0
    questions_left = 0
    time_id = None

    def summary():
        nonlocal index, questions_correct, questions_wrong, questions_left, time_id,gained_xp
        gained_xp=gained_xp+((questions_correct*20)-(questions_wrong*5))
        if questions_correct==total:
            gained_xp+=50
        gained_xp=difficulty_multiplier(path,gained_xp)
        title = CTkLabel(window,text="Quiz Summary",font=("Roboto", 32, "bold"))
        title.pack(pady=(30,20))
        # Container
        summary_frame = CTkFrame(window,fg_color="#17223B",corner_radius=15)
        summary_frame.pack(pady=20, padx=40)

        correct_frame=CTkFrame(summary_frame, fg_color="#1F2937", corner_radius=12)
        wrong_frame = CTkFrame(summary_frame, fg_color="#1F2937", corner_radius=12)
        left_frame = CTkFrame(summary_frame, fg_color="#1F2937", corner_radius=12)
        xp_frame = CTkFrame(summary_frame, fg_color="#1F2937", corner_radius=12)
        correct_frame.grid(row=0, column=0, padx=20, pady=20)
        wrong_frame.grid(row=0, column=1, padx=20, pady=20)
        left_frame.grid(row=1, column=0, padx=20, pady=20)
        xp_frame.grid(row=1, column=1, padx=20, pady=20)

        correct_label = CTkLabel(correct_frame,text="✅ Correct",font=("Roboto",18))
        correct_label.pack(padx=30, pady=(15,5))
        correct_value = CTkLabel(correct_frame,text=str(questions_correct),font=("Roboto",26,"bold"),text_color="#22C55E")
        correct_value.pack(pady=(0,15))
        wrong_label = CTkLabel(
        wrong_frame,text="❌ Wrong",font=("Roboto",18))
        wrong_label.pack(padx=30, pady=(15,5))
        wrong_value = CTkLabel(wrong_frame,text=str(questions_wrong),font=("Roboto",26,"bold"),text_color="#EF4444")
        wrong_value.pack(pady=(0,15))
        left_label = CTkLabel(left_frame,text="⏭ Skipped",font=("Roboto",18))
        left_label.pack(padx=30, pady=(15,5))
        left_value = CTkLabel(left_frame,text=str(questions_left),font=("Roboto",26,"bold"),text_color="#F59E0B")
        left_value.pack(pady=(0,15))
        xp_label = CTkLabel(xp_frame,text="⭐ XP Earned",font=("Roboto",18))
        xp_label.pack(padx=30, pady=(15,5))
        xp_value = CTkLabel(xp_frame,text=str(gained_xp),font=("Roboto",26,"bold"),text_color="#3B82F6")
        xp_value.pack(pady=(0,15))
        save_progress(username,gained_xp,path,questions_correct,questions_wrong,questions_left)

    def answer_process(user_answer):
        nonlocal index, questions_correct, questions_wrong, questions_left, time_id,gained_xp
        if index >= total:
            return
        q = all_questions[index]
        options=q["options"]
        correct=q["answer_index"]
        if correct==user_answer:
            questions_correct+=1
            if time_left>6:
                gained_xp+=5
            if time_left>3:
                gained_xp+=2
        else:
            questions_wrong+=1
        index+=1
        show_question()
        window.after_cancel(time_id)#cancels task

    random.shuffle(all_questions) #shuffles the questions to make it random each time
    def show_question():

        nonlocal index,time_left

        if index >= total:
            text.configure(text="Quiz Finished!",text_color="#22C55E")
            progress.configure(text="")
            questions_solved=questions_correct + questions_wrong
            if time_id is not None:
                window.after_cancel(time_id)
            for widget in optionFrame.winfo_children():
                widget.destroy()
            progressbar.destroy()
            timer_bar.destroy()
            timer_text.destroy()
            optionFrame.destroy()
            progress.destroy()
            summary()
            return

        q = all_questions[index]
        options=q["options"]
        correct=q["answer_index"]

        text.configure(text=q["question"])
        progress.configure(text=f"{index+1} of {total}")
        progressbar.set(((index+1)/total))
        option1.configure(text=options[0],command=lambda:answer_process(0))
        option2.configure(text=options[1],command=lambda:answer_process(1))
        option3.configure(text=options[2],command=lambda:answer_process(2))
        option4.configure(text=options[3],command=lambda:answer_process(3))

        #index += 1
        time_left = 10
        update_timer()

    def update_timer():
        nonlocal time_left, index, questions_left, time_id

        # make sure the label still exists before trying to update it
        if not timer_text.winfo_exists():
            return

        try:
            timer_text.configure(text=f"Time left: {time_left}s")
        except Exception:
            # widget may have been destroyed between calls
            return
        timer_bar.set(time_left / 10)

        if time_left <= 0:
            index += 1
            questions_left += 1
            show_question()
            return
        if time_left > 6:
            timer_bar.configure(progress_color="#22C55E")
        elif time_left > 3:
            timer_bar.configure(progress_color="#F59E0B")
        else:
            timer_bar.configure(progress_color="#EF4444")
        time_left -= 1
        time_id = window.after(1000, update_timer)

    show_question()