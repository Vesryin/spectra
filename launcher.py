#!/usr/bin/env python3
"""
SpectraAI Launcher - Choose your interface!
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

class SpectraLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_interface()
        
    def setup_window(self):
        self.root.title("🚀 SpectraAI Launcher")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Dark theme
        self.root.configure(bg='#1e1e1e')
        
    def create_interface(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="🤖 SpectraAI Launcher",
            font=('Segoe UI', 20, 'bold'),
            bg='#1e1e1e',
            fg='#00ff88'
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Choose your SpectraAI experience!",
            font=('Segoe UI', 12),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        subtitle_label.pack(pady=10)
        
        # Options frame
        options_frame = tk.Frame(self.root, bg='#1e1e1e')
        options_frame.pack(pady=30)
        
        # Terminal option
        self.create_option_button(
            options_frame,
            "💬 Terminal Chat",
            "Simple command-line interface",
            self.launch_terminal,
            '#0078d4'
        )
        
        # Basic GUI option
        self.create_option_button(
            options_frame,
            "🖥️ Basic GUI",
            "Clean desktop chat interface",
            self.launch_basic_gui,
            '#6264a7'
        )
        
        # Advanced GUI option
        self.create_option_button(
            options_frame,
            "🚀 Advanced GUI",
            "Professional desktop app with features",
            self.launch_advanced_gui,
            '#00ff88'
        )
        
        # Full terminal option
        self.create_option_button(
            options_frame,
            "⚡ Full Terminal Experience",
            "Complete SpectraAI with all features",
            self.launch_full_terminal,
            '#f85149'
        )
        
        # Info
        info_label = tk.Label(
            self.root,
            text="All options are 100% FREE using OpenHermes!",
            font=('Segoe UI', 10, 'italic'),
            bg='#1e1e1e',
            fg='#888888'
        )
        info_label.pack(side=tk.BOTTOM, pady=20)
        
    def create_option_button(self, parent, title, description, command, color):
        # Button frame
        button_frame = tk.Frame(parent, bg='#2d2d2d', relief='solid', bd=1)
        button_frame.pack(fill=tk.X, pady=5, padx=20)
        
        # Button
        button = tk.Button(
            button_frame,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            bg=color,
            fg='white' if color != '#00ff88' else 'black',
            relief='flat',
            command=command,
            cursor='hand2',
            padx=20,
            pady=10
        )
        button.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Description
        desc_label = tk.Label(
            button_frame,
            text=description,
            font=('Segoe UI', 9),
            bg='#2d2d2d',
            fg='#cccccc'
        )
        desc_label.pack(pady=(0, 10))
        
    def launch_terminal(self):
        """Launch simple demo"""
        self.launch_script('simple_demo.py')
        
    def launch_basic_gui(self):
        """Launch basic GUI"""
        self.launch_script('spectra_gui.py')
        
    def launch_advanced_gui(self):
        """Launch advanced GUI"""
        self.launch_script('spectra_advanced_gui.py')
        
    def launch_full_terminal(self):
        """Launch full experience"""
        self.launch_script('main.py')
        
    def launch_script(self, script_name):
        """Launch a Python script"""
        try:
            if os.path.exists(script_name):
                subprocess.Popen([sys.executable, script_name])
                tk.messagebox.showinfo("Launched", f"Starting {script_name}...")
            else:
                tk.messagebox.showerror("Error", f"Script {script_name} not found!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to launch: {e}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    launcher = SpectraLauncher()
    launcher.run()
