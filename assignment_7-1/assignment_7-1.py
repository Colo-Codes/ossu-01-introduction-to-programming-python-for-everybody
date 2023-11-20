# 7.1 Write a program that prompts for a file name, then opens that file and reads through the file, and print the contents of the file in upper case. 
# Use the file words.txt to produce the output below.
# You can download the sample data at http://www.py4e.com/code3/words.txt

# Use words.txt as the file name
file_name = input("Enter file name: ")

try:
    file_handle = open(file_name)
except:
    print('Error: file not found')
    quit()

file_content = file_handle.read()
print(file_content.upper().rstrip())