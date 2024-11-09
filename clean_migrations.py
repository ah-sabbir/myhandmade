import os
import shutil

def delete_migration_files(project_root):
    for root, dirs, files in os.walk(project_root):
        if root.endswith("migrations"):
            for file in files:
                # Delete all .py files except __init__.py
                if file.endswith(".py") and file != "__init__.py":
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            for root, dirs, files in os.walk(root):
                # print(root)
                if root.endswith("__pycache__") and os.path.isdir(root):
                    shutil.rmtree(root)
                    print(f"Directory '{root}' has been deleted.")
            # print(root)
        if root.endswith("__pycache__"):
            shutil.rmtree(root)
            print(f"Directory '{root}' has been deleted.")
    print("No Tree Has Detected!")

if __name__ == "__main__":
    # Replace 'your_project_root_directory' with the root path of your Django project
    project_root = "backend/apps"
    delete_migration_files(project_root)
