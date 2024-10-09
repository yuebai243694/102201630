import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from app import app, db, User, load_user  # 确保正确导入User模型和load_user函数

class UserLoaderTestCase(unittest.TestCase):

    def create_app(self):
        # 设置测试配置
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """在每个测试之前创建数据库表"""
        self.app = self.create_app()
        self.app_context = self.app.app_context()  # 创建应用上下文
        self.app_context.push()  # 推入应用上下文
        db.create_all()  # 创建数据库表

        # 创建测试用户
        self.user = User(username='test_user', password='password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """在每个测试后销毁数据库表"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # 弹出应用上下文

    def test_load_user(self):
        """测试load_user函数是否正确加载用户"""
        loaded_user = load_user(self.user.id)  # 调用load_user函数

        # 检查返回的用户对象是否正确
        self.assertIsNotNone(loaded_user)  # 确保加载的用户不为None
        self.assertEqual(loaded_user.id, self.user.id)
        self.assertEqual(loaded_user.username, 'test_user')

    def test_load_user_nonexistent(self):
        """测试load_user函数在用户不存在时返回None"""
        loaded_user = load_user(9999)  # 使用不存在的用户ID
        self.assertIsNone(loaded_user)  # 应该返回None

if __name__ == '__main__':
    unittest.main()
