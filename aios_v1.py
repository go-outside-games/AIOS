import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, colorchooser
import datetime
import subprocess
import os
import random

class Window:
    def __init__(self, parent, title, width, height, x, y):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.configure(bg="#2b2b2b")
        self.is_maximized = False
        self.normal_geometry = f"{width}x{height}+{x}+{y}"
        
        # Title bar
        self.titlebar = tk.Frame(self.window, bg="#1e1e1e", height=30)
        self.titlebar.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(self.titlebar, text=title, bg="#1e1e1e", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # Window controls
        btn_frame = tk.Frame(self.titlebar, bg="#1e1e1e")
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="−", bg="#1e1e1e", fg="white", bd=0, 
                 command=self.minimize, width=3).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="□", bg="#1e1e1e", fg="white", bd=0, 
                 command=self.maximize, width=3).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="✕", bg="#c42b1c", fg="white", bd=0, 
                 command=self.window.destroy, width=3).pack(side=tk.LEFT)
        
        self.content = tk.Frame(self.window, bg="#2b2b2b")
        self.content.pack(fill=tk.BOTH, expand=True)
        
    def minimize(self):
        self.window.iconify()
    
    def maximize(self):
        if self.is_maximized:
            self.window.geometry(self.normal_geometry)
            self.is_maximized = False
        else:
            self.normal_geometry = self.window.geometry()
            self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()-60}+0+0")
            self.is_maximized = True

class OperatingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("PyOS - Python Operating System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1a1a2e")
        
        # Show splash screen first
        self.show_splash_screen()
        
    def show_splash_screen(self):
        # Create splash window
        splash = tk.Toplevel(self.root)
        splash.title("AIOS")
        
        # Center the splash screen
        splash_width = 600
        splash_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        
        splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        splash.configure(bg="#0a0a1e")
        splash.overrideredirect(True)
        
        # AIOS Logo
        tk.Label(splash, text="AI", font=("Arial", 72, "bold"),
                bg="#0a0a1e", fg="#00d4ff").pack(pady=30)
        tk.Label(splash, text="OS", font=("Arial", 72, "bold"),
                bg="#0a0a1e", fg="#ff006e").pack()
        
        tk.Label(splash, text="Artificial Intelligence Operating System", 
                font=("Arial", 14), bg="#0a0a1e", fg="#aaa").pack(pady=20)
        
        # Loading bar
        progress_frame = tk.Frame(splash, bg="#0a0a1e")
        progress_frame.pack(pady=30)
        
        tk.Label(progress_frame, text="Loading...", font=("Arial", 11),
                bg="#0a0a1e", fg="white").pack(pady=10)
        
        progress_bg = tk.Canvas(progress_frame, width=400, height=20, 
                               bg="#1a1a2e", highlightthickness=0)
        progress_bg.pack()
        
        # Animate loading bar
        progress_bar = progress_bg.create_rectangle(0, 0, 0, 20, fill="#00d4ff", outline="")
        
        def animate_progress(width=0):
            if width <= 400:
                progress_bg.coords(progress_bar, 0, 0, width, 20)
                splash.after(10, lambda: animate_progress(width + 8))
            else:
                splash.after(500, lambda: self.finish_splash(splash))
        
        animate_progress()
        
    def finish_splash(self, splash):
        splash.destroy()
        self.initialize_os()
    
    def initialize_os(self):
        # Desktop
        self.desktop = tk.Frame(self.root, bg="#1a1a2e")
        self.desktop.pack(fill=tk.BOTH, expand=True)
        
        # Create desktop icons
        self.create_desktop_icons()
        
        # Taskbar
        self.taskbar = tk.Frame(self.root, bg="#16213e", height=50)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start button
        self.start_btn = tk.Button(self.taskbar, text="⊞ Start", bg="#0f3460", fg="white", 
                                   font=("Arial", 12, "bold"), command=self.toggle_start_menu,
                                   relief=tk.FLAT, padx=20)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Clock
        self.clock = tk.Label(self.taskbar, bg="#16213e", fg="white", font=("Arial", 10))
        self.clock.pack(side=tk.RIGHT, padx=20)
        self.update_clock()
        
        # Start menu (hidden initially)
        self.start_menu = None
        
    def create_desktop_icons(self):
        icons = [
            ("🌐 Browser", self.open_browser, 50, 50),
            ("📁 Files", self.open_file_explorer, 50, 150),
            ("📝 Editor", self.open_text_editor, 50, 250),
            ("🔢 Calculator", self.open_calculator, 50, 350),
            ("🎮 Games", self.open_game_launcher, 50, 450),
            ("🤖 AI Chat", self.open_ai_chat, 50, 550)
        ]
        
        for text, command, x, y in icons:
            icon_frame = tk.Frame(self.desktop, bg="#1a1a2e")
            icon_frame.place(x=x, y=y)
            
            btn = tk.Button(icon_frame, text=text, bg="#0f3460", fg="white",
                          font=("Arial", 10), command=command, relief=tk.FLAT,
                          width=12, height=3, cursor="hand2")
            btn.pack()
    
    def toggle_start_menu(self):
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None
        else:
            self.show_start_menu()
    
    def show_start_menu(self):
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.geometry("300x350+10+300")
        self.start_menu.configure(bg="#16213e")
        self.start_menu.overrideredirect(True)
        
        tk.Label(self.start_menu, text="PyOS Applications", bg="#0f3460", fg="white",
                font=("Arial", 12, "bold"), pady=10).pack(fill=tk.X)
        
        apps = [
            ("🌐 Web Browser", self.open_browser),
            ("📁 File Explorer", self.open_file_explorer),
            ("📝 Text Editor", self.open_text_editor),
            ("🔢 Calculator", self.open_calculator),
            ("🎮 Game Launcher", self.open_game_launcher),
            ("🤖 AI Assistant", self.open_ai_chat),
            ("ℹ️ About", self.show_about),
            ("🔌 Shut Down", self.root.quit)
        ]
        
        for text, command in apps:
            btn = tk.Button(self.start_menu, text=text, bg="#16213e", fg="white",
                          font=("Arial", 10), command=lambda c=command: self.menu_click(c),
                          relief=tk.FLAT, anchor="w", padx=20, pady=10)
            btn.pack(fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#0f3460"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#16213e"))
    
    def menu_click(self, command):
        if self.start_menu:
            self.start_menu.destroy()
            self.start_menu = None
        command()
    
    def open_browser(self):
        win = Window(self.root, "PyOS Browser", 900, 600, 150, 50)
        
        # Navigation bar
        nav = tk.Frame(win.content, bg="#1e1e1e")
        nav.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(nav, text="⬅", bg="#0f3460", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(nav, text="➡", bg="#0f3460", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(nav, text="⟳", bg="#0f3460", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        
        url_var = tk.StringVar(value="https://pyos.home")
        url_entry = tk.Entry(nav, textvariable=url_var, bg="#2b2b2b", fg="white", 
                            font=("Arial", 11))
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        def load_page():
            url = url_var.get()
            content_frame.pack_forget()
            for widget in content_frame.winfo_children():
                widget.destroy()
            
            if "home" in url.lower() or "pyos" in url.lower():
                tk.Label(content_frame, text="🌐", font=("Arial", 48), 
                        bg="#2b2b2b", fg="#0f3460").pack(pady=30)
                tk.Label(content_frame, text="Welcome to PyOS Browser!", 
                        font=("Arial", 24, "bold"), bg="#2b2b2b", fg="white").pack()
                tk.Label(content_frame, text="Your gateway to browsing", 
                        font=("Arial", 12), bg="#2b2b2b", fg="#aaa").pack(pady=10)
                
                shortcuts = tk.Frame(content_frame, bg="#2b2b2b")
                shortcuts.pack(pady=30)
                
                sites = [
                    ("📰 News", "https://news.pyos"),
                    ("📧 Mail", "https://mail.pyos"),
                    ("🎵 Music", "https://music.pyos"),
                    ("🎬 Videos", "https://videos.pyos")
                ]
                
                for i, (name, site_url) in enumerate(sites):
                    btn = tk.Button(shortcuts, text=name, bg="#0f3460", fg="white",
                                  font=("Arial", 10), width=15, height=2,
                                  command=lambda u=site_url: (url_var.set(u), load_page()))
                    btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            
            elif "news" in url.lower():
                tk.Label(content_frame, text="📰 PyOS News", font=("Arial", 20, "bold"),
                        bg="#2b2b2b", fg="white").pack(pady=20)
                articles = [
                    "PyOS 1.0 Released - New Features!",
                    "AI-Powered Development Reaches New Heights",
                    "Python Continues to Dominate in 2025"
                ]
                for article in articles:
                    frame = tk.Frame(content_frame, bg="#1e1e1e")
                    frame.pack(fill=tk.X, padx=50, pady=5)
                    tk.Label(frame, text=f"• {article}", bg="#1e1e1e", 
                            fg="white", font=("Arial", 11), anchor="w").pack(fill=tk.X, padx=10, pady=5)
            
            elif "mail" in url.lower():
                tk.Label(content_frame, text="📧 PyOS Mail", font=("Arial", 20, "bold"),
                        bg="#2b2b2b", fg="white").pack(pady=20)
                tk.Label(content_frame, text="Inbox (3)", bg="#2b2b2b", 
                        fg="white", font=("Arial", 12, "bold")).pack(anchor="w", padx=50, pady=10)
                mails = [
                    ("Welcome to PyOS", "System"),
                    ("Update Available", "System"),
                    ("Weekly Newsletter", "PyOS Team")
                ]
                for subject, sender in mails:
                    frame = tk.Frame(content_frame, bg="#1e1e1e")
                    frame.pack(fill=tk.X, padx=50, pady=2)
                    tk.Label(frame, text=f"📩 {subject}", bg="#1e1e1e", 
                            fg="white", font=("Arial", 10, "bold"), anchor="w").pack(fill=tk.X, padx=10, pady=2)
                    tk.Label(frame, text=f"   From: {sender}", bg="#1e1e1e",
                            fg="#aaa", font=("Arial", 9), anchor="w").pack(fill=tk.X, padx=10, pady=2)
            
            elif "music" in url.lower():
                tk.Label(content_frame, text="🎵 PyOS Music", font=("Arial", 20, "bold"),
                        bg="#2b2b2b", fg="white").pack(pady=20)
                tk.Label(content_frame, text="♫ Now Playing", 
                        bg="#2b2b2b", fg="#aaa", font=("Arial", 10)).pack(pady=5)
                tk.Label(content_frame, text="Ambient Coding Beats", 
                        bg="#2b2b2b", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
                
                controls = tk.Frame(content_frame, bg="#2b2b2b")
                controls.pack(pady=20)
                tk.Button(controls, text="⏮", bg="#0f3460", fg="white",
                         font=("Arial", 14), width=3).pack(side=tk.LEFT, padx=5)
                tk.Button(controls, text="⏸", bg="#0f3460", fg="white",
                         font=("Arial", 14), width=3).pack(side=tk.LEFT, padx=5)
                tk.Button(controls, text="⏭", bg="#0f3460", fg="white",
                         font=("Arial", 14), width=3).pack(side=tk.LEFT, padx=5)
            
            elif "videos" in url.lower():
                tk.Label(content_frame, text="🎬 PyOS Videos", font=("Arial", 20, "bold"),
                        bg="#2b2b2b", fg="white").pack(pady=20)
                videos = [
                    "Python Tutorial for Beginners",
                    "Introduction to AI",
                    "Web Development 101"
                ]
                for video in videos:
                    frame = tk.Frame(content_frame, bg="#1e1e1e")
                    frame.pack(fill=tk.X, padx=50, pady=5)
                    tk.Label(frame, text=f"▶ {video}", bg="#1e1e1e",
                            fg="white", font=("Arial", 11), anchor="w").pack(fill=tk.X, padx=10, pady=8)
            
            else:
                tk.Label(content_frame, text="404", font=("Arial", 48, "bold"),
                        bg="#2b2b2b", fg="#c42b1c").pack(pady=50)
                tk.Label(content_frame, text="Page not found", font=("Arial", 16),
                        bg="#2b2b2b", fg="white").pack()
                tk.Label(content_frame, text=f'"{url}" does not exist', font=("Arial", 10),
                        bg="#2b2b2b", fg="#aaa").pack(pady=10)
            
            content_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(nav, text="Go", bg="#0f3460", fg="white", command=load_page,
                 font=("Arial", 10), padx=15).pack(side=tk.LEFT, padx=2)
        
        # Content area
        content_frame = tk.Frame(win.content, bg="#2b2b2b")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        load_page()
    
    def open_file_explorer(self):
        win = Window(self.root, "File Explorer", 600, 400, 200, 100)
        
        toolbar = tk.Frame(win.content, bg="#1e1e1e")
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(toolbar, text="⬅", bg="#0f3460", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="➡", bg="#0f3460", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        
        path_entry = tk.Entry(toolbar, bg="#2b2b2b", fg="white", font=("Arial", 10))
        path_entry.insert(0, "C:/Users/Desktop")
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        file_frame = tk.Frame(win.content, bg="#2b2b2b")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        files = ["📁 Documents", "📁 Downloads", "📁 Pictures", "📁 Music", 
                "📄 readme.txt", "📄 notes.txt", "🖼️ image.png", "🎵 song.mp3"]
        
        for f in files:
            tk.Label(file_frame, text=f, bg="#2b2b2b", fg="white", 
                    font=("Arial", 10), anchor="w").pack(fill=tk.X, pady=2)
    
    def open_text_editor(self):
        win = Window(self.root, "AIOS Word Processor", 800, 600, 200, 50)
        
        # Toolbar
        toolbar = tk.Frame(win.content, bg="#1e1e1e")
        toolbar.pack(fill=tk.X)
        
        # File menu buttons
        file_frame = tk.Frame(toolbar, bg="#1e1e1e")
        file_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(file_frame, text="New", bg="#0f3460", fg="white", padx=10,
                 command=lambda: text_area.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=2)
        tk.Button(file_frame, text="Open", bg="#0f3460", fg="white", padx=10).pack(side=tk.LEFT, padx=2)
        tk.Button(file_frame, text="Save", bg="#0f3460", fg="white", padx=10).pack(side=tk.LEFT, padx=2)
        
        tk.Frame(toolbar, bg="#555", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Formatting frame
        format_frame = tk.Frame(toolbar, bg="#1e1e1e")
        format_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Font size
        tk.Label(format_frame, text="Size:", bg="#1e1e1e", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        font_size = tk.StringVar(value="11")
        size_combo = ttk.Combobox(format_frame, textvariable=font_size, width=5, 
                                  values=["8", "10", "11", "12", "14", "16", "18", "20", "24", "28", "36", "48"])
        size_combo.pack(side=tk.LEFT, padx=2)
        
        tk.Frame(toolbar, bg="#555", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Style buttons frame
        style_frame = tk.Frame(toolbar, bg="#1e1e1e")
        style_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        bold_btn = tk.Button(style_frame, text="B", bg="#0f3460", fg="white",
                            font=("Arial", 10, "bold"), width=3)
        bold_btn.pack(side=tk.LEFT, padx=2)
        
        italic_btn = tk.Button(style_frame, text="I", bg="#0f3460", fg="white",
                              font=("Arial", 10, "italic"), width=3)
        italic_btn.pack(side=tk.LEFT, padx=2)
        
        underline_btn = tk.Button(style_frame, text="U", bg="#0f3460", fg="white",
                                 font=("Arial", 10, "underline"), width=3)
        underline_btn.pack(side=tk.LEFT, padx=2)
        
        tk.Frame(toolbar, bg="#555", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Alignment buttons
        align_frame = tk.Frame(toolbar, bg="#1e1e1e")
        align_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        left_btn = tk.Button(align_frame, text="≡", bg="#0f3460", fg="white",
                            font=("Arial", 12), width=3)
        left_btn.pack(side=tk.LEFT, padx=2)
        
        center_btn = tk.Button(align_frame, text="≣", bg="#0f3460", fg="white",
                              font=("Arial", 12), width=3)
        center_btn.pack(side=tk.LEFT, padx=2)
        
        right_btn = tk.Button(align_frame, text="≡", bg="#0f3460", fg="white",
                             font=("Arial", 12), width=3)
        right_btn.pack(side=tk.LEFT, padx=2)
        
        tk.Frame(toolbar, bg="#555", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Color buttons
        color_frame = tk.Frame(toolbar, bg="#1e1e1e")
        color_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        text_color_btn = tk.Button(color_frame, text="A", bg="#0f3460", fg="#00d4ff",
                                   font=("Arial", 10, "bold"), width=3)
        text_color_btn.pack(side=tk.LEFT, padx=2)
        
        highlight_btn = tk.Button(color_frame, text="◼", bg="#ffff00", fg="black",
                                 font=("Arial", 10), width=3)
        highlight_btn.pack(side=tk.LEFT, padx=2)
        
        # Text area with better styling
        text_frame = tk.Frame(win.content, bg="white")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_area = tk.Text(text_frame, bg="white", fg="black",
                           font=("Arial", 11), wrap=tk.WORD, 
                           insertbackground="black", padx=10, pady=10,
                           undo=True, maxundo=-1)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scrollbar.set)
        
        # Configure text tags for formatting
        text_area.tag_configure("bold", font=("Arial", 11, "bold"))
        text_area.tag_configure("italic", font=("Arial", 11, "italic"))
        text_area.tag_configure("underline", underline=True)
        text_area.tag_configure("left", justify="left")
        text_area.tag_configure("center", justify="center")
        text_area.tag_configure("right", justify="right")
        text_area.tag_configure("highlight", background="yellow")
        
        # Font size tags
        for size in [8, 10, 11, 12, 14, 16, 18, 20, 24, 28, 36, 48]:
            text_area.tag_configure(f"size{size}", font=("Arial", size))
        
        # Color tags
        colors = ["black", "red", "blue", "green", "purple", "orange"]
        for color in colors:
            text_area.tag_configure(f"color_{color}", foreground=color)
        
        # Formatting functions
        def apply_tag(tag_name):
            try:
                current_tags = text_area.tag_names("sel.first")
                if tag_name in current_tags:
                    text_area.tag_remove(tag_name, "sel.first", "sel.last")
                else:
                    text_area.tag_add(tag_name, "sel.first", "sel.last")
            except:
                pass
        
        def change_font_size(event=None):
            try:
                size = font_size.get()
                # Remove old size tags
                for s in [8, 10, 11, 12, 14, 16, 18, 20, 24, 28, 36, 48]:
                    text_area.tag_remove(f"size{s}", "sel.first", "sel.last")
                text_area.tag_add(f"size{size}", "sel.first", "sel.last")
            except:
                pass
        
        def change_text_color():
            try:
                color = tk.colorchooser.askcolor(title="Choose text color")[1]
                if color:
                    text_area.tag_add(f"color_custom", "sel.first", "sel.last")
                    text_area.tag_configure(f"color_custom", foreground=color)
            except:
                pass
        
        def apply_alignment(align):
            try:
                # Get current line
                current_line = text_area.index("insert").split('.')[0]
                text_area.tag_add(align, f"{current_line}.0", f"{current_line}.end")
            except:
                pass
        
        # Bind buttons to functions
        bold_btn.config(command=lambda: apply_tag("bold"))
        italic_btn.config(command=lambda: apply_tag("italic"))
        underline_btn.config(command=lambda: apply_tag("underline"))
        size_combo.bind("<<ComboboxSelected>>", change_font_size)
        text_color_btn.config(command=change_text_color)
        highlight_btn.config(command=lambda: apply_tag("highlight"))
        left_btn.config(command=lambda: apply_alignment("left"))
        center_btn.config(command=lambda: apply_alignment("center"))
        right_btn.config(command=lambda: apply_alignment("right"))
        
        # Keyboard shortcuts
        text_area.bind("<Control-b>", lambda e: apply_tag("bold"))
        text_area.bind("<Control-i>", lambda e: apply_tag("italic"))
        text_area.bind("<Control-u>", lambda e: apply_tag("underline"))
        
        # Status bar
        status_bar = tk.Frame(win.content, bg="#1e1e1e", height=25)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        word_count = tk.Label(status_bar, text="Words: 0 | Characters: 0", 
                             bg="#1e1e1e", fg="white", font=("Arial", 9))
        word_count.pack(side=tk.RIGHT, padx=10)
        
        def update_word_count(event=None):
            content = text_area.get("1.0", tk.END)
            words = len(content.split())
            chars = len(content.strip())
            word_count.config(text=f"Words: {words} | Characters: {chars}")
        
        text_area.bind("<KeyRelease>", update_word_count)
        
        # Welcome text
        text_area.insert("1.0", "Welcome to AIOS Word Processor\n\n")
        text_area.tag_add("bold", "1.0", "1.end")
        text_area.tag_add("size20", "1.0", "1.end")
        text_area.insert("2.0", "Start typing your document here...\n\n")
        text_area.insert("3.0", "Features:\n• Bold, Italic, Underline\n• Font sizes\n• Text colors\n• Text alignment\n• Word count\n\nKeyboard shortcuts:\nCtrl+B = Bold\nCtrl+I = Italic\nCtrl+U = Underline")

    
    def open_calculator(self):
        win = Window(self.root, "Calculator", 350, 450, 300, 120)
        
        calc_display = tk.Entry(win.content, font=("Arial", 20), justify="right",
                                     bg="#2b2b2b", fg="white", bd=0)
        calc_display.pack(fill=tk.X, padx=10, pady=10)
        calc_display.insert(0, "0")
        
        calc_expr = [""]
        
        def calc_click(btn):
            if btn == 'C':
                calc_expr[0] = ""
                calc_display.delete(0, tk.END)
                calc_display.insert(0, "0")
            elif btn == '=':
                try:
                    result = eval(calc_expr[0])
                    calc_display.delete(0, tk.END)
                    calc_display.insert(0, str(result))
                    calc_expr[0] = str(result)
                except:
                    calc_display.delete(0, tk.END)
                    calc_display.insert(0, "Error")
                    calc_expr[0] = ""
            else:
                if calc_display.get() == "0" or calc_display.get() == "Error":
                    calc_display.delete(0, tk.END)
                calc_expr[0] += btn
                calc_display.delete(0, tk.END)
                calc_display.insert(0, calc_expr[0])
        
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '=', '+']
        ]
        
        for row in buttons:
            row_frame = tk.Frame(win.content, bg="#2b2b2b")
            row_frame.pack(fill=tk.BOTH, expand=True)
            
            for btn_text in row:
                btn = tk.Button(row_frame, text=btn_text, font=("Arial", 18),
                              bg="#0f3460", fg="white", relief=tk.FLAT,
                              command=lambda t=btn_text: calc_click(t))
                btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    def open_game_launcher(self):
        win = Window(self.root, "Game Launcher", 500, 400, 350, 150)
        
        tk.Label(win.content, text="🎮 Game Launcher", font=("Arial", 18, "bold"),
                bg="#2b2b2b", fg="white").pack(pady=20)
        
        tk.Label(win.content, text="Available Games", font=("Arial", 12),
                bg="#2b2b2b", fg="#aaa").pack(pady=10)
        
        # Galaga game button
        game_frame = tk.Frame(win.content, bg="#1e1e1e")
        game_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(game_frame, text="👾 Galaga", font=("Arial", 14, "bold"),
                bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=20)
        
        def launch_galaga():
            import subprocess
            import os
            try:
                # Check if galaga.py exists
                if os.path.exists("galaga.py"):
                    subprocess.Popen(["python", "galaga.py"])
                    messagebox.showinfo("Game Launcher", "Galaga is starting!")
                else:
                    messagebox.showerror("Error", "galaga.py not found!\n\nMake sure galaga.py is in the same folder as this program.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch Galaga:\n{str(e)}")
        
        tk.Button(game_frame, text="▶ Play", bg="#0f3460", fg="white",
                 font=("Arial", 11), command=launch_galaga, width=10).pack(side=tk.RIGHT, padx=20)
        
        # Instructions
        tk.Label(win.content, text="Click 'Play' to launch the game", 
                font=("Arial", 10), bg="#2b2b2b", fg="#aaa").pack(pady=30)
    
    def open_ai_chat(self):
        win = Window(self.root, "AI Assistant", 700, 600, 250, 50)
        
        # Header
        header = tk.Frame(win.content, bg="#0f3460")
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🤖 AIOS AI Assistant", font=("Arial", 14, "bold"),
                bg="#0f3460", fg="white").pack(pady=10)
        tk.Label(header, text="Your intelligent helper", font=("Arial", 9),
                bg="#0f3460", fg="#aaa").pack(pady=(0, 10))
        
        # Chat display area
        chat_frame = tk.Frame(win.content, bg="#2b2b2b")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        chat_display = scrolledtext.ScrolledText(chat_frame, bg="#1e1e1e", fg="white",
                                                 font=("Arial", 10), wrap=tk.WORD,
                                                 state=tk.DISABLED)
        chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for styling
        chat_display.tag_config("user", foreground="#00d4ff", font=("Arial", 10, "bold"))
        chat_display.tag_config("ai", foreground="#ff006e", font=("Arial", 10, "bold"))
        chat_display.tag_config("message", foreground="white")
        
        # Input area
        input_frame = tk.Frame(win.content, bg="#2b2b2b")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        user_input = tk.Entry(input_frame, bg="#1e1e1e", fg="white", 
                             font=("Arial", 11), insertbackground="white")
        user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        def add_message(sender, message, tag):
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"{sender}: ", tag)
            chat_display.insert(tk.END, f"{message}\n\n", "message")
            chat_display.see(tk.END)
            chat_display.config(state=tk.DISABLED)
        
        def get_ai_response(user_msg):
            user_msg_lower = user_msg.lower()
            
            # Check for math expressions
            try:
                # Look for math patterns
                math_keywords = ['calculate', 'solve', 'what is', 'what\'s', 'compute', '+', '-', '*', '/', 'x', '×', '÷']
                has_math = any(keyword in user_msg_lower for keyword in math_keywords)
                
                if has_math or any(char.isdigit() for char in user_msg):
                    # Clean up the message for evaluation
                    math_expr = user_msg_lower
                    # Remove common words
                    for word in ['calculate', 'solve', 'what is', 'what\'s', 'compute', 'equals', '=', '?']:
                        math_expr = math_expr.replace(word, '')
                    
                    # Replace common symbols
                    math_expr = math_expr.replace('x', '*').replace('×', '*').replace('÷', '/')
                    math_expr = math_expr.strip()
                    
                    # Try to evaluate
                    if math_expr and any(char.isdigit() for char in math_expr):
                        try:
                            result = eval(math_expr)
                            return f"The answer is: {result}\n\nCalculation: {math_expr} = {result}"
                        except:
                            pass
            except:
                pass
            
            # Simple response logic
            if "hello" in user_msg_lower or "hi" in user_msg_lower or "hey" in user_msg_lower:
                return "Hello! I'm AIOS Assistant. How can I help you today?"
            elif "how are you" in user_msg_lower:
                return "I'm functioning perfectly! Thanks for asking. How can I assist you?"
            elif "your name" in user_msg_lower or "who are you" in user_msg_lower:
                return "I'm AIOS Assistant, your AI-powered helper built into this operating system!"
            elif "time" in user_msg_lower or "date" in user_msg_lower:
                now = datetime.datetime.now()
                return f"The current time is {now.strftime('%I:%M %p')} and today is {now.strftime('%A, %B %d, %Y')}."
            elif "weather" in user_msg_lower:
                return "I don't have access to real-time weather data, but I hope it's nice where you are! 🌤️"
            elif "open" in user_msg_lower and "browser" in user_msg_lower:
                self.root.after(100, self.open_browser)
                return "Opening the browser for you!"
            elif "open" in user_msg_lower and ("file" in user_msg_lower or "files" in user_msg_lower):
                self.root.after(100, self.open_file_explorer)
                return "Opening File Explorer for you!"
            elif "open" in user_msg_lower and "calculator" in user_msg_lower:
                self.root.after(100, self.open_calculator)
                return "Opening Calculator for you!"
            elif "open" in user_msg_lower and "game" in user_msg_lower:
                self.root.after(100, self.open_game_launcher)
                return "Opening Game Launcher for you!"
            elif "joke" in user_msg_lower:
                jokes = [
                    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                    "Why did the AI go to school? To improve its learning algorithms! 🎓",
                    "What's an AI's favorite snack? Microchips! 🍟"
                ]
                return random.choice(jokes)
            elif "help" in user_msg_lower:
                return "I can help you with:\n- Solving math problems (e.g., 'what is 25 * 4?')\n- Opening apps (browser, files, calculator, games)\n- Telling jokes\n- Answering questions\n- General conversation\nJust ask me anything!"
            elif "thank" in user_msg_lower:
                return "You're welcome! Happy to help! 😊"
            elif "bye" in user_msg_lower or "goodbye" in user_msg_lower:
                return "Goodbye! Feel free to chat with me anytime!"
            elif "aios" in user_msg_lower:
                return "AIOS stands for Artificial Intelligence Operating System. It's a demonstration of AI-powered interface design!"
            elif "?" in user_msg:
                return "That's an interesting question! While I'm a simple AI assistant, I'm here to help with basic tasks and conversation."
            else:
                responses = [
                    "That's interesting! Tell me more.",
                    "I understand. How can I help you with that?",
                    "I'm processing that. Is there something specific you'd like to know?",
                    "Thanks for sharing! What else can I do for you?",
                    "I'm here to help! Try asking me to solve a math problem or open an app!"
                ]
                return random.choice(responses)
        
        def send_message(event=None):
            message = user_input.get().strip()
            if message:
                # Add user message
                add_message("You", message, "user")
                user_input.delete(0, tk.END)
                
                # Simulate thinking delay
                win.content.after(800, lambda: add_message("AI Assistant", get_ai_response(message), "ai"))
        
        send_btn = tk.Button(input_frame, text="Send", bg="#0f3460", fg="white",
                            font=("Arial", 10), command=send_message, width=10)
        send_btn.pack(side=tk.LEFT)
        
        user_input.bind("<Return>", send_message)
        
        # Welcome message
        add_message("AI Assistant", "Hello! I'm AIOS Assistant. I can help you navigate the system, open apps, and answer questions. How can I help you today?", "ai")
        
        user_input.focus()
    
    def show_about(self):
        messagebox.showinfo("About PyOS", 
                           "PyOS - Python Operating System Frontend\n\n"
                           "Version 1.0\n"
                           "Created with Python & Tkinter\n\n"
                           "Demonstrating AI-powered development!")
    
    def update_clock(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p\n%m/%d/%Y")
        self.clock.config(text=time_str)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = OperatingSystem(root)
    root.mainloop()
      

