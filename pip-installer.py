import subprocess
import time
import sys
import platform
import traceback

PIP_NOT_INSTALLED_ERROR = 1
PACKAGE_INSTALLATION_ERROR = 2
PACKAGE_UPDATE_ERROR = 3


def check_pip_availability():
    try:
        subprocess.run(['pip', '--version'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_pip():
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        print("Successfully installed pip.")
    except subprocess.CalledProcessError:
        print("Error installing pip.")
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


def install_package(package, version=None):
    try:
        if version:
            subprocess.run(['pip', 'install', f'{package}=={version}'], check=True)
            print(f"Successfully installed {package} version {version}")
        else:
            subprocess.run(['pip', 'install', package], check=True)
            print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Error installing {package}")
        sys.exit(PACKAGE_INSTALLATION_ERROR)


def install_packages(package_list):
    packages = [package.strip() for package in package_list.split(',')]
    for package in packages:
        if check_package_availability(package):
            print(f"Package '{package}' already installed")
        else:
            install_package(package)


def view_extensions():
    try:
        output = subprocess.run(['pip', 'list', '--outdated'], check=True, capture_output=True, text=True)
        print("Extensions:")
        print("-----------")
        print(output.stdout)
    except subprocess.CalledProcessError:
        print("Error retrieving extension information.")

def update_packages():
    try:
        # Update pip
        subprocess.run(['pip', 'install', '--upgrade', 'pip'], check=True)

        # Update other packages
        outdated_packages = subprocess.run(
            'pip list --outdated --format=legacy | grep -v \'^-e\' | cut -d \'=\' -f 1',
            shell=True, check=True, capture_output=True, text=True
        )

        packages = outdated_packages.stdout.strip().split('\n')

        num_updated_packages = 0
        for package in packages:
            if package.strip() != '':
                try:
                    subprocess.run(['pip', 'install', '-U', package], check=True)
                    num_updated_packages += 1
                except subprocess.CalledProcessError as e:
                    error_message = e.stderr
                    if error_message is not None:
                        error_message = error_message.decode().strip()
                        if not error_message.startswith("ERROR: Invalid requirement:"):
                            print(f"Error updating package '{package}': {error_message}")
                        else:
                            print(f"Skipped updating package '{package}' due to an error")
                    else:
                        print(f"Error updating package '{package}'")

        if num_updated_packages == 0:
            print("All packages are up to date.")
        else:
            print(f"{num_updated_packages} packages updated successfully.")
    except subprocess.CalledProcessError:
        print("Error updating packages.")
        sys.exit(PACKAGE_UPDATE_ERROR)







def display_stats(start_time, errors, num_updated_installed):
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\n---------- Statistics ----------")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Errors encountered: {errors}")
    print(f"Number of updated/installed packages: {num_updated_installed}")
    print("---------------------------------")


def display_crash_screen(error):
    print("\n========== Crash Report ==========")
    print("An error occurred while running the program.")
    print("Please help us improve by reporting this issue:")
    print("- Repository: https://github.com/LopeKinz/pip-installer/issues/new?assignees=&labels=Bug&projects=&template=Bug.md")
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
        while True:
            if not check_pip_availability():
                print("pip is not installed. Installing pip...")
                install_pip()

            print("\n===================================")
            print("           Package Installer       ")
            print("===================================")
            print("1. Single Mode")
            print("2. Multi Mode")
            print("3. View Extensions")
            print("4. Update Packages")
            print("0. Exit")
            print("-----------------------------------")
            print("Author: LopeKinz")
            print("GitHub: https://github.com/LopeKinz")
            print("-----------------------------------")

            choice = input("Enter your choice: ")

            if choice == '1':
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                while True:
                    print("Enter the package name to install (or type 'q' to quit):")
                    package_name = input()

                    if package_name.lower() == 'q':
                        break

                    if check_package_availability(package_name):
                        print(f"Package '{package_name}' already installed")
                    else:
                        versions = get_available_versions(package_name)
                        if versions:
                            print(f"Available versions for {package_name}:")
                            for i, version in enumerate(versions, start=1):
                                print(f"{i}. {version}")
                            version_choice = input("Choose the version number (or press Enter for the latest version): ")
                            if version_choice.isdigit() and int(version_choice) in range(1, len(versions) + 1):
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

            elif choice == '2':
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                print("Enter package names separated by commas (or type 'q' to quit):")
                package_list = input()

                if package_list.lower() == 'q':
                    continue

                try:
                    install_packages(package_list)
                    num_updated_installed = len(package_list.split(','))
                except subprocess.CalledProcessError:
                    errors += 1

                display_stats(start_time, errors, num_updated_installed)

            elif choice == '3':
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                view_extensions()

                display_stats(start_time, errors, num_updated_installed)

            elif choice == '4':
                start_time = time.time()
                errors = 0
                num_updated_installed = 0

                try:
                    update_packages()
                    num_updated_installed = 1
                except subprocess.CalledProcessError:
                    errors += 1

                display_stats(start_time, errors, num_updated_installed)

            elif choice == '0':
                break

            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        display_crash_screen(e)


if __name__ == '__main__':
    main()
