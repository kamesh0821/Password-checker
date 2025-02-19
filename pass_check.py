
import re
import string
import random
import math
import time
import logging
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Configuration
CONFIG = {
    'MIN_LENGTH': 8,
    'RECOMMENDED_LENGTH': 12,
    'EXCELLENT_LENGTH': 20,
    'SPECIAL_CHARS': '!@#$%^&*(),.?":{}|<>=_+-;\'[]\\',
    'COMMON_PATTERNS': ['123', 'abc', 'qwerty', 'admin', 'password', '111', '000'],
    'KEYBOARD_PATTERNS': ['qwerty', 'asdfgh', 'zxcvbn', '123456', 'qazwsx'],
    'MIN_ENTROPY': 60  # Minimum recommended entropy in bits
}

# Set up logging
logging.basicConfig(
    filename=f'password_checker_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def print_banner():
    banner = f"""{Fore.CYAN}
  _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____       
|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|      
|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|      
                                                                                                                                     
                                                                                                                                     
         ____                                     _   ____  _                        _   _        ____ _               _             
        |  _ \ __ _ ___ _____      _____  _ __ __| | / ___|| |_ _ __ ___ _ __   __ _| |_| |__    / ___| |__   ___  ___| | _____ _ __ 
        | |_) / _ / __/ __\ \ /\ / / _ \| '__/ _ | \___ \| __| '__/ _ \ '_ \ / _ | __| '_ \  | |   | '_ \ / _ \/ __| |/ / _ \ '__|
        |  __/ (_| \__ \__ \\ V  V / (_) | | | (_| |  ___) | |_| | |  __/ | | | (_| | |_| | | | | |___| | | |  __/ (__|   <  __/ |   
        |_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_| |____/ \__|_|  \___|_| |_|\__, |\__|_| |_|  \____|_| |_|\___|\___|_|\_\___|_|   
                                                                               |___/                                                 
             _____       _                              _   ____                       _ _           _____           _               
            | ____|_ __ | |__   __ _ _ __   ___ ___  __| | / ___|  ___  ___ _   _ _ __(_) |_ _   _  |_   _|__   ___ | |              
            |  _| | '_ \| '_ \ / _ | '_ \ / __/ _ \/ _ | \___ \ / _ \/ __| | | | '__| | __| | | |   | |/ _ \ / _ \| |              
            | |___| | | | | | | (_| | | | | (_|  __/ (_| |  ___) |  __/ (__| |_| | |  | | |_| |_| |   | | (_) | (_) | |              
            |_____|_| |_|_| |_|\__,_|_| |_|\___\___|\__,_| |____/ \___|\___|\__,_|_|  |_|\__|\__, |   |_|\___/ \___/|_|              
                                                                                             |___/                                   
              ____                _           _   _             _  __                         _                                      
             / ___|_ __ ___  __ _| |_ ___  __| | | |__  _   _  | |/ /__ _ _ __ ___   ___  ___| |__                                   
            | |   | '__/ _ \/ _ | __/ _ \/ _ | | '_ \| | | | | ' // _ | '_  _ \ / _ \/ __| '_ \                                  
            | |___| | |  __/ (_| | ||  __/ (_| | | |_) | |_| | | . \ (_| | | | | | |  __/\__ \ | | |                                 
             \____|_|  \___|\__,_|\__\___|\__,_| |_.__/ \__, | |_|\_\__,_|_| |_| |_|\___||___/_| |_|                                 
                                                        |___/                                                                        
                                                                                                                                     
 _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____       
|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|      
|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|      

  
{Style.RESET_ALL}
This tool will help you evaluate your password strength.
A strong password is essential for your security!\n
"""
    print(banner)

def calculate_entropy(password):
    """Calculate password entropy as a measure of randomness."""
    char_set_size = 0
    if re.search(r"[a-z]", password): 
        char_set_size += 26
    if re.search(r"[A-Z]", password): 
        char_set_size += 26
    if re.search(r"\d", password): 
        char_set_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): 
        char_set_size += 32
    if char_set_size == 0:
        return 0

    entropy = len(password) * math.log2(char_set_size)
    return round(entropy, 2)

def check_length(password):
    """Enhanced length check with more granular scoring."""
    length = len(password)
    if length < CONFIG['MIN_LENGTH']:
        return 0, f"{Fore.RED}❌ Password is too short ({length} chars). Minimum {CONFIG['MIN_LENGTH']} required."
    elif length < CONFIG['RECOMMENDED_LENGTH']:
        return 1, f"{Fore.YELLOW}ℹ️  Consider using a longer password ({length} chars)."
    elif length < CONFIG['EXCELLENT_LENGTH']:
        return 2, f"{Fore.GREEN}✅ Good length! ({length} chars)."
    else:
        return 3, f"{Fore.GREEN}✅ Excellent length! ({length} chars)."

def check_character_types(password):
    """Enhanced character type checking with detailed feedback."""
    points = 0
    feedback = []

    # Count different types
    char_counts = {
        'digits': len(re.findall(r"\d", password)),
        'uppercase': len(re.findall(r"[A-Z]", password)),
        'lowercase': len(re.findall(r"[a-z]", password)),
        'special': len(re.findall(r"[!@#$%^&*(),.?\":{}|<>]", password))
    }

    # Digits
    if char_counts['digits'] > 0:
        points += 1
        feedback.append(f"{Fore.GREEN}✅ Contains {char_counts['digits']} numbers")
    else:
        feedback.append(f"{Fore.RED}❌ Missing numbers")

    # Uppercase
    if char_counts['uppercase'] > 0:
        points += 1
        feedback.append(f"{Fore.GREEN}✅ Contains {char_counts['uppercase']} uppercase letters")
    else:
        feedback.append(f"{Fore.RED}❌ Missing uppercase letters")

    # Lowercase
    if char_counts['lowercase'] > 0:
        points += 1
        feedback.append(f"{Fore.GREEN}✅ Contains {char_counts['lowercase']} lowercase letters")
    else:
        feedback.append(f"{Fore.RED}❌ Missing lowercase letters")

    # Special characters
    if char_counts['special'] > 0:
        points += 1
        feedback.append(f"{Fore.GREEN}✅ Contains {char_counts['special']} special characters")
    else:
        feedback.append(f"{Fore.RED}❌ Missing special characters")

    return points, feedback

def check_patterns(password):
    """Comprehensive pattern checking."""
    points = 0
    feedback = []

    # Check common patterns
    for pattern in CONFIG['COMMON_PATTERNS']:
        if pattern in password.lower():
            points -= 1
            feedback.append(f"{Fore.RED}⚠️ Contains common pattern: '{pattern}'")

    # Check keyboard patterns
    for pattern in CONFIG['KEYBOARD_PATTERNS']:
        if pattern in password.lower() or pattern[::-1] in password.lower():
            points -= 1
            feedback.append(f"{Fore.RED}⚠️ Contains keyboard pattern: '{pattern}'")
            break

    # Check sequential numbers
    if re.search(r"(?:\d{3,})|(?:987|876|765|654|543|432|321)", password):
        points -= 1
        feedback.append(f"{Fore.RED}⚠️ Contains sequential numbers")

    # Check repeated characters
    if re.search(r"(.)\1{3,}", password):
        points -= 1
        feedback.append(f"{Fore.RED}⚠️ Contains repeated characters (4+ in a row)")

    return points, feedback

def generate_password_meter(score):
    """Generate a visual password strength meter."""
    total_blocks = 10
    filled_blocks = int((score / 10) * total_blocks)
    meter = []

    for i in range(total_blocks):
        if i < filled_blocks:
            if score <= 3:
                meter.append(f"{Fore.RED}█")
            elif score <= 6:
                meter.append(f"{Fore.YELLOW}█")
            else:
                meter.append(f"{Fore.GREEN}█")
        else:
            meter.append(f"{Fore.WHITE}░")

    return "".join(meter) + Style.RESET_ALL

def check_password_strength(password):
    """Main password strength checking function."""
    total_score = 0
    feedback = []

    # Length check
    length_points, length_msg = check_length(password)
    total_score += length_points
    feedback.append(length_msg)

    # Character types check
    char_points, char_fb = check_character_types(password)
    total_score += char_points
    feedback.extend(char_fb)

    # Pattern checks
    pattern_points, pattern_fb = check_patterns(password)
    total_score += pattern_points
    feedback.extend(pattern_fb)

    # Entropy check
    entropy = calculate_entropy(password)
    if entropy < CONFIG['MIN_ENTROPY']:
        feedback.append(f"{Fore.YELLOW}ℹ️ Low entropy ({entropy} bits). More randomness recommended.")
    else:
        total_score += 1
        feedback.append(f"{Fore.GREEN}✅ Good entropy ({entropy} bits)")

    # Ensure score stays within 0-10 range
    total_score = max(0, min(10, total_score))

    return total_score, feedback

def get_strength_label(score):
    """Get password strength label with color coding."""
    if score <= 2:
        return (f"{Fore.RED}Very Weak{Style.RESET_ALL}", "🔴")
    elif score <= 4:
        return (f"{Fore.YELLOW}Weak{Style.RESET_ALL}", "🟠")
    elif score <= 6:
        return (f"{Fore.YELLOW}Moderate{Style.RESET_ALL}", "🟡")
    elif score <= 8:
        return (f"{Fore.GREEN}Strong{Style.RESET_ALL}", "🟢")
    else:
        return (f"{Fore.MAGENTA}Very Strong{Style.RESET_ALL}", "🟣")

def main():
    print_banner()

    while True:
        password = input("Enter your password (or type 'quit' to exit):\n> ")

        if password.lower() == 'quit':
            print(f"\n{Fore.CYAN}Thank you for using the Password Strength Checker! Stay secure! 👋{Style.RESET_ALL}")
            break

        print(f"\nAnalyzing password strength", end="")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.3)
        print("\n")

        try:
            score, feedback = check_password_strength(password)
            strength_label, strength_emoji = get_strength_label(score)

            # Log the check (without storing the actual password)
            logging.info(f"Password check completed - Score: {score}/10")

            print(f"Password Strength: {strength_label} {strength_emoji}")
            meter = generate_password_meter(score)
            print(f"Strength Meter: {meter}")
            print(f"\nDetailed Analysis:")
            for fb in feedback:
                print(fb)

            print(f"\nOverall Score: {score}/10")

            if score <= 6:
                print(f"\n{Fore.YELLOW}Tips for a stronger password:")
                print("- Use at least 12 characters (20+ for excellent security)")
                print("- Combine uppercase, lowercase, numbers, and special characters")
                print("- Avoid common patterns and keyboard sequences")
                print("- Avoid repeated characters and personal information\n")

        except Exception as e:
            logging.error(f"Error during password check: {str(e)}")
            print(f"{Fore.RED}An error occurred while checking the password. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
