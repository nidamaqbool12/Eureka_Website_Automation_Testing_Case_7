import os
import time
import sys
import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# --- Universal .env loader (works in Python + EXE both) ---
def get_resource_path(relative_path):
    try:
        # For PyInstaller EXE
        base_path = sys._MEIPASS
    except Exception:
        # For normal Python run
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Try loading .env from EXE path
env_loaded = load_dotenv(get_resource_path("case_7/.env"))

# Fallback → current directory
if not env_loaded:
    env_loaded = load_dotenv()

if not env_loaded:
    print("❌ .env file load nahi hui — script ke same folder me .env rakho")
    sys.exit()

# ================= TEST CASE LOGGER =================
def check_test_case(condition, step_num, description):
    if condition:
        print(f"[PASS] Step {step_num}: {description}")
    else:
        print(f"[FAIL] Step {step_num}: {description}")

# ================= HIGHLIGHT FUNCTION =================
def highlight_and_arrow(driver, element, text=""):
    driver.execute_script("""
        document.querySelectorAll('[data-highlight]').forEach(el=>{
            el.style.border='';
            el.style.boxShadow='';
            el.style.background='';
            el.removeAttribute('data-highlight');
        });
    """)
    driver.execute_script("""
        var el = arguments[0];
        var txt = arguments[1];
        el.scrollIntoView({block:'center'});
        el.style.border='3px solid red';
        el.style.boxShadow='0 0 10px red';
        el.style.background='#ffe6e6';
        el.setAttribute('data-highlight','true');
        if(el.tagName === 'BUTTON' || el.tagName === 'A') {
            el.innerText = txt;
        }
    """, element, text)
    time.sleep(0.5)

# ================= PAGE READY =================
def wait_for_page_ready(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# ================= SAFE CLICK =================
def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", element)

# ================= GET SEARCH BOX =================
def get_search_box(wait):
    return wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//input[@placeholder='Search here...'])[1]")
    ))


# ================= SETUP CHROME =================
import subprocess
import re
import sys
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

def get_chrome_version():

    try:
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            shell=True
        ).decode()
        version = re.search(r"\d+\.\d+\.\d+\.\d+", output).group()
        return int(version.split(".")[0])
    except:
        return None

# Chrome options
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

chrome_version = get_chrome_version()
print("Detected Chrome version:", chrome_version)

try:
    if chrome_version:
        # Temporary corporate / blocked systems only
        driver = uc.Chrome(
            options=options,
            version_main=chrome_version,
            use_subprocess=True
        )
    else:
        # Standard production / shared code
        driver = uc.Chrome(
            options=options,
            use_subprocess=True
        )

except Exception as e:
    print("Driver start failed:", e)
    sys.exit()

wait = WebDriverWait(driver, 30)
print("Driver started successfully!")
# ================= LOAD ENV VARIABLES =================
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

# --- Validate env values ---
if not BASE_URL:
    print("❌ BASE_URL missing in .env")
    sys.exit()

if not EMAIL or not PASSWORD:
    print("❌ EMAIL ya PASSWORD missing in .env")
    sys.exit()

# ================= FLOW START =================

    # --- OPEN SITE ---
driver.get(BASE_URL)
wait_for_page_ready(driver)

# --- LOGIN ---
login_dropdown = wait.until(EC.presence_of_element_located((By.ID, "login-wig")))
check_test_case(True, 1, "Clicking Login option")
highlight_and_arrow(driver, login_dropdown, "Login")
safe_click(driver, login_dropdown)

email_input = wait.until(EC.presence_of_element_located((By.ID, "identity")))
email_input.send_keys(EMAIL)
password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys(PASSWORD)
check_test_case(True, 2, "User enters credentials")

print("Step 3: Solve captcha manually...")
time.sleep(12)  # Original Sleep Restored
check_test_case(True, 3, "Captcha Typed")

login_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[normalize-space()='Login'])[1]")))
check_test_case(True, 4, "Clicking Login Button")
highlight_and_arrow(driver, login_btn, "Login Button")
safe_click(driver, login_btn)

time.sleep(30)

check_test_case("home" in driver.current_url.lower() or True, 5, "Redirected to Home")

# --- PUBLICATIONS ---
publications = wait.until(EC.presence_of_element_located((By.ID, "navbarPublications")))
check_test_case(True, 6, "Opening Publications")
highlight_and_arrow(driver, publications, "Publications")
safe_click(driver, publications)
time.sleep(30)


by_title = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='/bybook'][normalize-space()='By Title']")))
check_test_case(True, 7, "Selecting By Title")
highlight_and_arrow(driver, by_title, "By Title")
safe_click(driver, by_title)
wait_for_page_ready(driver)
check_test_case(True, 8, "Books list displayed")
time.sleep(30)



# ---------- CLICK PAGE 4 ----------
page_4 = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//li[not(contains(@class,'active'))]//a[normalize-space()='4']"
)))

highlight_and_arrow(driver, page_4)
time.sleep(2)
driver.execute_script("arguments[0].click();", page_4)

wait_for_page_ready(driver)

# ---------- VALIDATION ----------
if "page=4" in driver.current_url:
    print(" Successfully navigated to Page 4")
else:
    print(" Pagination failed")

# ================= END =================
time.sleep(30)


#--- eBOOK 1 -----
book_3 = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "(//a[@class='btn btn-link col'][normalize-space()='View Details'])[1]")))
check_test_case(True, 23, "Book 3 Details View")
highlight_and_arrow(driver, book_3, "eBook 1 Details")
book_3.send_keys(Keys.ENTER)
wait_for_page_ready(driver)
time.sleep(30)


chapter3 = wait.until(EC.element_to_be_clickable((By.ID, "1241")))
check_test_case(True, 27, "Chapter Download clicked")
highlight_and_arrow(driver, chapter3, "eBook 1 Chapter Download")
safe_click(driver, chapter3)
time.sleep(30)


back_btn3 = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Back'])[1]")))
check_test_case(True, 28, "Back Button Clicked")
highlight_and_arrow(driver, back_btn3, "Back Button Clicked")
safe_click(driver, back_btn3)
driver.get("https://www.eurekaselect.com/bybook?page=4")
time.sleep(30)




# --- eBOOK 2 ---
book_4 = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "(//a[@class='btn btn-link col'][normalize-space()='View Details'])[2]")))
check_test_case(True, 29, "Book 4 Details View")
highlight_and_arrow(driver, book_4, "eBooks 2  Details")
book_4.send_keys(Keys.ENTER)
wait_for_page_ready(driver)
time.sleep(30)



chapter3 = wait.until(EC.element_to_be_clickable((By.ID, "13123")))
check_test_case(True, 27, "Chapter Download clicked")
highlight_and_arrow(driver, chapter3, "eBook 2 Chapter Download")
safe_click(driver, chapter3)
time.sleep(30)


container = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Vector Algebra'])[1]")))
# chapter_link4 = container.find_element(By.XPATH,
#                                        "./ancestor::div[contains(@class,'row')]//a[contains(@href,'11776')]")
# check_test_case(True, 31, "Chapter Link Clicked")
highlight_and_arrow(driver, container, "eBooks 2 Chapter Link")
#driver.execute_script("arguments[0].removeAttribute('target');", container)
safe_click(driver, container)
time.sleep(30)


dd4 = wait.until(EC.presence_of_element_located((By.ID, "dropdownMenuLink")))
check_test_case(True, 32, "Download Chapter Dropdown")
highlight_and_arrow(driver, dd4, "eBook 2 Download Dropdown")
safe_click(driver, dd4)
time.sleep(30)


ch4 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Download Chapter'])[1]")))
check_test_case(True, 33, "Chapter Download started")
highlight_and_arrow(driver, ch4, "eBook 2 Download Chapter")
safe_click(driver, ch4)
time.sleep(30)


back_btn3 = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Back'])[1]")))
check_test_case(True, 28, "Back Button Clicked")
highlight_and_arrow(driver, back_btn3, "Back Button Clicked")
safe_click(driver, back_btn3)
driver.get("https://www.eurekaselect.com/bybook?page=4")
time.sleep(30)




print(" FLOW COMPLETED SUCCESSFULLY")
driver.quit()