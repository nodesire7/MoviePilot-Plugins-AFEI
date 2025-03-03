import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.log import logger


class HHSignHelper:
    """
    HH论坛签到助手
    """
    _url = "https://hhanclub.top/"
    
    def __init__(self, cookie: str):
        self._cookie = cookie
        self._driver = None
        
    def _init_driver(self):
        """
        初始化 WebDriver
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无界面模式
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self._driver = webdriver.Chrome(options=chrome_options)

    def sign_in(self) -> bool:
        """
        执行签到
        """
        try:
            self._init_driver()
            
            # 访问网站
            self._driver.get(self._url)
            
            # 添加 Cookie
            for item in self._cookie.split(";"):
                name, value = item.strip().split("=", 1)
                self._driver.add_cookie({"name": name, "value": value})
            
            # 刷新页面
            self._driver.refresh()
            
            wait = WebDriverWait(self._driver, 10)
            
            # 点击用户头像
            avatar = wait.until(EC.element_to_be_clickable((By.ID, "user-avatar")))
            avatar.click()
            logger.info("已点击用户头像")
            
            # 点击签到链接
            sign_link = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, 'attendance.php')]")
            ))
            sign_link.click()
            logger.info("已点击签到链接")
            
            time.sleep(2)
            return True
            
        except Exception as e:
            logger.error(f"签到失败: {str(e)}")
            return False
            
        finally:
            if self._driver:
                self._driver.quit()

