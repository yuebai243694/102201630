import unittest
from flask import url_for
from app import app  # 确保从您的应用模块导入app

class IndexRouteTestCase(unittest.TestCase):

    def setUp(self):
        """在每个测试之前设置测试客户端和上下文"""
        self.app = app.test_client()
        self.app.testing = True  # 开启测试模式
        self.ctx = app.app_context()  # 创建应用上下文
        self.ctx.push()  # 推入上下文
        app.config['SERVER_NAME'] = 'localhost.localdomain'  # 设置一个假服务器名称

    def tearDown(self):
        """在每个测试之后弹出上下文"""
        self.ctx.pop()  # 弹出上下文

    def test_index_redirects_to_login(self):
        """测试index路由是否重定向到login"""
        with self.app:  # 使用上下文管理器确保上下文有效
            response = self.app.get('/')  # 访问index路由
            self.assertEqual(response.status_code, 302)  # 检查响应状态码是否为302（重定向）
            self.assertEqual(response.location, '/login')  # 检查重定向位置为相对路径

if __name__ == '__main__':
    unittest.main()
