#!/usr/bin/env python3
"""
SpectraAI Desktop GUI - Beautiful Chat Interface
A modern, user-friendly desktop application for SpectraAI
"""

import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import logging
from datetime import datetime
from pathlib import Path

# Import SpectraAI components
from logic.brain import SpectraBrain
from logic.ai_manager import AIManager
from core.memory import Memory
from core.personality import Personality
from core.emotions import EmotionEngine

class SpectraDesktopApp:
    """Beautiful desktop GUI for SpectraAI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        # SpectraAI components
        self.brain = None
        self.ai_manager = None
        self.memory = Memory()
        self.personality = Personality()
        self.emotions = EmotionEngine()
        
        # Threading for async operations
        self.message_queue = queue.Queue()
        self.loop = None
        self.loop_thread = None
        
        # Initialize SpectraAI
        self.initialize_spectra()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("🤖 SpectraAI - Your FREE AI Companion")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Modern color scheme
        self.colors = {
            'bg': '#1e1e1e',           # Dark background
            'chat_bg': '#2d2d2d',      # Chat area background
            'user_msg': '#0078d4',      # User message color
            'ai_msg': '#6264a7',        # AI message color
            'text': '#ffffff',          # Text color
            'accent': '#00ff88',        # Accent color (green)
            'button': '#484848',        # Button color
            'entry': '#3d3d3d'          # Entry background
        }
        
        self.root.configure(bg=self.colors['bg'])
        
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Chat.TFrame', background=self.colors['chat_bg'])
        style.configure('Sidebar.TFrame', background=self.colors['bg'])
        style.configure('Title.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Status.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 9))
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title area
        title_frame = ttk.Frame(main_frame, style='Sidebar.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                               text="🤖 SpectraAI - FREE OpenHermes Chat",
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = ttk.Label(title_frame,
                                     text="🔄 Initializing...",
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Chat area
        chat_frame = ttk.Frame(main_frame, style='Chat.TFrame')
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            bg=self.colors['chat_bg'],
            fg=self.colors['text'],
            font=('Segoe UI', 11),
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different message types
        self.chat_display.tag_configure('user', 
                                       foreground=self.colors['user_msg'],
                                       font=('Segoe UI', 11, 'bold'))
        self.chat_display.tag_configure('ai',
                                       foreground=self.colors['ai_msg'],
                                       font=('Segoe UI', 11))
        self.chat_display.tag_configure('system',
                                       foreground=self.colors['accent'],
                                       font=('Segoe UI', 10, 'italic'))
        self.chat_display.tag_configure('timestamp',
                                       foreground='#888888',
                                       font=('Segoe UI', 9))
        
        # Input area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        # Message entry
        self.message_entry = tk.Text(
            input_frame,
            height=3,
            bg=self.colors['entry'],
            fg=self.colors['text'],
            font=('Segoe UI', 11),
            borderwidth=1,
            relief='solid',
            padx=10,
            pady=8
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send\n💬",
            command=self.send_message,
            bg=self.colors['accent'],
            fg='black',
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            relief='flat',
            padx=20,
            cursor='hand2'
        )
        self.send_button.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind Enter key
        self.message_entry.bind('<Return>', self.on_enter_key)
        self.message_entry.bind('<Shift-Return>', self.on_shift_enter)
        
        # Add welcome message
        self.add_system_message("Welcome to SpectraAI! 🌟")
        self.add_system_message("Powered by FREE OpenHermes-2.5-Mistral-7B via Ollama")
        self.add_system_message("Start chatting with your AI companion below!")
        
    def initialize_spectra(self):
        """Initialize SpectraAI in background thread"""
        def init_thread():
            try:
                # Set up event loop
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                
                # Initialize components
                self.loop.run_until_complete(self._async_init())
                
                # Update status
                self.root.after(0, lambda: self.update_status("✅ Ready - FREE AI Active!"))
                self.root.after(0, lambda: self.add_system_message("🎉 SpectraAI is ready to chat!"))
                
                # Keep loop running for async operations
                self.loop.run_forever()
                
            except Exception as e:
                error_msg = f"❌ Initialization failed: {e}"
                self.root.after(0, lambda: self.update_status(error_msg))
                self.root.after(0, lambda: self.add_system_message(error_msg))
        
        self.loop_thread = threading.Thread(target=init_thread, daemon=True)
        self.loop_thread.start()
        
    async def _async_init(self):
        """Async initialization of SpectraAI components"""
        try:
            # Initialize AI Manager
            self.ai_manager = AIManager()
            await self.ai_manager.initialize()
            
            # Initialize Brain
            self.brain = SpectraBrain(
                ai_manager=self.ai_manager,
                memory=self.memory,
                personality=self.personality,
                emotions=self.emotions
            )
            await self.brain.initialize()
            
            return True
            
        except Exception as e:
            logging.error(f"Async init failed: {e}")
            raise
            
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        
    def add_message(self, sender, message, tag='user'):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        
    def add_system_message(self, message):
        """Add system message"""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, f"System: {message}\n\n", 'system')
        self.chat_display.see(tk.END)
        
    def on_enter_key(self, event):
        """Handle Enter key press"""
        self.send_message()
        return 'break'  # Prevent default newline
        
    def on_shift_enter(self, event):
        """Handle Shift+Enter for newline"""
        return  # Allow default newline
        
    def send_message(self):
        """Send user message and get AI response"""
        user_message = self.message_entry.get("1.0", tk.END).strip()
        
        if not user_message:
            return
            
        # Clear input
        self.message_entry.delete("1.0", tk.END)
        
        # Add user message to chat
        self.add_message("You", user_message, 'user')
        
        # Show thinking indicator
        self.update_status("🤔 Spectra is thinking...")
        
        # Get AI response in background
        if self.brain and self.loop:
            # Schedule the async response
            future = asyncio.run_coroutine_threadsafe(
                self.get_ai_response(user_message), 
                self.loop
            )
            
            # Check for response in separate thread
            def check_response():
                try:
                    response = future.result(timeout=30)  # 30 second timeout
                    self.root.after(0, lambda: self.handle_ai_response(response))
                except Exception as e:
                    error_msg = f"Error getting response: {e}"
                    self.root.after(0, lambda: self.handle_ai_response(error_msg))
                    
            threading.Thread(target=check_response, daemon=True).start()
        else:
            self.add_message("Spectra", "I'm still initializing. Please wait a moment!", 'ai')
            self.update_status("⚠️ Still initializing...")
            
    async def get_ai_response(self, user_message):
        """Get response from SpectraAI brain"""
        try:
            if self.brain:
                response = await self.brain.think(user_message)
                return response
            else:
                return "I'm still starting up. Give me a moment!"
        except Exception as e:
            logging.error(f"AI response error: {e}")
            return f"Sorry, I encountered an error: {e}"
            
    def handle_ai_response(self, response):
        """Handle AI response in main thread"""
        self.add_message("Spectra", response, 'ai')
        self.update_status("✅ Ready - FREE AI Active!")
        
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        finally:
            # Cleanup
            if self.loop and self.loop.is_running():
                self.loop.call_soon_threadsafe(self.loop.stop)

def main():
    """Main entry point"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run the app
    app = SpectraDesktopApp()
    app.run()

if __name__ == "__main__":
    main()
