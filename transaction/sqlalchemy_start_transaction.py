from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:805115148@localhost:3306/mysql_basic?charset=utf8mb4")
Session = sessionmaker(bind=engine)  # 通过engine获取连接

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'  # 表名必须与数据库中的表一致

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


with Session() as session:
    try:
        haojie = User(id=1, username='haojie', password='123456', email='haojie@qq.com')
        yuwen = User(id=1, username='yuwen', password='123456', email='yuwen@qq.com')

        session.add(haojie)
        session.add(yuwen)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Transaction failed: {e}")
