from tkinter import *
import csv
import pandas as pd

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
CHECK = "✔"
BLUE = "#053B50"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 20
reps = 0
PAUSED = False
paused_tracker = 0
timer = None

data_dict = {
    "Task": [],
    "Time": []
    }


def stop_watch():

    # ---------------------------- TIMER MECHANISM ------------------------------- # 
    def start_timer():
        global reps
        global paused_tracker
        global PAUSED

        window.config(bg=GREEN)
        canvas.config(bg=GREEN)

        start_button["state"] = DISABLED

        reps += 1  

        if reps % 8 == 0:
            count_down(0 * 60)
        elif reps % 2 == 0:
            count_down(0 * 60)
        else:
            count_down(0 * 60)


    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
    def count_down(count):
        global reps
        global PAUSED
        global timer
        global paused_time
        global count_min
        global count_sec

        count_min = count // 60
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        if count_min < 10:
            count_min = f"0{count_min}"

        canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")     

        if PAUSED == False:
            if count >= 0:
                timer = window.after(1000, count_down, count + 1)
        else:
            timer = window.after(0, count_down, count - 0)


    # ---------------------------- PAUSE MECHANISM ------------------------------- # 
    def pause_timer():
        global paused_tracker
        global PAUSED
        global timer

        paused_tracker += 1

        if paused_tracker % 2 != 0:
            PAUSED = True
            pause_button.config(text="Resume")
            window.config(bg=RED)
            canvas.config(bg=RED)
        else:
            PAUSED = False
            pause_button.config(text="Pause")
            window.config(bg=GREEN)
            canvas.config(bg=GREEN)

    # ---------------------------- DONE BUTTON ------------------------------- # 
    def done_button():
        global reps
        global PAUSED
        global paused_tracker
        global data_dict


        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text="00:00")

        start_button["state"] = NORMAL
        window.config(bg=BLUE)
        canvas.config(bg=BLUE)

        reps = 0
        paused_tracker = 0
        pause_button.config(text="Pause")
        PAUSED = False

        #-------------- APPEND DATA -----------------#
        data_dict["Task"].append(f"{task_entry.get()}")
        data_dict["Time"].append(f"{count_min}:{count_sec}")

        print(data_dict)

        #-------------- DATA TO CSV -----------------#
        data = pd.DataFrame(data_dict)
        data.to_csv("Session_data.csv", mode='w')



    # ---------------------------- UI SETUP ------------------------------- #
    window = Tk()
    window.attributes('-topmost', True)
    window.title("Work Stop Watch")
    window.minsize(width=450, height=50)
    window.maxsize(width=450, height=50)
    window.config(bg=BLUE)
  
    #Entry
    task_entry = Entry(width=12)
    task_entry.insert(END, string="Task Here")
    task_entry.grid(column=0,row=1)

    #Canvas
    canvas = Canvas(width=200, height=50, bg=BLUE, highlightthickness=0)
    timer_text = canvas.create_text(100, 25, text="00:00", fill="white", font=(FONT_NAME, 20, "bold"))
    canvas.grid(column=1, row=1)

    #Start Button
    start_button = Button(text="Start", font=("Arial", 9, "bold"), command=start_timer)
    start_button.grid(column=2, row=1)

    #Pause Button
    pause_button = Button(text="Pause", font=("Arial", 9, "bold"), command=pause_timer)
    pause_button.grid(column=3, row=1)

    #Done Button
    done_button = Button(text="DONE", font=("Arial", 9, "bold"), command=done_button)
    done_button.grid(column=4, row=1)

    window.mainloop()


if __name__ == "__main__":
    stop_watch()




