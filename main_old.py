# main.py

from core.personality import SpectraPersonality
from core.memory import SpectraMemory

def main():
    spectra = SpectraPersonality()
    memory = SpectraMemory()

    print(spectra.describe())
    print("How can I support you today, Richie?\n")

    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye, Richie. Be gentle with yourself.")
            break
        memory.remember(f"You said: {user_input}")
        print("Noted. I'm always listening.")

if __name__ == "__main__":
    main()
