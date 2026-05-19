import time
import pyperclip
import random
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

#====================== SETUP ======================

proxies = [
    
    "http://zjuesvmw:l1xtk7w106zk:6114",
    "http://zjuesvmw:l1xtk7w106zk:5863",
    "http://zjuesvmw:l1xtk7w106zk:6462",
    "http://zjuesvmw:l1xtk7w106zk:6014",
    
    # add more
]
options = uc.ChromeOptions()
# current_proxy = random.choice(proxies)
#options.add_argument(f'--proxy-server={current_proxy}')
options.add_argument("--start-maximized")
options.add_argument("--proxy-bypass-list=*")   # Try this
options.add_argument("--no-proxy-server")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-webrtc")           # Hide real IP
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options, use_subprocess=True)

# ========================= UTILITY FUNCTIONS =========================
def human_delay(min_sec=1.5, max_sec=4.5):
    time.sleep(random.uniform(min_sec, max_sec))

def scroll_into_view(element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(random.uniform(0.8, 1.6))

def human_move_to_element(element):
    try:
        scroll_into_view(element)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.5, 1.2))
        actions.perform()
    except:
        scroll_into_view(element)
        time.sleep(1.5)
        ActionChains(driver).move_to_element(element).perform()

def human_type(element, text):
    element.clear()
    human_delay(0.4, 0.9)
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.06, 0.17))

# ========================= MAIN SCRIPT =========================
try:
    print("🚀 Starting Deepgram Automation...")

    # 1. Temporary Email
    driver.get("https://smailpro.com/temporary-email")
    human_delay(4, 7)

    copy_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div[8]/div[2]/div[1]/div/div[1]/div[2]/button[1]'))
    )
    human_move_to_element(copy_btn)
    copy_btn.click()
    human_delay(3, 5)

    copied_text = pyperclip.paste().strip()
    print(f"✅ Email copied: {copied_text}")

    # 2. Deepgram Signup
    driver.switch_to.new_window('tab')
    driver.get("https://console.deepgram.com/signup")
    print("✅ Deepgram signup page loaded")
    human_delay(8, 12)   # Heavy page

    # Email
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="email"] | //input[contains(@placeholder,"email") or contains(@name,"email")]'))
    )
    human_move_to_element(email_field)
    human_type(email_field, copied_text)
    print("✅ Email filled")

    # Password
    password_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="new-password"] | //input[@type="password"]'))
    )
    human_move_to_element(password_field)
    human_type(password_field, "DeepgramTemp2026!")
    print("✅ Password filled")

    print("\n🔍 Looking for reCAPTCHA...")

    # ================== reCAPTCHA HANDLING ==================
    captcha_clicked = False
    
    try:
        # Method 1: Switch to iframe and click checkbox
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframes on page")

        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                print("   Switched to an iframe...")

                # Look for reCAPTCHA checkbox
                checkbox = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        '//div[@class="recaptcha-checkbox"] | //span[@id="recaptcha-anchor"] | //div[contains(@class,"checkbox")]'
                    ))
                )
                human_move_to_element(checkbox)
                checkbox.click()
                print("✅ reCAPTCHA checkbox clicked!")
                captcha_clicked = True
                break
            except:
                driver.switch_to.default_content()
                continue

    except Exception as e:
        print(f"ℹ️  CAPTCHA iframe method failed: {e}")

    # Switch back to main content
    driver.switch_to.default_content()

    # ================== Click Create Account ==================
    try:
        create_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/form/button'
            ))
        )
        human_move_to_element(create_btn)
        create_btn.click()
        print("✅ Create Account button clicked")
    except Exception as e:
        print(f"❌ Create Account button failed: {e}")
        
    # switch to previous tab    
    try:
        driver.switch_to.window(driver.window_handles[0])
        print("✅ Switched back to temporary email tab")
        
        email_notification=WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div[8]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div'))
        )
        human_move_to_element(email_notification)
        email_notification.click()
        print("✅ Opened verification email")
        
    except Exception as e:
        print(f"❌ Failed to find verification email: {e}")    
        
    try:
        print("🔍 Extracting verification link using page_source...")

        # Wait for email to fully load
        human_delay(6, 10)

        # Get full page source (this often works better)
        page_source = driver.page_source

        if "Verify My Email" in page_source:
            print("✅ Found 'Verify My Email' in page source")

            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find the link
            verify_link = soup.find("a", string=re.compile("Verify My Email", re.I))
            
            if verify_link and verify_link.get("href"):
                verification_url = verify_link["href"]
                print("✅ Verification URL extracted!")
                print(f"URL: {verification_url[:150]}...")

                # Open the link
                driver.get(verification_url)
                print("🚀 Opened verification URL directly")
                human_delay(8, 12)
                print("✅ Email verification completed!")
                    #Success

        # Fallback: Search in srcdoc of all iframes
        print("Trying srcdoc fallback...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        for i, iframe in enumerate(iframes):
            try:
                srcdoc = iframe.get_attribute("srcdoc")
                if srcdoc and "Verify My Email" in srcdoc:
                    print(f"✅ Found email content in iframe {i}")
                    soup = BeautifulSoup(srcdoc, 'html.parser')
                    link = soup.find("a", string=re.compile("Verify My Email", re.I))
                    if link and link.get("href"):
                        driver.get(link["href"])
                        print("🚀 Opened verification URL")
                        human_delay(8, 12)
                        
            except:
                continue

    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("verification_final_error.png")
        
    try:
        # click continue button
        continue_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div/div/div[2]/div[5]/div[2]/button[2]'
            ))
        )    
        human_move_to_element(continue_btn)
        continue_btn.click()
    except Exception as e:
        print(f"❌ Failed to click Continue button: {e}")
        
        
    try:
        # select options for "What do you want to use Deepgram for?"
        options = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div/div/div/div[1]/button[3]'
            ))
        )
        human_move_to_element(options)
        options.click()
    except Exception as e:
        print(f"❌ Failed to select use case options: {e}")
        
    try:
        # click continue button
        continue_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div/div/div/div[2]/div[2]/button[2]'
            ))
        )    
        human_move_to_element(continue_btn)
        continue_btn.click()
        human_delay()
    except Exception as e:
        print(f"❌ Failed to click Continue button: {e}")
        
    try:
        # click api key button
        api_key_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div/div[1]/div[1]/div/nav/div/div[2]/div[1]/div[2]/ul/li[2]/a'
            ))
        )
        human_move_to_element(api_key_btn)
        api_key_btn.click()
        human_delay(4, 7)
    except Exception as e:
        print(f"❌ Failed to navigate to API keys: {e}")
    
    try:
        # click new api key
        new_key_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/button'
            ))
        )
        human_move_to_element(new_key_btn)
        new_key_btn.click()
    except Exception as e:
        print(f"❌ Failed to create new API key: {e}")
    
    try:
        # enter api key name
        key_name_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, 
                '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/ol/li[1]/div[2]/label/input'
            ))
        )
        human_move_to_element(key_name_field)
        human_type(key_name_field, "MyAPIKey")
    except Exception as e:
        print(f"❌ Failed to name API key: {e}")
        
    try:
        # click create api key
        create_key_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/button'
            ))
        )
        human_move_to_element(create_key_btn)
        create_key_btn.click()
        print("✅ API key created successfully!")
        human_delay()
    except Exception as e:
        print(f"❌ Failed to create API key: {e}")
        
    try:
        # click copy api key button
        copy_key_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, 
                '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/button'
            ))
        )
        human_move_to_element(copy_key_btn)
        copy_key_btn.click()
        copied_text = pyperclip.paste().strip()
        print("✅ API key copied to clipboard!")
        print(f"✅ API key copied: {copied_text}")
        
        human_delay()
        
    except Exception as e:
        print(f"❌ Failed to copy API key: {e}")
                    

    print("\n🎉 Script finished.")
    if not captcha_clicked:
        print("⚠️  Please solve the CAPTCHA manually if it appeared.")

except Exception as e:
    print(f"❌ Critical Error: {e}")

finally:
    input("\nPress Enter to close browser...")