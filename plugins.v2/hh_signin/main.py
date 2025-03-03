import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .cookie_helper import CookieHelper  # 导入 CookieHelper

# Step 1: 读取 config.json 文件
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


# Step 2: 配置 Chrome 浏览器选项
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")  # 禁用信息栏
    chrome_options.add_argument("--disable-extensions")  # 禁用扩展
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    chrome_options.add_argument("--no-sandbox")  # 解决 DevToolsActivePort 文件不存在的问题
    chrome_options.add_argument("--disable-dev-shm-usage")  # 解决资源不足问题
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 隐藏自动化特征
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 初始化 WebDriver
    driver = webdriver.Chrome(options=chrome_options)  # 假设 MoviePilot 已经管理了 ChromeDriver
    return driver


# Step 3: 插件执行入口函数
def run(user_provided_cookies=None):
    # 加载配置
    config = load_config()
    TARGET_URL = config.get("target_url", "https://hhanclub.top/")  # 从 config.json 获取

    # 初始化 WebDriver
    driver = setup_driver()

    # 初始化 CookieHelper
    cookie_helper = CookieHelper()

    try:
        # Step 4: 访问目标网站
        driver.get(TARGET_URL)

        # Step 5: 获取 Cookie
        cookies = {}
        if user_provided_cookies:
            # 使用用户手动输入的 Cookie
            cookies = parse_cookie_string(user_provided_cookies)
            print("使用用户手动输入的 Cookie。")
        else:
            # 尝试从 MoviePilot 站点获取 Cookie
            try:
                # 使用 CookieHelper 获取 Cookie
                cookie_string = cookie_helper.get_cookie(TARGET_URL)
                if cookie_string:
                    cookies = parse_cookie_string(cookie_string)
                    print("从 MoviePilot 站点获取 Cookie 成功。")
                else:
                    print("从 MoviePilot 站点获取 Cookie 失败。")
                    # 提示用户手动输入 Cookie
                    user_provided_cookies = input("请手动输入 Cookie 字符串：")
                    cookies = parse_cookie_string(user_provided_cookies)
                    print("使用用户手动输入的 Cookie。")
            except Exception as e:
                print(f"从 MoviePilot 站点获取 Cookie 失败：{e}")
                # 提示用户手动输入 Cookie
                user_provided_cookies = input("请手动输入 Cookie 字符串：")
                cookies = parse_cookie_string(user_provided_cookies)
                print("使用用户手动输入的 Cookie。")

        # 添加 Cookie 到浏览器
        driver.delete_all_cookies()  # 清除默认 Cookie
        for name, value in cookies.items():
            driver.add_cookie({"name": name, "value": value})

        # 刷新页面以应用 Cookie
        driver.refresh()

        # 显式等待页面加载完成
        wait = WebDriverWait(driver, 10)

        # Step 6: 模拟点击用户头像
        user_avatar = wait.until(EC.element_to_be_clickable((By.ID, "user-avatar")))
        user_avatar.click()
        print("已点击用户头像，展开用户信息面板。")

        # Step 7: 点击签到链接
        sign_in_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'attendance.php')]")))
        sign_in_link.click()
        print("已点击签到链接。")

        # 等待几秒查看结果
        time.sleep(5)

    except Exception as e:
        print("发生错误：", str(e))

    finally:
        # 关闭浏览器
        driver.quit()


def parse_cookie_string(cookie_string):
    """
    将 Cookie 字符串解析为字典。
    """
    cookies = {}
    for item in cookie_string.split(";"):
        key, value = item.strip().split("=", 1)
        cookies[key] = value
    return cookies


if __name__ == "__main__":
    run()
