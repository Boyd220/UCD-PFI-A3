# !C:\Python311\python.exe
# Script:    Franken_Boyd_22206960_COMP40120_Assignment3.py
# Author:    Boyd Franken
# Purpose:   Assignment 3
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Note:     Question 4, 5 and 6 are not done the way the assignment asked me to. With all the documentations available,
# For some reason none of my machines could make the second half of the assignment work in pytsk3.
# So after a few days of trying I decided to finish the assignment with OSwalker. It uses the same logic as I
# would've used with pytsk3 and presumably the same results. Hopefully I've shown I know the logic and code behind
# making this assignment with the way I did it.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import shutil
import pandas as pd
import pytsk3
import os
import datetime
import csv


# The numbers I noted with the comments refer to the question number in the assignment. This makes it easier for
# you (and me) to understand what comment and piece of code belongs to what question.

def Question1():
    # 1.  Open the assignment3image.raw image file for processing using pytsk3.
    image_filename = "assignment3image.raw"
    disk_image = pytsk3.Img_Info(image_filename)
    # Confirmation message that image loaded correctly by pytsk3
    print('Loaded %s image file' % image_filename)
    # Display size of image
    print('The image file is %d bytes in size' %
          (disk_image.get_size()))
    Question2and3(disk_image)


def Question2and3(disk_image):
    # 2 Check how many partitions on image
    part_table = pytsk3.Volume_Info(disk_image)
    print('Number of partitions in partition table is %d' %
          part_table.info.part_count)
    print('Partition number\tDesc\t\t\t\tStart Sector\tNumber of sectors')
    print('---------------------------------------------------------------------')
    partition_count = 0
    # Create a list to hold the partition information
    part_list = []

    # 3 Prompt the user for which partition to examine
    part_num = input("Enter the partition number to examine, or '*' to examine all partitions: ")

    # 2 + 3 If the user entered '*', process all partitions
    if part_num == "*":
        # Loop over the partitions in the partition table
        for part in part_table:
            # Process the partition
            print("Processing partition {}...".format(part.addr))
            part_list.append({
                "Partition Number": part.addr,
                "Type": part.desc,
                "Start Sector": part.start,
                "End Sector": part.start + part.len - 1,
                "Size (sectors)": part.len
            })
            partition_count += 1


    # 2 + 3 Otherwise, process the specified partition
    else:
        # Convert the partition number to an integer
        part_num = int(part_num)

        # Find the partition with the specified number
        part = next((p for p in part_table if p.addr == part_num), None)
        # If the partition was found, process it
        if part:
            # Process the partition
            print("Processing partition {}...".format(part_num))

            part_list.append({
                "Partition Number": part.addr,
                "Type": part.desc,
                "Start Sector": part.start,
                "End Sector": part.start + part.len - 1,
                "Size (sectors)": part.len
            })

        # Otherwise, print an error message
        else:
            print("Partition {} not found.".format(part_num))
    Question4(part_list)


# Define a function to convert file sizes to human-readable format
def convert_size(size_bytes):
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} bytes"


# 4.  Processing each selected partition should list the files found and the corresponding information on each file
# including its file size, modification date, creation date, etc.
def Question4(part_list):
    with open('Franken_Boyd_22206960_Comp40120_output.csv', 'w', newline='') as csvfile:
        # First write Q2 and Q3 to the .csv
        fieldnames = ["Partition Number", "Type", "Start Sector", "End Sector", "Size (sectors)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for part in part_list:
            writer.writerow(part)

        fieldnames = ['drive', 'path', 'name', 'type', 'size', 'created', 'last_modified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        mostrecentfile = ''
        Q5mostrecentfiletime = ''
        Q5mostrecentfilename = ''
        Q5mostrecentfilesize = ''
        writer.writeheader()

        # Traverse the drives recursively using os.walk(). I mounted the drives, that are within the provided image, on my machine with these letters. E was partition 2. F was partition 1. HFS I exported to
        # a directory called "HFS" on my local machine since windows cannot mount it nor read it.
        for drive in ['E:\\', 'F:\\', 'HFS']:
            num_files = 0
            newest_file = None
            largest_file = None
            largest_file_size = 0

            for root, dirs, files in os.walk(drive):
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    dir_stat = os.stat(dir_path)

                    # Write directory information to the CSV file
                    writer.writerow({
                        'drive': drive,
                        'path': os.path.abspath(dir_path),
                        'name': name,
                        'type': 'Directory',
                        'size': '-',
                        'created': datetime.datetime.fromtimestamp(dir_stat.st_ctime).strftime(
                            '%Y-%m-%d %H:%M:%S'),
                        'last_modified': datetime.datetime.fromtimestamp(dir_stat.st_mtime).strftime(
                            '%Y-%m-%d %H:%M:%S')
                    })

                for name in files:
                    file_path = os.path.join(root, name)
                    file_stat = os.stat(file_path)

                    # Write file information to the CSV file
                    writer.writerow({
                        'drive': drive,
                        'path': os.path.abspath(file_path),
                        'name': name,
                        'type': 'File',
                        'size': convert_size(file_stat.st_size),
                        'created': datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime(
                            '%Y-%m-%d %H:%M:%S'),
                        'last_modified': datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime(
                            '%Y-%m-%d %H:%M:%S')

                    })

                    # Update statistics on the files
                    num_files += 1
                    if newest_file is None or file_stat.st_mtime > newest_file.st_mtime:
                        newest_file = file_stat
                        mostrecentfile = name
                    if file_stat.st_size > largest_file_size:
                        largest_file_size = file_stat.st_size
                        largest_file = file_stat
                    if Q5mostrecentfiletime == '':
                        Q5mostrecentfiletime = newest_file.st_mtime
                        Q5mostrecentfilename = mostrecentfile
                        Q5mostrecentfilesize = file_stat.st_size
                        Q5mostrecentfilepath = file_path
                    if Q5mostrecentfiletime < newest_file.st_mtime:
                        Q5mostrecentfiletime = newest_file.st_mtime
                        Q5mostrecentfiletime1 = datetime.datetime.fromtimestamp(newest_file.st_mtime).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        Q5mostrecentfilename = mostrecentfile
                        Q5mostrecentfilesize = file_stat.st_size
                        Q5mostrecentfilepath = file_path

            # Print partition summary information to the terminal
            print(f"Drive: {drive}")
            print(f"Total number of files processed: {num_files}")
            if newest_file is not None:
                print(
                    f"Newest file: {mostrecentfile} {datetime.datetime.fromtimestamp(newest_file.st_mtime).strftime('%Y-%m-%d %H:%M:%S')} {newest_file.st_size} bytes")
            else:
                print("No files found")
            if largest_file is not None:
                print(f"Largest file found: {convert_size(largest_file.st_size)} {largest_file}")
            else:
                print("No files found")
            print("=" * 50)
    Question5(Q5mostrecentfiletime1, Q5mostrecentfilename, Q5mostrecentfilesize, Q5mostrecentfilepath)


# 5 Partition summary information should be printed to the terminal (for each partition if multiple are being processed)
# when the script is running.: Because it is not explicitly asked in the assigment, I did not output everything to a .csv file.
# I only outputted, Largest file in all partitions, most recent modified file in all partitions and total files over all partitions
# I mounted the drives, that are within the provided image, on my machine with these letters. E was partition 2. F was partition 1. HFS I exported to
# directory called "HFS" on my local machine since windows cannot mount it nor read it.
def Question5(Q5mostrecentfiletime, Q5mostrecentfilename, Q5mostrecentfilesize, Q5mostrecentfilepath):
    drives = ['E:\\', 'F:\\', 'HFS']
    alltotal = 0
    alllargest = 0
    Largestpath = ''
    alllargesttitle =''
    for drive in drives:
        print(f"Processing drive {drive}")

        for dirpath, dirnames, filenames in os.walk(drive):
            total_files = 0
            most_recent_file = None
            largest_file = None
            largest_file_size = 0
            namefile = ''
            size = 0

            for file in filenames:
                total_files += 1
                file_path = os.path.join(dirpath, file)
                file_stat = os.stat(file_path)
                print((file_path))
                if (alllargest < file_stat.st_size):
                    alllargest = file_stat.st_size
                    Largestpath = file_path
                    alllargesttitle = file_path
                if largest_file_size < file_stat.st_size:
                    largest_file_size = file_stat.st_size
                    largest_file = file_stat

                if most_recent_file is not None and most_recent_file.st_mtime < file_stat.st_mtime:
                    most_recent_file = file_stat
                    namefile = file_stat
                    size = file_stat.st_size
                elif most_recent_file is None:
                    most_recent_file = file_stat
            alltotal += total_files

            print(f"Total number of files processed: {total_files}")
            print(
                f"Most recently modified file: {namefile} datetime: {datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')} size: {size} bytes")
            print(f"Largest file found: {convert_size(largest_file_size)} {largest_file}")
    print(f"Grand total number of files processed: {alltotal}")
    print(
        f"Most recently modified file: {Q5mostrecentfilename} datetime: {Q5mostrecentfiletime} size: {Q5mostrecentfilesize} bytes")
    print(f"Largest file found: {alllargesttitle} with size: {convert_size(alllargest)}")
    with open("Franken_Boyd_22206960_Comp40120_output.csv", 'a', newline='') as csvfile:
        fieldnames = ['Total files', 'Most recent modified file', 'Largest file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        recentlymod = "title: " + Q5mostrecentfilename + " time: " + Q5mostrecentfiletime + " " + str(Q5mostrecentfilesize) + " bytes"
        largestfile= "title: " + alllargesttitle + " size: "+convert_size(alllargest)
        writer.writerow({
            'Total files': alltotal,
            'Most recent modified file': str(recentlymod),
            'Largest file': str(largestfile)

        })

    Question6(Q5mostrecentfilepath, Largestpath)


# 6. Prompt the user to see what file they would like to carve from the image between these two choices: the most
# recently modified file or the largest. Whichever is selected should be carved and stored in the same folder as your
# python script.
def Question6(most_recent_file, largest_file):
    # Prompt the user to choose which file to carve
    while True:
        choice = input("Enter 'R' to carve the most recently modified file, or 'L' to carve the largest file: ")
        if choice.lower() == 'r':
            file_to_carve = most_recent_file
            break
        elif choice.lower() == 'l':
            file_to_carve = largest_file
            break
        else:
            print("Invalid input. Please enter 'R' or 'L'.")

    # Carve the selected file and store it in the same folder as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    carved_file_path = os.path.join(script_dir, os.path.basename(file_to_carve))
    shutil.copyfile(file_to_carve, carved_file_path)
    print(f"{file_to_carve} has been carved and saved as {carved_file_path}.")


Question1()
