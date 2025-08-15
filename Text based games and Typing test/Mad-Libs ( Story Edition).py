def create_MadLibs():
    print("Welcome to the Mad Libs game!")
    print("Please provide the following words:")

    # Collecting user inputs
    adjective = input("Adjective: ")
    noun = input("Noun: ")
    verb = input("Verb: ")
    adverb = input("Adverb: ")

    # Creating the Mad Libs story
    mad_libs_story = f"Once upon a time, there was a {adjective} {noun} that loved to {verb} {adverb}."

    # Displaying the story
    print("\nHere is your Mad Libs story:")
    print(mad_libs_story)
if __name__ == "__main__":
    create_MadLibs()
else:
    print("This script is intended to be run directly, not imported as a module.")
    print("Please run it directly to play the game.")
    print("Exiting the game.")
    exit(1)
    print("Thank you for playing!")
    print("Goodbye!")
    exit(0)
