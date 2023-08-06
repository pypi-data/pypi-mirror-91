from db.db_init import DBSession, User

class userDao(object):
    def add_user(self):
        # 创建session对象:
        session = DBSession()
        # 创建新User对象:
        new_user = User(name='BobAA')
        # 添加到session:
        session.add(new_user)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

    def find_user(self):
        # 创建Session:
        session = DBSession()
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        user = session.query(User).filter(User.id == 2).one()
        # 打印类型和对象的name属性:
        print('type:', type(user))
        print('name:', user.name)
        # 关闭Session:
        session.close()



if __name__ == '__main__':
    user = userDao()
    # user.add_user()
    user.find_user()