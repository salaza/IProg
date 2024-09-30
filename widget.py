import sys
import os
import glob
import json
import serial
import time
import shutil
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtCore import QProcess, QTimer, QThread, Signal
from ui_form import Ui_Widget

# Create a new thread class for handling firmware verification via COM port
class FirmwareVerificationThread(QThread):
    verification_complete = Signal(bool)  # Signal to notify when verification is complete
    verification_output = Signal(str)     # Signal to emit data read from the serial port

    def __init__(self, port='COM6', baudrate=115200, timeout=20):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.running = False  # Control flag for stopping the thread if needed

    def run(self):
        """Override the run method to execute the serial verification in a separate thread."""
        self.running = True
        try:
            with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
                ser.write(b'iRc0001DF\r\n')
                start_time = time.time()
                self.verification_output.emit("Command sent to MCU.")
                while self.running and time.time() - start_time < 30:  # 30-second timeout
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').strip()
                        self.verification_output.emit(f"Read from COM6: {line}")
                        if "SW-VER: V2" in line:
                            self.verification_output.emit("Firmware verification successful!")
                            self.verification_complete.emit(True)
                            self.stop()
                            return
                self.verification_output.emit("Firmware verification failed. 'SW-VER: V2' not received.")
                self.verification_complete.emit(False)
        except serial.SerialException as e:
            self.verification_output.emit(f"Error: Unable to connect to COM6 - {str(e)}")
            self.verification_complete.emit(False)

    def stop(self):
        """Stop the verification thread."""
        self.running = False

class Widget(QWidget):
    CONFIG_FILE = "config.json"  # Path to save/load the file paths

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.current_shortcut = None  # To store the current shortcut reference
        self.counter_value = 0  # Initialize the counter

        # QProcesses for asynchronous command execution
        self.flash_process = QProcess(self)
        self.telit_process = QProcess(self)
        self.verification_thread = None  # Initialize the firmware verification thread as None

        # Connect signals to the respective slots for QProcesses
        self.flash_process.readyReadStandardOutput.connect(self.read_flash_output)
        self.flash_process.readyReadStandardError.connect(self.read_flash_error)
        self.flash_process.finished.connect(self.flash_finished)

        self.telit_process.readyReadStandardOutput.connect(self.read_telit_output)
        self.telit_process.readyReadStandardError.connect(self.read_telit_error)
        self.telit_process.finished.connect(self.telit_finished)

        # Initialize progress bar settings
        self.current_step = 0
        self.total_steps = 0

        # Load saved paths, counter value, and hotkey from configuration file
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

        # Set the counter display
        self.ui.Counter.display(self.counter_value)

    def update_progress(self, step_increment=1):
        """Update the progress bar by incrementing the step count."""
        self.current_step += step_increment
        progress_value = int((self.current_step / self.total_steps) * 100)
        self.ui.FlashProgress.setValue(progress_value)

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
        telit_file_path = self.ui.TelitPathBox.text()
        flash_option = self.ui.FlashChooser.currentText()  # Get the current selection in the FlashChooser

        if not ipecmd_path:
            self.ui.DebugWindow.append("Error: IPECMD path not set!")
            return

        # Save the current file paths
        self.save_paths()

        # Initialize progress bar
        self.current_step = 0
        if flash_option == "Beide":
            self.total_steps = 8
        elif flash_option == "Nur MCU":
            self.total_steps = 2
        elif flash_option == "Nur Telit":
            self.total_steps = 6

        self.update_progress()  # Start with initial value of 0

        # Execute the appropriate sequence based on the selection in FlashChooser
        if flash_option == "Beide":
            # Flash MCU, verify, send command, and flash Telit module
            self.flash_mcu(ipecmd_path, hex_file_path)
        elif flash_option == "Nur MCU":
            # Flash only the MCU and verify
            self.flash_mcu(ipecmd_path, hex_file_path)
        elif flash_option == "Nur Telit":
            # Send the serial command and flash the Telit module
            self.send_serial_command()

    def flash_mcu(self, ipecmd_path, hex_file_path):
        """Flash the MCU using IPECMD."""
        if not hex_file_path:
            self.ui.DebugWindow.append("Error: No hex file selected!")
            return

        # Construct the IPECMD command for MCU flashing
        command = [
                ipecmd_path,
                '-TPAICE',  # Use Atmel-ICE programmer
                '-PATSAME70N19B',  # Target device
                '-M',  # Start programming
                f'-F{hex_file_path}'  # MCU Hex file
        ]

        if self.ui.IPECMDOutput.isChecked():
            command_str = ' '.join(command)
            self.ui.DebugWindow.append(f"Executing command: {command_str}")

        self.ui.DebugWindow.append("Starting MCU flashing...")
        # Remove all folders starting with "WE310_" before starting the flash process
        self.remove_we310_folders()

        # Start the command using QProcess
        self.flash_process.start(command[0], command[1:])

    def remove_we310_folders(self):
        """Remove all folders starting with 'WE310_' in the current directory."""
        current_directory = os.getcwd()  # Get the current working directory
        #self.ui.DebugWindow.append(f"Searching for folders starting with 'WE310_' in {current_directory}...")

        # Iterate through all files and directories in the current directory
        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)
            # Check if the item is a directory and its name starts with 'WE310_'
            if os.path.isdir(item_path) and item.startswith("WE310_"):
                try:
                    # Remove the directory and its contents
                    shutil.rmtree(item_path)
                    self.ui.DebugWindow.append(f"Removed folder: {item_path}")
                except Exception as e:
                    self.ui.DebugWindow.append(f"Error removing folder {item_path}: {str(e)}")


    def read_flash_output(self):
        """Read standard output from the flash process."""
        if self.ui.IPECMDOutput.isChecked():
            output = self.flash_process.readAllStandardOutput().data().decode()
            self.ui.DebugWindow.append(output)

    def read_flash_error(self):
        """Read error output from the flash process."""
        if self.ui.IPECMDOutput.isChecked():
            error = self.flash_process.readAllStandardError().data().decode()
            self.ui.DebugWindow.append(error)

    def flash_finished(self, exit_code, exit_status):
        """Handle the flash finished signal."""
        if exit_code == 0:
            self.ui.DebugWindow.append("MCU Flash complete.")
            self.update_counter()  # Increment and update the counter after successful flash
            self.update_progress()  # Step: MCU Flash complete
            QTimer.singleShot(5000, self.send_serial_command)
            #self.start_firmware_verification()
        elif exit_code == 36:
            self.ui.DebugWindow.append("Programming failed: INVALID_CMDLINE_ARG (Code 36).")
        else:
            self.ui.DebugWindow.append(f"Programming failed with exit code {exit_code}.")

    def start_firmware_verification(self):
        """Start the firmware verification process using the verification thread."""
        self.verification_thread = FirmwareVerificationThread()
        self.verification_thread.verification_complete.connect(self.on_verification_complete)
        self.verification_thread.verification_output.connect(self.ui.DebugWindow.append)
        self.verification_thread.start()

    def on_verification_complete(self, success):
        """Handle the firmware verification completion."""
        self.update_progress()  # Step: Firmware Verification Complete
        if success:
            self.send_serial_command()
        else:
            self.ui.DebugWindow.append("Firmware verification failed. Flashing process halted.")

    def send_serial_command(self):
        """Send a serial command to the MCU and flash the Telit module if successful."""
        self.ui.DebugWindow.append("Sending serial command to MCU...")

        try:
            with serial.Serial('COM6', 115200, timeout=5) as ser:
                ser.write(b'iRc0001DF\r\n')
                self.ui.DebugWindow.append("Serial command sent.")
                self.update_progress()  # Step: Serial command sent

                # Start a QTimer to delay the Telit flashing by 1 second
                QTimer.singleShot(1000, self.flash_telit)
        except serial.SerialException as e:
            self.ui.DebugWindow.append(f"Error: Unable to send serial command - {str(e)}")

    def flash_telit(self):
        """Flash the Telit module using Telit_Wifi_Image_Tool.exe."""
        telit_tool = "Telit_Wifi_Image_Tool.exe"
        telit_file_path = self.ui.TelitPathBox.text()

        if not telit_file_path:
            self.ui.DebugWindow.append("Error: No Telit firmware file selected.")
            return

        # Construct the Telit command
        command = [
            telit_tool,
            "-m", "WE310",
            "-d", telit_file_path,
            "-c", "COM7"
        ]

        self.ui.DebugWindow.append("Starting Telit flashing...")

        # Start the command using QProcess
        self.telit_process.start(command[0], command[1:])

    def read_telit_output(self):
        """Read standard output from the Telit flashing process."""
        output = self.telit_process.readAllStandardOutput().data().decode()
        # Update progress based on specific messages received
        if "Flashing Image 1 of 4" in output:
            self.ui.DebugWindow.append("Flashing Image 1 of 4")
            self.update_progress()
        elif "Flashing Image 2 of 4" in output:
            self.ui.DebugWindow.append("Flashing Image 2 of 4")
            self.update_progress()
        elif "Flashing Image 3 of 4" in output:
            self.ui.DebugWindow.append("Flashing Image 3 of 4")
            self.update_progress()
        elif "Flashing Image 4 of 4" in output:
            self.ui.DebugWindow.append("Flashing Image 4 of 4")
            self.update_progress()

        if self.ui.TelitImageOutput.isChecked():
            self.ui.DebugWindow.append(output)


    def read_telit_error(self):
        """Read error output from the Telit flashing process."""
        if self.ui.TelitImageOutput.isChecked():
            error = self.telit_process.readAllStandardError().data().decode()
            self.ui.DebugWindow.append(error)

    def telit_finished(self, exit_code, exit_status):
        """Handle the Telit flashing finished signal."""
        if exit_code == 0:
            self.ui.DebugWindow.append("Telit module flashed successfully.")
        else:
            self.ui.DebugWindow.append(f"Telit flashing failed with exit code {exit_code}.")

    def update_counter(self):

        flash_option = self.ui.FlashChooser.currentText()
        """Increment the counter by 1 and update the display and config."""
        if flash_option == "Beide":
            self.counter_value += 1
            self.ui.Counter.display(self.counter_value)
            self.save_paths()  # Save the updated counter value

    def browse_mcu_file(self):
        """Open file dialog for MCU Hex File."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select MCU Hex File", "", "HEX Files (*.hex);;All Files (*)")
        if file_path:
            self.ui.MCUPathBox.setText(file_path)
            self.save_paths()

    def browse_telit_file(self):
        """Open file dialog for Telit Bin File."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Telit Bin File", "", "Bin Files (*.bin);;All Files (*)")
        if file_path:
            self.ui.TelitPathBox.setText(file_path)
            self.save_paths()

    def browse_ipecmd(self):
        """Open file dialog for IPECMD path."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select IPECMD", "", "Executable Files (*.exe);;All Files (*)")
        if file_path:
            self.ui.IPECMDPathBox.setText(file_path)
            self.save_paths()

    def set_hotkey(self):
        """Set the hotkey for flashing based on user input."""
        key_sequence = self.ui.SetFlashHotkey.keySequence().toString()
        if key_sequence:
            # Remove old shortcut if it exists
            if self.current_shortcut:
                self.current_shortcut.activated.disconnect()
                del self.current_shortcut

            # Set a new shortcut
            self.current_shortcut = QShortcut(QKeySequence(key_sequence), self)
            self.current_shortcut.activated.connect(self.flash_button_clicked)

            # Save the hotkey in config
            self.save_paths()
            #self.ui.DebugWindow.append(f"Hotkey set to: {key_sequence}")
        else:
            self.ui.DebugWindow.append("No valid hotkey set.")

    def save_paths(self):
        """Save the MCU, Telit, and IPECMD paths, hotkey, and counter to a JSON file."""
        paths = {
            "mcu_file": self.ui.MCUPathBox.text(),
            "telit_file": self.ui.TelitPathBox.text(),
            "ipecmd_file": self.ui.IPECMDPathBox.text(),
            "hotkey": self.ui.SetFlashHotkey.keySequence().toString(),
            "counter": self.counter_value
        }
        try:
            with open(self.CONFIG_FILE, 'w') as config_file:
                json.dump(paths, config_file, indent=4)  # Use indent=4 for pretty formatting
        except Exception as e:
            self.ui.DebugWindow.append(f"Error saving paths: {str(e)}")

    def load_paths(self):
        """Load the saved MCU, Telit, IPECMD paths, hotkey, and counter from the JSON file."""
        if not os.path.exists(self.CONFIG_FILE):
            self.save_default_paths()
        else:
            try:
                with open(self.CONFIG_FILE, 'r') as config_file:
                    paths = json.load(config_file)
                    self.ui.MCUPathBox.setText(paths.get("mcu_file", ""))
                    self.ui.TelitPathBox.setText(paths.get("telit_file", ""))
                    self.ui.IPECMDPathBox.setText(paths.get("ipecmd_file", ""))
                    hotkey = paths.get("hotkey", "")
                    if hotkey:
                        self.ui.SetFlashHotkey.setKeySequence(QKeySequence(hotkey))
                        self.set_hotkey()
                    self.counter_value = paths.get("counter", 0)
                    self.ui.Counter.display(self.counter_value)
            except Exception as e:
                self.ui.DebugWindow.append(f"Error loading paths: {str(e)}")

    def save_default_paths(self):
        """Create a new configuration file with default (empty) values."""
        default_paths = {
            "mcu_file": "",
            "telit_file": "",
            "ipecmd_file": "",
            "hotkey": "",
            "counter": 0
        }
        try:
            with open(self.CONFIG_FILE, 'w') as config_file:
                json.dump(default_paths, config_file, indent=4)
        except Exception as e:
            self.ui.DebugWindow.append(f"Error creating default config: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.setWindowTitle("IRepell Programmer")  # Set a custom window title
    widget.show()
    sys.exit(app.exec())
