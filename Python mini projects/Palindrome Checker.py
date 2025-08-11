import unicodedata

text = input("Enter a word or phrase to check if it's a palindrome: ")

# Remove accents
text = ''.join(
    char for char in unicodedata.normalize('NFD', text)
    if unicodedata.category(char) != 'Mn'
)

# Normalize: lowercase + remove non-alphanumeric characters (spaces, punctuation, etc.)
cleaned = "".join(char.lower() for char in text if char.isalnum())

# Check palindrome
if cleaned == cleaned[::-1]:
    print("Palindrome!")
else:
    print("Not a palindrome.")
