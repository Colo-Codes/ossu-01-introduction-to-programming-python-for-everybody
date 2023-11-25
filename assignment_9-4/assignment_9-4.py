# 9.4 Write a program to read through the mbox-short.txt and figure out who has sent the greatest number of mail messages. 
# The program looks for 'From ' lines and takes the second word of those lines as the person who sent the mail. The program 
# creates a Python dictionary that maps the sender's mail address to a count of the number of times they appear in the file. 
# After the dictionary is produced, the program reads through the dictionary using a maximum loop to find the most prolific 
# committer.

file_name = input("Enter file: ")
if len(file_name) < 1:
    file_name = "mbox-short.txt"
file_handle = open(file_name)

line_starting_string = 'From '
emails = {}

for line in file_handle:
    if line.startswith(line_starting_string):
        email = line.split()[1]
        emails[email] = emails.get(email, 0) + 1

max_key = ''
max_value = 0
for key, value in emails.items():
    if value > max_value:
        max_key = key
        max_value = value

print(max_key, max_value)