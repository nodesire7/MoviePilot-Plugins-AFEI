import os
import platform
from webdriver_manager.chrome import ChromeDriverManager
from shutil import copyfile

def update_chromedriver(target_dir):
    """
    使用 ChromeDriverManager 自动下载并更新 chromedriver 到目标目录。
    """
    # 检查目标目录是否存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"目标目录不存在，已创建: {target_dir}")

    try:
        # 使用 ChromeDriverManager 自动下载 chromedriver
        print("正在通过 ChromeDriverManager 下载最新的 chromedriver...")
        driver_path = ChromeDriverManager().install()

        # 确定目标 ChromeDriver 的文件名（Linux 下不需要 .exe 后缀）
        if platform.system() == "Windows":
            driver_filename = "chromedriver.exe"
        else:
            driver_filename = "chromedriver"

        # 将下载的 chromedriver 复制到目标目录
        target_driver_path = os.path.join(target_dir, driver_filename)
        copyfile(driver_path, target_driver_path)
        print(f"chromedriver 已成功更新到目录: {target_dir}")

        # 设置 ChromeDriver 可执行权限 (Linux/macOS)
        if platform.system() != "Windows":
            os.chmod(target_driver_path, 0o755)

        return target_driver_path

    except Exception as e:
        print(f"更新 chromedriver 失败: {e}")
        return None

if __name__ == "__main__":
    # 目标目录
    target_directory = os.path.join(os.getcwd(), "drivers")
    driver_path = update_chromedriver(target_directory)
    if driver_path:
        print(f"ChromeDriver 的路径是: {driver_path}")
