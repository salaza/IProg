import sys
import subprocess
import os
import glob
import json
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtGui import QKeySequence, QShortcut
from ui_form import Ui_Widget

class Widget(QWidget):
    CONFIG_FILE = "config.json"  # Path to save/load the file paths

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.current_shortcut = None  # To store the current shortcut reference

        # Load saved paths and hotkey from configuration file
        self.load_paths()

        # Only search for ipecmd automatically if the path is not already saved
        if not self.ui.IPECMDPathBox.text():
            self.find_ipecmd()

        # Connect buttons to respective functions
        self.ui.FlashButton.clicked.connect(self.flash_button_clicked)
        self.ui.BrowseMCUFile.clicked.connect(self.browse_mcu_file)
        self.ui.BrowseTelitFile.clicked.connect(self.browse_telit_file)
        self.ui.BrowserIPECMD.clicked.connect(self.browse_ipecmd)

        # Connect the hotkey setting field
        self.ui.SetFlashHotkey.keySequenceChanged.connect(self.set_hotkey)

        # Connect the AutoFlash checkbox state change to toggle the visibility of auto_label and disable flash button
        self.ui.AutoFlash.stateChanged.connect(self.toggle_auto_label_visibility)

        # Set the initial visibility of the auto_label and enable/disable flash button based on the AutoFlash checkbox state
        self.toggle_auto_label_visibility(self.ui.AutoFlash.checkState())

    def toggle_auto_label_visibility(self, state):
        """Toggle the visibility of auto_label based on the AutoFlash checkbox state and enable/disable flash button and hotkey."""
        if state == 2:  # Checked
            self.ui.auto_label.setVisible(True)
            self.ui.FlashButton.setEnabled(False)  # Disable the flash button
            if self.current_shortcut:  # Disable the hotkey if it exists
                self.current_shortcut.setEnabled(False)
        else:  # Unchecked or Partially checked
            self.ui.auto_label.setVisible(False)
            self.ui.FlashButton.setEnabled(True)  # Enable the flash button
            if self.current_shortcut:  # Enable the hotkey if it exists
                self.current_shortcut.setEnabled(True)

    def find_ipecmd(self):
        """Attempt to automatically find ipecmd.exe in the predefined directory if it's not already set."""
        search_path = r"C:\Program Files\Microchip\MPLABX\v5.50\mplab_platform\mplab_ipe"
        ipecmd_path = glob.glob(os.path.join(search_path, "**", "ipecmd.exe"), recursive=True)

        if ipecmd_path:
            # Automatically found the path, set it in the UI and save
            ipecmd_path = ipecmd_path[0]  # Use the first match found
            self.ui.IPECMDPathBox.setText(ipecmd_path)
            self.ui.DebugWindow.append(f"ipecmd.exe found at: {ipecmd_path}")
            self.save_paths()  # Save the automatically found path
        else:
            # If not found, prompt the user to manually select the path
            self.ui.DebugWindow.append("ipecmd.exe not found. Please select it manually.")

    def flash_button_clicked(self):
        # Check if the ClearDebug checkbox is checked
        if self.ui.ClearDebug.isChecked():
            # If checked, clear the debug window before starting the flashing process
            self.ui.DebugWindow.clear()

        # Get the paths from the UI fields
        ipecmd_path = self.ui.IPECMDPathBox.text()
        hex_file_path = self.ui.MCUPathBox.text()
        flash_option = self.ui.FlashChooser.currentText()  # Get the current selection in the FlashChooser

        if not ipecmd_path:
            self.ui.DebugWindow.append("Error: IPECMD path not set!")
            return

        if not hex_file_path:
            self.ui.DebugWindow.append("Error: No hex file selected!")
            return

        # Check if the selected option allows flashing the MCU
        if flash_option not in ["Beide", "Nur MCU"]:
            self.ui.DebugWindow.append("MCU flashing not selected.")
            return

        # Save the current file paths
        self.save_paths()

        # Construct the IPECMD command
        command = [
            ipecmd_path,
            '-TATATMELICE',  # Using Atmel-ICE
            '-PATSAME70N19B',
            f'-F{hex_file_path}',
            '-M',
            '-V',
            '-C',
            '-OL'
        ]

        # Run the command using subprocess
        try:
            result = subprocess.run(command, capture_output=True, text=True)

            # Check if the programming was successful
            if result.returncode == 0:
                self.ui.DebugWindow.append("Programming complete.")
            else:
                self.ui.DebugWindow.append("Programming failed.")
                self.ui.DebugWindow.append(result.stderr)
        except Exception as e:
            self.ui.DebugWindow.append(f"Error running command: {str(e)}")

    def browse_mcu_file(self):
        # Function to open file dialog for MCU Hex File
        file_path, _ = QFileDialog.getOpenFileName(self, "Select MCU Hex File", "", "HEX Files (*.hex);;All Files (*)")
        if file_path:
            self.ui.MCUPathBox.setText(file_path)
            # Save paths automatically when the file is selected
            self.save_paths()

    def browse_telit_file(self):
        # Function to open file dialog for Telit Bin File
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Telit Bin File", "", "Bin Files (*.bin);;All Files (*)")
        if file_path:
            self.ui.TelitPathBox.setText(file_path)
            # Save paths automatically when the file is selected
            self.save_paths()

    def browse_ipecmd(self):
        # Function to open file dialog for IPECMD path
        file_path, _ = QFileDialog.getOpenFileName(self, "Select IPECMD", "", "Executable Files (*.exe);;All Files (*)")
        if file_path:
            self.ui.IPECMDPathBox.setText(file_path)
            # Save paths automatically when the file is selected
            self.save_paths()

    def set_hotkey(self):
        """Set the hotkey for flashing based on user input."""
        key_sequence = self.ui.SetFlashHotkey.keySequence().toString()
        if key_sequence:
            # Remove old shortcut if it exists
            if self.current_shortcut:
                self.current_shortcut.activated.disconnect()  # Disconnect the previous action
                del self.current_shortcut  # Delete the reference to the old shortcut

            # Set a new shortcut
            self.current_shortcut = QShortcut(QKeySequence(key_sequence), self)
            self.current_shortcut.activated.connect(self.flash_button_clicked)

            # Save the hotkey in config
            self.save_paths()

            self.ui.DebugWindow.append(f"Hotkey set to: {key_sequence}")
        else:
            self.ui.DebugWindow.append("No valid hotkey set.")

    def save_paths(self):
        """Save the MCU, Telit, and IPECMD paths, and hotkey to a JSON file."""
        paths = {
            "mcu_file": self.ui.MCUPathBox.text(),
            "telit_file": self.ui.TelitPathBox.text(),
            "ipecmd_file": self.ui.IPECMDPathBox.text(),
            "hotkey": self.ui.SetFlashHotkey.keySequence().toString()  # Save the hotkey
        }
        try:
            with open(self.CONFIG_FILE, 'w') as config_file:
                json.dump(paths, config_file, indent=4)  # Use indent=4 for pretty formatting
        except Exception as e:
            self.ui.DebugWindow.append(f"Error saving paths: {str(e)}")

    def load_paths(self):
        """Load the saved MCU, Telit, IPECMD paths, and hotkey from the JSON file."""
        if not os.path.exists(self.CONFIG_FILE):
            # File doesn't exist, create it with default values
            self.save_default_paths()
        else:
            # Load the existing file
            try:
                with open(self.CONFIG_FILE, 'r') as config_file:
                    paths = json.load(config_file)
                    self.ui.MCUPathBox.setText(paths.get("mcu_file", ""))
                    self.ui.TelitPathBox.setText(paths.get("telit_file", ""))
                    self.ui.IPECMDPathBox.setText(paths.get("ipecmd_file", ""))

                    # Load and set the hotkey if available
                    hotkey = paths.get("hotkey", "")
                    if hotkey:
                        self.ui.SetFlashHotkey.setKeySequence(QKeySequence(hotkey))
                        self.set_hotkey()  # Apply the hotkey after loading it
                        self.ui.DebugWindow.append(f"Hotkey loaded: {hotkey}")
            except Exception as e:
                self.ui.DebugWindow.append(f"Error loading paths: {str(e)}")

    def save_default_paths(self):
        """Create a new configuration file with default (empty) values."""
        default_paths = {
            "mcu_file": "",
            "telit_file": "",
            "ipecmd_file": "",
            "hotkey": ""
        }
        try:
            with open(self.CONFIG_FILE, 'w') as config_file:
                json.dump(default_paths, config_file, indent=4)  # Pretty formatting with indent
            self.ui.DebugWindow.append("Default configuration created.")
        except Exception as e:
            self.ui.DebugWindow.append(f"Error creating default config: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
