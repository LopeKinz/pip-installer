import subprocess
import sys
import tkinter as tk
import tkinter.scrolledtext as tkst
import time

def check_pip_availability():
    try:
        subprocess.run(['pip', '--version'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_pip():
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        console_output.insert(tk.END, "Successfully installed pip.\n")
    except subprocess.CalledProcessError:
        console_output.insert(tk.END, "Error installing pip.\n")

def check_package_availability(package):
    try:
        subprocess.run(['pip', 'show', package], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(package):
    try:
        subprocess.run(['pip', 'install', package], check=True)
        console_output.insert(tk.END, f"Successfully installed {package}\n")
    except subprocess.CalledProcessError:
        console_output.insert(tk.END, f"Error installing {package}\n")

def install_packages(package_list):
    packages = [package.strip() for package in package_list.split(',')]
    for package in packages:
        if check_package_availability(package):
            console_output.insert(tk.END, f"Package '{package}' already installed\n")
        else:
            install_package(package)

def view_extensions():
    try:
        output = subprocess.run(['pip', 'list', '--outdated'], check=True, capture_output=True, text=True)
        console_output.insert(tk.END, "Extensions:\n")
        console_output.insert(tk.END, "-----------\n")
        console_output.insert(tk.END, output.stdout)
    except subprocess.CalledProcessError:
        console_output.insert(tk.END, "Error retrieving extension information.\n")

def update_packages():
    try:
        # Update pip
        subprocess.run(['pip', 'install', '--upgrade', 'pip'], check=True)

        # Update other packages
        subprocess.run('pip list --outdated  | grep -v \'^-e\' | cut -d \'=\' -f 1 | xargs -n1 pip install -U', shell=True, check=True)

        console_output.insert(tk.END, "Packages updated successfully.\n")
    except subprocess.CalledProcessError:
        console_output.insert(tk.END, "Error updating packages.\n")

def display_stats(start_time, errors, num_updated_installed):
    end_time = time.time()
    elapsed_time = end_time - start_time

    console_output.insert(tk.END, "---------- Statistics ----------\n")
    console_output.insert(tk.END, f"Time elapsed: {elapsed_time:.2f} seconds\n")
    console_output.insert(tk.END, f"Errors encountered: {errors}\n")
    console_output.insert(tk.END, f"Number of updated/installed packages: {num_updated_installed}\n")
    console_output.insert(tk.END, "---------------------------------\n")

def single_mode():
    start_time = time.time()
    errors = 0
    num_updated_installed = 0

    console_output.insert(tk.END, "Enter the package name to install (or type 'q' to quit):\n")
    
    while True:
        package_name = entry.get()
        entry.delete(0, tk.END)
        
        if package_name.lower() == 'q':
            break

        if check_package_availability(package_name):
            console_output.insert(tk.END, f"Package '{package_name}' already installed\n")
        else:
            try:
                install_package(package_name)
                num_updated_installed += 1
            except subprocess.CalledProcessError:
                errors += 1
    
    display_stats(start_time, errors, num_updated_installed)

def multi_mode():
    start_time = time.time()
    errors = 0
    num_updated_installed = 0

    package_list = entry.get()
    entry.delete(0, tk.END)
    
    if package_list.lower() == 'q':
        return

    try:
        install_packages(package_list)
        num_updated_installed = len(package_list.split(','))
    except subprocess.CalledProcessError:
        errors += 1
    
    display_stats(start_time, errors, num_updated_installed)

def on_choice_selected():
    choice = choice_var.get()

    if choice == '1':
        single_mode()
    elif choice == '2':
        multi_mode()
    elif choice == '3':
        view_extensions()
    elif choice == '4':
        update_packages()
    elif choice == '0':
        root.destroy()
    else:
        console_output.insert(tk.END, "Invalid choice. Please try again.\n")

root = tk.Tk()
root.title("Package Installer")

# Main Frame
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack()

# Title
title_label = tk.Label(main_frame, text="Package Installer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Choice
choice_var = tk.StringVar()
choice_var.set('1')

choice_frame = tk.Frame(main_frame)
choice_frame.pack()

choice_label = tk.Label(choice_frame, text="Choose an option:")
choice_label.grid(row=0, column=0, sticky=tk.W)

choice_single_mode = tk.Radiobutton(choice_frame, text="Single Mode", variable=choice_var, value='1')
choice_single_mode.grid(row=1, column=0, sticky=tk.W)

choice_multi_mode = tk.Radiobutton(choice_frame, text="Multi Mode", variable=choice_var, value='2')
choice_multi_mode.grid(row=2, column=0, sticky=tk.W)

choice_view_extensions = tk.Radiobutton(choice_frame, text="View Extensions", variable=choice_var, value='3')
choice_view_extensions.grid(row=3, column=0, sticky=tk.W)

choice_update_packages = tk.Radiobutton(choice_frame, text="Update Packages", variable=choice_var, value='4')
choice_update_packages.grid(row=4, column=0, sticky=tk.W)

choice_exit = tk.Radiobutton(choice_frame, text="Exit", variable=choice_var, value='0')
choice_exit.grid(row=5, column=0, sticky=tk.W)

# Entry
entry_frame = tk.Frame(main_frame)
entry_frame.pack(pady=10)

entry_label = tk.Label(entry_frame, text="Enter package(s):")
entry_label.grid(row=0, column=0, sticky=tk.W)

entry = tk.Entry(entry_frame, width=50)
entry.grid(row=1, column=0)

# Button
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

button = tk.Button(button_frame, text="Execute", command=on_choice_selected, width=10, height=2, bd=0, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
button.pack()

# Console Output
console_frame = tk.Frame(main_frame)
console_frame.pack()

console_output = tkst.ScrolledText(console_frame, width=70, height=20)
console_output.pack()

def write_to_console_output(text):
    console_output.insert(tk.END, text)

# Redirect stdout and stderr to the console_output
sys.stdout.write = write_to_console_output
sys.stderr.write = write_to_console_output

root.mainloop()
