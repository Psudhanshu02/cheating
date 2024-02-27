import subprocess
from datetime import datetime, timedelta
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def modify_filename(args):
    original_filename, elapsed_seconds, i = args
    timestamp_str = original_filename.split('.')[0]
    original_time = datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
    
    # Calculate new timestamp by adding elapsed seconds
    new_datetime = original_time - timedelta(seconds=i * elapsed_seconds)
    
    # Switch the date if more than 24 hours have elapsed
    if i * elapsed_seconds >= 24 * 3600:
        new_datetime = new_datetime.replace(day=original_time.day - 1)
    
    new_timestamp_str = new_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    new_filename = original_filename.replace(timestamp_str, new_timestamp_str)
    
    return new_filename

def copy_video(args):
    original_filename, new_filename = args
    cp_command = f"cp {original_filename} {new_filename}"
    subprocess.run(cp_command, shell=True)
    print(f'Video copied: {new_filename}')

def copy_video_with_elapsed_time(original_filename, elapsed_seconds, num_copies):
    args_list = [(original_filename, elapsed_seconds, i) for i in range(num_copies)]
    new_filenames = ThreadPoolExecutor().map(modify_filename, args_list)
    pool_args = [(original_filename, new_filename) for new_filename in new_filenames]
    
    # Use ThreadPoolExecutor to concurrently execute the copy_video function
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(copy_video, arg) for arg in pool_args]
        for future in as_completed(futures):
            future.result()

# Example usage
original_filename = '2024-01-01_15-25-07.mp4'
elapsed_seconds = 30
num_copies = 100000

copy_video_with_elapsed_time(original_filename, elapsed_seconds, num_copies)
