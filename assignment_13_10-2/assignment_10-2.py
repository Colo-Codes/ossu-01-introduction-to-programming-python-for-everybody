# 10.2 Write a program to read through the mbox-short.txt and figure out the distribution by hour of the day for each of the messages. 
# You can pull the hour out from the 'From ' line by finding the time and then splitting the string a second time using a colon.
# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
# Once you have accumulated the counts for each hour, print out the counts, sorted by hour as shown below.

file_name = input("Enter file:")
if len(file_name) < 1:
    file_name = "mbox-short.txt"

file_handle = open(file_name)

hours_dict = dict()
matching_pattern = 'From '

for line in file_handle:
    if line.startswith(matching_pattern):
        words = line.split()
        # The hour is in the sixth position
        hour = words[5].split(':')[0]
        hours_dict[hour] = hours_dict.get(hour, 0) + 1

for k, v in sorted(hours_dict.items()):
    print(k, v)