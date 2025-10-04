from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time

def set_prompt_partial(driver, element, prompt_text, last_n_words=3, delay=0.05):
    """
    Set all except the last few words via JS, then type the last words manually.
    """
    words = prompt_text.strip().split()
    if len(words) <= last_n_words:
        js_part = ""
        type_part = prompt_text
    else:
        js_part = " ".join(words[:-last_n_words])
        type_part = " ".join(words[-last_n_words:])
    
    # Set main part via JS
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, element, js_part)

    # Type the last words slowly
    element.click()
    for char in type_part:
        element.send_keys(char)
        time.sleep(delay)

def clear_previous_image(driver, wait, retries=3):
    for attempt in range(retries):
        try:
            # Locate delete button
            delete_btn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='Delete image']")
            ))

            # Hover over it
            ActionChains(driver).move_to_element(delete_btn).perform()
            time.sleep(1)

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView(true);", delete_btn)
            time.sleep(0.5)

            # Wait until clickable and click
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Delete image']"))
            )
            delete_btn.click()
            print("🗑️ Previous image cleared.")
            time.sleep(3)
            return True
        except TimeoutException:
            print(f"⚠️ Attempt {attempt+1}: No previous image to clear or button not visible.")
            time.sleep(1)
    print("ℹ️ No previous image cleared after retries.")
    return False


# 📂 Folder with your images
INPUT_DIR = r"./processed/Download)"

# 📝 Your prompt
PROMPT = """A creepy, eerie comic-style horror illustration. Dark, unsettling, stylized artwork with exaggerated features, bold outlines, and moody shadows. The drawing should look hand-illustrated like a horror comic book panel, not realistic. Keep the scary atmosphere and unsettling tone. 

Remove or alter any visible text, logos, or brand names on clothing, objects, or in the background. Replace them with abstract markings, symbols, or fictional designs that fit the horror theme, never with readable text. Maintain the stylized, illustrated comic aesthetic consistently.
"""

# ✅ Path to ChromeDriver
chrome_driver_path = r"C:\tools\chromedriver\chromedriver.exe"

# ✅ Connect to running Chrome with debugging (must start Chrome with --remote-debugging-port=9222)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 60)

# Open Whisk project page
# driver.get("https://labs.google/fx/tools/whisk/project")

# Wait for login detection (My library link)
print("✅ Starting")
wait.until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='My library']")))
print("✅ Login detected. Starting automation...")


# ✅ Fill Prompt (robust)
textarea = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder,'Describe your idea')]")))
set_prompt_partial(driver, textarea, PROMPT, last_n_words=5, delay=0.05)
time.sleep(10)

# Loop through all images in folder
for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        continue

    image_path = os.path.join(INPUT_DIR, filename)
    print(f"\n🔄 Processing {image_path}")

    # ✅ Clear any previously uploaded image if delete button is active
    clear_previous_image(driver, wait)


    # ✅ Upload Image
    file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    file_input.send_keys(image_path)
    print("📤 Uploaded image.")
    time.sleep(15)

    # ✅ Open Aspect Ratio Menu
    aspect_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(text(),'aspect_ratio')]")))
    aspect_btn.click()
    print("📐 Opened aspect ratio menu.")
    time.sleep(5)

    # ✅ Select Portrait (9:16)
    portrait_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='9:16']]")))
    portrait_btn.click()
    print("📐 Set aspect ratio to Portrait.")
    time.sleep(5)

    # # ✅ Click Generate
    generate_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(text(),'arrow_forward')]")))
    generate_btn.click()
    # print("⚡ Clicked generate. Waiting 20s for result...")

    # Countdown while waiting
    for i in range(20, 0, -1):
        print(f"   ⏳ {i} seconds remaining...", end="\r")
        time.sleep(1)

    print(f"\n✅ Finished generation for {filename}. Please download manually.")
    time.sleep(5)

print("\n🎉 All images processed!")
