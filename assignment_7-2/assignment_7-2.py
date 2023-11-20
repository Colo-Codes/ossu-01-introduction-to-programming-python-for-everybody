# 7.2 Write a program that prompts for a file name, then opens that file and reads through the file, looking for lines of the form:
# X-DSPAM-Confidence:    0.8475
# Count these lines and extract the floating point values from each of the lines and compute the average of those values and produce 
# an output as shown below. Do not use the sum() function or a variable named sum in your solution.
# You can download the sample data at http://www.py4e.com/code3/mbox-short.txt when you are testing below enter mbox-short.txt 
# as the file name.

# Use the file name mbox-short.txt as the file name
file_name = input("Enter file name: ")
try:
    file_handle = open(file_name)
except:
    print("Error: file not found")
    quit()

matching_lines_count = 0
aggregated_value = 0.0

for line in file_handle:
    if not line.startswith("X-DSPAM-Confidence:"):
        continue
    matching_lines_count = matching_lines_count + 1
    dot_index = line.find('.')
    matching_line_value = line[dot_index - 1:]
    
    aggregated_value = aggregated_value + float(matching_line_value)

average = aggregated_value / float(matching_lines_count)

print("Average spam confidence:", average)