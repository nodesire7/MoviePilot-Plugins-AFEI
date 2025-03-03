from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .config import Config
from .logger import setup_logger
from .utils import setup_driver, load_cookies

logger = setup_logger()

class HHSignInPlugin:
    def __init__(self, config: Config):
        self.config = config

    def sign_in(self):
        driver = setup_driver(self.config.chrome_driver_path)

        try:
            driver.get(self.config.target_url)

            cookies = load_cookies(self.config.cookie_file_path)
            driver.delete_all_cookies()
            for name, value in cookies.items():
                driver.add_cookie({"name": name, "value": value})
            driver.refresh()

            wait = WebDriverWait(driver, 10)

            user_avatar = wait.until(EC.element_to_be_clickable((By.ID, "user-avatar")))
            user_avatar.click()
            logger.info("已点击用户头像，展开用户信息面板。")

            sign_in_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'attendance.php')]")))
            sign_in_link.click()
            logger.info("已点击签到链接。")

            time.sleep(5)

        except Exception as e:
            logger.error(f"发生错误：{str(e)}")

        finally:
            driver.quit()
