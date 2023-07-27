import os
 
# assign directory
directory = 'Data/Labels/Train'
 
# iterate over files in
# that directory
count = 0
for filename in os.scandir(directory):
    count += 1
    if filename.is_file():
        print(filename.path)
        
        # with open(filename.path, 'r') as file :
        #     filedata = file.read()

        # # Replace the target string
        # filedata = filedata.replace('Nail', '0')

        # # Write the file out again
        # with open(filename.path, 'w') as file:
        #     file.write(filedata)
print(f'Number Of Files: {count}')