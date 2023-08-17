from pathlib import Path

import requests
from bs4 import BeautifulSoup

from image import embed_watermark

import os


def send_post(username, password, text, file_path, url):
    s = requests.session()

    r = s.get(url + '/auth/login')
    soup = BeautifulSoup(r.text, 'html.parser')

    csrf_token = soup.find(id="csrf_token")['value']

    params = {
        'email': username,
        'password': password,
        'csrf_token': csrf_token
    }
    r = s.post(url + '/auth/login', data=params)
    if not r.status_code == 200:
        print('Login failed.')
        return

    image = Path(file_path)
    from_data = {'text': text}
    file = {'image': (image.name, open(image, 'rb'))}

    r = s.post(url + '/api/posts', data=from_data, files=file)
    if not r.status_code == 201:
        print('Upload post failed.')
        return


if __name__ == '__main__':
    username = '<uesr@email>'
    password = 'xxxxx'

    text = str(input('请输入博文内容：'))

    for i in range(40):
        image_file = input('请输入图片路径，例如./lena.jpg:\n')
        if os.path.exists(image_file) == False :
            print("您输入的路径错误！请重新输入！")
        else:
            break

    #image_file = r'./purple.jpeg'
    url = 'http://127.0.0.1:5000'

    new_image = Path(image_file).with_name('embed.jpg')

    water_input=str(input("请输入想要添加的水印："))

    embed_watermark(image_file, water_input, str(new_image))
    #embed_watermark(image_file, 'hello,world!', str(new_image))

    send_post(username, password, text, str(new_image), url)
