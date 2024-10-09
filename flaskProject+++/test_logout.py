import unittest
from flask import json
from app import app, db
from app import User

class LogoutRouteTestCase(unittest.TestCase):

    def setUp(self):
        """在每个测试之前设置测试客户端和上下文"""
        self.app = app.test_client()
        self.app.testing = True
        self.ctx = app.app_context()
        self.ctx.push()

        # 创建测试用户
        self.user = User(username='testuser', password='testpass')
        db.create_all()
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """在每个测试之后清理数据库和上下文"""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login(self):
        """模拟用户登录"""
        with self.app.session_transaction() as sess:
            sess['user_id'] = self.user.id

    def test_logout(self):
        """测试登出功能"""
        self.login()  # 模拟用户登录

        # 发送登出请求
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # 确保状态码为200
        self.assertIn(b'Welcome', response.data)  # 检查是否重定向到登录页面

    def test_login_page_render(self):
        """测试登录页面的呈现"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)  # 确保状态码为200
        self.assertIn(b'Welcome', response.data)  # 检查页面标题是否存在
        self.assertIn(b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d', response.data)  # 检查用户名输入框是否存在（用户输入框的 UTF-8 编码）
        self.assertIn(b'\xe5\xaf\x86\xe7\xa0\x81', response.data)  # 检查密码输入框是否存在（密码输入框的 UTF-8 编码）

if __name__ == '__main__':
    unittest.main()
