import time
from termcolor import colored

import list_of_files
import divide_video


total_number_of_saved_photos = 0

# Information about the program start (start time)
start_time = time.time()
message = f'Program started {time.strftime("%H:%M:%S", time.localtime())}'
print(colored(message,'blue'))

# Function responsible for obtaining a list of files (with the .mp4 extension),
# that have not yet been subjected to obliteration.
# Thanks to this, you can send new files to the input directory without deleting the previously used ones.
list_of_files = list_of_files.get_list_of_files()

# Create output
divide_video.create_folder_for_frames()

# Display information regarding how many files will be exposed to the program.
message_how_many_files = f'{len(list_of_files)} new files to blur faces and slice into frames.'
print(colored(message_how_many_files,'yellow'))
if len(list_of_files) > 0:
    print(list_of_files)
    print(colored('Please wait, application is running.', 'magenta'))

if len(list_of_files) > 0:
    for file in list_of_files:
        # Divide the movie into frames and save them in the specific folders
        number_of_saved_photos = divide_video.divide_video_into_frames(file, skipped=4)
        total_number_of_saved_photos += number_of_saved_photos

elif len(list_of_files) == 0:
    print(colored("There is no new videos (mp4) to blur and slice. Check your output folder.", 'red'))
    # If there is no new videos, code 20.
    exit(20)

# Information about the program end (end time)
message = f'Program ended {time.strftime("%H:%M:%S", time.localtime())}, this took: {round((time.time() - start_time),2)} seconds.'
print(colored(message,'blue'))

message = f'Saved total: {total_number_of_saved_photos} photos, for all data see stats.csv'
print(colored(message,'magenta'))