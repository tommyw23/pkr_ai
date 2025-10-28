import os
import time
import importlib

def test_capture_creates_file():
    # Import the capture module fresh every run
    # so we can call its function
    capture = importlib.import_module("capture")

    # Call the screenshot function directly (no prompt)
    filename = capture.take_screenshot()

    # Give the OS a moment to flush the file to disk
    time.sleep(0.5)

    # Check that the file actually exists
    if os.path.exists(filename):
        print(f"[PASS] Screenshot file '{filename}' exists.")
        # optional cleanup: comment this out if you want to keep screenshots
        # os.remove(filename)
    else:
        print(f"[FAIL] Screenshot file '{filename}' was NOT created.")

if __name__ == "__main__":
    test_capture_creates_file()
