import os, shutil
import cv2
from pathlib import Path
import copy_to_all as copy_all_content_to_all_directory

def extract_frames(video_path, output_folder, frame_interval=1):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_number = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_number % frame_interval == 0:
            frame_filename = f"{frame_number:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)
            cv2.imwrite(frame_path, frame)
            
        frame_number += 1
    
    cap.release()
    print(f"Extracted {frame_number // frame_interval} frames from {video_path} to {output_folder}")

def process_video_directory(input_directory, output_directory, frame_interval=1):
    for root, _, files in os.walk(input_directory):
        print(root)
        for file in files:
            if os.path.exists(file): continue
            if file.endswith(('.mp4', '.avi', '.mkv')):
                video_path = os.path.join(root, file)
                output_name =Path(video_path).stem + "_frames"
                extract_frames(video_path, output_directory+'/'+output_name, frame_interval)
            
def main(
    input_directory,
    output_directory,
    frame_interval = 10  # Set the desired frame extraction interval)
):
    
    process_video_directory(input_directory, output_directory, frame_interval)
    
    target_directory = output_directory
    copy_all_content_to_all_directory(target_directory)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('-D','--input_directory', help='folder of videos', default = "./videos")
    ap.add_argument('-O','--output_directory', help='folder of videos', default = "./frames")
    ap.add_argument('-F','--frame_interval', type=int,
                    help='Frame interval for extraction', default=150)
    args = ap.parse_args()
    
    main(args.input_directory, args.output_directory, args.frame_interval)

    

import os, shutil
import cv2
from pathlib import Path


def extract_frames(video_path, output_folder, frame_interval=1):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_number = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_number % frame_interval == 0:
            frame_filename = f"{frame_number:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)
            cv2.imwrite(frame_path, frame)
            
        frame_number += 1
    
    cap.release()
    print(f"Extracted {frame_number // frame_interval} frames from {video_path} to {output_folder}")

def process_video_directory(input_directory, output_directory, frame_interval=1):
    for root, _, files in os.walk(input_directory):
        print(root)
        for file in files:
            if os.path.exists(file): continue
            if file.endswith(('.mp4', '.avi', '.mkv')):
                video_path = os.path.join(root, file)
                output_name =Path(video_path).stem + "_frames"
                extract_frames(video_path, output_directory+'/'+output_name, frame_interval)

def copy_all_content_to_all_directory(target_directory):
    current_directory = Path.cwd()/target_directory
    call_directory = os.path.join(current_directory, 'all')

    # Create 'call' directory if it doesn't exist
    if not os.path.exists(call_directory):
      os.mkdir(call_directory)

    # Iterate through subdirectories
    for fp in Path(current_directory).glob('**/*'):
      if fp.parent.name =='all': continue
      if os.path.isfile(fp):  # Check if it's a file and not a directory
          fn = Path(fp).parent.name + '_' + Path(fp).name
          destination_path = os.path.join(call_directory, fn)
          shutil.copy(fp, destination_path)
          print(f"copied '{fp}' to 'all' directory")
            
def main(
    input_directory,
    output_directory,
    frame_interval = 10  # Set the desired frame extraction interval)
):
    
    process_video_directory(input_directory, output_directory, frame_interval)
    
    target_directory = 'frames'
    copy_all_content_to_all_directory(target_directory)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('-D','--input_directory', help='folder of videos', default = "./videos")
    ap.add_argument('-O','--output_directory', help='folder of videos', default = "./frames")
    ap.add_argument('-F','--frame_interval', type=int,
                    help='Frame interval for extraction', default=150)
    args = ap.parse_args()
    
    main(args.input_directory, args.output_directory, args.frame_interval)

    
