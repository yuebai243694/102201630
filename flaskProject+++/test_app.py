import unittest
from flask import Flask
from app import app, db, User, Message, socketio
from flask_socketio import SocketIOTestClient

class SocketIOTestCase(unittest.TestCase):
    def setUp(self):
        # 设置测试环境
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        # 创建一个测试用户
        self.test_user = User(username='testuser', password='testpassword')
        db.session.add(self.test_user)
        db.session.commit()

        # 创建 SocketIO 测试客户端
        self.socketio_client = socketio.test_client(app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.socketio_client.disconnect()

    # 测试 send_message 事件
    def test_handle_send_message(self):
        # 准备发送的数据
        data = {
            'username': 'testuser',
            'message': 'shibushirenna'
        }

        # 向服务器发送消息事件
        self.socketio_client.emit('send_message', data)

        # 从数据库中查询是否消息保存成功
        saved_message = Message.query.filter_by(username='testuser').first()
        self.assertIsNotNone(saved_message)
        self.assertEqual(saved_message.content, 'shibushirenna')

        # 确认服务器是否广播了消息
        received = self.socketio_client.get_received()  # 获取客户端接收到的所有事件
        self.assertTrue(any(event['name'] == 'receive_message' for event in received))

        # 检查广播的数据是否正确
        received_data = received[0]['args'][0]  # 获取广播的第一个事件及其参数
        self.assertEqual(received_data['username'], 'testuser')
        self.assertEqual(received_data['message'], 'shibushirenna')

if __name__ == '__main__':
    unittest.main()
