import os.path
from datetime import datetime

from github import Github

from utils.ImageCoder import ImageCoder
from utils.JsonManager import JsonManager

if not os.path.exists(f"downloads"):
    os.makedirs("downloads")

if not os.path.exists(f"uploads"):
    os.makedirs("uploads")

if not os.path.exists("config.json"):
    token = input("Enter GitHub API token: ")
    repository_name = input("Enter repository full name: ")

    try:
        Github(token).get_repo(repository_name)

        config = JsonManager("config.json").save({"token": token, "repository": repository_name})
    except Exception as e:
        print(e)
        print("Invalid login details!")
        exit()
else:
    config = JsonManager("config.json")
    token = config.get("token")
    repository_name = config.get("repository")

mode = int(input("Select operation mode:\n1. Upload images\n2. Download images\nEnter: "))

if mode not in [1, 2]:
    print("Invalid operation mode!")
    exit()

github = Github(token)
repository = github.get_repo(repository_name)

match mode:
    case 1:
        for filename in os.listdir("./uploads"):
            if not (filename.endswith(".png")):
                pass

            image = ImageCoder(f"./uploads/{filename}")
            b64 = image.convert_image_to_base64().decode("utf-8")

            git_file = f"{datetime.today().strftime('%Y-%m-%d_%H.%M.%S')}/" + f"{filename}"

            repository.create_file(git_file, "Upload from app", b64, branch="master")
            print(git_file + " CREATED")
    case 2:
        for directory in repository.get_contents("/"):
            if directory.type == "dir":
                for file in repository.get_contents(directory.name):
                    if not os.path.exists(f"./downloads/{directory.name}"):
                        os.makedirs(f"./downloads/{directory.name}")

                    image = ImageCoder(f"./downloads/{directory.name}/{file.name}")
                    image.convert_base64_to_image(file.decoded_content)
