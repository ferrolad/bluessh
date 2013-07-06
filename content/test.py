#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""生成简单的包含文字的图片
"""

import Image
import ImageDraw
import ImageFont

# 新建图片
img = Image.new("RGB", (60, 20), (255, 255, 255))
# 绘制图片
draw = ImageDraw.Draw(img)
# 字体
font = ImageFont.truetype('arialbd.ttf', 15)
# 绘入文字
draw.text((5, 3), u"a65b12", font=font, fill="#009000")
# 保存到文件, fill="#000000"
img.save('../static/img/no-cache/test.png', 'png')
