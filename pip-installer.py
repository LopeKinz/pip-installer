import subprocess
import time

def check_package_availability(package):
    try:
        subprocess.run(['pip', 'show', package], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(package):
    try:
        subprocess.run(['pip', 'install', package], check=True)
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Error installing {package}")

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
        subprocess.run('pip list --outdated  | grep -v \'^-e\' | cut -d \'=\' -f 1 | xargs -n1 pip install -U', shell=True, check=True)
        
        print("Packages updated successfully.")
    except subprocess.CalledProcessError:
        print("Error updating packages.")

def display_stats(start_time, errors, num_updated_installed):
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("---------- Statistics ----------")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Errors encountered: {errors}")
    print(f"Number of updated/installed packages: {num_updated_installed}")
    print("---------------------------------")

def main():
    while True:
        print("===================================")
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

if __name__ == '__main__':
    main()
