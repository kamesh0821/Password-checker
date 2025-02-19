# Advanced Password Strength Checker

This **Advanced Password Strength Checker** is a sophisticated command-line tool designed to help users evaluate the security of their passwords. By assessing various aspects of password strength, including length, complexity, and common vulnerability patterns, this tool provides actionable feedback to enhance password security.

---

## Features

- **Comprehensive Analysis**: Checks password length, character diversity, and common vulnerability patterns.
- **Entropy Calculation**: Measures the randomness and unpredictability of passwords.
- **Color-Coded Feedback**: Provides immediate visual feedback using color codes to highlight password strengths and weaknesses.
- **Logging**: Records each password check in a daily log file for audit and review purposes (without storing actual passwords).
- **Configurable Settings**: Allows customization of settings such as minimum length and entropy requirements through a configuration dictionary.

---

## Requirements

- **Python 3.6+** is required for proper execution of the script.
- **Colorama** library for colored output in the terminal.
- Ensure your system has Python and pip installed.

## Installation

   ### Clone the Repository:

```
git clone https://github.com/kamesh0821/Password-checker.git
cd password-strength-checker
```
### Install Required Libraries:
```
pip install -r requirements.txt
```

##  Usage

1. To use the password strength checker, follow these steps:

    Start the Script:
 ```
python password_checker.py
```
  Input Your Password:

 - Enter the password when prompted.
 - Your input will be analyzed, and feedback will be displayed immediately.

Review the Output:

 - The script will provide a detailed breakdown of the password's strengths and weaknesses.
 - A color-coded meter and a numerical score out of 10 will indicate the password's overall security level.
