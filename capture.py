import pyautogui
from datetime import datetime

def take_screenshot():
	# 1. Take a full screenshot
	screenshot = pyautogui.screenshot()

	# 2. Make a timestamped filename
	filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

	# 3. Save it to the current folder
	screenshot.save(filename)

	print(f"[OK] Saved screenshot as {filename}")
	return filename


if __name__ == "__main__":
	answer = input("Take screenshot now? (y/n): ").strip().lower()
	if answer == "y":
		take_screenshot()
	else:
		print("[CANCELLED] No screenshot taken.")
