import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def clear_all_csv():
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".csv") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                count += 1
    print(f"Đã xoá {count} file CSV và PNG trong project.")

if __name__ == "__main__":
    clear_all_csv()  
