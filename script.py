import cv2
import os
import time
from datetime import datetime

import objc
from Foundation import NSArray
from AVFoundation import AVCaptureDevice


import subprocess


def prevent_sleep():
    """Prevent the Mac from sleeping using the caffeinate command."""
    global caffeinate_process
    caffeinate_process = subprocess.Popen(["caffeinate", "-s"])
    print("Sleep prevention enabled.")


def allow_sleep():
    """Allow the Mac to sleep by terminating the caffeinate process."""
    global caffeinate_process
    if caffeinate_process:
        caffeinate_process.terminate()
        caffeinate_process = None
        print("Sleep prevention disabled.")


def list_cameras_with_names():
    available_cameras = []

    # Get all available video devices using macOS APIs
    devices = AVCaptureDevice.devicesWithMediaType_("vide")
    device_list = NSArray.arrayWithArray_(devices)

    for index, device in enumerate(device_list):
        device_name = str(device.localizedName())
        # Verify if the device is accessible via OpenCV
        camera = cv2.VideoCapture(index)
        if camera.isOpened():
            available_cameras.append({"index": index, "name": device_name})
            camera.release()
        else:
            print(f"Device '{device_name}' (index {index}) is not accessible via OpenCV.")

    if not available_cameras:
        print("No accessible cameras found.")

    print("Available cameras:")
    for cam in available_cameras:
        print(f"Index: {cam['index']}, Name: {cam['name']}")
    return available_cameras


def main():
    # Prevent the Mac from sleeping
    prevent_sleep()

    try:

        # Config:
        CAMERA_INDEX = 0
        INTERVAL_IN_MILLISECONDS = 5000
        DISPLAY_IMAGES = True

        # Get the current date to create a folder
        current_date = datetime.now().strftime("%Y-%m-%d")
        containing_folder = os.path.expanduser("~/Desktop/timelapses")
        output_folder = os.path.join(containing_folder, current_date)
        print(f"Output folder: {output_folder}")

        # Create the folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Initialize the webcam (0 is usually the default camera)
        camera = cv2.VideoCapture(CAMERA_INDEX)

        # Check if the camera opened successfully
        if not camera.isOpened():
            print("Error: Could not access the camera.")
            exit()

        print("Press Ctrl+C in the terminal to stop capturing images.")

        count = 0

        while True:
            # Capture frame-by-frame
            ret, frame = camera.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            # Generate a filename based on the current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_folder, f"image_{timestamp}.jpg")

            # Save the frame as an image file
            cv2.imwrite(filename, frame)
            print(f"{count}: {filename}")
            count += 1

            # Display the most recently taken image
            if DISPLAY_IMAGES:
                cv2.imshow("Most Recently Taken Image", frame)
                # Wait some milliseconds so the frame can be rendered;
                # don't break on 'q' or any key.
                cv2.waitKey(1)

            # Sleep for the interval
            time.sleep(INTERVAL_IN_MILLISECONDS / 1000.0)

    except KeyboardInterrupt:
        print("Stopped capturing images.")




    finally:
        # Release resources
        camera.release()
        cv2.destroyAllWindows()
        allow_sleep()
        print("Camera released, and sleep allowed again.")


list_cameras_with_names()
main()
