import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def download_video():
    url = url_entry.get()
    folder = folder_var.get()

    if not url or not folder:
        messagebox.showwarning("Input Required", "Please enter a URL and choose a folder.")
        return

    try:
        # Download using yt-dlp
        command = ['yt-dlp', '-o', os.path.join(folder, '%(title)s.%(ext)s'), url]
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Video downloaded successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Download Failed", f"An error occurred:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("YouTube Video Downloader (yt-dlp)")
root.geometry("500x220")

tk.Label(root, text="YouTube Video URL:").pack(pady=(10, 0))
url_entry = tk.Entry(root, width=60)
url_entry.pack()

tk.Label(root, text="Download Folder:").pack(pady=(10, 0))
folder_var = tk.StringVar()
folder_frame = tk.Frame(root)
folder_frame.pack()
tk.Entry(folder_frame, textvariable=folder_var, width=45).pack(side="left", padx=(0, 5))
tk.Button(folder_frame, text="Browse", command=browse_folder).pack(side="left")

tk.Button(root, text="Download Video", command=download_video, bg="green", fg="white", height=2, width=20).pack(pady=20)

root.mainloop()
