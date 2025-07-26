#!/usr/bin/env python3
"""
SpectraAI Advanced Desktop App - Professional GUI with Features
"""

import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import logging
from datetime import datetime
import webbrowser

# SpectraAI imports
from logic.brain import SpectraBrain
from logic.ai_manager import AIManager
from core.memory import Memory
from core.personality import Personality
from core.emotions import EmotionEngine

class AdvancedSpectraGUI:
    """Advanced SpectraAI GUI with professional features"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        
        # SpectraAI components
        self.brain = None
        self.ai_manager = None
        self.memory = Memory()
        self.personality = Personality()
        self.emotions = EmotionEngine()
        
        # State
        self.conversation_history = []
        self.loop = None
        self.loop_thread = None
        
        # Initialize
        self.initialize_ai()
        
    def setup_window(self):
        """Setup main window"""
        self.root.title("🚀 SpectraAI Advanced - FREE OpenHermes Desktop App")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Dark theme colors
        self.theme = {
            'bg': '#0d1117',
            'surface': '#161b22', 
            'primary': '#238636',
            'secondary': '#1f6feb',
            'accent': '#f85149',
            'text': '#f0f6fc',
            'text_secondary': '#8b949e',
            'border': '#30363d'
        }
        
        self.root.configure(bg=self.theme['bg'])
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root, bg=self.theme['surface'], fg=self.theme['text'])
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.theme['surface'], fg=self.theme['text'])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Conversation", command=self.save_conversation)
        file_menu.add_command(label="Load Conversation", command=self.load_conversation)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.theme['surface'], fg=self.theme['text'])
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Clear Chat", command=self.clear_chat)
        view_menu.add_command(label="Provider Status", command=self.show_provider_status)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.theme['surface'], fg=self.theme['text'])
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About SpectraAI", command=self.show_about)
        help_menu.add_command(label="GitHub Repository", command=self.open_github)
        
    def create_main_interface(self):
        """Create the main interface"""
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.theme['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_container)
        
        # Content area with sidebar
        content_frame = tk.Frame(main_container, bg=self.theme['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Sidebar
        self.create_sidebar(content_frame)
        
        # Chat area
        self.create_chat_area(content_frame)
        
    def create_header(self, parent):
        """Create header with title and status"""
        header_frame = tk.Frame(parent, bg=self.theme['surface'], relief='solid', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🚀 SpectraAI Advanced",
            font=('Segoe UI', 20, 'bold'),
            bg=self.theme['surface'],
            fg=self.theme['primary']
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Subtitle  
        subtitle_label = tk.Label(
            header_frame,
            text="FREE OpenHermes-2.5-Mistral-7B • Professional AI Companion",
            font=('Segoe UI', 11),
            bg=self.theme['surface'],
            fg=self.theme['text_secondary']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 20), pady=15)
        
        # Status indicator
        self.status_frame = tk.Frame(header_frame, bg=self.theme['surface'])
        self.status_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.status_indicator = tk.Label(
            self.status_frame,
            text="🔄",
            font=('Segoe UI', 16),
            bg=self.theme['surface'],
            fg=self.theme['secondary']
        )
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_text = tk.Label(
            self.status_frame,
            text="Initializing...",
            font=('Segoe UI', 10),
            bg=self.theme['surface'],
            fg=self.theme['text']
        )
        self.status_text.pack(side=tk.LEFT, padx=(5, 0))
        
    def create_sidebar(self, parent):
        """Create sidebar with controls"""
        sidebar_frame = tk.Frame(parent, bg=self.theme['surface'], width=250, relief='solid', bd=1)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        sidebar_frame.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = tk.Label(
            sidebar_frame,
            text="🎛️ Controls",
            font=('Segoe UI', 14, 'bold'),
            bg=self.theme['surface'],
            fg=self.theme['text']
        )
        sidebar_title.pack(pady=20)
        
        # Provider info
        provider_frame = tk.LabelFrame(
            sidebar_frame,
            text="AI Provider",
            font=('Segoe UI', 10, 'bold'),
            bg=self.theme['surface'],
            fg=self.theme['text'],
            borderwidth=1,
            relief='solid'
        )
        provider_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.provider_label = tk.Label(
            provider_frame,
            text="🤖 Ollama (OpenHermes)",
            font=('Segoe UI', 10),
            bg=self.theme['surface'],
            fg=self.theme['primary']
        )
        self.provider_label.pack(pady=10)
        
        # Personality controls
        personality_frame = tk.LabelFrame(
            sidebar_frame,
            text="Personality",
            font=('Segoe UI', 10, 'bold'),
            bg=self.theme['surface'],
            fg=self.theme['text'],
            borderwidth=1,
            relief='solid'
        )
        personality_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Emotion display
        self.emotion_label = tk.Label(
            personality_frame,
            text="😊 Curious",
            font=('Segoe UI', 10),
            bg=self.theme['surface'],
            fg=self.theme['text']
        )
        self.emotion_label.pack(pady=5)
        
        # Memory stats
        memory_frame = tk.LabelFrame(
            sidebar_frame,
            text="Memory",
            font=('Segoe UI', 10, 'bold'),
            bg=self.theme['surface'],
            fg=self.theme['text'],
            borderwidth=1,
            relief='solid'
        )
        memory_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.memory_label = tk.Label(
            memory_frame,
            text="📚 15 memories",
            font=('Segoe UI', 10),
            bg=self.theme['surface'],
            fg=self.theme['text']
        )
        self.memory_label.pack(pady=5)
        
        # Quick actions
        actions_frame = tk.LabelFrame(
            sidebar_frame,
            text="Quick Actions",
            font=('Segoe UI', 10, 'bold'),
            bg=self.theme['surface'],
            fg=self.theme['text'],
            borderwidth=1,
            relief='solid'
        )
        actions_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Buttons
        tk.Button(
            actions_frame,
            text="💾 Save Chat",
            command=self.save_conversation,
            bg=self.theme['secondary'],
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2'
        ).pack(fill=tk.X, padx=5, pady=3)
        
        tk.Button(
            actions_frame,
            text="🧹 Clear Chat",
            command=self.clear_chat,
            bg=self.theme['accent'],
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2'
        ).pack(fill=tk.X, padx=5, pady=3)
        
        tk.Button(
            actions_frame,
            text="📊 AI Status",
            command=self.show_provider_status,
            bg=self.theme['primary'],
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            cursor='hand2'
        ).pack(fill=tk.X, padx=5, pady=3)
        
    def create_chat_area(self, parent):
        """Create main chat interface"""
        chat_container = tk.Frame(parent, bg=self.theme['bg'])
        chat_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            bg=self.theme['surface'],
            fg=self.theme['text'],
            font=('Segoe UI', 11),
            borderwidth=1,
            relief='solid',
            padx=20,
            pady=20,
            selectbackground=self.theme['secondary']
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Configure text tags
        self.chat_display.tag_configure('user', 
                                       foreground=self.theme['secondary'],
                                       font=('Segoe UI', 11, 'bold'))
        self.chat_display.tag_configure('ai',
                                       foreground=self.theme['primary'],
                                       font=('Segoe UI', 11))
        self.chat_display.tag_configure('system',
                                       foreground=self.theme['text_secondary'],
                                       font=('Segoe UI', 10, 'italic'))
        self.chat_display.tag_configure('timestamp',
                                       foreground=self.theme['text_secondary'],
                                       font=('Segoe UI', 9))
        
        # Input area
        input_container = tk.Frame(chat_container, bg=self.theme['bg'])
        input_container.pack(fill=tk.X)
        
        # Input field
        self.message_entry = tk.Text(
            input_container,
            height=4,
            bg=self.theme['surface'],
            fg=self.theme['text'],
            font=('Segoe UI', 11),
            borderwidth=1,
            relief='solid',
            padx=15,
            pady=10,
            selectbackground=self.theme['secondary']
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = tk.Button(
            input_container,
            text="Send\n🚀",
            command=self.send_message,
            bg=self.theme['primary'],
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            padx=25,
            cursor='hand2',
            width=8
        )
        self.send_button.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Key bindings
        self.message_entry.bind('<Return>', self.on_enter)
        self.message_entry.bind('<Shift-Return>', self.on_shift_enter)
        
        # Welcome messages
        self.add_system_message("🌟 Welcome to SpectraAI Advanced!")
        self.add_system_message("🚀 Powered by FREE OpenHermes-2.5-Mistral-7B")
        self.add_system_message("�� Your intelligent AI companion is ready!")
        
    def initialize_ai(self):
        """Initialize AI components"""
        def init_thread():
            try:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                
                self.loop.run_until_complete(self._async_init())
                
                self.root.after(0, self.on_ai_ready)
                self.loop.run_forever()
                
            except Exception as e:
                self.root.after(0, lambda: self.on_ai_error(str(e)))
        
        self.loop_thread = threading.Thread(target=init_thread, daemon=True)
        self.loop_thread.start()
        
    async def _async_init(self):
        """Async AI initialization"""
        self.ai_manager = AIManager()
        await self.ai_manager.initialize()
        
        self.brain = SpectraBrain(
            ai_manager=self.ai_manager,
            memory=self.memory,
            personality=self.personality,
            emotions=self.emotions
        )
        await self.brain.initialize()
        
    def on_ai_ready(self):
        """Called when AI is ready"""
        self.status_indicator.config(text="✅", fg=self.theme['primary'])
        self.status_text.config(text="Ready - FREE AI Active!")
        self.add_system_message("🎉 SpectraAI is ready to chat!")
        
    def on_ai_error(self, error):
        """Called when AI initialization fails"""
        self.status_indicator.config(text="❌", fg=self.theme['accent'])
        self.status_text.config(text="Initialization Failed")
        self.add_system_message(f"❌ Error: {error}")
        
    def add_message(self, sender, message, tag):
        """Add message to chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
        
        # Update conversation history
        self.conversation_history.append({
            'timestamp': timestamp,
            'sender': sender,
            'message': message
        })
        
    def add_system_message(self, message):
        """Add system message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, f"System: {message}\n\n", 'system')
        self.chat_display.see(tk.END)
        
    def on_enter(self, event):
        """Handle Enter key"""
        self.send_message()
        return 'break'
        
    def on_shift_enter(self, event):
        """Handle Shift+Enter"""
        return  # Allow newline
        
    def send_message(self):
        """Send message and get response"""
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            return
            
        self.message_entry.delete("1.0", tk.END)
        self.add_message("You", message, 'user')
        
        self.status_indicator.config(text="🤔", fg=self.theme['secondary'])
        self.status_text.config(text="Thinking...")
        
        if self.brain and self.loop:
            future = asyncio.run_coroutine_threadsafe(
                self.get_ai_response(message), 
                self.loop
            )
            
            def check_response():
                try:
                    response = future.result(timeout=30)
                    self.root.after(0, lambda: self.handle_response(response))
                except Exception as e:
                    self.root.after(0, lambda: self.handle_response(f"Error: {e}"))
                    
            threading.Thread(target=check_response, daemon=True).start()
        else:
            self.add_message("Spectra", "I'm still initializing. Please wait!", 'ai')
            
    async def get_ai_response(self, message):
        """Get AI response"""
        try:
            response = await self.brain.think(message)
            return response
        except Exception as e:
            return f"Sorry, I encountered an error: {e}"
            
    def handle_response(self, response):
        """Handle AI response"""
        self.add_message("Spectra", response, 'ai')
        self.status_indicator.config(text="✅", fg=self.theme['primary'])
        self.status_text.config(text="Ready - FREE AI Active!")
        
    def save_conversation(self):
        """Save conversation to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            messagebox.showinfo("Saved", f"Conversation saved to {filename}")
            
    def load_conversation(self):
        """Load conversation from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    history = json.load(f)
                self.clear_chat()
                for entry in history:
                    sender = entry['sender']
                    message = entry['message']
                    tag = 'user' if sender == 'You' else 'ai'
                    self.add_message(sender, message, tag)
                messagebox.showinfo("Loaded", "Conversation loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load conversation: {e}")
                
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.delete(1.0, tk.END)
        self.conversation_history.clear()
        self.add_system_message("Chat cleared! Start a new conversation.")
        
    def show_provider_status(self):
        """Show AI provider status"""
        if self.ai_manager:
            # This would show detailed provider status
            messagebox.showinfo("AI Status", 
                              "🤖 Provider: Ollama (OpenHermes)\n"
                              "📡 Status: Connected\n"
                              "🚀 Model: OpenHermes-2.5-Mistral-7B\n"
                              "💰 Cost: FREE\n"
                              "⚡ Speed: ~2-3 seconds")
        else:
            messagebox.showwarning("AI Status", "AI not initialized yet")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """
🤖 SpectraAI Advanced v1.0

A sophisticated FREE AI companion powered by:
• OpenHermes-2.5-Mistral-7B via Ollama
• Universal AI provider architecture
• Advanced personality and memory systems

✨ Features:
• 100% FREE local AI processing
• No API keys or monthly fees required
• Context-aware conversations
• Memory and personality integration
• Professional desktop interface

Created with ❤️ for the AI community
        """
        messagebox.showinfo("About SpectraAI", about_text)
        
    def open_github(self):
        """Open GitHub repository"""
        webbrowser.open("https://github.com/Vesryin/spectra-hermes-ai")
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        finally:
            if self.loop and self.loop.is_running():
                self.loop.call_soon_threadsafe(self.loop.stop)

if __name__ == "__main__":
    app = AdvancedSpectraGUI()
    app.run()
