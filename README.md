# Tinder Automation Bot

![Tinder Automation](./tinder.png)

I have implemented a Selenium + image recognition project using Selenium and OpenCV respectively. Reason why I have used this combination is that even though application bypasses the Selenium just to apply dynamic front-end implementations, we can still use image recognition to achieve same results.

## Features

- Automatically logs into Tinder using your browser's saved session.
- Swipes right (like) or left (dislike) based on user-defined age ranges.
- Checks if a profile is "Recently Active" and sends notifications to Telegram.
- Uses HTML elements for finding Like and Dislike buttons; falls back to image recognition if needed.
- Error detection with fallback for handling unexpected popups.
- Ability to pause and resume the script with the spacebar.
- Gracefully exits when pressing the escape key.

## Installation

### Prerequisites
- Python 3.x
- Google Chrome browser
- Chrome WebDriver
- [Tinder account](https://tinder.com)

### Python Dependencies
Make sure you have the required Python packages installed. You can install them using the `requirements.txt` file provided in this repository.

1. **Create a virtual environment (optional but recommended):**

```bash
   python -m venv venv
```
2. **Activate the virtual environment:**

- On Windows:
  - venv\Scripts\activate

- On macOS/Linux:
  - source venv/bin/activate

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Web Driver Setup**

- Download Chrome WebDriver and ensure it's in your system's PATH or specify the path to the WebDriver in the script.

5. **Telegram Setup**

- This script sends notifications to a Telegram bot. To set it up:

1. Create a bot with BotFather on Telegram.
2. Get your TELEGRAM_TOKEN and CHAT_ID.
3. Replace the placeholders in the script with your token and chat ID.


## Usage

1. **Run the Script:**

- After setting up everything, run the script by navigating to the project directory and typing the following command:

```bash
   python tinder.py
```

2. **Login to Tinder:**

- The script will open a Chrome browser and navigate to Tinder. Please log in to your Tinder account manually.

- Once logged in, the script will ask: Tinder'a giriş yaptınız mı? (Y/N):
 - Enter Y to continue.

3. **Provide Age Range:**

```bash
Enter age range (e.g., 18-25): 
```

- Enter the desired age range to filter profiles.

4. **Automation Begins:**

- The bot will begin swiping profiles based on the age range you provided. It will attempt to:

  - Swipe right (Like) if the profile's age is within the specified range.
  - Swipe left (Dislike) if the profile's age is outside the range.

**Notes**
- If HTML elements for swiping are not detected, the script will fallback to image recognition using the provided like/dislike images.
- The bot will send a Telegram notification when it encounters a "Recently Active" profile.

5. **Pause/Resume and Exit:**

- Press Space to pause or resume the bot.
- Press Esc to exit and close the browser session.

## Troubleshooting

1. **PyAutoGUI/Pillow Issues:**

   If you encounter the following error:

```bash
   PyAutoGUI was unable to import pyscreeze. (This is likely because you're running a version of Python that Pillow (which pyscreeze depends on) doesn't support currently.)
```

```bash
    pip install pillow
```

2. **ChromeDriver Version Compatibility:**
- Ensure that the version of ChromeDriver matches your installed version of Google Chrome. You can download the appropriate version here.

3. **Telegram Notification Issues:**
- If Telegram notifications are not being sent, double-check your bot token and chat ID. You can create a bot and get your chat ID by following the Telegram Bot API documentation.

4. **Image Recognition Accuracy:**
- The image recognition functionality depends on matching the screenshots of the like and dislike buttons. If the bot fails to recognize these images:

- Ensure your screen resolution and scaling settings match the screenshots provided.
You can take your own screenshots and replace the files in the assets/ folder to improve accuracy.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -m 'Add YourFeature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.
6. Please make sure to update tests as appropriate.