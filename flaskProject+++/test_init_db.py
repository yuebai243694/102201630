import unittest
from app import app, db, User  # 直接导入 app

class InitDBTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 创建应用程序实例
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()  # 创建所有表

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()  # 删除所有表

    def test_init_db_creates_users(self):
        with self.app.app_context():
            # 确保数据库初始化之前没有用户
            self.assertIsNone(User.query.filter_by(username='111').first())
            self.assertIsNone(User.query.filter_by(username='yjj').first())

            # 初始化数据库
            self.init_db()

            # 验证用户是否被添加到数据库
            user_111 = User.query.filter_by(username='111').first()
            user_yjj = User.query.filter_by(username='yjj').first()

            self.assertIsNotNone(user_111)
            self.assertEqual(user_111.password, '111')  # 密码应正确
            self.assertIsNotNone(user_yjj)
            self.assertEqual(user_yjj.password, 'yjj')  # 密码应正确

    def init_db(self):
        # 创建所有表
        with self.app.app_context():
            db.create_all()

            # 添加默认用户
            if not User.query.filter_by(username='111').first():
                admin_user = User(id=1024, username='111', password='111')
                db.session.add(admin_user)
                db.session.commit()
            if not User.query.filter_by(username='yjj').first():
                admin_user = User(id=111, username='yjj', password='yjj')
                db.session.add(admin_user)
                db.session.commit()

if __name__ == '__main__':
    unittest.main()
