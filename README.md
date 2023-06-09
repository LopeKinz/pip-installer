# pip-installer

## Overview
The pip-installer repository provides a user-friendly solution for managing Python packages with pip, simplifying the installation process for developers.

## Features
- Streamlined package installation: Easily install and manage Python packages with a simplified approach.
- Intuitive interface: The pip-installer offers a user-friendly interface, making it straightforward to set up development environments or deploy applications.
- Time-saving: By automating the package installation process, pip-installer saves valuable time and effort for developers.

## Getting Started
To get started with the pip-installer, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/LopeKinz/pip-installer.git
   ```

2. Run the pip-installer script:
   ```
   python pip-installer.py
   ```
3. If PiP is not installed it will be Automaticly installed.

4. Follow the on-screen prompts to install the desired Python packages.
5. Wanna Try GUI Version? Download [HERE](https://github.com/LopeKinz/pip-installer/tree/dev)

## Contributing
Contributions to the pip-installer project are welcome! If you encounter any issues or have suggestions for improvements, please submit a pull request or open an issue in the GitHub repository.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
For any questions or inquiries, feel free to reach out to the project maintainer, [LopeKinz](https://github.com/LopeKinz).

## Changelog
```
### Version 1.4.0 (2023.05.24)

- Added "Install from text file" Mode

### Version 1.3.1 (2023.05.23)

- Added "Create own Package" Mode

### Version 1.3.0 (2023.05.23)

- Added Uninstall Option
- Added Stats to the Main Menu
- Fixed update_packages() not returning the full list of outdated packages
- Implementing Stats Correctly
- fixed a bug displaying the stats twice

### Version 1.2.1 (2023.05.22)

- Fixed update_packages() 

### Version 1.2.0 (2023.05.22)

- Added Version control

### Version 1.1.1 (2023.05.22)

- Better Error Handling

### Version 1.1.0 (2023.05.22)

- Added error handling for subprocess calls
- Improved user input validation
- Refactored code into smaller functions for better organization
- Fixed minor bugs

### Version 1.0.0 (2023.05.22)

- Initial release
- Added package installation functionality
- Implemented single and multi-mode installation options
- Added view extensions and update packages options
```
# Documentation

## Package Installer

Package Installer is a command-line tool that allows you to install, view, and update Python packages using the `pip` package manager.

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/LopeKinz/pip-installer.git
   ```

2. Navigate to the project directory:
   ```
   cd pip-installer
   ```

3. Run the script:
   ```
   python installer.py
   ```

## Options

The Package Installer provides the following options:
## Features

- Single Mode: Install a single package with optional version specification.
- Multi Mode: Install multiple packages listed in a comma-separated format.
- View Updatable Extensions: Display a list of installed packages with available updates.
- Update Packages: Update pip and all installed packages.
- Uninstall Package: Remove a specific package from the system.
- Create Own Package: Create your own PiP Package.
- Install From Text File

## Single Mode

In Single Mode, you can install a single package by following these steps:

1. Enter the package name to install.
2. Enter the Desired Version.
3. Repeat step 1 to install more packages or enter 'q' to quit.

## Multi Mode

In Multi Mode, you can install multiple packages by following these steps:

1. Enter package names separated by commas.

2. Repeat step 1 to install more packages or press 'Enter' to quit.

## View Extensions

In View Extensions mode, you can view outdated packages by running the command.

## Update Packages

In Update Packages mode, you can update all installed packages by running the command.

## Uninstall Packages

In Uninstall mode you, can easily uninstall any package by their name.

## Create Own Package

In Create Own Package mode, you can easily create own PiP packages!

## Install From Text File

In this mode you can easily install packages from text file! (Format : Module,Module)

## Statistics

After each operation, statistics will be displayed, including:

- Time elapsed: The total time taken to complete the operation.

- Errors encountered: The number of errors encountered during the operation.

- Number of updated/installed packages: The total number of packages that were updated or installed.

## Author

This package installer is developed by LopeKinz.

- GitHub: [https://github.com/LopeKinz](https://github.com/LopeKinz)

## Star History <a name="star-history"></a>

<a href="https://github.com/lopekinz/pip-installer/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=lopekinz/pip-installer&type=Date">
      </a> 
