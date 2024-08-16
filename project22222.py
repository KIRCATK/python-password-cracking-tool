import random
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import threading

# Check if the password consists only of numeric characters
def is_numeric_password(password):
    return password.isdigit()

# Generate a random password of given length from the given character set
def generate_random_password(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

# Function to crack the password by trying random combinations
def crack_password(password):
    predicted_pass = ''
    characters = '0123456789'

    if not is_numeric_password(password):
        characters += 'abcdefghijklmnopqrstuvwxyz'

    characters += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|;:,.<>?'

    random.seed(time.time())
    attempts = 0

    # Keep generating random passwords until the correct one is found
    while predicted_pass != password:
        predicted_pass = generate_random_password(len(password), characters)
        attempts += 1
        update_display(predicted_pass)
        progress_bar['value'] = (attempts % 100)  # Mock progress update
    
    return predicted_pass

# Update the display with the current predicted password
def update_display(predicted_pass):
    text_display.config(state=tk.NORMAL)
    text_display.insert(tk.END, predicted_pass + '\n')
    text_display.config(state=tk.DISABLED)
    text_display.see(tk.END)
    root.update_idletasks()

# Start the password cracking process
def start_cracking():
    password = password_entry.get()
    if password:
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0, tk.END)
        text_display.config(state=tk.DISABLED)
        progress_bar['value'] = 0
        
        # Start password cracking in a new thread
        crack_thread = threading.Thread(target=crack_password_threaded, args=(password,))
        crack_thread.start()
    else:
        messagebox.showwarning("Input Error", "Please enter a password.")

# Run the password cracking function in a separate thread
def crack_password_threaded(password):
    cracked_password = crack_password(password)
    messagebox.showinfo("Result", f"Your password is: {cracked_password}")

# Set up the main application window
root = tk.Tk()
root.title("Password Cracker")
root.configure(bg='#1e1e1e')

frame = tk.Frame(root, bg='#1e1e1e')
frame.pack(padx=10, pady=10)

# ASCII art for the application
ascii_art = """
  _____         _____ _______          ______  _____  _____  
 |  __ \ /\    / ____/ ____\ \        / / __ \|  __ \|  __ \ 
 | |__) /  \  | (___| (___  \ \  /\  / / |  | | |__) | |  | |
 |  ___/ /\ \  \___ \\___ \  \ \/  \/ /| |  | |  _  /| |  | |
 | |  / ____ \ ____) |___) |  \  /\  / | |__| | | \ \| |__| |
 |_|_/_/ ___\_\_____/_____/____\/  \/___\____/|_| _\_\_____/ 
  / ____|  __ \     /\   / ____| |/ /_   _| \ | |/ ____|     
 | |    | |__) |   /  \ | |    | ' /  | | |  \| | |  __      
 | |    |  _  /   / /\ \| |    |  <   | | | . ` | | |_ |     
 | |____| | \ \  / ____ \ |____| . \ _| |_| |\  | |__| |     
  \_____|_|  \_\/_/    \_\_____|_|\_\_____|_| \_|\_____|     
                                                             
                                                   kiran_Damai                                                          
"""

# Display the ASCII art in the application
ascii_label = tk.Label(frame, text=ascii_art, fg='#00ffff', bg='#1e1e1e', font=('Courier', 12))
ascii_label.pack(pady=10)

# Label and entry for password input
password_label = tk.Label(frame, text="Enter your password:", fg='#ffffff', bg='#1e1e1e')
password_label.pack(pady=5)

password_entry = tk.Entry(frame, show='*', width=30, bg='#333333', fg='#ffffff', insertbackground='white')
password_entry.pack(pady=5)

# Button to start the password cracking process
start_button = tk.Button(frame, text="Start Cracking", command=start_cracking, bg='#444444', fg='#ffffff', activebackground='#555555')
start_button.pack(pady=10)

# Progress bar to show cracking progress
progress_bar = Progressbar(frame, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=10)

# Text display to show generated passwords
text_display = tk.Text(frame, height=30, width=100, state=tk.DISABLED, bg='#1e1e1e', fg='#00ff00', insertbackground='white')
text_display.pack(padx=5, pady=5)

# Scrollbar for the text display
scrollbar = tk.Scrollbar(frame, command=text_display.yview, bg='#1e1e1e')
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_display['yscrollcommand'] = scrollbar.set

# Center the text display within the frame
frame.pack(anchor='center', expand=True)

# Start the main application loop
root.mainloop()
