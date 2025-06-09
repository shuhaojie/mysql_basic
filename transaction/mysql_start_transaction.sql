# 开启事务
begin;
insert into user(id, username, password, email) values (1, "haojie", "123456", "haojie@qq.com");
insert into user(id, username, password, email) values (1, "yuwen", "123456", "yuwen@qq.com");
commit;


# 查看隔离级别
show variables like 'transaction_isolation';

# 设置隔离级别为读未提交
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;



