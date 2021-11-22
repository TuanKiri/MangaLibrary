import time
import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser, follows, Manga, logs


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='123')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='123')
        with self.assertRaises(AttributeError):
            u.password
    
    def test_password_verification(self):
        u = User(password='123')
        self.assertTrue(u.verify_password('123'))
        self.assertFalse(u.verify_password('456'))

    def test_password_salts_are_random(self):
        u = User(password='123')
        u2 = User(password='456')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='123')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='123')
        u2 = User(password='456')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='123')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, '456'))
        self.assertTrue(u.verify_password('456'))

    def test_invalid_reset_token(self):
        u = User(password='123')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + '1', '456'))
        self.assertTrue(u.verify_password('123'))

    def test_valid_email_change_token(self):
        u = User(email='artem@mail.ru', password='123')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('roma@mail.ru')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'roma@mail.ru')

    def test_invalid_email_change_token(self):
        u1 = User(email='artem@mail.ru', password='123')
        u2 = User(email='roma@mail.ru', password='456')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_email_change_token('denis@mail.ru')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'roma@mail.ru')

    def test_duplicate_email_change_token(self):
        u1 = User(email='artem@mail.ru', password='123')
        u2 = User(email='roma@mail.ru', password='456')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token('artem@mail.ru')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'roma@mail.ru')

    def test_user_role(self):
        u = User(email='artem@mail.ru', password='123')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.PUBLICATION))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
        self.assertFalse(u.can(Permission.BANNED))
        self.assertFalse(u.can(Permission.PREMIUM))

    def test_moderator_role(self):
        r = Role.query.filter_by(name='Moderator').first()
        u = User(email='artem@mail.ru', password='123', role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.PUBLICATION))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
        self.assertFalse(u.can(Permission.BANNED))
        self.assertFalse(u.can(Permission.PREMIUM))

    def test_administrator_role(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='artem@mail.ru', password='123', role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.PUBLICATION))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))
        self.assertFalse(u.can(Permission.BANNED))
        self.assertFalse(u.can(Permission.PREMIUM))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.PUBLICATION))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
        self.assertFalse(u.can(Permission.BANNED))
        self.assertFalse(u.can(Permission.PREMIUM))

    def test_banned_role(self):
        r = Role.query.filter_by(name='Banned').first()
        u = User(email='artem@mail.ru', password='123', role=r)
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.PUBLICATION))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
        self.assertTrue(u.can(Permission.BANNED))
        self.assertFalse(u.can(Permission.PREMIUM))

    def test_premium_role(self):
        r = Role.query.filter_by(name='Premium').first()
        u = User(email='artem@mail.ru', password='123', role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.PUBLICATION))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
        self.assertFalse(u.can(Permission.BANNED))
        self.assertTrue(u.can(Permission.PREMIUM))

    def test_timestamps(self):
        u = User(password='123')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.member_since).total_seconds() < 3)
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User(password='123')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)

    def test_follows(self):
        u1 = User(email='artem@mail.ru', password='123')
        u2 = User(email='roma@mail.ru', password='456')
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))
        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))
        self.assertTrue(u1.followed.count() == 1)
        self.assertTrue(u1.followers.count() == 0)
        self.assertTrue(u2.followed.count() == 0)
        self.assertTrue(u2.followers.count() == 1)
        u2.follow(u1)
        self.assertTrue(u1.followed.count() == 1)
        self.assertTrue(u1.followers.count() == 1)
        self.assertTrue(u2.followed.count() == 1)
        self.assertTrue(u2.followers.count() == 1)
        f = u1.followed.all()[0]
        self.assertTrue(f == u2)
        f = u2.followers.all()[0]
        self.assertTrue(f == u1)
        u1.unfollow(u2)
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.followed.count() == 0)
        self.assertTrue(u2.followers.count() == 0)
        self.assertTrue(u1.followers.count() == 1)
        self.assertTrue(db.session.query(follows).count() == 1)
        db.session.delete(u2)
        db.session.commit()
        self.assertTrue(db.session.query(follows).count() == 0)

    def test_is_administrator(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='artem@mail.ru', password='123', role=r)
        self.assertTrue(u.is_administrator)

    def test_is_banned_role(self):
        r = Role.query.filter_by(name='Banned').first()
        u = User(email='artem@mail.ru', password='123', role=r)
        self.assertTrue(u.banned)

    def test_avatar_url(self):
        u = User(email='artem@mail.ru')
        with self.app.test_request_context('/'):
            self.assertTrue(u.avatar_url() == '/static/img/avatar.jpg')
        
    def test_background_url(self):
        u = User(email='artem@mail.ru')
        with self.app.test_request_context('/'):
            self.assertTrue(u.background_url() == '/static/img/background.png')

    def test_user_read(self):
        u = User(email='artem@mail.ru')
        m = Manga(title='Ванпанчмен')
        db.session.add_all([u,m])
        db.session.commit()
        self.assertFalse(u.is_reading(m))
        u.read(m)
        db.session.commit()
        self.assertTrue(u.is_reading(m))
        self.assertTrue(m.users.count() == 1)
        f = m.users.all()[0]
        self.assertTrue(f == u)
        u.unread(m)
        db.session.commit()
        self.assertFalse(u.is_reading(m))
        u.read(m)
        db.session.add(u)
        db.session.commit()
        db.session.delete(m)
        db.session.commit()
        self.assertTrue(db.session.query(logs).count() == 0)

