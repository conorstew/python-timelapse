import os
import subprocess

# Directory where your images are stored
images_folder = "2025-01-11"
image_directory = f"./timelapses/{images_folder}"

# Output video filename
output_video = f"{image_directory}/videos/output_video.mp4"

# Frame rate is how many images to show per second
images_to_show_per_second = 80
frame_rate = 1 / images_to_show_per_second


def get_unique_filename(directory, filename):
    """
    Check if a file exists, and if it does, generate a unique filename by appending a number.
    """
    base_name, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename

    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base_name}_{counter}{ext}"
        counter += 1

    return unique_filename

def create_video(image_directory, frame_rate):
    # Make sure the output directory exists
    output_directory = os.path.join(image_directory, "videos")
    os.makedirs(output_directory, exist_ok=True)

    # Determine unique output filename
    base_output_filename = "output_video.mp4"
    output_video = get_unique_filename(output_directory, base_output_filename)

    # Check if FFmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, 
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("FFmpeg is not installed. Please install FFmpeg and try again.")
        return
    
    # Construct the FFmpeg command
    ffmpeg_command = [
        "ffmpeg",
        "-framerate", str(1 / frame_rate),    # e.g., if frame_rate = 0.2, this becomes 5
        "-pattern_type", "glob",
        "-i", os.path.join(image_directory, "image_*.jpg"), 
        "-vf", "format=yuv420p",             # Ensure output uses yuv420p pixel format
        "-c:v", "libx264",
        os.path.join(output_directory, output_video)
    ]
    
    # Run FFmpeg
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Video successfully created: {os.path.join(output_directory, output_video)}")
    except subprocess.CalledProcessError as e:
        print(f"Error while creating video: {e}")

# Create the video
create_video(image_directory, frame_rate)
