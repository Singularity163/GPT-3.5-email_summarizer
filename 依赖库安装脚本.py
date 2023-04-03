import os
import sys

def install_requirements():
    try:
        with open("requirements.txt", "r") as file:
            packages = file.read().splitlines()
        for package in packages:
            print(f"正在安装: {package}")
            os.system(f"{sys.executable} -m pip install {package}")
    except FileNotFoundError:
        print("找不到 requirements.txt 文件，请确保文件存在。")

if __name__ == "__main__":
    install_requirements()