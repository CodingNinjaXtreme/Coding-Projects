def caesar_cipher(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            # Determine ASCII offset based on uppercase/lowercase
            offset = ord('A') if char.isupper() else ord('a')

            # Convert char to 0-25 index, apply shift with wrap-around
            shifted_index = (ord(char) - offset + shift) % 26

            # Convert back to character
            result += chr(shifted_index + offset)
        else:
            # Non-letter characters remain unchanged
            result += char

    return result

# Get user input
message = input("Enter the message to encrypt: ")
shift_amount = int(input("Enter the shift number: "))

# Encrypt and display
encrypted = caesar_cipher(message, shift_amount)
print("Encrypted message:", encrypted)
