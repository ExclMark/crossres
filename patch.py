#!/usr/bin/env python3

import os
import shutil
import re
import plistlib
from datetime import datetime, timezone

print("\033[37m")
print(r"    _________         _______                __________               ")
print(r"    \_   ___ \_______ \   _  \   ______ _____\______   \ ____   ______")
print(r"    /    \  \/\_  __ \/  /_\  \ /  ___//  ___/|       _// __ \ /  ___/")
print(r"    \     \____|  | \/\  \_/   \\___ \ \___ \ |    |   \  ___/ \___ \ ")
print(r"     \______  /|__|    \_____  /____  >____  >|____|_  /\___  >____  >")
print(r"            \/               \/     \/     \/        \/     \/     \/ ")
print("\033[0m")

print("\033[37m[   ]\033[0m Resetting First Run Date...", end="")

# Set os path
userPath = os.path.expanduser('~')

# Open plist configuration file
try:
    with open(f'{userPath}/Library/Preferences/com.codeweavers.CrossOver.plist', 'rb') as f:
        pl = plistlib.load(f)
except FileNotFoundError:
    print("\r\033[K\033[37m[\033[31m x \033[37m]\033[0m Resetting First Run Date... \033[37mFailed\033[0m")
    print(f"- Could not locate the \033[37m{userPath}/Library/Preferences/com.codeweavers.CrossOvera.plist\033[0m file.")
    exit()

# Set first run date to correct time
pl['FirstRunDate'] = datetime.now(timezone.utc)

# Save plist
with open(f'{userPath}/Library/Preferences/com.codeweavers.CrossOver.plist', 'wb') as f:
    plistlib.dump(pl, f)

print("\r\033[K\033[37m[\033[32m + \033[37m]\033[0m Resetting Crossover FirstRunDate... \033[37mDone\033[0m")
print("\033[37m[\033[32m   \033[37m]\033[0m Locating Bottles...", end="")

# Locate bottles
bottles = os.path.expanduser(f"{userPath}/Library/Application Support/CrossOver/Bottles/")
bottles_list = [d for d in os.listdir(bottles) if os.path.isdir(os.path.join(bottles, d))]

if not bottles_list:
    print("\r\033[K\033[37m[\033[31m x \033[37m]\033[0m No bottles found in CrossOver.\n")
    print("You can now use the trial version of CrossOver for 14 days!")
    exit()
else:
    print(f"\r\033[K\033[37m[\033[32m + \033[37m]\033[0m Locating Bottles... \033[37mFound {len(bottles_list)}\033[0m")

def reset_bottle(bottle_name):
    print(f"┏━━━ {bottle_name}")
    print("┃ \033[37m[   ]\033[0m Creating backup...", end="")

    # Locate the registry file and create a backup
    regfile = os.path.expanduser(f"{userPath}/Library/Application Support/CrossOver/Bottles/{bottle_name}/system.reg")
    bakfile = regfile + ".bak"
    try:
        shutil.copy2(regfile, bakfile)
        print(f"\r┃ \033[K\033[37m[\033[32m + \033[37m]\033[0m Backup created for \033[37m{bottle_name}\033[0m: \033[37m{bakfile}\033[0m")
    except FileNotFoundError:
        print(f"\r┃ \033[K\033[37m[\033[31m x \033[37m]\033[0m Backup failed for \033[37m{bottle_name}\033[0m: \033[37mFile not found\033[0m")
        print(f"┗━━━ Failed to reset \033[37m{bottle_name}\033[0m.")
        return

    print("┃ \033[37m[   ]\033[0m Deleting Install Time lines...", end="")

    # Compile the regex pattern
    pattern = re.compile(r"\[Software\\\\CodeWeavers\\\\CrossOver\\\\cxoffice\] [0-9]*")

    # Read the file and search for match line
    with open(regfile, 'r') as f:
        lines = f.readlines()

    match_line_num = None
    for i, line in enumerate(lines):
        if pattern.search(line):
            match_line_num = i
            break

    # If match is found, delete the 5 lines starting from the match line
    if match_line_num is not None:
        new_lines = lines[:match_line_num] + lines[match_line_num + 5:]
        with open(regfile, 'w') as f:
            f.writelines(new_lines)
        print(f"\r┃ \033[K\033[37m[\033[32m + \033[37m]\033[0m Lines deleted for \033[37m{bottle_name}\033[0m.")
    else:
        print(f"\r┃ \033[K\033[37m[ - ]\033[0m \033[37m{bottle_name}\033[0m is already reset.")

    print(f"┗━━━ \033[37m{bottle_name}\033[0m is now reset.")

while True:
    print()
    print("\033[37m| \033[0m\033[1m1\033[0m \033[37m|\033[0m Reset a specific bottle")
    print("\033[37m| \033[0m\033[1m2\033[0m \033[37m|\033[0m Reset all bottles")
    print("\033[37m| \033[0m\033[1m3\033[0m \033[37m|\033[0m Exit")
    print()
    choice = input("Enter your choice: \033[1m").strip()
    print("\033[0m")

    # Exit
    if choice == '3':
        print("Exiting...")
        exit()

    # Reset all bottles
    elif choice == '2':
        print("Resetting all bottles...\n")

        for bottle_name in bottles_list:
            reset_bottle(bottle_name)

        print("\nAll bottles reset!")
        print("You can now use the trial version of CrossOver for 14 days!")
        break

    # Reset specific bottle
    elif choice == '1':
        print("Available bottles:")

        for i, bottle_name in enumerate(bottles_list, start=1):
            print(f"\033[37m| \033[0m\033[1m{i}\033[0m \033[37m|\033[0m {bottle_name}")
        print()

        bottle_choice = input("Enter the number of the bottle to reset: \033[1m").strip()
        print("\033[0m")

        # Validate bottle choice and reset the selected bottle
        if bottle_choice.isdigit() and 1 <= int(bottle_choice) <= len(bottles_list):
            selected_bottle = bottles_list[int(bottle_choice) - 1]
            reset_bottle(selected_bottle)
        else:
            print("Invalid bottle choice. Please try again.")

    else:
        print("Invalid choice. Please try again.")