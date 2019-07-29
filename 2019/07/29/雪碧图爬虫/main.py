#-*- coding:utf-8 -*-
#author:ciker
#version:0.0.1
'''
    
    
'''

import requests
import re
from PIL import Image
from io import BytesIO
import base64

class SESSION2:
    def __init__(self):
        self.name = '爬虫联系2'
        self.url_base = 'http://glidedsky.com/level/web/crawler-basic-2?page=%d'
        self.cookie = {'glidedsky_session':'eyJpdiI6IjQxb2NEOXRNTDVzUzlmN3IrMUQwRHc9PSIsInZhbHVlIjoiZDhvb3FGNHZSdmpub0Vlajd4Sk5yZHVodjZtNGRhTFp1RFh1VHRKR3haN3ZkbXp1S2ZzOGJQQk9EbDdrdVRiaCIsIm1hYyI6ImM4YzI1OTNjMTViMDc3YmQ5YjQ0NmQzYTJhZjQ1NjAzMzYyZjEyZjYzZDg0OGIyOGI4YTU4ODdjNmFjZjM2ODUifQ%3D%3D'}
        self.num = r'<div class="col-md-1">(.*?)</div>'

    def T(self):
        rt = requests.get(self.url_base, cookies=self.cookie).content
        print(rt)

    def Main(self):
        num_sum = 0
        for i in range(1,1001,1):
            rt = requests.get(self.url_base % i, cookies=self.cookie).text
            for n in re.findall(self.num, rt, re.S|re.M):
                # print(n.strip())
                num_sum = num_sum + int(n.strip())
            print('%d page sum : %d'%(i, num_sum))

        print(num_sum)


class SESSION10:
    def __init__(self):
        self.url_base = 'http://glidedsky.com/level/web/crawler-sprite-image-1?page=%d'
        self.style_reg = r'<style>(.*?)</style>'
        self.image_reg = r'"data:image/png;base64,(.*?)"\)'
        self.position_reg = '\.(\w+)\s*{\s*background-position-x:(-?\d+)px }'
        self.class_block = '<div class="col-md-1">(.*?)\s</div>'
        self.num_reg = r'<div class="(\w+)\s+sprite'

        self.cookie = {
            'glidedsky_session': 'eyJpdiI6Im9yV1RkbERTYUhialhYOXhoajVMbVE9PSIsInZhbHVlIjoiQkZqRlc5WnBYakN3bU1YQ0pUNE9oNmRBb2pFVkNlS3M4MHBoS2J6RmNueFZleWxKVUNOR1B3SmlGOHlSc3pRNiIsIm1hYyI6ImI3OTEwNGYwZWYzZjhiNWRlMDJjOTkxZjk4OWJhZmJkYjA5YmFiNDY5ODFhNWQ1MGVkNDAzZmZlOTZiYzYwMzUifQ%3D%3D'}
        self.position_dic = {}


    def T(self, url):
        rt = requests.get(url, cookies=self.cookie).text
        # print(re.findall(self.style_reg, rt, re.S|re.M))
        # print(re.findall(self.image_reg, rt))
        # print(re.findall(self.position_reg, rt))
        image_base64 = re.findall(self.image_reg, rt)[0]

        for name, px in re.findall(self.position_reg, rt):
            self.position_dic[name] = px.replace('-','')

        block_arr = []
        for block in re.findall(self.class_block, rt, re.S|re.M):
            tmp = []
            for num in re.findall(self.num_reg, block):
                tmp.append(num)
            block_arr.append(tmp)

        image_data = BytesIO(base64.b64decode(image_base64))
        img = Image.open(image_data)

        width = img.size[0]
        height = img.size[1]
        is_sign = False
        split_num = []
        for x in range(0, width):
            check_flag = False
            for y in range(0, height):
                pix_data = img.getpixel((x,y))
                if not (pix_data[0] > 250 and pix_data[1] > 250 and pix_data[2] > 250):
                    check_flag = True
                    break
            if is_sign ^ check_flag:
                split_num.append(int(x))
                is_sign = not is_sign
        sum_num = 0
        for block in block_arr:
            rt_str = ''
            for num_str in block:
                for i in range(0, len(split_num)):
                    if int(self.position_dic[num_str]) < split_num[i]:
                        rt_str = rt_str + str(int(i/2))
                        break
            sum_num = sum_num + int(rt_str)

        return sum_num

    def Main(self):
        snum = 0
        for i in range(1, 1001):
            url = self.url_base % i
            snum = snum + self.T(url=url)
            print(snum)

        print(snum)



if __name__ == '__main__':
    s = SESSION10()
    # s.T()
    s.Main()
