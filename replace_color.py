#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
import os
import shutil
import re
from collections import Counter


def get_rgb(val):
    if not isinstance(val, str):
        raise ValueError('参数val不正确')
    if not re.match(r'#[0-9A-F]{6}', val):
        raise ValueError('参数val格式不正确')
    return int(val[1:3], 16), int(val[3:5], 16), int(val[5:7], 16)


def to_rgb(pixel):
    if not isinstance(pixel, (tuple, list)) or len(pixel) < 3:
        raise ValueError('参数pixel格式不正确')
    l = []
    for i in pixel:
        l.append(hex(i)[2:].zfill(2))
        if len(l) == 3:
            break
    return ''.join(map(str, l))


if __name__ == '__main__':
    # 配置信息
    srcDir = '/Users/wenin/mygit/xnb-app-web/static/icons/tabbar' # 替换目录
    mode = 0  # 0 模糊处理，按red、green、blue有一个色彩大于100， 1 指定颜色
    sRGB = '#3074FF' # 当mode为1时有效
    tRGB = '#EA6077' # 目标色彩

    spixel = get_rgb(sRGB)
    tpixel = get_rgb(tRGB)
    print('%s(%s) -> %s(%s)' % (sRGB, spixel, tRGB, tpixel))
    backupPath = os.path.join(srcDir, 'backup')
    if not os.path.exists(backupPath):
        os.mkdir(backupPath)
    for filename in os.listdir(srcDir):
        sfile = os.path.join(srcDir, filename)
        if not os.path.isfile(sfile) or filename.startswith(r'.') or not filename.endswith(('.jpg', '.png')):
            continue
        print('处理图片：', filename)
        flag = False
        img = Image.open(sfile)
        height = img.size[1]
        width = img.size[0]
        print(filename, '=> 宽：', width, ', 高：', height)
        c = Counter()
        for x in range(width):
            for y in range(height):
                cpixel = img.getpixel((x, y))
                if not isinstance(cpixel, tuple) or len(cpixel) < 3:
                    continue
                r, g, b, *o = cpixel
                c[(r, g, b)] += 1
                if (mode == 0 and max(r, g, b) > 120 and (r, g, b) != tpixel) or (mode == 1 and (r, g, b) == spixel):
                    img.putpixel((x, y), (*tpixel, *o))
                    flag = True
        if flag:
            tfile = os.path.join(backupPath, filename)
            if not os.path.exists(tfile):
                shutil.copyfile(sfile, tfile)
            img.save(sfile)
        print(filename, '是否处理成功：', flag, '，最多色彩：', list(map(lambda ele: (to_rgb(ele[0]), ele[1]), c.most_common(5))))
