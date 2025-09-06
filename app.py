# from tkinter import *
# from chat import get_response, bot_name


# BG_GRAY = "#ABB2B9"
# BG_COLOR = "#17202A"
# TEXT_COLOR = "#EAECEE"

# FONT = "Helvetica 14"
# FONT_BOLD = "Helvetica 13 bold"


# class ChatApplication:
#     def __init__(self):
#         self.window = Tk()
#         self._setup_main_window()

#     def run(self):
#         self.window.mainloop()


#     def _setup_main_window(self):
#         self.window.title("Chat")
#         self.window.resizable(width=False, height=False)
#         self.window.configure(width=470, height=550, bg=BG_COLOR)

#         head_label = Label(self.window, bg = BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)

#         head_label.place(relwidth=1)

#         line = Label(self.window, width=450, bg=BG_GRAY)
#         line.place(relwidth=1, rely=0.07, relheight=0.012)


#         self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)


#         self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
#         self.text_widget.configure(cursor="arrow", state=DISABLED)


#         scrollbar = Scrollbar(self.text_widget)
#         scrollbar.place(relheight=1, relx=0.974)
#         scrollbar.configure(command=self.text_widget.yview)


#         bottom_label = Label(self.window, bg=BG_GRAY, height=80)
#         bottom_label.place(relwidth=1, rely=0.825)


#         self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font = FONT)
#         self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
#         self.msg_entry.focus()
#         self.msg_entry.bind("<Return>", self.on_enter_pressed)


#         send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda : self.on_enter_pressed(None))

#         send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        


#     def on_enter_pressed(self, event):
#         msg = self.msg_entry.get()
#         self._insert_message(msg, "You")


#     def _insert_message(self, msg, sender):
#         if not msg:
#             return
        
#         self.msg_entry.delete(0, END)
#         msg1 = f"{sender} : {msg}\n\n"
#         self.text_widget.configure(state=NORMAL)
#         self.text_widget.insert(END, msg1)
#         self.text_widget.configure(state=DISABLED)


#         msg2 = f"{bot_name} : {get_response(msg)}\n\n"
#         self.text_widget.configure(state=NORMAL)
#         self.text_widget.insert(END, msg2)
#         self.text_widget.configure(state=DISABLED)

#         self.text_widget.see(END)




# if __name__ == "__main__":
#     app = ChatApplication()
#     app.run()


from tkinter import *
from tkinter import ttk, messagebox
from chat import get_response, bot_name
import datetime
import threading
import time

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


FONT = ("Georgia", 11)
FONT_BOLD = ("Georgia", 12, "bold")
HEADER_FONT = ("Georgia", 16, "bold")
SMALL_FONT = ("Georgia", 9)


class CoffeeShopChatBot:
    def __init__(self):
        self.window = Tk()
        self.setup_main_window()
        self.setup_styles()
        self.message_count = 0
        
    def run(self):
        self.show_welcome_message()
        self.window.mainloop()

    def setup_main_window(self):
        """Setup the main window with coffee shop theme"""
        self.window.title("☕ Coffee Shop Assistant - How can I help you today?")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600, height=700, bg=BG_COLOR)
        
        # Center the window on screen
        self.center_window()
        
        # Setup header
        self.setup_header()
        
        # Setup chat area
        self.setup_chat_area()
        
        # Setup input area
        self.setup_input_area()
        
        # Setup status bar
        self.setup_status_bar()

    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = 600
        height = 700
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        """Setup ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure("Coffee.TButton",
                       background=BUTTON_COLOR,
                       foreground=TEXT_COLOR,
                       font=FONT_BOLD,
                       focuscolor="none",
                       borderwidth=0,
                       relief="flat")
        
        style.map("Coffee.TButton",
                 background=[('active', BUTTON_HOVER),
                           ('pressed', '#654321')])

    def setup_header(self):
        """Setup the header with coffee shop branding"""
        header_frame = Frame(self.window, bg=HEADER_COLOR, height=80)
        header_frame.pack(fill=X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Coffee shop title
        title_label = Label(header_frame, 
                           text="☕ CAFÉ ASSISTANT ☕", 
                           font=HEADER_FONT, 
                           bg=HEADER_COLOR, 
                           fg=TEXT_COLOR)
        title_label.pack(pady=(15, 5))
        
        # Subtitle
        subtitle_label = Label(header_frame, 
                              text="Your friendly coffee shop companion", 
                              font=SMALL_FONT, 
                              bg=HEADER_COLOR, 
                              fg=ACCENT_COLOR)
        subtitle_label.pack()
        
        # Separator line
        separator = Frame(self.window, bg=ACCENT_COLOR, height=2)
        separator.pack(fill=X)

    def setup_chat_area(self):
        """Setup the chat display area"""
        chat_frame = Frame(self.window, bg=BG_COLOR)
        chat_frame.pack(fill=BOTH, expand=True, padx=10, pady=(10, 0))
        
        # Chat display with scrollbar
        self.text_widget = Text(chat_frame, 
                               wrap=WORD,
                               bg=CHAT_BG, 
                               fg=TEXT_COLOR, 
                               font=FONT,
                               padx=10, 
                               pady=10,
                               selectbackground=ACCENT_COLOR,
                               selectforeground=TEXT_COLOR,
                               insertbackground=TEXT_COLOR,
                               relief=FLAT,
                               border=0)
        
        # Scrollbar
        scrollbar = Scrollbar(chat_frame, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack chat components
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Configure text tags for styling messages
        self.text_widget.tag_configure("user", 
                                      background=USER_MSG_BG, 
                                      foreground=TEXT_COLOR,
                                      font=FONT,
                                      spacing1=5,
                                      spacing3=5,
                                      wrap=WORD,
                                      )
        
        self.text_widget.tag_configure("bot", 
                                      background=BOT_MSG_BG, 
                                      foreground="#2C1810",
                                      font=FONT,
                                      spacing1=5,
                                      spacing3=5,
                                      wrap=WORD)
        
        self.text_widget.tag_configure("system", 
                                      background=HEADER_COLOR, 
                                      foreground=ACCENT_COLOR,
                                      font=("Georgia", 10, "italic"),
                                      justify=CENTER,
                                      spacing1=10,
                                      spacing3=10)
        
        self.text_widget.configure(state=DISABLED)

    def setup_input_area(self):
        """Setup the input area with modern styling"""
        input_frame = Frame(self.window, bg=BG_COLOR, height=100)
        input_frame.pack(fill=X, padx=10, pady=10)
        input_frame.pack_propagate(False)
        
        # Input label
        input_label = Label(input_frame, 
                           text="💬 Ask me anything about our coffee shop:",
                           font=SMALL_FONT,
                           bg=BG_COLOR,
                           fg=ACCENT_COLOR)
        input_label.pack(anchor=W, pady=(0, 5))
        
        # Input field and button frame
        entry_frame = Frame(input_frame, bg=BG_COLOR)
        entry_frame.pack(fill=X)
        
        # Message entry field
        self.msg_entry = Entry(entry_frame,
                              bg=ENTRY_BG,
                              fg=TEXT_COLOR,
                              font=FONT,
                              insertbackground=TEXT_COLOR,
                              relief=FLAT,
                              border=0,
                              width=50)
        self.msg_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10), ipady=8)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_enter_pressed)
        
        # Send button
        self.send_button = ttk.Button(entry_frame,
                                     text="Send ☕",
                                     style="Coffee.TButton",
                                     command=lambda: self.on_enter_pressed(None))
        self.send_button.pack(side=RIGHT, padx=5, ipady=5)
        
        # Quick action buttons frame
        quick_actions_frame = Frame(input_frame, bg=BG_COLOR)
        quick_actions_frame.pack(fill=X, pady=(10, 0))
        
        # Quick action buttons
        quick_actions = [
            ("📋 Menu", "Show me your menu"),
            ("🕐 Hours", "What are your hours?"),
            ("📍 Location", "Where are you located?"),
            ("🎉 Specials", "Any specials today?")
        ]
        
        for text, command in quick_actions:
            btn = Button(quick_actions_frame,
                        text=text,
                        font=SMALL_FONT,
                        bg=BUTTON_COLOR,
                        fg=TEXT_COLOR,
                        relief=FLAT,
                        border=0,
                        padx=8,
                        pady=2,
                        command=lambda cmd=command: self.quick_action(cmd))
            btn.pack(side=LEFT, padx=(0, 5))
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BUTTON_COLOR))

    def setup_status_bar(self):
        """Setup status bar at the bottom"""
        self.status_bar = Label(self.window,
                               text="Ready to chat! ☕",
                               font=SMALL_FONT,
                               bg=HEADER_COLOR,
                               fg=ACCENT_COLOR,
                               relief=SUNKEN,
                               anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

    def show_welcome_message(self):
        """Display welcome message when app starts"""
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
        """Handle quick action button clicks"""
        self.msg_entry.delete(0, END)
        self.msg_entry.insert(0, message)
        self.on_enter_pressed(None)

    def on_enter_pressed(self, event):
        """Handle message sending"""
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
            
        # Update status
        self.status_bar.configure(text="Processing your request... ☕")
        self.window.update()
        
        # Disable input temporarily
        self.msg_entry.configure(state=DISABLED)
        self.send_button.configure(state=DISABLED)
        
        # Insert user message
        self.insert_message(msg, "You", "user")
        
        # Get bot response in separate thread to prevent UI freezing
        threading.Thread(target=self.get_bot_response, args=(msg,), daemon=True).start()

    def get_bot_response(self, message):
        """Get bot response in separate thread"""
        try:
            response = get_response(message)
            # Update UI in main thread
            self.window.after(0, lambda: self.handle_bot_response(response))
        except Exception as e:
            error_msg = "Sorry, I'm having trouble right now. Please try again! ☕"
            self.window.after(0, lambda: self.handle_bot_response(error_msg))

    def handle_bot_response(self, response):
        """Handle bot response and update UI"""
        # Insert bot response
        self.insert_message(response, "Café Assistant", "bot")
        
        # Re-enable input
        self.msg_entry.configure(state=NORMAL)
        self.send_button.configure(state=NORMAL)
        self.msg_entry.focus()
        
        # Update status
        self.status_bar.configure(text=f"Ready to chat! Messages: {self.message_count} ☕")

    def insert_message(self, msg, sender, tag):
        """Insert message with proper formatting"""
        if not msg:
            return
            
            
        # Get current time
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        # Format message
        if sender == "You":
            message_text = f"{sender} ({current_time}):\n{msg}\n\n"
        else:
            message_text = f"☕ {sender} ({current_time}):\n{msg}\n\n"
        
        # Insert message
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, message_text, tag)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        
        self.message_count += 1

    def show_about(self):
        """Show about dialog"""
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