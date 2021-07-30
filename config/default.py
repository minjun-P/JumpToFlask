import os

#프로젝트의 루트 디렉터리 설정
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if __name__ == "__main__":
    print(BASE_DIR)