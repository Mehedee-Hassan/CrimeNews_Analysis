import os

root_path = os.path.abspath('..')
print("files in :", root_path)
temp_crime_files = root_path + "\\temp_files\\crime\\"
temp_n_crime_files = root_path + "\\temp_files\\ncrime\\"

files = [file for file in os.listdir(temp_crime_files) if os.path.isfile(temp_crime_files+"\\"+file)]

# Iterate through every file

files2  = os.listdir(temp_crime_files)

if os.path.isfile(files2[0]):
    print("file")


print("debug##", temp_crime_files,len(files))