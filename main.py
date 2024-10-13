import cv2
import pyautogui
import time
import keyboard
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
import json
import os

base_dir = os.path.dirname(__file__)
image_dir = os.path.join(base_dir, "images")  # Create a path for the images folder

images = {
    "start": os.path.join(image_dir, "start.png"),
    "jett": os.path.join(image_dir, "jett_icon.png"),
    "reyna": os.path.join(image_dir, "reyna_icon.png"),
    "clove": os.path.join(image_dir, "clove_icon.png"),
    "fade": os.path.join(image_dir, "fade_icon.png"),
    "brimstone": os.path.join(image_dir, "brimstone_icon.png"),
    "raze": os.path.join(image_dir, "raze_icon.png"),
    "omen": os.path.join(image_dir, "omen_icon.png"),
    "neon": os.path.join(image_dir, "neon_icon.png"),
    "yoru": os.path.join(image_dir, "yoru_icon.png"),
    "viper": os.path.join(image_dir, "viper_icon.png"),
    "skye": os.path.join(image_dir, "skye_icon.png"),
    "breach": os.path.join(image_dir, "breach_icon.png"),
    "phoenix": os.path.join(image_dir, "phoenix_icon.png"),
    "vyse": os.path.join(image_dir, "vyse_icon.png"),
    "sova": os.path.join(image_dir, "sova_icon.png"),
    "sage": os.path.join(image_dir, "sage_icon.png"),
    "killjoy": os.path.join(image_dir, "killjoy_icon.png"),
    "kay/o": os.path.join(image_dir, "kayo_icon.png"),
    "astra": os.path.join(image_dir, "astra_icon.png"),
    "chamber": os.path.join(image_dir, "chamber_icon.png"),
    "gekko": os.path.join(image_dir, "gekko_icon.png"),
    "cypher": os.path.join(image_dir, "cypher_icon.png"),
    "harbor": os.path.join(image_dir, "harbor_icon.png"),
    "deadlock": os.path.join(image_dir, "deadlock_icon.png"),
    "iso": os.path.join(image_dir, "iso_icon.png"),
    "lock_in": os.path.join(image_dir, "lock_in.png"),
    "settings": os.path.join(image_dir, "settings_icon.png")
    
}

# File to store user settings
settings_file = 'user_settings.json'

# Load user settings from file
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            return json.load(f)
    return {"hotkey": "s", "profile": "default", "theme": "Light"}

# Save user settings to file
def save_settings(settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

# Variable to hold the chosen agent and settings
selected_agent = None
wait_before_select = 0.01  # Default wait time before selecting the agent
wait_after_select = 0.01   # Default wait time after selecting the agent
user_settings = load_settings()  # Load user settings

class AgentSelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.apply_settings()  # Apply the saved settings

    def initUI(self):
        self.setWindowTitle('Select Your Agent')
        self.setGeometry(100, 100, 600, 200)  # Initial size of the window

        layout = QtWidgets.QVBoxLayout()  # Main vertical layout

        label = QtWidgets.QLabel("Choose an agent to insta-lock:")
        layout.addWidget(label)

        # Create a grid layout for buttons to have 3 rows
        button_layout = QtWidgets.QGridLayout()

        # Create buttons for each agent
        agents = [
            "jett", "reyna", "clove", "fade", "brimstone",
            "raze", "omen", "neon", "yoru", "viper",
            "skye", "breach", "phoenix", "vyse","kay/o",
            "killjoy", "sage", "astra", "chamber", "gekko",
            "sova", "cypher", "harbor", "deadlock", "iso"
        ]

        # Add buttons to the grid layout (3 rows)
        for index, agent in enumerate(agents):
            row = index // 5  # 5 buttons per row
            col = index % 5
            button = QtWidgets.QPushButton()
            button.setIcon(QtGui.QIcon(images[agent]))
            button.setIconSize(QtCore.QSize(40, 40))  # Adjust icon size
            button.setText(agent.capitalize())
            button.setToolTip(f"Select {agent.capitalize()}")  # Tooltip for clarity
            button.setStyleSheet("text-align: left;")  # Align text to the left
            button.clicked.connect(lambda checked, agent=agent: self.set_agent(agent))
            button_layout.addWidget(button, row, col)  # Add button to grid layout

        # Settings button
        settings_button = QtWidgets.QPushButton()
        settings_button.setIcon(QtGui.QIcon(images["settings"]))  # Add your settings icon image
        settings_button.setIconSize(QtCore.QSize(30, 30))
        settings_button.clicked.connect(self.open_settings_dialog)
        button_layout.addWidget(settings_button, len(agents) // 3, 0, 1, 5)  # Span settings button across all columns in the last row

        layout.addLayout(button_layout)  # Add grid layout to main layout

        # Show the UI
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setLayout(layout)  # Set the main layout
        self.show()

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.settings_updated.connect(self.apply_settings)  # Connect signal to apply settings
        dialog.exec_()

    def set_agent(self, agent):
        global selected_agent
        selected_agent = agent
        QtWidgets.QMessageBox.information(self, "Agent Selected", f"You selected {agent.capitalize()}!")
        self.close()  # Close the GUI window after selection
        self.start_insta_lock()

    def start_insta_lock(self):
        if selected_agent:
            print(f"Press '{user_settings['hotkey']}' to start the insta-lock process...")
            keyboard.wait(user_settings['hotkey'])  # Wait for the user to press the configured hotkey
            self.automate_insta_lock()  # Start the insta-lock automation

    def find_and_click(self, image_path, action_name):
        print(f"Searching for {action_name}...")

        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        target_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        if target_image is None:
            print(f"Error: Could not load image {image_path}")
            return False

        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8  # Fixed threshold value
        if max_val >= threshold:
            h, w, _ = target_image.shape
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            pyautogui.moveTo(center)
            pyautogui.click()
            print(f"{action_name} clicked!")
            return True

        print(f"{action_name} not found, retrying...")
        return False

    def automate_insta_lock(self):
        # Step 1: Click the "Start" button
        while not self.find_and_click(images['start'], "Start Button"):
            time.sleep(wait_before_select)

        print("Game started! Waiting for agent selection...")

        # Step 2: Select the agent based on user choice
        if selected_agent:
            while not self.find_and_click(images[selected_agent], f"{selected_agent.capitalize()} Icon"):
                time.sleep(wait_before_select)

            print(f"{selected_agent.capitalize()} selected! Locking in...")

            # Step 3: Click the "Lock-in" button
            while not self.find_and_click(images['lock_in'], "Lock-in Button"):
                time.sleep(wait_after_select)

            print(f"{selected_agent.capitalize()} locked in!")
            QtWidgets.QMessageBox.information(self, "Insta-lock Complete", f"{selected_agent.capitalize()} has been locked in!")
        else:
            print("No agent selected.")

    def apply_settings(self):
        # Apply theme
        theme = user_settings.get("theme", "Light")
        if theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")

class SettingsDialog(QtWidgets.QDialog):
    settings_updated = QtCore.pyqtSignal()  # Signal to notify that settings have changed

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 250)  # Increased height for better layout

        layout = QtWidgets.QVBoxLayout()

        # Current Hotkey Display
        hotkey_label = QtWidgets.QLabel(f"Current Hotkey: {user_settings['hotkey']}")
        layout.addWidget(hotkey_label)

        # Hotkey Input
        self.hotkey_input = QtWidgets.QLineEdit(self)
        self.hotkey_input.setPlaceholderText("Enter your desired hotkey (e.g., 's')")
        layout.addWidget(self.hotkey_input)

        save_button = QtWidgets.QPushButton("Save Hotkey")
        save_button.clicked.connect(self.save_hotkey)
        layout.addWidget(save_button)

        # Group for Theme Selection
        theme_group = QtWidgets.QGroupBox("Appearance Settings")
        theme_layout = QtWidgets.QVBoxLayout()

        # Icon for Theme Selection
        theme_icon = QtWidgets.QLabel()
        theme_icon.setPixmap(QtGui.QPixmap(images["settings"]))  # Assuming you have a settings icon
        theme_icon.setFixedSize(30, 30)  # Set a fixed size for the icon

        theme_label = QtWidgets.QLabel("Select Theme:")
        theme_label.setBuddy(theme_icon)  # Associate label with icon

        theme_layout.addWidget(theme_icon)
        theme_layout.addWidget(theme_label)

        self.theme_combo = QtWidgets.QComboBox(self)
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setCurrentText(user_settings.get("theme", "Light"))  # Default to Light
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(self.theme_combo)

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        save_button = QtWidgets.QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)


    def save_hotkey(self):
        new_hotkey = self.hotkey_input.text().strip()
        if new_hotkey:
            user_settings['hotkey'] = new_hotkey
            save_settings(user_settings)  # Save settings to file
            QtWidgets.QMessageBox.information(self, "Success", "Hotkey saved!")

    def change_theme(self, theme):
        user_settings['theme'] = theme
        self.settings_updated.emit()  # Emit signal to update the main window

    def save_settings(self):
        save_settings(user_settings)  # Save settings to file
        QtWidgets.QMessageBox.information(self, "Success", "Settings saved!")

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = AgentSelector()
    sys.exit(app.exec_())
