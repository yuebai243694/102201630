from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////sqlite.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)
migrate = Migrate(app, db)

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# 项目模型
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))  # 添加描述字段
    due_date = db.Column(db.String(50))  # 添加截止日期字段
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('projects', lazy=True))

# 消息模型
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 消息 ID
    username = db.Column(db.String(150), nullable=False)  # 发送者用户名
    content = db.Column(db.String(500), nullable=False)  # 消息内容

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
@login_required
def search():
    search_term = request.form.get('search_term')
    # 在项目中进行搜索
    projects = Project.query.filter(Project.name.ilike(f'%{search_term}%')).all()
    return {
        'projects': [{'name': project.name, 'description': project.description, 'due_date': project.due_date} for project in projects]
    }

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('登录失败，请检查用户名和密码')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    with app.app_context():  # 确保在应用上下文中执行数据库操作
        projects = Project.query.all()
    return render_template('dashboard.html', projects=projects)

@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['description']
        project_due_date = request.form['due_date']
        with app.app_context():  # 确保在应用上下文中执行数据库操作
            new_project = Project(name=project_name, description=project_description, due_date=project_due_date, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_project.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get_messages')
@login_required
def get_messages():
    messages = Message.query.all()  # 查询所有历史消息
    return {
        'messages': [{'username': msg.username, 'message': msg.content} for msg in messages]
    }

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在，请选择其他用户名')
            return redirect(url_for('register'))
        
        # 创建新用户并添加到数据库
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# 更新其他现有的路由...

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@socketio.on('send_message')
def handle_send_message(data):
    # 保存消息到数据库
    new_message = Message(username=data['username'], content=data['message'])
    db.session.add(new_message)
    db.session.commit()

    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    with app.app_context():  # 确保在应用上下文中创建数据库
        db.create_all()
    app.run(host='0.0.0.0', port=5000)


# if __name__ == '__main__':
#     with app.app_context():  # 确保在应用上下文中创建数据库
#         db.create_all()
#     app.run(host='0.0.0.0', port=5000)
#
#
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
# app.config['SECRET_KEY'] = 'your_secret_key'
# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# socketio = SocketIO(app)
#
# # 用户模型
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#
# # 项目模型
# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     description = db.Column(db.String(500))
#     due_date = db.Column(db.String(50))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
# @app.route('/')
# def index():
#     return redirect(url_for('login'))
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username, password=password).first()
#         if user:
#             login_user(user)
#             return redirect(url_for('dashboard'))
#         else:
#             flash('登录失败，请检查用户名和密码')
#     return render_template('login.html')
#
# @app.route('/dashboard')
# @login_required
# def dashboard():
#     projects = Project.query.filter_by(user_id=current_user.id).all()
#     return render_template('dashboard.html', projects=projects)
#
# @app.route('/create_project', methods=['GET', 'POST'])
# @login_required
# def create_project():
#     if request.method == 'POST':
#         project_name = request.form['project_name']
#         project_description = request.form['description']
#         project_due_date = request.form['due_date']
#         new_project = Project(name=project_name, description=project_description, due_date=project_due_date, user_id=current_user.id)
#         db.session.add(new_project)
#         db.session.commit()
#         return redirect(url_for('dashboard'))
#     return render_template('create_project.html')
#
# @app.route('/delete_project/<int:project_id>')
# @login_required
# def delete_project(project_id):
#     project = Project.query.get(project_id)
#     if project and project.user_id == current_user.id:
#         db.session.delete(project)
#         db.session.commit()
#     return redirect(url_for('dashboard'))
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
#
# @app.route('/chat')
# @login_required
# def chat():
#     return render_template('chat.html')
#
# @socketio.on('send_message')
# def handle_send_message(data):
#     emit('receive_message', data, broadcast=True)
#
# if __name__ == '__main__':
#     with app.app_context():  # 确保在应用上下文中创建数据库
#         db.create_all()
#     app.run(host='0.0.0.0', port=5000)