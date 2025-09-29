from tkinter import *
from tkinter import ttk, messagebox
from chat import get_response, bot_name
import datetime
import threading

# Coffee Shop Color Scheme
BG_COLOR = "#2C1810"          # Dark coffee brown
CHAT_BG = "#3D2817"           # Medium coffee brown
USER_MSG_BG = "#8B4513"       # Saddle brown
BOT_MSG_BG = "#D2691E"        # Chocolate/orange brown
TEXT_COLOR = "#F5F5DC"        # Beige
ACCENT_COLOR = "#CD853F"      # Peru/coffee accent
BUTTON_COLOR = "#A0522D"      # Sienna
BUTTON_HOVER = "#8B4513"      # Darker brown on hover
HEADER_COLOR = "#4A2C17"      # Dark header
ENTRY_BG = "#5D4037"          # Input field background

# Fonts
FONT = ("Inter", 13)
FONT_BOLD = ("Inter", 14, "bold")
HEADER_FONT = ("Inter", 18, "bold")
SMALL_FONT = ("Inter", 11)

class CoffeeShopChatBot:
    def __init__(self):
        self.window = Tk()
        self.message_count = 0
        self.setup_main_window()
        self.setup_styles()
        self.setup_menu()  # Add menu setup

    def run(self):
        self.show_welcome_message()
        self.window.mainloop()

    def setup_main_window(self):
        """Setup the main window"""
        self.window.title("☕ Coffee Shop Assistant")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=700, height=800, bg=BG_COLOR)  # Increased size
        self.center_window(700, 800)  # Pass new size
        self.setup_header()
        self.setup_chat_area()
        self.setup_input_area()
        self.setup_status_bar()

    def center_window(self, width=700, height=800):
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Coffee.TButton",
                        background=BUTTON_COLOR,
                        foreground=TEXT_COLOR,
                        font=FONT_BOLD,
                        relief="flat")
        style.map("Coffee.TButton",
                  background=[('active', BUTTON_HOVER),
                              ('pressed', '#654321')])

    def setup_menu(self):
        menubar = Menu(self.window, bg=HEADER_COLOR, fg=TEXT_COLOR)
        self.window.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0, bg=HEADER_COLOR, fg=TEXT_COLOR)
        file_menu.add_command(label="About", command=self.show_about)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menubar, tearoff=0, bg=HEADER_COLOR, fg=ACCENT_COLOR)
        help_menu.add_command(label="Help", command=lambda: messagebox.showinfo("Help", "Type your question or use quick actions!"))
        menubar.add_cascade(label="Help", menu=help_menu)

    def setup_header(self):
        header_frame = Frame(self.window, bg=HEADER_COLOR, height=80)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)
        title_label = Label(header_frame, text=bot_name, font=HEADER_FONT,
                            bg=HEADER_COLOR, fg=TEXT_COLOR)
        title_label.pack(pady=(15,5))
        subtitle_label = Label(header_frame, text="Your friendly coffee shop companion",
                               font=SMALL_FONT, bg=HEADER_COLOR, fg=ACCENT_COLOR)
        subtitle_label.pack()
        separator = Frame(self.window, bg=ACCENT_COLOR, height=2)
        separator.pack(fill=X)

    def setup_chat_area(self):
        chat_frame = Frame(self.window, bg=BG_COLOR)
        chat_frame.pack(fill=BOTH, expand=True, padx=10, pady=(10,0))
        self.text_widget = Text(chat_frame, wrap=WORD, bg=CHAT_BG, fg=TEXT_COLOR,
                                font=FONT, padx=10, pady=10, selectbackground=ACCENT_COLOR,
                                selectforeground=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                relief=FLAT, border=0)
        scrollbar = Scrollbar(chat_frame, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)

        # Configure message tags
        self.text_widget.tag_configure("user", background=USER_MSG_BG, foreground=TEXT_COLOR,
                                       font=FONT, lmargin1=10, lmargin2=10, rmargin=10,
                                       spacing1=5, spacing3=5, relief="raised", borderwidth=3, wrap=WORD)
        self.text_widget.tag_configure("bot", background=BOT_MSG_BG, foreground="#2C1810",
                                       font=FONT, lmargin1=10, lmargin2=10, rmargin=10,
                                       spacing1=5, spacing3=5, relief="raised", borderwidth=3, wrap=WORD)
        self.text_widget.tag_configure("system", background=HEADER_COLOR, foreground=ACCENT_COLOR,
                                       font=("Georgia", 11, "italic"), justify=CENTER,
                                       spacing1=10, spacing3=10)
        self.text_widget.configure(state=DISABLED)

    def setup_input_area(self):
        input_frame = Frame(self.window, bg=BG_COLOR, height=100)
        input_frame.pack(fill=X, padx=10, pady=10)
        input_frame.pack_propagate(False)
        input_label = Label(input_frame, text="💬 Ask me anything about our coffee shop:",
                            font=SMALL_FONT, bg=BG_COLOR, fg=ACCENT_COLOR)
        input_label.pack(anchor=W, pady=(0,5))

        entry_frame = Frame(input_frame, bg=BG_COLOR)
        entry_frame.pack(fill=X)
        self.msg_entry = Entry(entry_frame, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT,
                               insertbackground=TEXT_COLOR, relief=FLAT, border=0, width=50)
        self.msg_entry.pack(side=LEFT, fill=X, expand=True, padx=(0,10), ipady=8)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_enter_pressed)
        self.send_button = ttk.Button(entry_frame, text="Send ☕", style="Coffee.TButton",
                                      command=lambda: self.on_enter_pressed(None))
        self.send_button.pack(side=RIGHT, padx=5, ipady=5)

        # Quick action buttons
        quick_actions_frame = Frame(input_frame, bg=BG_COLOR)
        quick_actions_frame.pack(fill=X, pady=(10,0))
        quick_actions = [("📋 Menu","Show me your menu"),
                         ("🕐 Hours","What are your hours?"),
                         ("📍 Location","Where are you located?"),
                         ("🎉 Specials","Any specials today?")]
        for text, command in quick_actions:
            btn = Button(quick_actions_frame, text=text, font=SMALL_FONT, bg=BUTTON_COLOR,
                         fg=TEXT_COLOR, relief=FLAT, border=0, padx=8, pady=2,
                         command=lambda cmd=command: self.quick_action(cmd))
            btn.pack(side=LEFT, padx=(0,5))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BUTTON_COLOR))

    def setup_status_bar(self):
        self.status_bar = Label(self.window, text="Ready to chat! ☕", font=SMALL_FONT,
                                bg=HEADER_COLOR, fg=ACCENT_COLOR, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

    def show_welcome_message(self):
        welcome_text = """
☕ Welcome to our Coffee Shop! ☕
I'm here to help you with:
• Menu items and recommendations
• Store hours and location
• Daily specials and promotions
• Dietary restrictions and alternatives
• General questions about our café

How can I assist you today?
"""
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, welcome_text, "system")
        self.text_widget.insert(END, "\n" + "="*50 + "\n\n")
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    def quick_action(self, message):
        self.msg_entry.delete(0, END)
        self.msg_entry.insert(0, message)
        self.on_enter_pressed(None)

    def on_enter_pressed(self, event):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        self.msg_entry.delete(0, END)
        self.status_bar.configure(text="Processing your request... ☕")
        self.window.update()
        self.msg_entry.configure(state=DISABLED)
        self.send_button.configure(state=DISABLED)
        self.insert_message(msg, "You", "user")
        threading.Thread(target=self.get_bot_response, args=(msg,), daemon=True).start()

    def get_bot_response(self, message):
        try:
            response = get_response(message)
            self.window.after(0, lambda: self.handle_bot_response(response))
        except Exception as e:
            error_msg = "Sorry, I'm having trouble right now. Please try again! ☕"
            self.window.after(0, lambda: self.handle_bot_response(error_msg))

    def handle_bot_response(self, response):
        self.insert_message(response, bot_name, "bot")
        self.msg_entry.configure(state=NORMAL)
        self.send_button.configure(state=NORMAL)
        self.msg_entry.focus()
        self.status_bar.configure(text=f"Ready to chat! Messages: {self.message_count} ☕")

    def insert_message(self, msg, sender, tag):
        if not msg:
            return
        current_time = datetime.datetime.now().strftime("%H:%M")
        if sender != "You":
            message_text = f"☕ {sender} ({current_time}):\n{msg}\n\n"
        else:
            message_text = f"{sender} ({current_time}):\n{msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, message_text, tag)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        self.message_count += 1

    def show_about(self):
        messagebox.showinfo("About", 
                            "Coffee Shop Chat Assistant\n\n"
                            "Your friendly AI companion for all\n"
                            "coffee shop related questions!\n\n"
                            "Enjoy your visit! ☕")

if __name__ == "__main__":
    try:
        app = CoffeeShopChatBot()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application:\n{e}")
