def checking():
    import os
    from tkinter import messagebox
    from pathlib import Path

    try:
        with open("remember.txt","r") as created:
            pass
    except:
        with open("remember.txt","w") as created:
            pass

    os.makedirs("users", exist_ok=True)
    os.makedirs("users/imgs", exist_ok=True)
    os.makedirs("assets", exist_ok=True)
    os.makedirs("assets/questions", exist_ok=True)

    files = [
        "autocorrect.py",
        "Quiz.py",
        "xpCalculator.py",
        "assets/info.txt",
        "assets/default.png"
    ]

    x = True

    for file in files:
        if not Path(file).exists():
            messagebox.showerror(
                "Missing Assets",
                "Some files are missing\nPlease reinstall app or contact developer to modify files"
            )
            x = False
            break

    return x