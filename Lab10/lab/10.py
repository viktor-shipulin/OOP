import re
with open("mockdata.txt", "r") as f:
    data = f.readlines()


name_pattern = r"([A-Za-z]+)"
surname_pattern = r"\t([A-Za-z]+)"
filetype_pattern = r"\.([a-z]+)"

with open("name.txt", "w") as name_file, \
     open("surname.txt", "w") as surname_file, \
     open("typeFile.txt", "w") as type_file:

    for line in data:
        name_match = re.match(name_pattern, line)
        if name_match:
            name_file.write(name_match.group(1) + "\n")
            
        surname_match = re.search(surname_pattern, line)
        if surname_match:
            surname_file.write(surname_match.group(1) + "\n")

        filetype_match = re.search(filetype_pattern, line)
        if filetype_match:
            type_file.write(filetype_match.group(1) + "\n")
