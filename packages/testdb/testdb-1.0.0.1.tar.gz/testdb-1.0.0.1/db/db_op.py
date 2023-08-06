from db.db_init import DBSession, User, Role, Goods, Order


class userDao(object):
    def add(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        # 创建session对象:
        session = DBSession()
        # 创建新User对象:
        new_user = User(name='userN')
        # 添加到session:
        session.add(new_user)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

    def find(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        # 创建Session:
        session = DBSession()
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        user = session.query(User).filter(User.id == 2).one()
        # 打印类型和对象的name属性:
        print('type:', type(user))
        print('name:', user.name)
        # 关闭Session:
        session.close()
        return user



class roleDao(object):
    def add(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        session = DBSession()
        new_user = Role(name='roleN')
        session.add(new_user)
        session.commit()
        session.close()

    def find(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        session = DBSession()
        user = session.query(Role).filter(Role.id == 1).one()
        print('type:', type(user))
        print('name:', user.name)
        session.close()
        return user



class goodsDao(object):
    def add(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        session = DBSession()
        new_user = Goods(name='roleN')
        session.add(new_user)
        session.commit()
        session.close()

    def find(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        session = DBSession()
        user = session.query(Goods).filter(Goods.id == 1).one()
        print('type:', type(user))
        print('name:', user.name)
        session.close()
        return user



class orderDao(object):
    def add(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        session = DBSession()
        new_user = Order(name='roleN')
        session.add(new_user)
        session.commit()
        session.close()

    def find(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        session = DBSession()
        user = session.query(Order).filter(Order.id == 1).one()
        print('type:', type(user))
        print('name:', user.name)
        session.close()
        return user

if __name__ == '__main__':
    user = userDao()
    print("find_user==>>>", user.find())

    role = roleDao()
    print("find_role==>>>", role.find())

    goods = goodsDao()
    print("find_goods==>>>", goods.find())

    order = orderDao()
    print("find_order==>>>", order.find(name="chaizhichao"))