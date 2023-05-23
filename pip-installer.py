import os
import subprocess
import time
import sys
import platform
import traceback
import json

PIP_NOT_INSTALLED_ERROR = 1
PACKAGE_INSTALLATION_ERROR = 2
PACKAGE_UPDATE_ERROR = 3


def create_package(author, name, version, requirements, main_file_path):
    # Create package directory
    package_dir = f"{name.lower().replace(' ', '_')}"
    os.makedirs(package_dir)

    # Create package files
    with open(os.path.join(package_dir, "__init__.py"), "w") as init_file:
        pass

    if main_file_path:
        # Read content from user-specified file path
        with open(main_file_path, "r") as main_content_file:
            main_content = main_content_file.read()
    else:
        # Use default content for main.py if no file path is provided
        main_content = f"""
def hello():
    print("Hello, {name}!")

if __name__ == "__main__":
    hello()
"""

    with open(os.path.join(package_dir, "main.py"), "w") as main_file:
        main_file.write(main_content)

    with open("setup.py", "w") as setup_file:
        setup_file.write(
            f"""
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='{name}',
    version='{version}',
    author='{author}',
    description='{name} package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['{package_dir}'],
    install_requires={requirements},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
"""
        )

    with open("README.md", "w") as readme_file:
        readme_file.write(f"# {name}\n\nThis is the {name} package.\n")

    # Print success message
    print(f"Package '{name}' created successfully!")


def display_stats(start_time, errors, num_updated_installed):
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\n---------- Statistics ----------")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Errors encountered: {errors}")
    print(f"Number of updated/installed packages: {num_updated_installed}")
    print("---------------------------------")


def get_installed_packages_count():
    try:
        output = subprocess.run(
            ["pip", "list"], check=True, capture_output=True, text=True
        )
        lines = output.stdout.strip().split("\n")
        # Subtract 2 from the total count to exclude header and footer lines
        count = max(len(lines) - 2, 0)
        return count
    except subprocess.CalledProcessError:
        return 0


def get_updatable_packages_count():
    try:
        output = subprocess.run(
            ["pip", "list", "--outdated"], check=True, capture_output=True, text=True
        )
        lines = output.stdout.strip().split("\n")
        # Subtract 2 from the total count to exclude header and footer lines
        count = max(len(lines) - 2, 0)
        return count
    except subprocess.CalledProcessError:
        return 0


def check_pip_availability():
    try:
        subprocess.run(["pip", "--version"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_pip():
    try:
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
        print("Successfully installed pip.")
    except subprocess.CalledProcessError:
        print("Error installing pip.")
        sys.exit(PIP_NOT_INSTALLED_ERROR)


def check_package_availability(package):
    try:
        subprocess.run(["pip", "show", package], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_available_versions(package):
    try:
        output = subprocess.run(
            ["pip", "search", package], check=True, capture_output=True, text=True
        )
        lines = output.stdout.strip().split("\n")
        versions = [line.split("(")[1].split(")")[0].strip() for line in lines]
        return versions
    except subprocess.CalledProcessError:
        return []


def install_package(package, version=None, combined=False):
    start_time = time.time()
    errors = 0
    num_updated_installed = 0

    try:
        if version:
            subprocess.run(["pip", "install", f"{package}=={version}"], check=True)
            print(f"Successfully installed {package} version {version}")
            num_updated_installed += 1
        else:
            subprocess.run(["pip", "install", package], check=True)
            print(f"Successfully installed {package}")
            num_updated_installed += 1

    except subprocess.CalledProcessError:
        print(f"Error installing {package}")
        errors += 1
    if combined is False:
        display_stats(start_time, errors, num_updated_installed)


def install_packages(package_list):
    start_time = time.time()
    errors = 0
    num_updated_installed = 0

    packages = [package.strip() for package in package_list.split(",")]
    for package in packages:
        if check_package_availability(package):
            print(f"Package '{package}' already installed")
        else:
            if package.strip() != "":
                result = install_package(package, combined=True)
                if result != 0:
                    errors += 1
                else:
                    num_updated_installed += 1

    display_stats(start_time, errors, num_updated_installed)
    return errors


def view_extensions():
    try:
        output = subprocess.run(
            ["pip", "list", "--outdated"], check=True, capture_output=True, text=True
        )
        print("Extensions:")
        print("-----------")
        print(output.stdout)
    except subprocess.CalledProcessError:
        print("Error retrieving extension information.")


def update_packages():
    try:
        start_time = time.time()
        num_updated_packages = 0
        errors = 0

        # Update pip
        subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)
        num_updated_packages += 1

        # Update other packages
        outdated_packages = subprocess.run(
            "pip list --outdated --format=json",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )

        packages = json.loads(outdated_packages.stdout)

        for package in packages:
            package_name = package["name"]
            if package_name.strip() != "":
                try:
                    subprocess.run(["pip", "install", "-U", package_name], check=True)
                    num_updated_packages += 1
                except subprocess.CalledProcessError as e:
                    error_message = e.stderr
                    if error_message is not None:
                        error_message = error_message.decode().strip()
                        if not error_message.startswith("ERROR: Invalid requirement:"):
                            print(
                                f"Error updating package '{package_name}': {error_message}"
                            )
                        else:
                            print(
                                f"Skipped updating package '{package_name}' due to an error"
                            )
                    else:
                        print(f"Error updating package '{package_name}'")
                        errors += 1
                else:
                    print(f"Updated package '{package_name}'")

        if num_updated_packages == 1:
            print("All packages are up to date.")
        else:
            print(f"{num_updated_packages - 1} packages updated successfully.")

        display_stats(start_time, errors, num_updated_packages)
    except subprocess.CalledProcessError:
        print("Error updating packages.")
        sys.exit(PACKAGE_UPDATE_ERROR)


def display_crash_screen(error):
    print("\n========== Crash Report ==========")
    print("An error occurred while running the program.")
    print("Please help us improve by reporting this issue:")
    print(
        "- Repository: https://github.com/LopeKinz/pip-installer/issues/new?assignees=&labels=Bug&projects=&template=Bug.md"
    )
    print("-----------------------------------")
    print("System Information:")
    print(f"Python Version: {sys.version}")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print("-----------------------------------")
    print("Error Details:")
    traceback.print_exception(type(error), error, error.__traceback__)
    print("-----------------------------------")
    print("Thank you for your support!")
    print("===================================")


def main():
    try:
        installed_count = get_installed_packages_count()
        updatable_count = get_updatable_packages_count()
        while True:
            if not check_pip_availability():
                print("pip is not installed. Installing pip...")
                install_pip()

            print("\n===================================")
            print("           Pip Installer            ")
            print("===================================")
            print("1. Single Mode")
            print("2. Multi Mode")
            print("3. View Updatable Extensions")
            print("4. Update Packages")
            print("5. Uninstall Package")
            print("6. Create Own Package")
            print("0. Exit")
            print("-----------------------------------")
            print("Author: LopeKinz")
            print("GitHub: https://github.com/LopeKinz")
            print("-----------------------------------")
            print("Installed packages:", installed_count)
            print("Updatable packages:", updatable_count)
            print("-----------------------------------")

            choice = input("Enter your choice: ")

            if choice == "1":
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                while True:
                    print("Enter the package name to install (or type 'q' to quit):")
                    package_name = input()

                    if package_name.lower() == "q":
                        break

                    if check_package_availability(package_name):
                        print(f"Package '{package_name}' already installed")
                    else:
                        versions = get_available_versions(package_name)
                        if versions:
                            print(f"Available versions for {package_name}:")
                            for i, version in enumerate(versions, start=1):
                                print(f"{i}. {version}")
                            version_choice = input(
                                "Choose the version number (or press Enter for the latest version): "
                            )
                            if version_choice.isdigit() and int(
                                version_choice
                            ) in range(1, len(versions) + 1):
                                version = versions[int(version_choice) - 1]
                            else:
                                version = None
                            try:
                                install_package(package_name, version)
                                num_updated_installed += 1
                            except subprocess.CalledProcessError:
                                errors += 1
                        else:
                            try:
                                install_package(package_name)
                                num_updated_installed += 1
                            except subprocess.CalledProcessError:
                                errors += 1

                display_stats(start_time, errors, num_updated_installed)

            elif choice == "2":
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                print("Enter package names separated by commas (or type 'q' to quit):")
                package_list = input()

                if package_list.lower() == "q":
                    continue

                try:
                    install_packages(package_list)
                    num_updated_installed = len(package_list.split(","))
                except subprocess.CalledProcessError:
                    errors += 1

            elif choice == "3":
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                view_extensions()

            elif choice == "4":
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                try:
                    update_packages()
                    num_updated_installed = 1
                except subprocess.CalledProcessError:
                    errors += 1

            elif choice == "5":
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                print("Enter the package name to uninstall (or type 'q' to quit):")
                package_name = input()

                if package_name.lower() == "q":
                    continue

                try:
                    subprocess.run(["pip", "uninstall", package_name], check=True)
                    num_updated_installed += 1
                except subprocess.CalledProcessError:
                    errors += 1

                display_stats(start_time, errors, num_updated_installed)

            elif choice == "6":
                author = input("Enter the author name: ")
                name = input("Enter the package name: ")
                version = input("Enter the package version: ")
                requirements = input(
                    "Enter the package requirements (comma-separated): "
                ).split(",")
                main_file_path = input(
                    "Enter the path to the main.py file (leave blank to use default content): "
                )

                # Create the package
                create_package(author, name, version, requirements, main_file_path)

            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        display_crash_screen(e)


if __name__ == "__main__":
    main()
