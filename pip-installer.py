import subprocess
import time
import sys
import platform
import traceback
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext

PIP_NOT_INSTALLED_ERROR = 1
PACKAGE_INSTALLATION_ERROR = 2
PACKAGE_UPDATE_ERROR = 3


def display_stats(start_time, errors, num_updated_installed):
    end_time = time.time()
    elapsed_time = end_time - start_time

    result_text = f"\n---------- Statistics ----------\n"
    result_text += f"Time elapsed: {elapsed_time:.2f} seconds\n"
    result_text += f"Errors encountered: {errors}\n"
    result_text += f"Number of updated/installed packages: {num_updated_installed}\n"
    result_text += "---------------------------------"
    command_output.config(state=tk.NORMAL)
    command_output.delete(1.0, tk.END)
    command_output.insert(tk.END, result_text)
    command_output.config(state=tk.DISABLED)


def get_installed_packages_count():
    try:
        output = subprocess.run(['pip', 'list'], check=True, capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        # Subtract 2 from the total count to exclude header and footer lines
        count = max(len(lines) - 2, 0)
        return count
    except subprocess.CalledProcessError:
        return 0


def get_updatable_packages_count():
    try:
        output = subprocess.run(['pip', 'list', '--outdated'], check=True, capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        # Subtract 2 from the total count to exclude header and footer lines
        count = max(len(lines) - 2, 0)
        return count
    except subprocess.CalledProcessError:
        return 0


def check_pip_availability():
    try:
        subprocess.run(['pip', '--version'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_pip():
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        messagebox.showinfo("Installation Complete", "Successfully installed pip.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Installation Error", "Error installing pip.")
        sys.exit(PIP_NOT_INSTALLED_ERROR)


def check_package_availability(package):
    try:
        subprocess.run(['pip', 'show', package], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_available_versions(package):
    try:
        output = subprocess.run(['pip', 'search', package], check=True, capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        versions = [line.split('(')[1].split(')')[0].strip() for line in lines]
        return versions
    except subprocess.CalledProcessError:
        return []


def install_package(package, version=None, combined=False):
    start_time = time.time()
    errors = 0
    num_updated_installed = 0

    try:
        if version:
            subprocess.run(['pip', 'install', f'{package}=={version}'], check=True)
            messagebox.showinfo("Installation Complete", f"Successfully installed {package} version {version}")
            num_updated_installed += 1
        else:
            subprocess.run(['pip', 'install', package], check=True)
            messagebox.showinfo("Installation Complete", f"Successfully installed {package}")
            num_updated_installed += 1
    except subprocess.CalledProcessError:
        errors += 1

    display_stats(start_time, errors, num_updated_installed)


def update_package(package, version=None):
    start_time = time.time()
    errors = 0
    num_updated_installed = 0

    try:
        if version:
            subprocess.run(['pip', 'install', f'{package}=={version}', '--upgrade'], check=True)
            messagebox.showinfo("Update Complete", f"Successfully updated {package} to version {version}")
            num_updated_installed += 1
        else:
            subprocess.run(['pip', 'install', '--upgrade', package], check=True)
            messagebox.showinfo("Update Complete", f"Successfully updated {package}")
            num_updated_installed += 1
    except subprocess.CalledProcessError:
        errors += 1

    display_stats(start_time, errors, num_updated_installed)


def main():
    def execute_command():
        command_output.config(state=tk.NORMAL)
        command_output.delete(1.0, tk.END)

        if option_var.get() == "single":
            package_name = package_entry.get()
            version = version_entry.get()
            install_package(package_name, version)

        elif option_var.get() == "multi":
            package_list = package_entry.get()
            install_packages(package_list)

        elif option_var.get() == "update":
            package_name = package_entry.get()
            version = version_entry.get()
            update_package(package_name, version)

        # Update command output with the result
        result_text = "Command output..."
        command_output.insert(tk.END, result_text)
        command_output.config(state=tk.DISABLED)

    def install_packages(package_list):
        packages = package_list.split(',')
        for package in packages:
            package = package.strip()
            if package:
                install_package(package)

    def update_packages(package_list):
        packages = package_list.split(',')
        for package in packages:
            package = package.strip()
            if package:
                update_package(package)

    window = tk.Tk()
    window.title("Package Installer")

    # Create the radio button options
    option_var = tk.StringVar()
    option_var.set("single")

    single_mode_radio = tk.Radiobutton(window, text="Single Mode", variable=option_var, value="single")
    single_mode_radio.pack(anchor=tk.W)

    multi_mode_radio = tk.Radiobutton(window, text="Multi Mode", variable=option_var, value="multi")
    multi_mode_radio.pack(anchor=tk.W)

    update_mode_radio = tk.Radiobutton(window, text="Update Mode", variable=option_var, value="update")
    update_mode_radio.pack(anchor=tk.W)

    # Create the package input entry
    package_label = tk.Label(window, text="Package(s):")
    package_label.pack(anchor=tk.W)

    package_entry = tk.Entry(window, width=50)
    package_entry.pack()

    # Create the version input entry
    version_label = tk.Label(window, text="Version:")
    version_label.pack(anchor=tk.W)

    version_entry = tk.Entry(window, width=50)
    version_entry.pack()

    # Create the command output text widget
    command_output = scrolledtext.ScrolledText(window, height=10, width=50, state=tk.DISABLED)
    command_output.pack()

    # Create the execute button
    execute_button = tk.Button(window, text="Execute", command=execute_command)
    execute_button.pack()

    window.mainloop()


if __name__ == '__main__':
    main()
