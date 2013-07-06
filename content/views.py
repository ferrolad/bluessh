#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from content.models import *
from django.http import HttpResponse
import json
import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# need PIL
import Image
import ImageDraw
import ImageFont
import os.path


def show_content(request, url):
    obj_content = get_object_or_404(link_content, link_url=url)
    title = obj_content.title
    content = obj_content.content
    return render_to_response('content/content.html',
                              {'page_title': title, 'content': content})


def show_freessh(request):
    freessh = get_object_or_404(FreeSSH, username='bluessh')
    return render_to_response('content/freessh.html',
                              {'username': freessh.username,
                               'passwd': freessh.passwd,
                               'update_time': freessh.update_time})


def get_menu(request):
    """获取菜单,返回json"""
    if request.method == 'GET':
        menu_list = []
        try:
            menus = menu_tab.objects.filter(is_display=True)
            for menu in menus:
                menu_list.append((menu.name, menu.link_url))
        except:
            pass
        menu_json = json.dumps(menu_list)
        return HttpResponse(menu_json)


def get_notice(request):
    """获取公告,返回json"""
    if request.method == 'GET':
        notice_dic = {}
        try:
            now = datetime.datetime.now()
            notice = Notice.objects.filter(is_shown=True,
                                           start_date__lte=now, end_date__gte=now)[0]
            notice_dic = {'notice': notice.info}
        except:
            pass
        notice_json = json.dumps(notice_dic)
        return HttpResponse(notice_json)


@csrf_exempt
def post_freessh(request):
    """免费SSH帐号信息"""
    if request.method == "POST":
        if request.POST['pri_key'] == settings.PRI_KEY:
            username = request.POST['username']
            passwd = request.POST['passwd']
            try:
                freessh = FreeSSH.objects.get(username=username)
                freessh.passwd = passwd
            except FreeSSH.DoesNotExist:
                freessh = FreeSSH(username=username, passwd=passwd)
            finally:
                freessh.save()
                # 密码生成图片
                text2img(passwd)
                return HttpResponse('Success')
        else:
            return HttpResponse('the post private key is incorrect!')
    else:
        return HttpResponse('no paras!')


def text2img(txt):
    """文字生成图片"""
    save_path = os.path.join(settings.PROJECT_DIR, 'static/img/no-cache/passwd.png').replace('\\', '/')
    font_path = os.path.join(
        settings.PROJECT_DIR, 'content/arialbd.ttf').replace('\\', '/')
    # 新建图片
    img = Image.new("RGB", (60, 20), "#eee")
    # 绘制图片
    draw = ImageDraw.Draw(img)
    # 字体
    font = ImageFont.truetype(font_path, 16)
    # 绘入文字
    draw.text((1, 3), txt, font=font, fill="#009000")
    # 保存到文件, fill="#000000"
    img.save(save_path, 'png')
