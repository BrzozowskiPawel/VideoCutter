import time
import cv2
import os
from termcolor import colored
import random
import string
from csv import writer


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_folder_for_frames():
    # Declaration of constants that are paths.
    MYDIR = "output/ (files will be saved here)"
    CHECK_FOLDER = os.path.isdir(MYDIR)

    # If folder doesn't exist, then create it (and subfolders).
    if not CHECK_FOLDER:
        if not os.path.isdir(MYDIR):
            os.makedirs(MYDIR)
            print(colored("Created output/", "green"))

    else:
        message = "folder already exists! -> Delete 'output' folder or single one that already exists: "+MYDIR
        print(colored(message, 'red'))
        # If folder already exist we are exiting program with code 10.
        exit(10)


def divide_video_into_frames(path, skipped = 5):
    # Total number of frames (not only skipped)
    total_number_of_frames = 0

    # Number of photos skipper to before saving
    skipped_index = 0

    # Number of photos saved
    saved_photos = 0

    # Start counting the time it took to complete this function
    start_time = time.time()

    # Creating variable that contain path to the folder
    # folder_path = create_folder_for_frames(path)

    # Variables responsible for counting frames in the video.
    number_of_frame = 1

    # Here the image is loaded for the test of correct operation
    # VideoCapture() takes filename as argument or you can type device index.
    captured_video = cv2.VideoCapture(path)

    # MOVIE DURATON SECUNDS
    fps = captured_video.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_miliseconds = frame_count / fps

    # Data List to CVS (order -> proces time, creted frames , total frames, vid duration, path_name)
    CSV_LIST = []

    # Random string seed:
    string_seed = get_random_string(6)
    while True:
        # Getting frame from video.
        # This function returns 2 variables: 1. is flag if frame was read correctly, 2. is frame
        success, frame = captured_video.read()

        # Save the photo as consecutive numbers.
        if success:
            total_number_of_frames += 1
            if skipped == skipped_index:
                cv2.imwrite("output/"+str(string_seed)+str(number_of_frame)+".jpg", frame)
                saved_photos += 1
                skipped_index = 0
            number_of_frame += 1

        elif not success:
            final_info = f"Process done (this took {round((time.time() - start_time), 2)} seconds), created {saved_photos} frames from video (total frames: {total_number_of_frames}). Video duration: {round(duration_miliseconds, 2)}"


            CSV_LIST.append(str(round((time.time() - start_time), 2)).replace(".",",")) #proces time
            CSV_LIST.append(saved_photos) # creted frames
            CSV_LIST.append(total_number_of_frames) # total frames
            CSV_LIST.append(str(round(duration_miliseconds, 2)).replace(".",","))# movie duration
            CSV_LIST.append(path) # file name (to be precise path)

            with open('stats.csv', 'a') as f_object:

                # Pass this file object to csv.writer()
                # and get a writer object
                writer_object = writer(f_object)

                # Pass the list as an argument into
                # the writerow()
                writer_object.writerow(CSV_LIST)

                # Close the file object
                f_object.close()

            print(colored(final_info, 'green'))

            break
        skipped_index += 1

    return saved_photos