import os
from webdriver_manager.chrome import ChromeDriverManager
from shutil import copyfile

class Config:
    def __init__(self):
        self.target_url = "https://hhanclub.top/"
        self.cookie_file_path = os.path.join(os.path.dirname(__file__), "hhck.json")
        self.chrome_driver_path = self.update_chromedriver()

    def update_chromedriver(self):
        """
        使用 ChromeDriverManager 自动下载并更新 chromedriver 到当前运行目录。
        """
        target_dir = os.path.dirname(__file__)
        try:
            # 使用 ChromeDriverManager 自动下载 chromedriver
            print("正在通过 ChromeDriverManager 下载最新的 chromedriver...")
            driver_path = ChromeDriverManager().install()

            # 将下载的 chromedriver 复制到目标目录
            target_driver_path = os.path.join(target_dir, "chromedriver")
            copyfile(driver_path, target_driver_path)
            print(f"chromedriver 已成功更新到目录: {target_dir}")
            return target_driver_path

        except Exception as e:
            print(f"更新 chromedriver 失败: {e}")
            raise
