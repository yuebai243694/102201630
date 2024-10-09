from app import app, db, User, Project

def init_db():
    # 创建所有表
    with app.app_context():
        # 创建所有表
        db.create_all()

    # 添加一个默认用户（如果需要）
        if not User.query.filter_by(username='111').first():
            admin_user = User(id = 1024, username='111', password='111')
            db.session.add(admin_user)
            db.session.commit()
        if not User.query.filter_by(username='yjj').first():
            admin_user = User(id = 111, username='yjj', password='yjj')
            db.session.add(admin_user)
            db.session.commit()
if __name__ == '__main__':
    init_db()
