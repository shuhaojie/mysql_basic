import pymysql

con = pymysql.connect(host="localhost", user="root", passwd="805115148",
                      db="mysql_basic", port=int(3306), charset='utf8',
                      autocommit=True)

try:
    with con.cursor() as cursor:
        # 执行SQL（此时事务隐式开启）
        cursor.execute("insert into user(id, username, password, email) values (1, 'haojie', '123456', 'haojie@qq.com')")
        cursor.execute("insert into user(id, username, password, email) values (1, 'yuwen', '123456', 'yuwen@qq.com')")

    # 手动提交事务
    con.commit()  # ⭐⭐⭐ 关键步骤 ⭐⭐⭐

except Exception as e:
    # 出错时回滚
    con.rollback()  # ⭐⭐⭐ 关键步骤 ⭐⭐⭐
    print(f"Transaction failed: {e}")

finally:
    con.close()
