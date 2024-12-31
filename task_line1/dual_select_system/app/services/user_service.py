import bcrypt
from app.dao.user_dao import get_user_by_id, insert_user
from app.dao.advisor_dao import get_advisor_by_id  # 导入新的 DAO 方法

def authenticate_user(userid, password):
    """
    验证普通用户身份
    :param userid: 用户 ID
    :param password: 用户密码
    :return: 返回用户信息（字典形式），如果验证失败，返回 None
    """
    user = get_user_by_id(userid)  # 从数据库中获取用户信息
    if user:
        hashed_password = user['password']  # 数据库中存储的加密密码
        # 校验密码
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return user  # 返回用户信息，包括角色
    return None

def authenticate_advisor(advisor_id):
    """
    验证导师身份
    :param advisor_id: 导师 ID
    :return: 返回导师信息（字典形式），如果验证失败，返回 None
    """
    advisor = get_advisor_by_id(advisor_id)  # 从数据库中获取导师信息
    if advisor:
        return advisor  # 如果找到对应的导师记录，则返回导师信息
    return None

def register_user(userid, password, role):
    """
    注册新用户
    :param userid: 用户 ID
    :param password: 用户密码
    :param role: 用户角色
    :return: 如果注册成功，返回 True；如果用户已存在，返回 False
    """
    existing_user = get_user_by_id(userid)
    if existing_user:
        return False  # 如果用户已存在，则返回 False
    # 对密码进行 bcrypt 加密
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # 将加密后的密码存入数据库
    return insert_user(userid, hashed_password.decode('utf-8'), role)