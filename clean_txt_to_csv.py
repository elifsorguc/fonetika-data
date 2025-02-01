# Function to clean the input text file and save it as a proper TXT file
def clean_txt_to_txt(input_txt, output_txt):
    # Open the input text file
    with open(input_txt, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Prepare a list to hold the cleaned words
    cleaned_words = []

    # Process each line to remove the unnecessary delimiters (;;;)
    for line in lines:
        # Strip extra spaces and split by ';;;'
        words = line.strip().split(';;;')

        # Only keep non-empty words and add them to the list
        for word in words:
            if word.strip() and word.strip() != ";":  # Check if the word is not empty or just a semicolon
                cleaned_words.append(word.strip())  # Add word to the list

    # Write the cleaned words into a TXT file
    with open(output_txt, 'w', encoding='utf-8') as txtfile:
        for word in cleaned_words:
            txtfile.write(f"{word}\n")  # Write each word in a new line

    print(f"Cleaned TXT saved to {output_txt}")

# Example usage
input_txt = 'words.txt'  # The name of your input text file with the words
output_txt = 'cleaned_words.txt'  # The output TXT file to save

# Call the function to clean and convert the file
clean_txt_to_txt(input_txt, output_txt)
