import os
import cv2

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
    print(f"Extracted {frame_number // frame_interval} frames from {video_path}.")

def process_video_directory(input_directory, frame_interval=1):
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv')):
                video_path = os.path.join(root, file)
                output_folder = os.path.splitext(video_path)[0] + "_frames"
                extract_frames(video_path, output_folder, frame_interval)

def main(
    input_directory,
    frame_interval = 10  # Set the desired frame extraction interval)
):
    
    process_video_directory(input_directory, frame_interval)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('-D','--input_directory', help='folder of videos', default = "./crown-plaza")
    ap.add_argument('-F','--frame_interval', type=int,
                    help='Frame interval for extraction', default=150)
    args = ap.parse_args()
    
    main(args.input_directory, args.frame_interval)

    
