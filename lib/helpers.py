import sys


def do_faultsim() -> bool:
    """Ask user if run fault simulation

    Returns:
        _type_: True if proceed
    """
    print(f"Do you want to run fault simulation?")
    yes = {"yes", "y", "ye", ""}
    no = {"no", "n"}
    choice = input().lower()
    if choice in yes:
        return True
    elif choice in no:
        sys.exit(2)
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")
