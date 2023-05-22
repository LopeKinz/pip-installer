# pip-installer

pip-installer is a Python package installation and management tool with a user-friendly GUI. It allows you to install, update, and view information about Python packages using the pip package manager.

## Installation

To use pip-installer, you need to have Python installed on your system. The recommended Python version is 3.6 or above.

1. Clone the repository or download the source code from the development branch.
2. Navigate to the project directory.

```bash
$ cd pip-installer
```

3. Install the required dependencies by running the following command:

```bash
$ pip install -r requirements.txt
```

## Usage

To launch the pip-installer GUI, run the following command:

```bash
$ python main.py
```

The GUI window will appear, providing various options for package installation and management:

### Single Mode

In Single Mode, you can install a single package by entering the package name in the provided input field and clicking the "Execute" button. The console output will display the installation progress and any errors encountered.

### Multi Mode

In Multi Mode, you can install multiple packages at once. Enter a comma-separated list of package names in the input field and click the "Execute" button. The console output will show the installation progress and errors, if any.

### View Extensions

Choosing the "View Extensions" option will display a list of outdated packages installed in your system. The console output will show the package names and their current versions.

### Update Packages

Selecting the "Update Packages" option will update pip to the latest version and upgrade all outdated packages on your system. The console output will provide information about the updated packages and any errors encountered during the update process.

### Exit

Clicking the "Exit" option will close the pip-installer GUI.

## Development

The development branch contains the latest features and improvements that are still being tested. Use this branch if you want to contribute or test the latest changes.

## Contributing

Contributions to pip-installer are welcome! If you want to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes and test them thoroughly.
4. Commit your changes and push the branch to your forked repository.
5. Submit a pull request to the development branch of the main repository.

Please ensure that your code follows the project's coding conventions and includes appropriate documentation.

## License

pip-installer is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments

- This project was inspired by the need for a user-friendly package installer tool.
- Special thanks to the contributors who have helped improve and expand the functionality of pip-installer.
