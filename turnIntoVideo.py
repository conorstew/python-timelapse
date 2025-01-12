import os
import subprocess

# Directory where your images are stored
images_folder = "2025-01-11"
image_directory = f"./timelapses/{images_folder}" 

# Output video filename
output_video = f"{image_directory}/videos/output_video.mp4"

# Frame rate (number of images shown per second in the video)
frame_rate = 1 / 5  # Change to 1/5 for 5-second intervals per image

def create_video(image_directory, output_video, frame_rate):
    # Make sure FFmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("FFmpeg is not installed. Please install FFmpeg and try again.")
        return

    # Run FFmpeg command
    try:
        ffmpeg_command = [
            "ffmpeg",
            "-framerate", str(1 / frame_rate),
            "-i", os.path.join(image_directory, "image_%Y%m%d_%H%M%S.jpg"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_video
        ]
        subprocess.run(ffmpeg_command, check=True)
        print(f"Video successfully created: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error while creating video: {e}")

# Replace with your actual path and output filename
create_video(image_directory, output_video, frame_rate)
