from webapp.exts import celery
import smtplib
from email.mime.text import MIMEText
from webapp.models import Reminder, Post
import datetime
from flask import render_template
from webapp.exts import mail
from flask_mail import Message

@celery.task
def log(msg):
    return msg


@celery.task
def multiply(x,y):
    return x*y


# 给用户发送reminder邮件
@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5)
def remind(self,pk):
    reminder = Reminder.query.get(pk)
    msg = Message('Your reminder',
                  sender='from@example.com',
                  recipients=[reminder.email])
    msg.body = reminder.text
    mail.send(msg)


# 通过回调函数触发remind任务
def on_reminder_save(mapper, connect, self):
    remind.apply_async(args=(self.id,), eta=self.date)


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def digest(self):
    # 找出这周的起始和结束日
    year, week = datetime.datetime.now().isocalendar()[0:2]
    # isocalendar()：返回(ISO year, ISO week number, ISO weekday)元组。
    date = datetime.datetime(year, 1, 1)
    # iso时间的第一周必须大于等于4天
    if date.weekday() > 3:
        date = date + datetime.timedelta(days=7 - date.weekday())
    delta = datetime.timedelta(days=(week-1)*7)
    start, end = date + delta, date + delta + datetime.timedelta(days=6)

    # 筛选出本周的文章
    posts = Post.query.filter(Post.publish_date >= start,
                              Post.publish_date<= end
                              ).all()

    if len(posts) ==0:
        return

    msg = MIMEText(
        render_template('digest.html', posts=posts), 'html'
    )

    user = '404846497@qq.com'
    password = 'ade17605085910'
    your_email = user

    msg['Subject'] = 'Weekly Digest'
    msg['From'] = your_email

    try:
        smtp_server = smtplib.SMTP('localhost')
        smtp_server.starttls()
        smtp_server.login(user, password)
        smtp_server.sendmail(
            your_email,
            [recipients],  # 如何获取recipients?
            msg.as_string()
        )
        smtp_server.close()

        return

    except Exception as e:
        self.retry(exc=e)


