import time
import pyperclip
import random
import re
import csv
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from utils.clone_human_behavior import human_delay, human_move_to_element, human_type


class DeepgramAutomation:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-webrtc")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
        )

        try:
            # Force correct Chrome version
            self.driver = uc.Chrome(
                options=options,
                use_subprocess=True,
                version_main=148   # ← This is the fix
            )
            print("✅ Browser launched successfully (Version 148)")
            
        except Exception as e:
            print(f"❌ Failed to launch with version 148: {e}")
            # Fallback
            print("Trying fallback method...")
            self.driver = uc.Chrome(options=options, use_subprocess=True)

    def extract_temp_email(self):
        try:
            print("🚀 Starting Deepgram Automation...")

            # 1. Temporary Email
            self.driver.get("https://smailpro.com/temporary-email")
            human_delay(4, 7)

            copy_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/main/div[1]/div[8]/div[2]/div[1]/div/div[1]/div[2]/button[1]",
                    )
                )
            )
            human_move_to_element(copy_btn, self.driver)
            copy_btn.click()
            human_delay(3, 5)

            mail = pyperclip.paste().strip()
            print(f"✅ Email copied: {mail}")
            return mail
        except Exception as e:
            print(f"❌ Failed to extract temporary email: {e}")
            return None

    def deepgram_signup(self, mail):
        try:
            # 2. Deepgram Signup
            self.driver.switch_to.new_window("tab")
            self.driver.get("https://console.deepgram.com/signup")
            print("✅ Deepgram signup page loaded")
            human_delay(8, 12)  # Heavy page

            # Email
            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//input[@type="email"] | //input[contains(@placeholder,"email") or contains(@name,"email")]',
                    )
                )
            )
            human_move_to_element(email_field, self.driver)
            human_type(email_field, mail)
            print("✅ Email filled")

            # Password
            password_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="new-password"] | //input[@type="password"]')
                )
            )
            human_move_to_element(password_field, self.driver)
            human_type(password_field, "DeepgramTemp2026!")
            print("✅ Password filled")

            print("\n🔍 Looking for reCAPTCHA...")

            # ================== reCAPTCHA HANDLING ==================
            captcha_clicked = False

            try:
                # Method 1: Switch to iframe and click checkbox
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                print(f"Found {len(iframes)} iframes on page")

                for iframe in iframes:
                    try:
                        self.driver.switch_to.frame(iframe)
                        print("   Switched to an iframe...")

                        # Look for reCAPTCHA checkbox
                        checkbox = WebDriverWait(self.driver, 8).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    '//div[@class="recaptcha-checkbox"] | //span[@id="recaptcha-anchor"] | //div[contains(@class,"checkbox")]',
                                )
                            )
                        )
                        human_move_to_element(checkbox, self.driver)
                        checkbox.click()
                        print("✅ reCAPTCHA checkbox clicked!")
                        captcha_clicked = True
                        break
                    except:
                        self.driver.switch_to.default_content()
                        continue

            except Exception as e:
                print(f"ℹ️  CAPTCHA iframe method failed: {e}")

            # Switch back to main content
            self.driver.switch_to.default_content()

            # ================== Click Create Account ==================
            try:
                create_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/form/button",
                        )
                    )
                )
                human_move_to_element(create_btn, self.driver)
                create_btn.click()
                print("✅ Create Account button clicked")
            except Exception as e:
                print(f"❌ Create Account button failed: {e}")

        except Exception as e:
            print(f"deepgram signup failed: {e}")
            return

    def verify_email(self):
        # switch to previous tab
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("✅ Switched back to temporary email tab")

            email_notification = WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/main/div[1]/div[8]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div",
                    )
                )
            )
            human_move_to_element(email_notification, self.driver)
            email_notification.click()
            print("✅ Opened verification email")

        except Exception as e:
            print(f"❌ Failed to find verification email: {e}")

        try:
            print("🔍 Extracting verification link using page_source...")

            # Wait for email to fully load
            human_delay(6, 10)

            # Get full page source (this often works better)
            page_source = self.driver.page_source

            if "Verify My Email" in page_source:
                print("✅ Found 'Verify My Email' in page source")

                soup = BeautifulSoup(page_source, "html.parser")

                # Find the link
                verify_link = soup.find("a", string=re.compile("Verify My Email", re.I))

                if verify_link and verify_link.get("href"):
                    verification_url = verify_link["href"]
                    print("✅ Verification URL extracted!")
                    print(f"URL: {verification_url[:150]}...")

                    # Open the link
                    self.driver.get(verification_url)
                    print("🚀 Opened verification URL directly")
                    human_delay(8, 12)
                    print("✅ Email verification completed!")
                    # Success

            # Fallback: Search in srcdoc of all iframes
            print("Trying srcdoc fallback...")
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

            for i, iframe in enumerate(iframes):
                try:
                    srcdoc = iframe.get_attribute("srcdoc")
                    if srcdoc and "Verify My Email" in srcdoc:
                        print(f"✅ Found email content in iframe {i}")
                        soup = BeautifulSoup(srcdoc, "html.parser")
                        link = soup.find(
                            "a", string=re.compile("Verify My Email", re.I)
                        )
                        if link and link.get("href"):
                            self.driver.get(link["href"])
                            print("🚀 Opened verification URL")
                            human_delay(8, 12)

                except:
                    continue

        except Exception as e:
            print(f"verifiation email step failed:{e}")
            return 
            

    def extract_api_key(self):
        try:
            # click continue button
            continue_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div[2]/div[5]/div[2]/button[2]",
                    )
                )
            )
            human_move_to_element(continue_btn, self.driver)
            continue_btn.click()
        except Exception as e:
            print(f"❌ Failed to click Continue button: {e}")

        try:
            # select options for "What do you want to use Deepgram for?"
            options = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div/div/div/div[1]/button[3]")
                )
            )
            human_move_to_element(options, self.driver)
            options.click()
        except Exception as e:
            print(f"❌ Failed to select use case options: {e}")

        try:
            # click continue button
            continue_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/button[2]")
                )
            )
            human_move_to_element(continue_btn, self.driver)
            continue_btn.click()
            human_delay()
        except Exception as e:
            print(f"❌ Failed to click Continue button: {e}")

        try:
            # click api key button
            api_key_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[1]/div[1]/div/nav/div/div[2]/div[1]/div[2]/ul/li[2]/a",
                    )
                )
            )
            human_move_to_element(api_key_btn, self.driver)
            api_key_btn.click()
            human_delay(4, 7)
        except Exception as e:
            print(f"❌ Failed to navigate to API keys: {e}")

        try:
            # click new api key
            new_key_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/button",
                    )
                )
            )
            human_move_to_element(new_key_btn, self.driver)
            new_key_btn.click()
        except Exception as e:
            print(f"❌ Failed to create new API key: {e}")

        try:
            # enter api key name
            key_name_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/ol/li[1]/div[2]/label/input",
                    )
                )
            )
            human_move_to_element(key_name_field, self.driver)
            human_type(key_name_field, "MyAPIKey")
        except Exception as e:
            print(f"❌ Failed to name API key: {e}")

        try:
            # click create api key
            create_key_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/button",
                    )
                )
            )
            human_move_to_element(create_key_btn, self.driver)
            create_key_btn.click()
            print("✅ API key created successfully!")
            human_delay()
        except Exception as e:
            print(f"❌ Failed to create API key: {e}")

        try:
            # click copy api key button
            copy_key_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/button",
                    )
                )
            )
            human_move_to_element(copy_key_btn, self.driver)
            copy_key_btn.click()
            api_key = pyperclip.paste().strip()
            print(f"✅ API key copied: {api_key}")
            return api_key
        except Exception as e:
            print(f"❌ Failed to copy API key: {e}")
            return None

    def store_api_key(self, api_key, email):
        try:
            csv_file = "deepgram_api_keys.csv"
            file_exists = os.path.isfile(csv_file)

            with open(csv_file, "a", newline="") as f:
                writer = csv.writer(f)

                # Write header if file doesn't exist
                if not file_exists:
                    writer.writerow(["Email", "API Key"])

                # Append the new row
                writer.writerow([email, api_key])

            print(f"✅ API key and email stored in {csv_file}")
        except Exception as e:
            print(f"❌ Failed to store API key: {e}")
            
    def close(self):
        self.driver.quit()
        print("✅ Browser closed")


if __name__ == "__main__":
    automation = DeepgramAutomation()
    email = automation.extract_temp_email()
    if email:
        automation.deepgram_signup(email)
        automation.verify_email()
        api_key = automation.extract_api_key()
        if api_key:
            automation.store_api_key(api_key, email)
            automation.close()
    else:
        print("❌ Failed to retrieve temporary email.")
        automation.close()
