from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

association_subscriptions = db.Table('association_subscriptions',
                                     db.Column('subscriber_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                     db.Column('subscription_obj_id', db.Integer, db.ForeignKey('user.id'),
                                               primary_key=True)
                                     )

likes = db.Table('likes',
                 db.Column('id_publication', db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE'), primary_key=True),
                 db.Column('id_user', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
                 )

dislikes = db.Table('dislikes',
                    db.Column('id_publication', db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE'), primary_key=True),
                    db.Column('id_user', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
                    )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(256), default='https://s3.eu-north-1.amazonaws.com/lemmycases.ru/avatars/ricardo.jpg')
    description = db.Column(db.Text)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))  # , nullable=False)
    registration_date = db.Column(db.DateTime(), default=datetime.utcnow)
    subscriptions = db.relationship(
        'User', secondary=association_subscriptions,
        primaryjoin=(association_subscriptions.c.subscriber_id == id),
        secondaryjoin=(association_subscriptions.c.subscription_obj_id == id),
        backref=db.backref('association_subscriptions', lazy='dynamic'), lazy='dynamic')
    subscribers = db.relationship(
        'User', secondary=association_subscriptions,
        primaryjoin=(association_subscriptions.c.subscription_obj_id == id),
        secondaryjoin=(association_subscriptions.c.subscriber_id == id),
        lazy='dynamic')
    likes = db.relationship(
        'Publication', secondary=likes,
        primaryjoin=(likes.c.id_user == id),
        lazy='dynamic')
    dislikes = db.relationship(
        'Publication', secondary=dislikes,
        primaryjoin=(dislikes.c.id_user == id),
        lazy='dynamic')
    publications = db.relationship('Publication', backref='author', lazy='dynamic')
    settings = db.relationship('Settings', uselist=False, backref='author')
    notifications = db.relationship('Notification', backref='recipient', lazy='dynamic')

    def sub(self, user):
        """
        Позволяет подписаться на user, т.е. отправляет уведомление
        :param user: объект пользователя на которого нужно подписаться
        """
        if not self.is_subscribed(user):
            self.subscriptions.append(user)
            db.session.add(Notification(type='subscription', id_user=user.id))

    def count_subscriptions(self):
        return len(self.subscriptions.all())

    def count_subscribers(self):
        return len(self.subscribers.all())

    def count_publications(self):
        return len(self.publications.all())

    def show_subscriptions(self):
        for user in self.subscriptions:
            print(user)

    def show_subscribers(self):
        for user in self.subscribers:
            print(user)

    def unsub(self, user):
        """
        Позволяет отписаться от user, т.е. отправляет уведомление
        :param user: объект пользователя от которого нужно отписаться
        """
        if self.is_subscribed(user):
            self.subscriptions.remove(user)
            db.session.add(Notification(type='unsubscription', id_user=user.id))

    def is_subscribed(self, user):
        """
        Проверяет, подписан ли self на user
        :param user: объект пользователя
        """
        if self.id != user.id:
            return self.subscriptions.filter(
                association_subscriptions.c.subscription_obj_id == user.id).count() > 0

    def set_pass(self, password):
        """
        Позволяет установить пароль и захэшировать его
        :param password: пароль
        """
        self.password_hash = generate_password_hash(password)

    def check_pass(self, password):
        """
        Сравнивает пароль с хэшем
        :param password: пароль
        :return:
            True: верный пароль
            False: неверный пароль
        """
        return check_password_hash(self.password_hash, password)

    def create_pub(self, description, content=None):
        """
        Позволяет создать публикацию
        :param description: описание публикации
        :param content: ссылка на фото/видео
        """
        if not content:
            new_publication = Publication(description=description, id_user=self.id)
        else:
            new_publication = Publication(content=content, description=description, id_user=self.id)
        db.session.add(new_publication)

    def show_pub(self):
        for pub in self.publications:
            print(pub)

    def get_pubs(self):
        return self.publications

    def delete_pub(self, id_publication):
        if self.publications.filter(Publication.id == id_publication).count() > 0:
            self.publications.filter(Publication.id == id_publication).delete()

    def set_like(self, id_publication):
        """
        Позволяет поставить лайк на публикацию, т.е. отправляет уведомление
        :param id_publication: айди публикации
        """
        publication = Publication.query.get(id_publication)
        publication.set_like(self)
        db.session.add(Notification(type='like', id_user=publication.author.id, id_publication=publication.id))

    def set_dislike(self, id_publication):
        """
        Позволяет поставить дизлайк на публикацию, т.е. отправляет уведомление
        :param id_publication: айди публикации
        """
        publication = Publication.query.get(id_publication)
        publication.set_dislike(self)
        db.session.add(Notification(type='dislike', id_user=publication.author.id, id_publication=publication.id))

    def create_comment(self, id_publication, text):
        """
        Позволяет создать комментарий, т.е. отправляет уведомление
        :param id_publication: айди публикации
        :param text: текст комментария
        """
        publication = Publication.query.get(id_publication)
        if publication.author.settings.op_to_com:
            publication.set_comment(self, text)
            db.session.add(Notification(type='comment',
                                        id_user=publication.author.id,
                                        id_publication=publication.id,
                                        text=text))

    @classmethod
    def delete_comment(cls, id_comment):
        Comment.query.filter(Comment.id == id_comment).delete()

    def change_ea(self):
        self.settings.email_alerts_change()

    def change_otc(self):
        self.settings.op_to_com_change()

    def show_notification(self, **kwargs):
        """
        Позволяет просмотреть уведомления
        :param kwargs:
            read=True (показать прочитанные уведомления)
            read=False (показать непрочитанные уведомления)
            read=None (показать все уведомления)
        """
        if kwargs.get('read') is None:
            for notification in self.notifications:
                print(notification)
        elif kwargs.get('read'):
            for notification in self.notifications:
                if notification.read:
                    print(notification)
        elif not kwargs.get('read'):
            for notification in self.notifications:
                if not notification.read:
                    print(notification)

    def read_notification(self, id_notification=None):
        """
        Позволяет прочитать уведомлени(е/я)
        :param id_notification: айди уведомления (если необходимо удалить выборочно)
        """
        if not id_notification:
            for notification in self.notifications:
                notification.read = True
        else:
            for notification in self.notifications:
                if notification.id == id_notification:
                    notification.read = True
                    break

    def __repr__(self):
        return '<User {}>'.format(self.login)


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), default='/static/publications/default.jpg')
    description = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    publication_date = db.Column(db.DateTime(), default=datetime.utcnow)
    likes = db.relationship(
        'User', secondary=likes,
        primaryjoin=(likes.c.id_publication == id),
        lazy='dynamic')
    dislikes = db.relationship(
        'User', secondary=dislikes,
        primaryjoin=(dislikes.c.id_publication == id),
        lazy='dynamic')
    comments = db.relationship('Comment', backref='publication', lazy='dynamic')

    def set_like(self, user):
        if user in self.likes:
            self.likes.remove(user)
        elif user in self.dislikes:
            self.dislikes.remove(user)
            self.likes.append(user)
        else:
            self.likes.append(user)

    def set_dislike(self, user):
        if user in self.dislikes:
            self.dislikes.remove(user)
        elif user in self.likes:
            self.likes.remove(user)
            self.dislikes.append(user)
        else:
            self.dislikes.append(user)

    def set_comment(self, user, text):
        new_comment = Comment(id_publication=self.id, id_user=user.id, text=text)
        db.session.add(new_comment)

    def show_likes(self):
        for user in self.likes:
            print(user)

    def show_dislikes(self):
        for user in self.dislikes:
            print(user)

    def show_comments(self):
        for user in self.comments:
            print(user)

    def __repr__(self):
        return '<Publication {} from {}>'.format(self.id, self.author)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_publication = db.Column(db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment {} on publication {} from user {}>'.format(self.id, self.id_publication, self.id_user)


class Settings(db.Model):
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    op_to_com = db.Column(db.Boolean, default=True)
    email_alerts = db.Column(db.Boolean, default=True)

    def email_alerts_change(self):
        self.email_alerts = not self.email_alerts

    def op_to_com_change(self):
        self.op_to_com = not self.op_to_com

    def __repr__(self):
        return '<Settings {} EO = {}, OTC={}>'.format(self.author, self.email_alerts, self.op_to_com)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    id_publication = db.Column(db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Notification {} with type {} for user {} ~ read = {}>'.format(self.id, self.type, self.id_user,
                                                                                self.read)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))