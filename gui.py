#!/usr/bin/env python3
"""
Generic Video Downloader - GUI Version with Multi-Download Support
A PySide6 GUI application to download multiple videos simultaneously from various sites.
"""

import os
import sys
import shutil
import subprocess
import time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar,
    QTextEdit, QFileDialog, QGroupBox, QMessageBox, QCheckBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont, QColor
import socket
import json

from downloader import DownloadConfig, download_video
from server import HTTPServerThread, ExtensionRequestHandler

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return False  # Port is free
        except socket.error:
            return True  # Port is in use

def is_facebook_url(url):
    """Check if the URL is a Facebook URL."""
    return "facebook.com" in url.lower() or "fb.watch" in url.lower()


class DownloadThread(QThread):
    """Thread to handle video download without freezing the UI"""
    progress_update = Signal(str, dict)
    download_complete = Signal(str, str)
    download_error = Signal(str, str)
    video_info = Signal(str, dict)


    def __init__(self, download_id, config, platform="generic"):
        super().__init__()
        self.download_id = download_id
        self.config = config
        self.platform = platform

    def progress_hook(self, d):
        self.progress_update.emit(self.download_id, d)

    def run(self):
        """Download the video in a separate thread"""
        try:
            info = download_video(self.config, self.progress_hook)

            print("[Thread] Info object received:", info) # Add this line for debugging

            if info is None:
                raise Exception("The download function returned None. The video may have failed to process.")

            self.video_info.emit(self.download_id, info)
            self.download_complete.emit(self.download_id, "Download completed successfully!")

        except Exception as e:
            import traceback
            error_msg = str(e) if str(e) else "Unknown error occurred"
            print(f"""
{'='*70}
Download Error for {self.download_id}:
{'='*70}
""")
            traceback.print_exc()
            print(f"""
{'='*70}
""")
            self.download_error.emit(self.download_id, error_msg)


class DownloadItem:
    """Represents a single download item"""
    def __init__(self, url, quality, output_path, audio_only, download_playlist, platform="generic"):
        self.url = url
        self.quality = quality
        self.output_path = output_path
        self.audio_only = audio_only
        self.download_playlist = download_playlist
        self.platform = platform
        self.status = "Queued"
        self.progress = 0
        self.thread = None
        self.title = "Unknown"
        self.speed = "N/A"
        self.eta = "N/A"

    def to_dict(self):
        return {
            "url": self.url,
            "quality": self.quality,
            "output_path": self.output_path,
            "audio_only": self.audio_only,
            "download_playlist": self.download_playlist,
            "platform": self.platform,
            "status": self.status,
            "progress": self.progress,
            "title": self.title,
            "speed": self.speed,
            "eta": self.eta,
        }

    @classmethod
    def from_dict(cls, data):
        item = cls(
            data["url"],
            data["quality"],
            data["output_path"],
            data["audio_only"],
            data["download_playlist"],
            data["platform"],
        )
        item.status = data.get("status", "Queued")
        item.progress = data.get("progress", 0)
        item.title = data.get("title", "Unknown")
        item.speed = data.get("speed", "N/A")
        item.eta = data.get("eta", "N/A")
        return item


class VideoDownloaderGUI(QMainWindow):
    """Main GUI window for the video downloader"""
    extension_download_signal = Signal(str, str, bool)

    def __init__(self):
        super().__init__()
        self.downloads = {}
        self.download_counter = 0
        self.http_server = None
        self.bgutil_process = None
        self.extension_download_signal.connect(self.add_download_from_extension)
        ExtensionRequestHandler.app_instance = self
        self.init_ui()
        self.load_state()  # Load state at startup
        self.start_bgutil_server()
        self.start_http_server()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Video Downloader")
        self.setMinimumSize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Video Downloader")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        url_group = QGroupBox("Add Download")
        url_layout = QVBoxLayout()

        url_input_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        url_label.setFixedWidth(80)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL here...")
        self.url_input.setMinimumHeight(35)
        url_input_layout.addWidget(url_label)
        url_input_layout.addWidget(self.url_input)
        url_layout.addLayout(url_input_layout)

        settings_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setFixedWidth(80)
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Best Quality", "8K (UHD)", "4K (UHD)", "1080p (Full HD)",
            "720p (HD)", "480p (SD)", "360p", "Audio Only (MP3)"
        ])
        self.quality_combo.setFixedHeight(28)
        self.quality_combo.currentTextChanged.connect(self.update_output_path)
        settings_layout.addWidget(quality_label)
        settings_layout.addWidget(self.quality_combo, 1)

        self.playlist_checkbox = QCheckBox("Download playlist")
        self.playlist_checkbox.setChecked(False)
        settings_layout.addWidget(self.playlist_checkbox)

        self.auto_start_checkbox = QCheckBox("Auto-start download")
        self.auto_start_checkbox.setChecked(True)
        settings_layout.addWidget(self.auto_start_checkbox)
        url_layout.addLayout(settings_layout)

        folder_layout = QHBoxLayout()
        folder_label = QLabel("Save to:")
        folder_label.setFixedWidth(80)
        self.folder_input = QLineEdit()
        self.folder_input.setText(os.path.join(os.getcwd(), "downloads", "video"))
        self.folder_input.setFixedHeight(28)
        self.browse_button = QPushButton("Browse...")
        self.browse_button.setFixedHeight(28)
        self.browse_button.setFixedWidth(90)
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.browse_button)
        url_layout.addLayout(folder_layout)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        self.add_button = QPushButton("Add to Queue")
        self.add_button.setMinimumHeight(35)
        self.add_button.setMinimumWidth(150)
        button_font = QFont()
        button_font.setPointSize(10)
        button_font.setBold(True)
        self.add_button.setFont(button_font)
        self.add_button.clicked.connect(self.add_download)
        self.add_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; } QPushButton:hover { background-color: #45a049; }")
        add_button_layout.addWidget(self.add_button)
        url_layout.addLayout(add_button_layout)
        url_group.setLayout(url_layout)
        main_layout.addWidget(url_group)

        downloads_group = QGroupBox("Downloads")
        downloads_layout = QVBoxLayout()
        self.downloads_table = QTableWidget()
        self.downloads_table.setColumnCount(7)
        self.downloads_table.setHorizontalHeaderLabels(["Title", "URL", "Quality", "Progress", "Speed", "Status", "Actions"])
        self.downloads_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.downloads_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.downloads_table.setColumnWidth(2, 100)
        self.downloads_table.setColumnWidth(3, 150)
        self.downloads_table.setColumnWidth(4, 80)
        self.downloads_table.setColumnWidth(5, 100)
        self.downloads_table.setColumnWidth(6, 120)
        self.downloads_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.downloads_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.downloads_table.verticalHeader().setVisible(False)
        downloads_layout.addWidget(self.downloads_table)

        control_layout = QHBoxLayout()
        self.start_all_button = QPushButton("Start All")
        self.start_all_button.setMinimumHeight(35)
        self.start_all_button.clicked.connect(self.start_all_downloads)
        self.start_all_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; border-radius: 5px; } QPushButton:hover { background-color: #0b7dda; }")
        self.stop_all_button = QPushButton("Stop All")
        self.stop_all_button.setMinimumHeight(35)
        self.stop_all_button.clicked.connect(self.stop_all_downloads)
        self.stop_all_button.setStyleSheet("QPushButton { background-color: #ff9800; color: white; border-radius: 5px; } QPushButton:hover { background-color: #e68900; }")
        self.clear_completed_button = QPushButton("Clear Completed")
        self.clear_completed_button.setMinimumHeight(35)
        self.clear_completed_button.clicked.connect(self.clear_completed)
        self.clear_completed_button.setStyleSheet("QPushButton { background-color: #9E9E9E; color: white; border-radius: 5px; } QPushButton:hover { background-color: #757575; }")
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.setMinimumHeight(35)
        self.clear_all_button.clicked.connect(self.clear_all)
        self.clear_all_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; border-radius: 5px; } QPushButton:hover { background-color: #da190b; }")

        self.open_folder_button = QPushButton("Open Download Folder")
        self.open_folder_button.setMinimumHeight(35)
        self.open_folder_button.clicked.connect(self.open_download_folder)
        self.open_folder_button.setStyleSheet("QPushButton { background-color: #607D8B; color: white; border-radius: 5px; } QPushButton:hover { background-color: #455A64; }")

        control_layout.addWidget(self.start_all_button)
        control_layout.addWidget(self.stop_all_button)
        control_layout.addWidget(self.clear_completed_button)
        control_layout.addWidget(self.clear_all_button)
        control_layout.addWidget(self.open_folder_button) # Add the new button
        downloads_layout.addLayout(control_layout)
        downloads_group.setLayout(downloads_layout)
        main_layout.addWidget(downloads_group)

        log_group = QGroupBox("Status Log")
        log_layout = QVBoxLayout()
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(120)
        log_layout.addWidget(self.log_display)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        self.log("Ready to download videos!")

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.folder_input.text())
        if folder:
            self.folder_input.setText(folder)
            self.log(f"Output folder set to: {folder}")

    def update_output_path(self, quality_text):
        base_path = os.path.join(os.getcwd(), "downloads")
        new_path = os.path.join(base_path, "audio") if "Audio Only" in quality_text else os.path.join(base_path, "video")
        self.folder_input.setText(new_path)

    def log(self, message):
        self.log_display.append(message)
        self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())

    def add_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a video URL!")
            return

        platform = "facebook" if is_facebook_url(url) else "generic"
        output_path = self.folder_input.text().strip() or os.path.join(os.getcwd(), "downloads")
        quality_text = self.quality_combo.currentText()
        audio_only = "Audio Only" in quality_text
        quality = "Audio Only" if audio_only else quality_text.split(" ")[0]
        download_playlist = self.playlist_checkbox.isChecked()

        download_id = f"download_{self.download_counter}"
        self.download_counter += 1
        item = DownloadItem(url, quality, output_path, audio_only, download_playlist, platform=platform)
        self.downloads[download_id] = item
        self.add_download_to_table(download_id, item)

        platform_name = "Facebook" if platform == "facebook" else "Generic"
        self.log(f"Added to queue ({platform_name}): {url[:50]}...")
        if self.auto_start_checkbox.isChecked():
            self.start_download(download_id)
        self.url_input.clear()

    def add_download_to_table(self, download_id, item):
        row = self.downloads_table.rowCount()
        self.downloads_table.insertRow(row)
        self.downloads_table.setItem(row, 0, QTableWidgetItem(item.title))
        url_display = item.url[:40] + "..." if len(item.url) > 40 else item.url
        url_item = QTableWidgetItem(url_display)
        url_item.setToolTip(item.url)
        self.downloads_table.setItem(row, 1, url_item)
        self.downloads_table.setItem(row, 2, QTableWidgetItem(item.quality))
        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setTextVisible(True)
        self.downloads_table.setCellWidget(row, 3, progress_bar)
        self.downloads_table.setItem(row, 4, QTableWidgetItem(item.speed))
        self.downloads_table.setItem(row, 5, QTableWidgetItem(item.status))

        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(2, 2, 2, 2)
        start_btn = QPushButton("Start")
        start_btn.clicked.connect(lambda _, did=download_id: self.start_download(did))
        start_btn.setMaximumHeight(25)
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda _, did=download_id: self.remove_download(did))
        remove_btn.setMaximumHeight(25)
        action_layout.addWidget(start_btn)
        action_layout.addWidget(remove_btn)
        self.downloads_table.setCellWidget(row, 6, action_widget)

    def get_download_row(self, download_id):
        for row in range(self.downloads_table.rowCount()):
            url_item = self.downloads_table.item(row, 1)
            if url_item and download_id in self.downloads and url_item.toolTip() == self.downloads[download_id].url:
                return row
        return -1

    def start_download(self, download_id):
        if download_id not in self.downloads:
            return
        item = self.downloads[download_id]
        if item.thread and item.thread.isRunning():
            self.log(f"Download already in progress: {item.url[:50]}...")
            return

        item.status = "Starting..."
        row = self.get_download_row(download_id)
        if row >= 0:
            self.downloads_table.item(row, 5).setText(item.status)

        platform_name = "Facebook" if item.platform == "facebook" else "Generic"
        self.log(f"Starting download ({platform_name}): {item.url[:50]}...")

        config = DownloadConfig(url=item.url, output_path=item.output_path, quality=item.quality, audio_only=item.audio_only, download_playlist=item.download_playlist, platform=item.platform)

        thread = DownloadThread(download_id, config, item.platform)
        thread.progress_update.connect(self.update_download_progress)
        thread.download_complete.connect(self.download_finished)
        thread.download_error.connect(self.download_failed)
        thread.video_info.connect(self.update_video_info)
        thread.start()
        item.thread = thread
        item.status = "Downloading"

    def start_all_downloads(self):
        started = sum(1 for item in self.downloads.values() if item.status in ["Queued", "Failed"] and not (self.start_download(next(did for did, d in self.downloads.items() if d is item)) is None))
        self.log(f"Started {started} download(s)" if started > 0 else "No queued downloads to start")

    def stop_all_downloads(self):
        stopped = 0
        for download_id, item in self.downloads.items():
            if item.thread and item.thread.isRunning():
                item.thread.terminate()
                item.thread.wait()
                item.status = "Stopped"
                row = self.get_download_row(download_id)
                if row >= 0:
                    self.downloads_table.item(row, 5).setText(item.status)
                stopped += 1
        if stopped > 0:
            self.log(f"Stopped {stopped} download(s)")

    def remove_download(self, download_id):
        if download_id in self.downloads:
            item = self.downloads[download_id]
            if item.thread and item.thread.isRunning():
                item.thread.terminate()
                item.thread.wait()
            row = self.get_download_row(download_id)
            if row >= 0:
                self.downloads_table.removeRow(row)
            del self.downloads[download_id]
            self.log(f"Removed download: {item.url[:50]}...")

    def clear_completed(self):
        to_remove = [did for did, item in self.downloads.items() if item.status in ["Completed", "Failed"]]
        for did in to_remove:
            self.remove_download(did)
        if to_remove:
            self.log(f"Cleared {len(to_remove)} completed download(s)")

    def clear_all(self):
        if QMessageBox.question(self, "Clear All", "Are you sure you want to clear all downloads?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.stop_all_downloads()
            for did in list(self.downloads.keys()):
                self.remove_download(did)
            self.log("Cleared all downloads")

    def open_download_folder(self):
        folder_path = self.folder_input.text()
        if not folder_path:
            QMessageBox.warning(self, "No Folder Selected", "Please select a download folder first.")
            return

        if not os.path.exists(folder_path):
            QMessageBox.warning(self, "Folder Not Found", f"The folder '{folder_path}' does not exist.")
            return

        try:
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux and other Unix-like systems
                subprocess.Popen(["xdg-open", folder_path])
            self.log(f"Opened download folder: {folder_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error Opening Folder", f"Could not open folder '{folder_path}': {e}")
            self.log(f"Error opening download folder '{folder_path}': {e}")

    def update_download_progress(self, download_id, d):
        if download_id in self.downloads:
            item = self.downloads[download_id]
            row = self.get_download_row(download_id)
            if row < 0: return

            if d['status'] == 'downloading':
                percent_str = d.get('_percent_str', '0%').strip()
                try:
                    percent = float(percent_str.replace('%', ''))
                    item.progress = int(percent)
                    progress_bar = self.downloads_table.cellWidget(row, 3)
                    if progress_bar:
                        progress_bar.setValue(item.progress)
                    item.speed = d.get('_speed_str', 'N/A')
                    self.downloads_table.item(row, 4).setText(item.speed)
                    item.eta = d.get('_eta_str', 'N/A')
                    item.status = f"Downloading ({percent_str})"
                    self.downloads_table.item(row, 5).setText(item.status)
                except ValueError: pass
            elif d['status'] == 'finished':
                item.progress = 100
                item.status = "Processing..."
                progress_bar = self.downloads_table.cellWidget(row, 3)
                if progress_bar:
                    progress_bar.setValue(100)
                self.downloads_table.item(row, 5).setText(item.status)

    def update_video_info(self, download_id, info):
        if download_id in self.downloads:
            item = self.downloads[download_id]
            item.title = info.get('title', 'Unknown')
            row = self.get_download_row(download_id)
            if row >= 0:
                self.downloads_table.item(row, 0).setText(item.title)

    def download_finished(self, download_id, message):
        if download_id in self.downloads:
            item = self.downloads[download_id]
            item.status = "Completed"
            item.progress = 100
            row = self.get_download_row(download_id)
            if row >= 0:
                self.downloads_table.item(row, 5).setText(item.status)
                self.downloads_table.item(row, 5).setBackground(QColor(76, 175, 80, 100))
            self.log(f"Completed: {item.title}")

    def download_failed(self, download_id, error_message):
        if download_id in self.downloads:
            item = self.downloads[download_id]
            item.status = "Failed"
            row = self.get_download_row(download_id)
            if row >= 0:
                self.downloads_table.item(row, 5).setText(item.status)
                self.downloads_table.item(row, 5).setBackground(QColor(244, 67, 54, 100))
            first_line = error_message.split('\n')[0] if error_message else "Unknown error"
            self.log(f"Failed: {item.url[:50]}... - {first_line}")

    def start_bgutil_server(self):
        po_token_port = 4416
        if is_port_in_use(po_token_port):
            QMessageBox.warning(self, "Port in Use",
                                f"Port {po_token_port} is already in use. Please close the application or process using this port and restart the downloader.")
            self.log(f"Failed to start PO Token server: Port {po_token_port} is already in use.")
            return

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bgutil_server_path = os.path.join(script_dir, 'bgutil-ytdlp-pot-provider', 'server', 'build', 'main.js')
            nodejs_path = os.path.join(script_dir, 'nodejs', 'node-v25.2.1-win-x64', 'node.exe')
            if not os.path.exists(bgutil_server_path) or not os.path.exists(nodejs_path):
                print("[bgutil] PO Token server or Node.js not found.")
                self.log("[bgutil] PO Token server or Node.js not found.")
                return
            print("[bgutil] Starting PO Token server...")
            self.log("[bgutil] Starting PO Token server...")
            self.bgutil_process = subprocess.Popen([nodejs_path, bgutil_server_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            time.sleep(2) # Give the server a moment to start and produce output

            if self.bgutil_process.poll() is None:
                # If the process is still running after the delay, consider it started
                print(f"[bgutil] PO Token server started successfully on port {po_token_port}")
                self.log(f"[bgutil] PO Token server started successfully on port {po_token_port}")
            else:
                # Process terminated within the delay, read its output for error messages
                stdout, stderr = self.bgutil_process.communicate()
                print(f"[bgutil] stdout: {stdout.decode(errors='ignore')}")
                print(f"[bgutil] stderr: {stderr.decode(errors='ignore')}")
                print("[bgutil] PO Token server failed to start (exited immediately)")
                self.log("[bgutil] PO Token server failed to start (exited immediately)")
                self.bgutil_process = None
        except Exception as e:
            print(f"[bgutil] Failed to start PO Token server: {e}")
            self.log(f"[bgutil] Failed to start PO Token server: {e}")
            self.bgutil_process = None

    def start_http_server(self):
        self.http_server = HTTPServerThread(app_instance=self, port=8765)
        self.http_server.start()
        self.log("HTTP server started on port 8765 - ready for Chrome extension")

    def handle_extension_download(self, url, quality, download_playlist):
        self.extension_download_signal.emit(url, quality, download_playlist)

    def add_download_from_extension(self, url, quality, download_playlist):
        self.log(f"Received from extension: {url[:50]}...")
        self.url_input.setText(url)
        quality_map = {'best': 'Best Quality', '1080p': '1080p (Full HD)', '720p': '720p (HD)', '480p': '480p (SD)', '360p': '360p', 'audio': 'Audio Only (MP3)'}
        combo_quality = quality_map.get(quality, '720p (HD)')
        index = self.quality_combo.findText(combo_quality)
        if index >= 0:
            self.quality_combo.setCurrentIndex(index)
        self.playlist_checkbox.setChecked(download_playlist)
        original_auto_start = self.auto_start_checkbox.isChecked()
        self.auto_start_checkbox.setChecked(True)
        self.add_download()
        self.auto_start_checkbox.setChecked(original_auto_start)

    def get_state_file_path(self):
        return os.path.join(os.getcwd(), "status.json")

    def save_state(self):
        state_file = self.get_state_file_path()
        try:
            serializable_downloads = {
                did: item.to_dict()
                for did, item in self.downloads.items()
            }
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_downloads, f, indent=4)
            self.log(f"Application state saved to {state_file}")
        except Exception as e:
            self.log(f"Error saving application state: {e}")

    def load_state(self):
        state_file = self.get_state_file_path()
        if not os.path.exists(state_file):
            self.log("No saved state found.")
            return

        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                loaded_downloads = json.load(f)

            if not isinstance(loaded_downloads, dict):
                raise ValueError("Loaded state is not a dictionary.")

            max_download_counter = 0
            for download_id, data in loaded_downloads.items():
                try:
                    item = DownloadItem.from_dict(data)
                    self.downloads[download_id] = item
                    self.add_download_to_table(download_id, item)
                    # Update max_download_counter based on existing IDs
                    try:
                        counter_val = int(download_id.split('_')[1])
                        if counter_val > max_download_counter:
                            max_download_counter = counter_val
                    except (ValueError, IndexError):
                        pass # Ignore malformed IDs
                except Exception as item_e:
                    self.log(f"Error loading download item {download_id}: {item_e}")
            self.download_counter = max_download_counter + 1
            self.log(f"Application state loaded from {state_file}")
        except json.JSONDecodeError as e:
            self.log(f"Error decoding saved state file: {e}. File might be corrupted.")
            # Optionally, back up the corrupted file and start fresh
            # os.rename(state_file, state_file + ".bak")
        except Exception as e:
            self.log(f"Error loading application state: {e}")


    def closeEvent(self, event):
        self.stop_all_downloads()
        self.save_state()  # Save state before closing
        if self.http_server:
            self.http_server.stop()
        try:
            cache_dir = os.path.expanduser("~/.cache/yt-dlp")
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
            windows_cache = os.path.join(os.getenv('APPDATA', ''), 'yt-dlp')
            if os.path.exists(windows_cache):
                shutil.rmtree(windows_cache)
        except Exception as e:
            print(f"Error cleaning cache: {e}")
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = VideoDownloaderGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()