"""
Author: Serena Ban

Uploads Arduino specific scripts to Arduino from Raspberry Pi
This allows simple upload without needing to download Arduino IDE
"""
import os
import subprocess

# AVR related constants

avr_gcc = "avr-gcc"
avr_objcopy = "avr-objcopy"
avrdude = "avrdude"

# Constants to be modified

mcu = "atmega328p"  # Microcontroller Unit specific to Arduino chip
f_cpu = "16000000UL"  # MCU Frequency
port = "/dev/ttyACMO"  # Raspberry Pi port that Arduino is connected to
baud_rate = "115200"  # Baud Rate

# Path to Arduino Core Library
# git clone https://github.com/arduino/ArduinoCore-avr to download the related folders

arduino_core_path = os.path.expanduser("ArduinoCore-avr/cores/arduino")
arduino_variants_path = os.path.expanduser("ArduinoCore-avr/variants/standard")
arduino_libraries_path = os.path.expanduser("Arduino-avr/Libraries")


def compile_sketch(project_name):
    cpp_file = f"{project_name}.cpp"  # cpp file (Arduino Script) to upload
    hex_file = f"{project_name}.hex"

    build_dir = "build"
    os.makedirs(build_dir, exist_ok=True)

    print("Compiling...")

    compile_command = [
        avr_gcc,
        "-mmcu=" + mcu,
        "-DF_CPU=" + f_cpu,
        "-Os",
        "-I" + arduino_core_path,
        "-I" + arduino_variants_path,
        "-o", f"{build_dir}/{project_name}.elf",
        cpp_file,
        os.path.join(arduino_core_path, "main_cpp"),
        os.path.join(arduino_core_path, "wiring_digital.c"),
        os.path.join(arduino_core_path, "wiring_analog.c"),
        os.path.join(arduino_core_path, "wiring.c"),
        os.path.join(arduino_core_path, "wiring_pulse.c"),
        os.path.join(arduino_core_path, "wiring_shift.c"),
        os.path.join(arduino_core_path, "hooks.c"),
        os.path.join(arduino_core_path, "wiring_pulse.S"),
    ]

    subprocess.run(compile_command, check=True)

    print("Converting to .hex file...")
    objcopy_command = [
        avr_objcopy,
        "-O", "ihex",
        "-R", ".eeprom",
        f"{build_dir}/{project_name}.elf",
        f"{build_dir}/{hex_file}",
    ]

    subprocess.run(objcopy_command, check=True)


def upload_sketch(project_name):
    build_dir = "build"
    os.makedirs(build_dir, exist_ok=True)

    hex_file = f"{project_name}.hex"

    print("Uploading...")

    upload_command = [
        avrdude,
        "-c", "arduino",
        "-p", mcu,
        "-p", port,
        "-b", baud_rate,
        '-U', f"flash:w:{build_dir}/{hex_file}:i"
    ]

    subprocess.run(upload_command, check=True)
    print("Upload Complete!")



