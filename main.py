
import json
import pyttsx3
import time
from datetime import datetime
from carbonfootprint import get_response
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from tkinter import simpledialog

import threading


window_size = "400x400"
LIGHTGRAY="#EEEEEE"
WHITE="#FFFFFF"
DARKGREEN="#003333"
DARKGRAY = "#2a2b2d"
TORQUOISE = "#669999"
DARKBLUE= "#263b54"
NAVYBLUE="#1c2e44"
ALMOSTBLACK = "#0F0F0F"
MEDIUMGRAY = "#444444"
BRIGHTGREEN = "#33FF33"
GRAY="#4f4f4f"
VERYDARKGRAY = "#212121"
BLACK = "#000000"
HUMAN_BACKGROUND = LIGHTGRAY
AI_BACKGROUND = WHITE
class ChatInterface(Frame):
    """
    Draw the chat interface where user can chat with the bot
    """
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.speaker_thread = None
        self.event = threading.Event()
        self.master = master
        self.tl_bg = LIGHTGRAY
        self.tl_bg2 = LIGHTGRAY
        self.tl_fg = BLACK
        self.font = "Verdana 10"

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu, bd=5)
        
        file = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file)
        file.add_command(label="Save Chat Log", command=self.save_chat)
        file.add_command(label="Clear Chat", command=self.clear_chat)
        file.add_separator()
        file.add_command(label="Exit", command=self.chatexit)

        options = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=options)
        options.add_command(label="Speaker Settings", command=self.edit_response_settings)

        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default", command=self.font_change_default)
        font.add_command(label="Times", command=self.font_change_times)
        font.add_command(label="System", command=self.font_change_system)
        font.add_command(label="Helvetica", command=self.font_change_helvetica)
        font.add_command(label="Fixedsys", command=self.font_change_fixedsys)

        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=self.color_theme_default)
        color_theme.add_command(label="Gray", command=self.color_theme_grey)
        color_theme.add_command(label="Blue", command=self.color_theme_dark_blue)
        color_theme.add_command(label="Turquoise", command=self.color_theme_turquoise)
        color_theme.add_command(label="Matrix", command=self.color_theme_matrix)

        help_option = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="About me", command=self.msg)
        help_option.add_command(label="Train me!", command=self.about)

        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)

        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message_insert(None), activebackground=WHITE,
                                  activeforeground=BLACK)
        self.send_button.pack(side=LEFT, ipady=8)
        self.master.bind("<Return>", self.send_message_insert)
        self.default_speaker_values()
        self.last_sent_label(date="No messages sent.")
        self.color_theme_default()
    def default_speaker_values(self):
        self.speaker = pyttsx3.init()
        voices = self.speaker.getProperty('voices')  
        self.speaker.setProperty('rate', 200)
        self.speaker.setProperty('volume', 100)
        self.speaker.setProperty('voices',voices[0].id)

    def edit_response_settings(self):
        # Create a new top-level window for editing settings
        self.settings_window = Toplevel(self.master)
        self.settings_window.title("Edit Settings")
        
        # Create labels and entry fields for the settings
        label_speed = Label(self.settings_window, text="Speed:")
        entry_speed = Entry(self.settings_window)
        label_volume = Label(self.settings_window, text="Volume:")
        entry_volume = Entry(self.settings_window)
        
        # Create a label and radio buttons for selecting the speaker gender
        label_speaker = Label(self.settings_window, text="Speaker Gender:")
        speaker_var = IntVar(value=0)
        radio_male = Radiobutton(self.settings_window, text="Male", variable=speaker_var, value=0)
        radio_female = Radiobutton(self.settings_window, text="Female", variable=speaker_var, value=1)
        
        # Set the default values for the settings
        entry_speed.insert(0, "200")
        entry_volume.insert(0, "100")
        
        # Grid layout for the labels, entry fields, and radio buttons
        label_speed.grid(row=0, column=0, sticky="e")
        entry_speed.grid(row=0, column=1, padx=10)
        label_volume.grid(row=1, column=0, sticky="e")
        entry_volume.grid(row=1, column=1, padx=10)
        label_speaker.grid(row=2, column=0, sticky="e")
        radio_male.grid(row=2, column=1, sticky="w")
        radio_female.grid(row=2, column=1, sticky="e")
        
        # Create a button to save the settings
        save_button = Button(self.settings_window, text="Save", command=lambda: self.save_response_settings(entry_speed.get(), entry_volume.get(), speaker_var.get()))
        save_button.grid(row=3, column=1, pady=10)
            
    def save_response_settings(self, speed, volume, speaker_gender):
        # Convert the speed and volume to integers
        speed = int(speed)
        volume = int(volume)
        
        # Set the properties for the speaker
        self.speaker.setProperty('rate', speed)
        self.speaker.setProperty('volume', volume)
        
        # Select the appropriate voice based on the speaker gender
        voices = self.speaker.getProperty('voices')
        voice_id = voices[0].id if speaker_gender == 0 else voices[1].id
        self.speaker.setProperty('voice', voice_id)
        
        # Close the settings window
        self.settings_window.destroy()


    def save_chat(self):
        current_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        default_filename = f"Chatbot_history_{current_time}.txt"
        file_path = asksaveasfilename(defaultextension=".txt",initialfile=default_filename)
        if file_path:
            chat_history = self.text_box.get("1.0", "end-1c")
            try:
                with open(file_path,"w") as file:
                    file.write(chat_history)
                    messagebox.showinfo(title="Success!",message=f"Chat history was saved in {file_path}")
            except Exception as e:
                messagebox.showerror("Something went wrong!",str(e))
        else: messagebox.showerror(title="Failed!",message=f"Did not receive where to save")

    def thread_handler(self,response):
        if self.speaker_thread and self.speaker_thread.is_alive():
            self.event.set()

        self.event.clear()
        self.speaker_thread = threading.Thread(target=self.playresponse, args=(response,),daemon=True)
        self.speaker_thread.start()

    def playresponse(self, response):
        try:
            self.speaker.stop()
        except:
            pass
        self.speaker.say(response)
        self.speaker.runAndWait()

    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        exit()

    def msg(self):
        messagebox.showinfo("Carbon Footprint Assistant v1.0",
                                    "I specialize in carbon footprint reduction strategies, eco-friendly practices, sustainable living, and environmental conservation. I can offer guidance on these topics to help you make a positive impact on the environment.")

    def about(self):
        acknowledgment = "I understand that any info added here cannot be deleted or modified. "

        user_acknowledged = simpledialog.askstring("Type Confirm to acknowledge.", acknowledgment)

        if user_acknowledged == "Confirm":
            # Training screen
            keywords = simpledialog.askstring("Enter Keywords", "Enter the keywords (separated by commas):")
            response = simpledialog.askstring("Enter Response", "Enter the bot's response:")

            # Save the data as a JSON object
            new_data = {
                "type": "question",
                "keywords": [kw.strip() for kw in keywords.split(",")],
                "response": response.strip()
            }

            with open("data.json", "r+") as file:
                current_data = json.load(file)
                current_data.append(new_data)
                file.seek(0)
                json.dump(current_data, file, indent=4)
                file.truncate() 

            messagebox.showinfo("Confirmation", "Training data saved successfully!")
        else:
            messagebox.showerror("Error", "Please acknowledge the terms before proceeding.")


    def send_message_insert(self, event):
        user_input = self.entry_field.get()
        human_prompt = "Human: " + user_input + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, human_prompt)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)

        response = get_response(user_input)
        ai_response = "AI: " + response + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, ai_response)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        self.last_sent_label(str(time.strftime("Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.entry_field.delete(0, END)
        self.thread_handler(response)
        return response

    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

    def color_theme_default(self):
        PRIMARY_COLOR = "#afc1c6"  # Light blue-gray
        SECONDARY_COLOR = "#f3f4ef"  # Off-white
        TEXT_COLOR = "#000000"  # Black
        BUTTON_COLOR = "#f68081"  # Coral
        BORDER_COLOR = "#cacaca"  # Light gray
        
        self.master.config(bg=PRIMARY_COLOR)
        self.menu.config(bg=BUTTON_COLOR)
        self.text_frame.config(bg=PRIMARY_COLOR)
        self.entry_frame.config(bg=PRIMARY_COLOR)
        self.text_box.config(bg=SECONDARY_COLOR, fg=TEXT_COLOR)
        self.entry_field.config(bg=SECONDARY_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        self.send_button_frame.config(bg=PRIMARY_COLOR)
        self.send_button.config(bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_COLOR, activeforeground=TEXT_COLOR)
        self.sent_label.config(bg=PRIMARY_COLOR, fg=TEXT_COLOR)
        self.text_box.config(highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR)

        self.tl_bg = SECONDARY_COLOR
        self.tl_bg2 = PRIMARY_COLOR
        self.tl_fg = TEXT_COLOR


    def color_theme_dark(self):
        self.master.config(bg=DARKGRAY)
        self.text_frame.config(bg=DARKGRAY)
        self.text_box.config(bg=VERYDARKGRAY, fg=WHITE)
        self.entry_frame.config(bg=DARKGRAY)
        self.entry_field.config(bg=VERYDARKGRAY, fg=WHITE, insertbackground=WHITE)
        self.send_button_frame.config(bg=DARKGRAY)
        self.send_button.config(bg=VERYDARKGRAY, fg=WHITE, activebackground=VERYDARKGRAY, activeforeground=WHITE)
        self.sent_label.config(bg=DARKGRAY, fg=WHITE)

        self.tl_bg = VERYDARKGRAY
        self.tl_bg2 = DARKGRAY
        self.tl_fg = WHITE

    def color_theme_grey(self):
        self.master.config(bg=MEDIUMGRAY)
        self.text_frame.config(bg=MEDIUMGRAY)
        self.text_box.config(bg=GRAY, fg=WHITE)
        self.entry_frame.config(bg=MEDIUMGRAY)
        self.entry_field.config(bg=GRAY, fg=WHITE, insertbackground=WHITE)
        self.send_button_frame.config(bg=MEDIUMGRAY)
        self.send_button.config(bg=GRAY, fg=WHITE, activebackground=GRAY, activeforeground=WHITE)
        self.sent_label.config(bg=MEDIUMGRAY, fg=WHITE)

        self.tl_bg = GRAY
        self.tl_bg2 = MEDIUMGRAY
        self.tl_fg = WHITE

    def color_theme_turquoise(self):
        self.master.config(bg=DARKGREEN)
        self.text_frame.config(bg=DARKGREEN)
        self.text_box.config(bg=TORQUOISE, fg=WHITE)
        self.entry_frame.config(bg=DARKGREEN)
        self.entry_field.config(bg=TORQUOISE, fg=WHITE, insertbackground=WHITE)
        self.send_button_frame.config(bg=DARKGREEN)
        self.send_button.config(bg=TORQUOISE, fg=WHITE, activebackground=TORQUOISE, activeforeground=WHITE)
        self.sent_label.config(bg=DARKGREEN, fg=WHITE)

        self.tl_bg = TORQUOISE
        self.tl_bg2 = DARKGREEN
        self.tl_fg = WHITE

    def color_theme_dark_blue(self):
        self.master.config(bg=DARKBLUE)
        self.text_frame.config(bg=DARKBLUE)
        self.text_box.config(bg=NAVYBLUE, fg=WHITE)
        self.entry_frame.config(bg=DARKBLUE)
        self.entry_field.config(bg=NAVYBLUE, fg=WHITE, insertbackground=WHITE)
        self.send_button_frame.config(bg=DARKBLUE)
        self.send_button.config(bg=NAVYBLUE, fg=WHITE, activebackground=NAVYBLUE, activeforeground=WHITE)
        self.sent_label.config(bg=DARKBLUE, fg=WHITE)

        self.tl_bg = NAVYBLUE
        self.tl_bg2 = DARKBLUE
        self.tl_fg = WHITE

    def color_theme_turquoise(self):
        self.master.config(bg=DARKGREEN)
        self.text_frame.config(bg=DARKGREEN)
        self.text_box.config(bg=TORQUOISE, fg=WHITE)
        self.entry_frame.config(bg=DARKGREEN)
        self.entry_field.config(bg=TORQUOISE, fg=WHITE, insertbackground=WHITE)
        self.send_button_frame.config(bg=DARKGREEN)
        self.send_button.config(bg=TORQUOISE, fg=WHITE, activebackground=TORQUOISE, activeforeground=WHITE)
        self.sent_label.config(bg=DARKGREEN, fg=WHITE)

        self.tl_bg = TORQUOISE
        self.tl_bg2 = DARKGREEN
        self.tl_fg = WHITE

    def color_theme_matrix(self):
        self.master.config(bg=ALMOSTBLACK)
        self.text_frame.config(bg=ALMOSTBLACK)
        self.entry_frame.config(bg=ALMOSTBLACK)
        self.text_box.config(bg=ALMOSTBLACK, fg=BRIGHTGREEN)
        self.entry_field.config(bg=ALMOSTBLACK, fg=BRIGHTGREEN, insertbackground=BRIGHTGREEN)
        self.send_button_frame.config(bg=ALMOSTBLACK)
        self.send_button.config(bg=ALMOSTBLACK, fg=WHITE, activebackground=ALMOSTBLACK, activeforeground=WHITE)
        self.sent_label.config(bg=ALMOSTBLACK, fg=BRIGHTGREEN)

        self.tl_bg = ALMOSTBLACK
        self.tl_bg2 = ALMOSTBLACK
        self.tl_fg = BRIGHTGREEN

    def default_format(self):
        self.font_change_default()
        self.color_theme_default()

if __name__ == "__main__":

    chatApp = Tk()

    chat_interface = ChatInterface(chatApp)
    chatApp.geometry(window_size)
    chatApp.title("Carbon Footprint AI Assistant")
    chatApp.mainloop()