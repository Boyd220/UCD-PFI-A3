#!C:\Python311\python.exe
# Script:    Franken_Boyd_22206960_COMP40120_Assignment3.py
# Author:    Boyd Franken
# Purpose:   Assignment 3

import pandas as pd
import pytsk3
import datetime

# The numbers I noted with the comments refer to the question number in the assignment. This makes it easier for
# you (and me) to understand what comment belongs to what question.

# 1. Create objects with pytsk3 from the raw file so that it be processed further
image_filename = "assignment3image.raw"
disk_image = pytsk3.Img_Info(image_filename)
# Confirmation message that image loaded correctly by pytsk3
print('Loaded %s image file' % image_filename)
# Display size of image
print('The image file is %d bytes in size' %
      (disk_image.get_size()))

# Check how many partitions on image
part_table = pytsk3.Volume_Info(disk_image)
print('Number of partitions in partition table is %d' %
      part_table.info.part_count)
print('Partition number\tDesc\t\t\t\tStart Sector\tNumber of sectors')
print('---------------------------------------------------------------------')
partition_count = 0
partition_offsets = []
# Create a list to hold the partition information
part_list = []
file_list = []
# 3 Prompt the user for which partition to examine
part_num = input("Enter the partition number to examine, or '*' to examine all partitions: ")

# 2If the user entered '*', process all partitions
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
    file_system = pytsk3.FS_Info(disk_image, partition_offsets[part_num] * 512)
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

# 2 + 3. Create a DataFrame from the partition information
df = pd.DataFrame(part_list)

# 2. Write the DataFrame to a nicely formatted CSV file
df.to_csv("Franken_Boyd_22206960_Comp40120_output.csv", index=False, float_format='%.0f')
