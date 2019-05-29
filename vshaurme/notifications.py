from flask import url_for

from vshaurme.extensions import db
from vshaurme.models import Notification


def push_follow_notification(follower, receiver):
    message = 'Пользователь <a href="%s">%s</a> подписался на вас.' % \
              (url_for('user.index', username=follower.username), follower.username)
    notification = Notification(message=message, receiver=receiver)


def push_comment_notification(photo_id, receiver, page=1):
    message = '<a href="%s#comments">Под этой фотографией</a> появился новый комментарий/reply.' % \
              (url_for('main.show_photo', photo_id=photo_id, page=page))
    notification = Notification(message=message, receiver=receiver)


def push_collect_notification(collector, photo_id, receiver):
    message = 'Пользователь <a href="%s">%s</a> добавил ваше фото в свою коллекцию <a href="%s">photo</a>' % \
              (url_for('user.index', username=collector.username),
               collector.username,
               url_for('main.show_photo', photo_id=photo_id))
    notification = Notification(message=message, receiver=receiver)
