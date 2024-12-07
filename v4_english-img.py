import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import os
from collections import OrderedDict
import sys

def load_json(file_path):
    """Load a JSON file in UTF-8 with error handling."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file, object_pairs_hook=OrderedDict)  # Use OrderedDict to preserve order
    except json.JSONDecodeError as e:
        messagebox.showerror("JSON Error", f"Error in file {file_path}:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error while reading {file_path}:\n{e}")
    return OrderedDict()


def save_json(data, file_path):
    """Save a JSON file in UTF-8."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"Error while saving {file_path}: {e}")


def merge_json_files(modify_folders, output_folder):
    """Merge JSON files from multiple folders while preserving the order of additions."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create a dictionary for merged files
    merged_count = 0
    for file_name in os.listdir(modify_folders[0]):
        # Assume the folders contain the same files
        if os.path.isfile(os.path.join(modify_folders[0], file_name)):
            merged_data = OrderedDict()  # Use OrderedDict to preserve order

            # Load and merge data
            for folder in modify_folders:
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    data = load_json(file_path)
                    # Merge the data
                    for key, value in data.items():
                        merged_data[key] = value  # Add the key-value pair to the end

            # Save the merged file
            output_path = os.path.join(output_folder, file_name)
            save_json(merged_data, output_path)
            merged_count += 1

    messagebox.showinfo("Success", f"Merge completed! {merged_count} files created in {output_folder}.")


def select_folders(folders_list_var):
    """Select multiple folders for input files."""
    folders = []
    while True:
        folder = filedialog.askdirectory(title="Select a folder")
        if folder:
            folders.append(folder)
            response = messagebox.askyesno("Add another folder?", "Would you like to add another folder?")
            if not response:
                break
        else:
            break
    folders_list_var.set(folders)


def select_output_folder():
    """Select the output folder."""
    folder = filedialog.askdirectory()
    if folder:
        output_folder_var.set(folder)


def start_merge():
    """Start merging after validation."""
    modify_folders = folders_list_var.get()
    output_folder = output_folder_var.get()

    if not modify_folders or not output_folder:
        messagebox.showerror("Error", "Please select the folders and the output folder.")
        return

    merge_json_files(modify_folders, output_folder)


# Main interface
root = tk.Tk()
root.title("Automatic JSON File Merger")

# The window adjusts automatically to its content
root.resizable(False, False)  # The size won't be manually resizable
root.geometry('')  # Let the window adjust automatically

# Load and display the header image
try:
    # Handle the image path depending on whether we're running from a .exe or directly
    if getattr(sys, 'frozen', False):
        # If running as a packaged .exe
        image_path = os.path.join(sys._MEIPASS, 'header.jpg')
    else:
        # If running from the source code
        image_path = 'header.jpg'

    header_image = Image.open(image_path)  # Load the image
    header_image = header_image.resize((500, 188))  # Resize for the interface
    header_photo = ImageTk.PhotoImage(header_image)
    header_label = tk.Label(root, image=header_photo)
    header_label.pack(pady=10)  # Add some space around the image

except Exception as e:
    messagebox.showerror("Image Error", f"Could not load header.jpg:\n{e}")

# Variables to store the folder paths
folders_list_var = tk.Variable(value=[])
output_folder_var = tk.StringVar()

# Interface
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# Create widgets in a compact interface
tk.Label(frame, text="Folders with files to modify:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
tk.Entry(frame, textvariable=folders_list_var, width=40).grid(row=0, column=1, padx=10)
tk.Button(frame, text="Browse", command=lambda: select_folders(folders_list_var)).grid(row=0, column=2)

tk.Label(frame, text="Output folder:", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame, textvariable=output_folder_var, width=40).grid(row=1, column=1, padx=10)
tk.Button(frame, text="Browse", command=select_output_folder).grid(row=1, column=2)

tk.Button(frame, text="Start merging", command=start_merge, bg="green", fg="white").grid(row=2, column=0, columnspan=3, pady=20)

# Start the application
root.mainloop()
