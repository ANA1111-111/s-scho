import os
import sys
import requests
import hashlib
import time
import mimetypes
from PyQt5.QtCore import QUrl, Qt, QStandardPaths
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                            QWidget, QToolBar, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings

# Configuration for self-updating
GITHUB_RAW_URL = "https://raw.githubusercontent.com/ANA1111-111/s-scho/main/aa.py"
CHECK_INTERVAL = 3600  # Check for updates every hour (in seconds)
CURRENT_SCRIPT = os.path.abspath(__file__)

# Embedded HTML files with Tailwind support
HTML_FILES = {
    "Dashboard.html": """...""",  # Keep your existing Dashboard.html content
    "Student.html": """...""",    # Keep your existing Student.html content
    "Teacher.html": """..."""     # Keep your existing Teacher.html content
}

class StudentManagementBrowser(QMainWindow):
    def __init__(self, initial_page="Dashboard.html"):
        super().__init__()
        self.setWindowTitle("Smart School - Student Management System")
        mimetypes.init()
        
        # Initialize update checker
        self.last_update_check = 0
        self.update_timer = self.startTimer(60000)  # Check every minute
        
        # Configure web engine settings
        self.browser = QWebEngineView()
        self.profile = QWebEngineProfile.defaultProfile()
        
        # Enable localStorage and other features
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        
        # Set initial zoom to 135%
        self.zoom_factor = 1.35
        self.browser.setZoomFactor(self.zoom_factor)
        
        # Create empty toolbar (just for spacing if needed)
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins
        layout.setSpacing(0)  # Remove spacing
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Connect signals
        self.browser.urlChanged.connect(self.handle_url_changed)
        self.browser.loadFinished.connect(self.apply_zoom)  # Apply zoom after page loads
        
        # Start with the initial page
        self.load_page(initial_page)
        
        # Show maximized by default
        self.showMaximized()
    
    def timerEvent(self, event):
        """Handle timer events for update checking"""
        current_time = time.time()
        if current_time - self.last_update_check > CHECK_INTERVAL:
            self.last_update_check = current_time
            self.check_for_updates()
    
    def check_for_updates(self):
        """Check for updates from GitHub"""
        if self.is_update_available():
            reply = QMessageBox.question(
                self, 'Update Available',
                'A new version is available. Would you like to update now?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.update_script():
                    QMessageBox.information(
                        self, 'Update Complete',
                        'The application will now restart to apply the update.'
                    )
                    self.restart_application()
    
    def is_update_available(self):
        """Check if a newer version exists on GitHub"""
        try:
            with open(CURRENT_SCRIPT, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            remote_content = self.get_remote_script()
            if remote_content is None:
                return False
            
            return self.get_file_hash(current_content) != self.get_file_hash(remote_content)
        except Exception as e:
            print(f"Error checking for updates: {str(e)}")
            return False
    
    def get_remote_script(self):
        """Fetch the remote script from GitHub"""
        try:
            response = requests.get(GITHUB_RAW_URL)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching remote script: {str(e)}")
            return None
    
    def get_file_hash(self, content):
        """Calculate SHA-256 hash of file content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def update_script(self):
        """Update the script directly without backups"""
        try:
            remote_content = self.get_remote_script()
            if remote_content is None:
                return False
            
            # Verify the content looks like Python code (basic safety check)
            if not remote_content.strip().startswith(("import ", "from ", "#", "\"\"\"", "'''")):
                raise ValueError("Downloaded content doesn't appear to be valid Python code")
            
            # Write directly to current file
            with open(CURRENT_SCRIPT, 'w', encoding='utf-8') as f:
                f.write(remote_content)
            
            return True
        except Exception as e:
            print(f"Update failed: {str(e)}")
            return False
    
    def restart_application(self):
        """Restart the application"""
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    def load_page(self, page_name):
        """Load HTML content from embedded strings"""
        if page_name in HTML_FILES:
            # Set a base URL to allow external resources to load
            base_url = QUrl.fromLocalFile(os.path.abspath("."))
            self.browser.setHtml(HTML_FILES[page_name], base_url)
            self.current_page = page_name
        else:
            self.browser.setHtml("<h1>Error: Page not found</h1>")
    
    def handle_url_changed(self, url):
        """Handle URL changes from the web view"""
        # Extract the filename from the URL
        filename = url.fileName()
        if filename in HTML_FILES:
            self.load_page(filename)
    
    def apply_zoom(self):
        """Apply the zoom factor after page loads"""
        self.browser.setZoomFactor(self.zoom_factor)

if __name__ == "__main__":
    # Check for updates on startup
    def is_update_available():
        try:
            with open(CURRENT_SCRIPT, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            remote_content = requests.get(GITHUB_RAW_URL).text
            return hashlib.sha256(current_content.encode('utf-8')).hexdigest() != \
                   hashlib.sha256(remote_content.encode('utf-8')).hexdigest()
        except:
            return False
    
    # If update is available on startup, apply it immediately
    if is_update_available():
        app = QApplication(sys.argv)
        reply = QMessageBox.question(
            None, 'Update Available',
            'A new version is available. Would you like to update now?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                remote_content = requests.get(GITHUB_RAW_URL).text
                with open(CURRENT_SCRIPT, 'w', encoding='utf-8') as f:
                    f.write(remote_content)
                python = sys.executable
                os.execl(python, python, *sys.argv)
            except Exception as e:
                QMessageBox.critical(
                    None, 'Update Failed',
                    f'Failed to apply update: {str(e)}'
                )
    
    # Run the application
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    browser = StudentManagementBrowser()
    browser.show()
    sys.exit(app.exec_())
