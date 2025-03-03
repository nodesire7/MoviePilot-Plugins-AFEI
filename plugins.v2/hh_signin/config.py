import os
import platform
from .utils import update_chromedriver

TARGET_URL = "https://hhanclub.top/"

# 确定 ChromeDriver 的文件名（Linux 下不需要 .exe 后缀）
if platform.system() == "Windows":
    driver_filename = "chromedriver.exe"
else:
    driver_filename = "chromedriver"

# 自动更新 ChromeDriver 并获取路径
CHROMEDRIVER_DIR = os.path.join(os.path.dirname(__file__), "drivers")
CHROMEDRIVER_PATH = update_chromedriver(CHROMEDRIVER_DIR)

if not CHROMEDRIVER_PATH:
    raise FileNotFoundError("ChromeDriver 更新失败，请检查配置。")
