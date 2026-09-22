import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading


# Function to log errors
def log_error(error_message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{error_message}\n")


# Function to handle progress
def progress_hook(d):
    if d['status'] == 'finished':
        status_label['text'] = "Download completed!"
        progress_bar['value'] = 100  # Set the progress bar to 100% when done
    elif d['status'] == 'downloading':
        percent = d['_percent_str']  # Percentage of download completed
        status_label['text'] = f"Downloading... {percent}"
        progress_bar['value'] = float(percent[:-1])  # Remove the '%' sign and convert to float


# Function to fetch available formats and ask user to select quality
def fetch_formats_and_select_quality(url, download_folder):
    ydl_opts = {'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

        # Add the 'bestvideo+bestaudio/best' option
        formats.append({
            'format': 'bestvideo+bestaudio/best',
            'ext': 'mp4',
            'resolution': 'best',
            'format_id': 'bestvideo+bestaudio/best'
        })

        # Open quality selection window only if 'bestvideo+bestaudio/best' is not selected
        if not best_video_audio_var.get():
            open_quality_window(formats, url, download_folder)
        else:
            # If 'bestvideo+bestaudio/best' is selected, skip quality selection and start download
            start_download_thread(url, download_folder, ['bestvideo+bestaudio/best'])

    except Exception as e:
        error_message = f"An error occurred: {e}"
        log_error(error_message)
        messagebox.showerror("Error", error_message)


# Function to open a window for quality selection
def open_quality_window(formats, url, download_folder):
    quality_window = tk.Toplevel(root)
    quality_window.title("Select Video Quality")

    # Set window size to 50% height and 10% width of the screen
    screen_width = quality_window.winfo_screenwidth()
    screen_height = quality_window.winfo_screenheight()
    quality_window.geometry(f"{int(screen_width * 0.1)}x{int(screen_height * 0.5)}")

    # Canvas and scrollbar for scrolling
    canvas = tk.Canvas(quality_window)
    scrollbar = tk.Scrollbar(quality_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame to hold the checkbuttons
    frame = tk.Frame(canvas)

    # Dictionary to hold the Checkbutton vars
    format_vars = {}

    # Add all formats to the frame as checkbuttons (initially no selection)
    for idx, f in enumerate(formats):
        resolution = f.get('resolution', 'N/A')
        format_desc = f"{f['format']} - {resolution} - {f['ext']}"
        var = tk.BooleanVar()
        format_vars[f['format_id']] = var
        tk.Checkbutton(frame, text=format_desc, variable=var).grid(row=idx, column=0, padx=10, pady=5, sticky="w")

    # Configure canvas scroll region
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Bind mouse wheel scroll for canvas
    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Place the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Download button for the selected quality
    def start_download_for_selected_quality():
        selected_formats = [f for f, var in format_vars.items() if var.get()]

        if not selected_formats:
            messagebox.showerror("Error", "Please select at least one video quality.")
            return

        # Close the quality window
        quality_window.destroy()

        # Start the download with the selected formats
        start_download_thread(url, download_folder, selected_formats)

    tk.Button(quality_window, text="Download", command=start_download_for_selected_quality).pack(pady=10)

    # Ensure the download button is re-enabled if the quality window is closed (e.g., user cancels)
    def on_close():
        download_button.config(state=tk.NORMAL)  # Re-enable the download button
        quality_window.destroy()  # Close the quality window

    quality_window.protocol("WM_DELETE_WINDOW", on_close)


# Function to handle the download process in a separate thread
def start_download_thread(url, download_folder, selected_formats):
    # Disable download button while downloading
    download_button.config(state=tk.DISABLED)

    ydl_opts = {
        'format': '+'.join(selected_formats),  # Use the selected formats, joined by '+'
        'outtmpl': f"{download_folder}/%(title)s.%(ext)s",
        'progress_hooks': [progress_hook],
        'noplaylist': False if playlist_var.get() else True,  # Handle playlists
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        error_message = f"An error occurred: {e}"
        log_error(error_message)
        messagebox.showerror("Error", error_message)
    finally:
        # Enable download button after download is complete
        download_button.config(state=tk.NORMAL)


# Function to browse for folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)


# Function to start the process
def start_download():
    url = url_entry.get()
    download_folder = folder_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    if not download_folder:
        messagebox.showerror("Error", "Please select a download folder.")
        return

    # Disable download button while processing
    download_button.config(state=tk.DISABLED)

    # Fetch formats and let user select quality
    fetch_formats_and_select_quality(url, download_folder)


# Create the GUI
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL Input
tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# 'Best Quality' Option - Checked by default
best_video_audio_var = tk.BooleanVar(value=True)  # Default checked
best_video_audio_check = tk.Checkbutton(root, text="Best Quality", variable=best_video_audio_var)
best_video_audio_check.grid(row=0, column=2, padx=10, pady=5)

# Folder Selection
tk.Label(root, text="Download Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=10, pady=5)

# Playlist Option
playlist_var = tk.BooleanVar()
playlist_check = tk.Checkbutton(root, text="Download Playlist", variable=playlist_var)
playlist_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Status Label
status_label = tk.Label(root, text="Status: Waiting...", fg="blue")
status_label.grid(row=3, column=0, columnspan=3, pady=10)

# Download Button
download_button = tk.Button(root, text="Download", command=start_download, bg="green", fg="white")
download_button.grid(row=4, column=1, pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Run the GUI
root.mainloop()
