#encoding=utf-8
from django.core.mail import send_mail,send_mass_mail
from threading import Thread
from django.conf import settings
 
def mail_to_one(subject,content,to_email):
    """多线程发送电子邮件到一个指定用户，to_email为字符串"""
    from_email = settings.EMAIL_HOST_USER
    th = Thread(target=send_mail,args=(subject,content,from_email,[to_email]))
    th.start()

def mail_to_list(subject,content,recipient_list):
    """多线程群发邮件,不会在收件人中显示所有收件人
       recipient_list -- 收件人list
    """
    from_email = settings.EMAIL_HOST_USER
    data_list = []
    for to_email in recipient_list :
        one_data_tuple = (subject,content,from_email,[to_email])
        data_list.append(one_data_tuple)
    data_tuple=tuple(data_list)
    th = Thread(target=send_mass_mail,args=(data_tuple,))
    th.start()
