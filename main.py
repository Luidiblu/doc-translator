
import openai
import os
import re
import shutil
from time import sleep

# Initialize GPT-3 API
openai.api_key = 'YOUR_API_KEY_HERE'

# Translate English text to Portuguese
def translate_to_portuguese(eng_text):
    print(f'\n{"-"*40}\nTranslating section...\n{"-"*40}\n"{eng_text[:50]}..."')  # Printing first 50 chars
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{eng_text}\nTranslate the above text to Brazilian Portuguese but DON'T translate technical norms,URLs, edit the text format or add new text to it. The text to be translated starts now:",
        temperature=0.4,
        max_tokens=1000
    )
    return response.choices[0].text.strip()

# Main function
def main():
    directory = './hacktricks-remix'  # Replace with your directory path
    print(f'\n{"="*40}\nProcessing files in directory: {directory}\n{"="*40}')

    # Create a directory for the translated files
    translated_dir = './translated'
    if not os.path.exists(translated_dir):
        os.makedirs(translated_dir)

    # Iterate over each file or directory in the main directory
    for root, dirs, files in os.walk(directory):
        # Create corresponding subdirectories in the "translated" directory
        translated_subdir = os.path.join(translated_dir, os.path.relpath(root, directory))
        if not os.path.exists(translated_subdir):
            os.makedirs(translated_subdir)

        # Translate and copy files
        for filename in files:
            file_path = os.path.join(root, filename)
            translated_file_path = os.path.join(translated_subdir, filename)

            print(f'\n{"-"*40}\nProcessing file: {file_path}\n{"-"*40}')

            with open(file_path, 'r') as file:
                content = file.read()

                # Split the Markdown text by headers
                sections = re.split(r'(\n#+ .+\n)', content)

                portuguese_text = ''
                for section in sections:
                    sleep(5)
                    portuguese_section = translate_to_portuguese(section.strip())
                    portuguese_text += portuguese_section + '\n'

                # Save the translated text to a new file in the "translated" directory
                with open(translated_file_path, 'w') as translated_file:
                    translated_file.write(portuguese_text)

        # Copy directories recursively
        for dirname in dirs:
            dir_path = os.path.join(root, dirname)
            translated_dir_path = os.path.join(translated_subdir, dirname)
            #shutil.copytree(dir_path, translated_dir_path)

    print('\nTranslation finished.')

if __name__ == "__main__":
    main()

