import sys
import time
import keyboard
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from colorama import init, Fore, Style
import requests
import cv2
import pyautogui
import numpy as np

# Start Colorama
init(autoreset=True)

# For Turkish characters stdout set to utf-8
sys.stdout.reconfigure(encoding='utf-8')

# Telegram bot token and chat ID
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Telegram message sent: {message}")
        else:
            print(f"Failed to send message: {response.status_code}")
    except Exception as e:
        print(f"Error sending Telegram message: {str(e)}", flush=True)

# Protect current browser session.
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\path\\to\\your\\chrome\\profile")  # Update with your Chrome profile path
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Disable automation control warning
options.add_experimental_option('useAutomationExtension', False)  # Disable automation extension
driver = webdriver.Chrome(options=options)

driver.maximize_window()
driver.get("https://tinder.com/app/recs")  # Tinder recommendation page

paused = False  # Pause/Continue option for space key.

def pause_or_continue():
    global paused
    paused = not paused
    if paused:
        print("Script paused. Continue with Space.", flush=True)
    else:
        print("Script continue...", flush=True)

def save_and_exit():
    print("Script durduruluyor...", flush=True)
    try:
        driver.quit()
        print("Browser closed. Script will be terminated...", flush=True)
    except Exception as e:
        print(f"Tarayıcı kapatılırken bir hata oluştu: {str(e)}", flush=True)
    finally:
        sys.exit()

# Terminate with ESC
keyboard.add_hotkey('esc', save_and_exit)
# Press Space key to pause/continue
keyboard.add_hotkey('space', pause_or_continue)

def image_recognition_click(template_path, threshold=0.8):
    """Function to detect the button using OpenCV and click it."""
    template = cv2.imread(template_path)
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    if len(loc[0]) > 0:
        pyautogui.click(loc[1][0], loc[0][0])  # Click at the location of the match
        return True
    return False

async def process_profile(profile, min_age, max_age):
    try:
        # Get the age element
        age_element = profile.find_element(By.XPATH, '//span[@class="As(b)" and @itemprop="age"]')
        age_text = age_element.text.strip()
        age = int(age_text)

        # Check if profile has 'Recently Active' status
        try:
            recently_active_element = profile.find_element(By.XPATH, '//span[contains(@class, "C($c-ds-text-primary-overlay)") and contains(text(), "Recently Active")]')
            recently_active_status = "Recently Active"
            send_telegram_message(f"Profile is {recently_active_status}, Age: {age_text}")
        except NoSuchElementException:
            recently_active_status = "Not Recently Active"

        # Swipe logic based on age
        if min_age <= age <= max_age:
            try:
                # First attempt to find the "Like" button via HTML element
                right_swipe_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "Hidden") and text()="Beğen"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", right_swipe_button)
                right_swipe_button.click()  # Click the HTML button
                print(f"{Fore.GREEN}Right swiped (Age: {age}) using HTML element.{Style.RESET_ALL}", flush=True)
            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException):
                # If HTML element failed, use image recognition
                print("Failed to locate 'Like' button using HTML. Trying image recognition.", flush=True)
                if image_recognition_click('./assets/full_screen_like.PNG'):
                    print(f"{Fore.GREEN}Right swiped using image recognition.{Style.RESET_ALL}", flush=True)
                else:
                    print(f"{Fore.RED}Failed to swipe right using image recognition.", flush=True)
        else:
            try:
                # First attempt to find the "Dislike" button via HTML element
                left_swipe_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Nope"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", left_swipe_button)
                left_swipe_button.click()  # Click the HTML button
                print(f"{Fore.RED}Left swiped (Age: {age}) using HTML element.{Style.RESET_ALL}", flush=True)
            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException):
                # If HTML element failed, use image recognition
                print("Failed to locate 'Nope' button using HTML. Trying image recognition.", flush=True)
                if image_recognition_click('./assets/full_screen_dislike.PNG'):
                    print(f"{Fore.RED}Left swiped using image recognition.{Style.RESET_ALL}", flush=True)
                else:
                    print(f"{Fore.RED}Failed to swipe left using image recognition.", flush=True)

        time.sleep(3)

    except NoSuchElementException as e:
        print(f"Element not found in profile: {str(e)}", flush=True)
        time.sleep(3)
        
        # Check for error image when encountering an issue
        print("Checking for error icon...")
        if image_recognition_click('./assets/error_icon.png'):
            print(f"{Fore.YELLOW}Error icon found and handled.{Style.RESET_ALL}", flush=True)
        else:
            print(f"{Fore.RED}No error icon detected.", flush=True)

async def main():
    try:
        # First ask if user has logged into Tinder
        print("Tarayıcı açıldı. Lütfen Tinder'a giriş yapın.", flush=True)
        user_input = input("Tinder'a giriş yaptınız mı? (Y/N): ")

        if user_input.lower() != 'y':
            print("Lütfen Tinder'a giriş yapın ve scripti tekrar başlatın.", flush=True)
            return
        
        # Now ask for the age range
        age_range_input = input("Enter age range (e.g., 18-25): ")
        try:
            min_age, max_age = map(int, age_range_input.split('-'))
        except ValueError:
            print("Invalid age range format. Please enter in the format 'min-max'.")
            return

        try:
            while True:
                if paused:
                    time.sleep(1)
                    continue

                try:
                    profiles = driver.find_elements(By.CLASS_NAME, 'recsCardboard__cards')

                    if not profiles:
                        print("There is no processing profile. Bot will be stopped.", flush=True)
                        break

                    for profile in profiles:
                        await process_profile(profile, min_age, max_age)

                except NoSuchElementException as e:
                    print(f"Profil bulunamadı: {str(e)}", flush=True)
                    break

        except NoSuchElementException as e:
            print(f"Element bulunamadı: {str(e)}", flush=True)
            driver.quit()

        except Exception as e:
            print(f"Bir hata oluştu: {str(e)}", flush=True)
            driver.quit()

    except KeyboardInterrupt:
        save_and_exit()

if __name__ == "__main__":
    asyncio.run(main())
