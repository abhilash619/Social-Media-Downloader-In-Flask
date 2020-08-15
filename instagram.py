from datetime import datetime
from tqdm import tqdm
import requests
import re
import os
import sys

# Function to check the internet connection
def connection(url='http://www.google.com/', timeout=5):
    try:
        req = requests.get(url, timeout=timeout)
        req.raise_for_status()
        print("You're connected to internet\n")
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
            e.response.status_code))
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


# Function to download an instagram photo or video
def download_image_video(url):
    home_folder = os.path.expanduser('~') + "\Downloads\\"
    home_folder = home_folder.replace("\\", "/")
    try:
        request_image = requests.get(url)
        src = request_image.content.decode('utf-8')
        check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
        check_type_f = check_type.group()
        final = re.sub('<meta name="medium" content="', '', check_type_f)

        if final == "image":
            print("\nDownloading the image...")
            extract_image_link = re.search(r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
            image_link = extract_image_link.group()
            final = re.sub('meta property="og:image" content="', '', image_link)
            _response = requests.get(final).content
            file_size_request = requests.get(final, stream=True)
            file_size = int(file_size_request.headers['Content-Length'])
            block_size = 1024
            filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
            t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
            with open(home_folder + filename + '.jpg', 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            t.close()
            print("Image downloaded successfully")

        if final == "video":
            print("Downloading the video...")
            extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
            video_link = extract_video_link.group()
            final = re.sub('meta property="og:video" content="', '', video_link)
            _response = requests.get(final).content
            file_size_request = requests.get(final, stream=True)
            file_size = int(file_size_request.headers['Content-Length'])
            block_size = 1024
            filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
            t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
            with open(home_folder + filename + '.mp4', 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            t.close()
            print("Video downloaded successfully")
    except AttributeError:
        print("Unknown URL")



