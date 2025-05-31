import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import threading

class ModernChatbot:
    def __init__(self):
        # Set up the window theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create the main window
        self.window = ctk.CTk()
        self.window.title("PyChat")
        self.window.geometry("500x700")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create chat display
        self.chat_display = ctk.CTkTextbox(
            self.main_frame,
            wrap="word",
            font=("Helvetica", 12),
            height=500
        )
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure text widget tags for message formatting
        text_widget = self.chat_display._textbox
        text_widget.tag_configure("user", foreground="#4A90E2")
        text_widget.tag_configure("bot", foreground="#4CAF50")
        text_widget.tag_configure("system", foreground="#FF5252")
        
        # Create input area frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="x", padx=5, pady=5)
        
        # Create message input
        self.input_field = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message...",
            font=("Helvetica", 12),
            height=40
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Create send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=80,
            height=40,
            command=self.send_message
        )
        self.send_button.pack(side="right")
        
        # Create status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Loading model...",
            font=("Helvetica", 10)
        )
        self.status_label.pack(anchor="w", padx=5)
        
        # Bind enter key to send message
        self.window.bind("<Return>", lambda event: self.send_message())
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Initialize chatbot model
        self.model_name = "facebook/blenderbot-400M-distill"
        
        # Loading message
        self.append_message("System", "Initializing chatbot...")
        
        # Load model in a separate thread to keep UI responsive
        threading.Thread(target=self.load_model, daemon=True).start()
        
    def load_model(self):
        """Load the chatbot model and tokenizer"""
        try:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name, 
                use_safetensors=False
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.append_message("System", "Model loaded successfully!")
            self.status_label.configure(text="Ready")
            self.append_message("PyChat", "Hello! How can I help you today?")
        except Exception as e:
            self.append_message("System", f"Error loading model: {str(e)}")
            self.status_label.configure(text="Error")
    
    def append_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.configure(state="normal")
        text_widget = self.chat_display._textbox
        
        # Format the message
        if sender == "You":
            text_widget.insert("end", "You: ", "user")
            text_widget.insert("end", f"{message}\n\n")
        elif sender == "System":
            text_widget.insert("end", f"System: {message}\n\n", "system")
        else:
            text_widget.insert("end", f"{sender}: ", "bot")
            text_widget.insert("end", f"{message}\n\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def generate_response(self, user_input):
        """Generate a response from the chatbot model"""
        history_string = "\n".join(self.conversation_history[-4:])
        inputs = self.tokenizer.encode_plus(history_string, user_input, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return response
    
    def process_message(self, user_input):
        """Process the user's message and generate a response"""
        try:
            response = self.generate_response(user_input)
            self.conversation_history.append(user_input)
            self.conversation_history.append(response)
            self.append_message("PyChat", response)
        except Exception as e:
            self.append_message("System", f"Error: {str(e)}")
        finally:
            self.status_label.configure(text="Ready")
            self.send_button.configure(state="normal")
            self.input_field.configure(state="normal")
            self.input_field.focus()
    
    def send_message(self):
        """Send a message and get a response"""
        user_input = self.input_field.get().strip()
        if user_input:
            self.status_label.configure(text="Processing...")
            self.send_button.configure(state="disabled")
            self.input_field.configure(state="disabled")
            self.append_message("You", user_input)
            self.input_field.delete(0, "end")
            threading.Thread(
                target=self.process_message,
                args=(user_input,),
                daemon=True
            ).start()
    
    def run(self):
        """Start the chatbot application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernChatbot()
    app.run()
