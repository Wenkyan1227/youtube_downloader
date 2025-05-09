import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import openpyxl

def browse_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        excel_path_var.set(file_path)

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def download_videos():
    excel_file = excel_path_var.get()
    folder = folder_var.get()

    if not excel_file or not folder:
        messagebox.showwarning("Input Required", "Please select an Excel file and a download folder.")
        return

    try:
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        links = []
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1):
            cell_value = row[0].value
            if cell_value and str(cell_value).startswith("http"):
                links.append(str(cell_value))

        if not links:
            messagebox.showerror("No URLs Found", "No valid YouTube URLs found in Column A.")
            return

        for url in links:
            command = ['yt-dlp', '-o', os.path.join(folder, '%(title)s.%(ext)s'), url]
            subprocess.run(command, check=True)

        messagebox.showinfo("Success", f"{len(links)} video(s) downloaded successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("YouTube Downloader from Excel (yt-dlp)")
root.geometry("520x280")

tk.Label(root, text="Select Excel File (Column A contains URLs):").pack(pady=(10, 0))
excel_path_var = tk.StringVar()
tk.Entry(root, textvariable=excel_path_var, width=60).pack()
tk.Button(root, text="Browse Excel File", command=browse_excel).pack(pady=(5, 10))

tk.Label(root, text="Select Download Folder:").pack()
folder_var = tk.StringVar()
tk.Entry(root, textvariable=folder_var, width=60).pack()
tk.Button(root, text="Browse Folder", command=browse_folder).pack(pady=(5, 10))

tk.Button(root, text="Download All Videos", command=download_videos, bg="green", fg="white", height=2, width=25).pack(pady=15)

root.mainloop()
