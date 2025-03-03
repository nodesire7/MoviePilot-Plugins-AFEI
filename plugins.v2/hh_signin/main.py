from .plugin import HHSignInPlugin
from .config import Config

def main():
    config = Config()
    plugin = HHSignInPlugin(config)
    plugin.sign_in()

if __name__ == "__main__":
    main()
