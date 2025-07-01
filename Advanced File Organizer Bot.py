import os
import shutil
import time
from tkinter import *
from tkinter import filedialog, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Logic
def organize_files(directory, by_extension=False, by_type=False, by_size=False):
    if not os.path.exists(directory):
        return

    for filename in os.listdir(directory):
        src_path = os.path.join(directory, filename)
        if os.path.isdir(src_path):
            continue

        try:
            if by_extension:
                ext = filename.split('.')[-1]
                dest_dir = os.path.join(directory, ext.upper() + "_Files")
            elif by_type:
                file_type = get_file_type(filename)
                dest_dir = os.path.join(directory, file_type + "_Files")
            elif by_size:
                size = os.path.getsize(src_path)
                if size < 1024 * 1024:
                    dest_dir = os.path.join(directory, "Small_Files")
                elif size < 10 * 1024 * 1024:
                    dest_dir = os.path.join(directory, "Medium_Files")
                else:
                    dest_dir = os.path.join(directory, "Large_Files")
            else:
                continue

            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(src_path, os.path.join(dest_dir, filename))
        except Exception as e:
            print(f"Error organizing {filename}: {e}")

def get_file_type(filename):
    image_ext = ['jpg', 'jpeg', 'png', 'gif']
    doc_ext = ['pdf', 'doc', 'docx', 'txt']
    video_ext = ['mp4', 'mov', 'avi']
    ext = filename.split('.')[-1].lower()
    if ext in image_ext:
        return "Image"
    elif ext in doc_ext:
        return "Document"
    elif ext in video_ext:
        return "Video"
    else:
        return "Other"

# Watchdog Handler
class FileHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.dir = directory

    def on_created(self, event):
        time.sleep(1)  # wait for file to be ready
        organize_files(self.dir, ext_var.get(), type_var.get(), size_var.get())

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)

def start_monitoring():
    folder = path_var.get()
    if not folder or not os.path.exists(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    organize_files(folder, ext_var.get(), type_var.get(), size_var.get())

    observer = Observer()
    event_handler = FileHandler(folder)
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    messagebox.showinfo("Running", "Monitoring started. Close the window to stop.")

# GUI
root = Tk()
root.title("📁 Advanced File Organizer Bot")
root.geometry("500x300")
root.resizable(False, False)

path_var = StringVar()
ext_var = BooleanVar()
type_var = BooleanVar()
size_var = BooleanVar()

Label(root, text="Select Folder to Monitor:").pack(pady=5)
Entry(root, textvariable=path_var, width=50).pack(padx=10)
Button(root, text="📂 Browse", command=choose_folder).pack(pady=5)

Label(root, text="Sort Options:").pack(pady=5)
Checkbutton(root, text="By Extension", variable=ext_var).pack()
Checkbutton(root, text="By File Type (Image, Video, etc.)", variable=type_var).pack()
Checkbutton(root, text="By File Size", variable=size_var).pack()

Button(root, text="▶ Start Organizing and Monitoring", bg="green", fg="white", command=start_monitoring).pack(pady=15)

Label(root, text="🛑 Close this window to stop monitoring", fg="red").pack()

root.mainloop()
