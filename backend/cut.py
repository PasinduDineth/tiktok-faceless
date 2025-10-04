import os
import shutil
import cv2

def process_videos(root_dir, output_dir):
    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(root_dir):
        if file.lower().endswith(".mp4"):
            video_path = os.path.join(root_dir, file)
            video_name = os.path.splitext(file)[0]

            # Create a folder for this video
            video_folder = os.path.join(output_dir, video_name)
            os.makedirs(video_folder, exist_ok=True)

            # Move the video to its new folder
            new_video_path = os.path.join(video_folder, file)
            if not os.path.exists(new_video_path):
                shutil.move(video_path, new_video_path)

            # Open video with OpenCV
            cap = cv2.VideoCapture(new_video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps

            frame_number = int(fps * 1)  # Start at 1 second
            step = int(fps * 4)          # Every 4 seconds
            frame_index = 0

            while frame_number < total_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                if not ret:
                    break

                frame_filename = os.path.join(video_folder, f"frame_{frame_index:04d}.jpg")
                cv2.imwrite(frame_filename, frame)

                frame_index += 1
                frame_number += step

            cap.release()

    print("✅ All videos processed successfully.")

# Example usage:
root_directory = "./"      # Folder where your .mp4 files are
output_directory = "./processed" # Where folders will be created
process_videos(root_directory, output_directory)
