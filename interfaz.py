import os
import time

def clear_screen():
    """Clear the terminal screen for a clean interface."""
    os.system("cls" if os.name == "nt" else "clear")

def show_logo():
    """Display the logo at the top of the interface."""
    logo = r'''
    88b           d88  88888888888  ,ad8888ba,    ,ad8888ba,    88888888888  88           88  8b        d8  
    888b         d888  88          d8"'    `"8b  d8"'    `"8b   88           88           88   Y8,    ,8P   
    88`8b       d8'88  88         d8'           d8'        `8b  88           88           88    `8b  d8'    
    88 `8b     d8' 88  88aaaaa    88            88          88  88aaaaa      88           88      Y88P      
    88  `8b   d8'  88  88"""""    88            88          88  88"""""      88           88      d88b      
    88   `8b d8'   88  88         Y8,           Y8,        ,8P  88           88           88    ,8P  Y8,    
    88    `888'    88  88          Y8a.    .a8P  Y8a.    .a8P   88           88           88   d8'    `8b   
    88     `8'     88  88888888888  `"Y8888Y"'    `"Y8888Y"'    88           88888888888  88  8P        Y8
    
                                            by: K1loWatt
    '''
    print(logo)
    print("=" * 50)

def menu():
    """Display the menu options."""
    print("Choose an option:")
    print("[1] Option One")
    print("[2] Option Two")
    print("[3] Exit")

def option_one():
    """Perform the first option."""
    print("\nYou selected Option One!")
    time.sleep(2)  # Simulate some processing

def option_two():
    """Perform the second option."""
    print("\nYou selected Option Two!")
    time.sleep(2)  # Simulate some processing

def main():
    """Main loop of the shell interface."""
    while True:
        # Clear the screen and display the interface
        clear_screen()
        show_logo()
        menu()
        
        # Get user input
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            option_one()
        elif choice == "2":
            option_two()
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)

# Run the interface
if __name__ == "__main__":
    main()

