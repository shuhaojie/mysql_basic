## 一、MySQL概述

### 1. 相关概念

- 数据库：存储数据的仓库，数据是有组织的进行存储
- 数据库管理系统：操纵和管理数据库的大型软件
- SQL：操作关系型数据库的编程语言，定义了一套操作关系型数据库统一标准

### 2. MySQL安装及启动

MySQL的安装参考官网，https://dev.mysql.com/doc/refman/8.4/en/macos-installation-pkg.html

MySQL服务安装好之后，如果想连接mysql，可以使用如下命令来进行连接

```bash
mysql [-h 127.0.0.1] [-P 3306] -uroot -p
```

### 3. 数据模型

下图右侧是MySQL服务器，左侧是客户端

![image-20250702205328933](./assets/image-20250702205328933.png)

在数据库服务器中有个软件，称之为DBMS，它会创建、维护和操作多个数据库，而一个数据库里由可以维护多张表，而我们的数据是存储在表结构当中的。

## 二、SQL

### 1. SQL通用语法

- SQL语句可以单行或多行书写，以分号结尾。
- SQL语句可以使用空格/缩进来增强语句的可读性。
- MySQL数据库的SQL语句不区分大小写，关键字建议使用大写。
- 注释:
  - 单行注释：-- 注释内容 或 # 注释内容(MySQL特有)
  - 多行注释：/*注释内容 */

### 2. SQL分类

SQL可以分为四大类

- DDL：Data Definition Language，数据定义语言，用来定义数据库对象(数据库，表，字段)
- DML：Data Manipulation Language，数据操作语言，用来对数据库表中的数据进行增、删、改
- DQL：Data Query Language，数据查询语言，用来查询数据库中表的记录
- DCL：Data Control Language，数据控制语言，用来创建数据库用户、控制数据库的访问权限

### 3. DDL

#### （1）数据库操作

- 查询
  - 查询所有数据库：`SHOW DATABASES;`
  - 查询当前数据库：`SELECT DATABASE();`注意这个括号里不要填任何东西。
- 创建：`CREATE DATABASE [IF NOT EXISTS] 数据库名 [DEFAULT CHARSET 字符集] [COLLATE 排序规则]; `这里建议使用字符集为utf8mb4，可以存储的字符长度比较长。
- 删除：`DROP DATABASE [IF EXISTS] 数据库名;`
- 使用：`USE 数据库名;`

#### （2）表操作

##### i. 查询

- 查询当前数据库所有表： `SHOW TABLES;`
- 查询表结构：`DESC 表名;`
- 查询指定表的建表语句：`SHOW CREATE TABLE 表名;`

##### ii. 创建

```sql
CREATE TABLE 表名(
	字段1 字段1类型 [COMMENT 字段1注释],
  字段2 字段2类型 [COMMENT 字段2注释],
	字段3 字段3类型 [COMMENT 字段3注释],
	字段n 字段n类型 [COMMENT 字段n注释]
)[COMMENT 表注释];
```

数据类型：

1. 数值类型：

![image-20250702212902495](./assets/image-20250702212902495.png)

- 对于无符号和有符号的使用，在定义的时候可以加上关键字，例如`age TINYINT UNSIGNED`
- 使用小数的方法：`score double(4,1)`，其中4代表的是整体长度，1代表的是小数点位数

2. 字符串类型：

<img src="./assets/image-20250702213428688.png" alt="image-20250702213428688" style="zoom: 60%;" />

- char和varchar：char是定长，varchar是变长。varchar性能相对较差，因为长度不确定。

3. 日期时间类型：

<img src="./assets/image-20250702214026615.png" alt="image-20250702214026615" style="zoom:67%;" />

例子：设计一张员工信息表，要求如下:

- 编号(纯数字)
- 员工工号(字符串类型，长度不超过10位)
- 员工姓名(字符串类型，长度不超过10位) 
- 性别(男/女，存储一个汉字)
- 年龄(正常人年龄，不可能存储负数)
- 身份证号(二代身份证号均为18位，身份证中有X这样的字符)
- 入职时间(取值年月日即可)

```sql
create table emp(
  id int comment '编号',
  workno varchar(10) comment '工号', 
  name varchar(10) comment '姓名',
  gender char(1) comment '性别',
  age tinyint unsigned comment '年龄',
  idcard char(18) comment '身份证',
  entrydate date comment '入职时间')
  comment '员工表';
```

##### iii. 修改

- 添加字段：`ALTER TABLE 表名 ADD 字段名 类型(长度)[COMMENT 注释][约束];`
- 修改字段：
  - 修改数据类型：`ALTER TABLE 表名 MODIFY 字段名 新数据类型(长度);`
  - 修改字段名和字段类型：`ALTER TABLE 表名 CHANGE 旧字段名 新字段名 类型(长度) [COMMENT 注释][约束];`
- 删除字段：`ALTER TABLE 表名 DROP 字段名;`
- 修改表名：`ALTER TABLE 表名 RENAME TO 新表名;`

例子：将emp表的nickname字段修改为username，类型为varchar(30)

```sql
alter table emp change nickname username varchar(30) comment 用户名;
```

##### iv. 删除

- 删除表：`DROP TABLE [IF EXISTS] 表名;`
- 删除指定表，并重新创建该表：`TRUNCATE TABLE 表名;`

### 4. DML

#### （1）添加数据

- 给**指定**字段添加数据：`INSERT INTO 表名(字段名1,字段名2,…) VALUES(值1,值2,…);`

```sql
insert into emp(id, workno, name, gender, age, idcard, entrydate) values (1, '1', 'haojie', 'M', 33, "4211211", "2000-01-01")
```

> 为什么可以给指定字段添加数据，而不用全部呢？
>
> 1. 如果表的某些字段定义了默认值，这部分字段值可以不提供
> 2. 如果某些字段可以为 NULL，这部分字段值可以不提供

- 给**全部**字段添加数据：`INSERT INTO 表名 VALUES (值1,值2, ..);`

```sql
insert into emp values (2, '2', 'yuwen', 'F', 32, "4221211", "2001-01-01")
```

- 批量添加数据：
  	- `INSERT INTO 表名(字段名1,字段名2,..) VALUES(值1,值2,..),(值1,值2,.),(值1,值2,.);`
  	- `INSERT INTO 表名 VALUES (值1,值2,…..),(值1,值2,….),(值1,值2,.);`

```sql
insert into emp values (4, '4', 'jiajia', 'F', 53, "4231211", "1972-01-01"), (3, '3', 'luoan', 'F', 1, "110105", "2024-01-01")
```

#### （2）修改数据

- 基本语法：`UPDATE 表名 SET 字段名1=值1,字段名2=值2,…[WHERE 条件];`

注意：where条件可以不要，如果不要代表的是修改整张表的所有数据

```sql
# 修改一个字段
update emp set name="shuhaojie" where id=1
# 修改两个字段
update emp set name="zengyuwen", entrydate="2022-01-01" where id=2
# 修改整张表所有数据
update emp set entrydate="2025-02-01"
```

#### （3）删除数据

- 基本语法：`DELETE FROM 表名[WHERE 条件]`

注意：

- DELETE语句的条件可以有，也可以没有，如果没有条件，则会删除整张表的所有数据
- DELETE 语句不能删除某一个字段的值(可以使用UPDATE)

```sql
delete from emp where id=4
```

### 5. DQL

#### （1）引言

在一个正常的业务系统中，查询数据的操作是远高于添加数据、修改数据、删除数据的。例如在京东官网中，我们可以做如下操作：

<img src="./assets/image-20250707210147234.png" alt="image-20250707210147234" style="zoom:67%;" />

- 在输入框里输入关键字，进行搜索，例如【笔记本】
- 按照品牌进行查询，例如【宏基acer】
- 按照价格进行范围查询，例如【3000-4000】
- 查询出来的数据有很多，可以点击分页条，进行分页展示
- 还可以对查出来的数据，进行排序，例如按照价格进行降序排序

#### （2）语法

查询的基本语法如下：

```sql
SELECT
		字段列表
FROM
		表名列表
WHERE
		条件列表
GROUP BY
		分组字段列表
HAVING
		分组后条件列表
ORDER BY
		排序字段列表
LIMIT
		分页参数
```

#### （3）基本查询

##### i. 基本语法

1. 查询多个字段

- `SELECT 字段1,字段2,字段3... FROM 表名`
- `SELECT * FROM 表名`

2. 设置别名：`SELECT 字段1 [AS 别名1],字段2 [AS 别名2]…FROM 表名;`
3. 去除重复记录：`SELECT DISTINCT 字段列表 FROM 表名;`

##### ii. 数据准备

建表：

```sql
create table emp(
  	id int,
		workno varchar(10),
		name varchar(10),
		gender char,
		age tinyint unsigned ,
		idcard char(18),
		workaddress varchar(50),
		entrydatedate date)
```

插入数据：

```sql
INSERT INTO emp (id, workno, name, gender, age, idcard, workaddress, entrydate) VALUES
(1, 'E0001', '张无忌', '男', 26, '110101199805010011', '明教光明顶', '2020-01-15'),
(2, 'E0002', '赵敏', '女', 24, '110101199905230012', '汝阳王府', '2021-03-10'),
(3, 'E0003', '周芷若', '女', 23, '110101200006180013', '峨眉山', '2022-05-20'),
(4, 'E0004', '谢逊', '男', 50, '110101197301300014', '冰火岛', '2019-08-05'),
(5, 'E0005', '杨逍', '男', 42, '110101198102140015', '明教光明顶', '2018-12-01'),
(6, 'E0006', '小昭', '女', 22, '110101200202180016', '波斯总教', '2021-07-13'),
(7, 'E0007', '殷素素', '女', 38, '110101198603150017', '明教', '2017-11-30'),
(8, 'E0008', '宋青书', '男', 28, '110101199605180018', '武当山', '2020-04-22'),
(9, 'E0009', '灭绝师太', '女', 55, '110101196701100019', '峨眉山', '2015-09-17'),
(10, 'E0010', '纪晓芙', '女', 30, '110101199309050020', '峨眉山', '2020-06-01'),
(11, 'E0011', '杨不悔', '女', 25, '110101199804120021', '光明顶', '2021-08-19'),
(12, 'E0012', '韦一笑', '男', 46, '110101197703260022', '明教光明顶', '2016-10-03'),
(13, 'E0013', '张三丰', '男', 90, '110101193301010023', '武当山', '2010-05-25'),
(14, 'E0014', '殷天正', '男', 70, '110101195309210024', '明教', '2012-12-12'),
(15, 'E0015', '范遥', '男', 48, '110101197501180025', '明教西域分舵', '2018-03-14'),
(16, 'E0016', '紫衫龙王', '女', 40, '110101198309220026', '灵蛇岛', '2017-06-30'),
(17, 'E0017', '金花婆婆', '女', 60, '110101196211110027', '灵蛇岛', '2014-02-07'),
(18, 'E0018', '彭莹玉', '男', 52, '110101197102050028', '明教西域分舵', '2015-10-10'),
(19, 'E0019', '庄铮', '男', 45, '110101197808080029', '明教光明顶', '2019-04-04'),
(20, 'E0020', '黄衫女子', '女', 21, '110101200305160030', '古墓派', '2023-01-01');
```

##### iii. 查询示例

- 查询指定字段 name，workno，age返回

  ```sql
  select name,workno,age from emp;

- 查询所有字段返回

  ```sql
  select * from emp;
  ```

- 查询所有员工的工作地址，起别名

  ```sql
  select workaddress as '工作地址' from emp;
  ```

- 查询公司员工的上班地址（不要重复）

  ```sql
  select distinct workaddress '工作地址' from emp;
  ```

#### （4）条件查询

##### i. 基本语法

`SELECT 字段列表 FROM 表名 WHERE 条件列表;`

##### ii. 查询条件

**（1）比较运算符**

- `>`：大于
- `>=`：大于等于
- `<`：小于
- `<=`：小于等于
- `=`：等于
- `!=`或者`<>`：不等于
- `BETWEEN ... AND...`：某个范围内，包含最大值、最小值
- `IN(...)`：在in之后的列表中的值，多选一
- `LIKE 占位符`：模糊匹配，`_`匹配单个字符，`%`匹配任意个字符
- `IS NULL`：为NULL

**（2）逻辑运算符**

- `AND或&&`：并且
- `OR或||`：或者
- `NOT或！`：不是

##### iii. 查询示例

- 查询年龄等于88的员工

  ```sql
  select * from emp where age=88;
  ```

- 查询年龄小于20的员工信息

  ```sql
  select * from emp where age<20;
  ```

- 查询年龄小于等于 20的员工信息

  ```sql
  select * from emp where age <= 20;
  ```

- 查询没有身份证号的员工信息

  ```sql
  select * from emp where idcard is null;
  ```

- 查询有身份证号的员工信息

  ```sql
  select * from emp where idcard is not null;
  ```

- 查询年龄不等于 88 的员工信息

  ```sql
  select * from emp where age != 88;
  select * from emp where age <> 88;
  ```

- 查询年龄在15岁(包含)到20岁(包含)之间的员工信息

  ```sql
  select * from emp where age >= 15 && age <= 20;
  select * from emp where age >= 15 and age <= 20;
  select * from emp where age betweeh 15 and 20;
  ```

- 查询性别为女且年龄小于 25岁的员工信息

  ```sql
  select * from emp where gender='女'and age < 25;
  ```

- 查询年龄等于18或20或40的员工信息

  ```sql
  select * from emp where age =18 or age = 20 or age =40;
  select * from emp where age in(18,20,40);
  ```

- **查询姓名为两个字的员工信息**

  ```sql
  select * from emp where name like '__';
  ```

- 查询身份证号最后一位是X的员工信息

  ```sql
  select * from emp where idcard like '%X';
  # 因为身份证号是17位，前面16位可以用16个_来表示
  select * from emp where idcard like '________________X'; 
  ```

#### （5）聚合函数

##### i. 基本概念

聚合函数是将**一列数据作为一个整体**，进行纵向计算。

- count：统计数量
- max：最大值
- min：最小值
- avg：平均值
- sum：求和

注意：

（1）聚合函数都是作用于表的某一列。

（2）所有null值不参与聚合函数的计算 

##### ii. 基本语法

`SELECT 聚合函数(字段列表) FROM 表名;`

##### iii. 查询示例

- 统计该企业员工数量

  ```sql
  select count(*) from emp;
  # 注意，如果身份证号有为空的，此时统计的总数要去掉身份证号为空的
  select count(idcard) from emp;
  ```

- 统计该企业员工的平均年龄

  ```sql
  select avg(age) from emp;
  ```

- 统计该企业员工的最大年龄

  ```sql
  select max(age) from emp;
  ```

- 统计该企业员工的最小年龄

  ```sql
  select min(age) from emp;
  ```

- 统计西安地区员工的年龄之和

  ```sql
  select sum(age) from emp where workaddress='西安';
  ```

#### （6）分组查询

##### i. 基本语法

```sql
SELECT 字段列表 FROM 表名 [WHERE 条件] GROUP BY 分组字段名 [HAVING 分组后过滤条件];
```

`where`与`having`区别：

- 执行时机不同：where是分组之前进行过滤，不满足where条件，不参与分组;而having是分组之后对结果进行过滤。
- 判断条件不同：where不能对聚合函数进行判断，而having可以。

注意：

（1）分组通常伴随着聚合来一起操作

（2）执行顺序：where > 聚合函数 > having

（3）分组之后，查询的字段一般为聚合函数和分组字段，查询其他字段无任何意义。

##### ii. 查询示例

- 根据性别分组，统计男性员工和女性员工的数量

  ```sql
  select gender, count(*) from emp group by gender;
  ```

- 根据性别分组，统计男性员工和女性员工的平均年龄

  ```sql
  select gender, avg(age) from emp group by gender; 
  ```

- **查询年龄小于45的员工，并根据工作地址分组，获取员工数量大于等于3的工作地址**

  ```sql
  select workaddress, count(*) as address_count from emp where age < 45 group by workaddress having address_count >= 3;
  ```

#### （7）排序查询

##### i. 基本语法

```sql
SELECT 字段列表 FROM 表名 ORDER BY 字段1 排序方式1,字段2 排序方式2;
```

##### ii. 查询示例

- 根据年龄对公司的员工进行升序排序

  ```sql
  select * from emp order by age asc;
  ```

- 根据年龄对公司的员工进行升序排序，年龄相同，再按照入职时间进行降序排序

  ```sql
  select * from emp order by age asc, entrydate desc;
  ```

#### （8）分页查询

##### i. 基本概述

在进行分页的时候，我们需要用到分页查询，例如下图所示

![image-20250709224050325](./assets/image-20250709224050325.png)

##### ii. 基本语法

```sql
SELECT 字段列表 FROM 表名 LIMIT, 起始索引, 查询记录数;
```

注意：

（1）起始索引从0开始，起始索引=(查询页码-1)*每页显示记录数

（2）分页查询是数据库的方言，不同的数据库有不同的实现，MySQL中是LIMIT

（3）如果查询的是第一页数据，起始索引可以省略，直接简写为limit 10

##### iii. 查询示例

- 查询第1页员工数据，每页展示10条记录

  ```sql
  select * from emp limit 0,10;
  ```

- 查询第2页员工数据，每页展示10条记录

  ```sql
  # 注意上面说的公式：起始索引=(查询页码-1)*每页显示记录数，(2-1)*10;
  select * from emp limit 10,10;
  ```

#### （9）DQL执行顺序

##### i. 执行顺序

在前面介绍过DQL语句的编写顺序，但是它和DQL语句的编写顺序并不相同

<img src="./assets/image-20250709225022793.png" alt="image-20250709225022793" style="zoom: 50%;" />

##### ii. 验证

1. 先做一个基础的查询：查询年龄大于15的员工的姓名、年龄，并根据年龄进行升序排序：

```sql
select name, age from emp where age > 15 order by age asc;
```

2. 上面说了执行顺序是从`from 表名列表开始`，那么我们可以对表名取个别名：

```sql
select name, age from emp as e where age > 15 order by age asc;
```

此时，执行这句话正常不报错

3. 接着执行的是`where 条件列表`，我们可以使用上面的别名

```sql
select name, age from emp as e where e.age > 15 order by age asc;
```

此时，执行这句话正常不报错

4. 接着执行的是`GROUP BY`和`HAVING`, 这里没有就不讨论

5. 再就是SELECT，这里可以使用前面的别名

```sql
select e.name, e.age from emp as e where e.age > 15 order by age asc;
```

此时，执行这句话正常不报错

6. 这里我们还可以验证一下`SELECT`和`WHERE`的顺序，方法是给`SELECT`起别名

```sql
select e.name as ename, e.age as eage from emp as e where eage > 15 order by age asc;
```

此时，**执行这句话报错**，因为where的执行顺序高于select

7. 但是，我们在order by里使用select里的别名，就不报错

```sql
select e.name as ename, e.age as eage from emp as e where e.age > 15 order by eage asc;
```

这就说明，select的执行顺序先于order by

### 6. DCL

## 三、函数

## 四、约束

## 五、多表查询

## 六、事务

### 1. 什么是事务

#### （1）概念

事务是数据库系统中保证一组相关操作具有原子性（不可分割）、一致性、隔离性和持久性（ACID）特性的**逻辑工作单元**。它通过明确的开始（BEGIN）、结束（COMMIT 或 ROLLBACK）边界，确保这些操作要么全部成功永久生效，要么全部失败完全回滚。

- 表现形式：**逻辑工作单元**，它把多个操作（SQL语句）捆绑在一起。

- 目的：保证ACID 特性，这是事务存在的根本原因。
- 核心目的：在ACID中，最核心的目的，是原子性，“全部成功”或“全部失败”是其最核心的承诺。
- 关键操作：明确的边界控制，`BEGIN` 标记开始，`COMMIT` 确认永久生效（成功结束），`ROLLBACK` 撤销所有更改（失败结束）。

#### （2）类比
类比理解：想象在填写一份复杂的申请表（事务）：

1. **开始填表（`START TRANSACTION`）**： 你拿出一张新表开始填写。
2. **填写多个字段（执行SQL操作）**： 你填写姓名、地址、电话等信息（INSERT/UPDATE/DELETE）。此时，表还没交上去，你可以随意修改或划掉重写。
3. **检查并提交（`COMMIT`）**： 你仔细检查所有信息都正确无误后，**正式递交（提交）** 给柜台。柜台收下你的表，存档（持久化），这份表就正式生效了。其他人（其他事务）现在才能看到或查询到这份表的内容（受隔离级别限制）。
4. **发现错误并作废（`ROLLBACK`）**： 如果你在提交前发现填错了，你可以直接把这张表**撕掉（回滚）** ，重新拿一张新表填写（数据库恢复到填表前的状态）。柜台永远不知道你填错过。

例如下面的事务，由于id是pk，因此会rollback

```sql
begin;
insert into user(id, username, password, email) values (1, "haojie", "123456", "haojie@qq.com");
insert into user(id, username, password, email) values (1, "yuwen", "123456", "yuwen@qq.com");
commit;
```

### 2. 事务的开启

#### （1）单sql语句

在MySQL中，事务是默认开启的`autocommit=ON`, **当执行一条DML语句，MySQL会隐式的提交事务，也就是说每一条DML语句都是在一个事务之内的**。

#### （2）多sql语句

**当我们想把多条SQL语句包裹在一个事务中时**，可以使用如下的方式

```sql
begin; # 或者start transaction;
# DML语句
commit; # 或者rollback
```

#### （3）pymysql

对pymysql会有个误区，认为`with con.cursor() as cursor`这个语句就是开启事务，其实并不对。

- PyMySQL中，事务时默认关闭的：`autocommit=False`
- **当执行第一条修改数据的 SQL 语句（如 `INSERT/UPDATE/DELETE`）时，事务会隐式开启**

```python
import pymysql

con = pymysql.connect(host="localhost", user="root", passwd="805115148",
                      db="mysql_basic", port=int(3306), charset='utf8')

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
```

这里注意对比：

（1）游标（cursor）只是执行 SQL 的工具，事务是连接（connection）级别的操作

（2）pymysql也可以设置事务自动提交：

```python
# 如果设置 autocommit=True，每条 SQL 会立即提交（不推荐用于事务）
con = pymysql.connect(..., autocommit=True)
```

（3）事务边界：一个连接可以包含多个事务；每次 `commit()` 或 `rollback()` 后会结束当前事务，下次执行修改语句时开启新事务。

#### （4）sqlalchemy

同pymysql，`with Session() as session`这个语句不会开启事务，当执行第一个数据库操作（查询/修改）时，SQLAlchemy 会**自动开启一个新事务**。

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://user:pass@localhost/db")
Session = sessionmaker(bind=engine)

# 推荐的事务处理方式
with Session() as session:  # 创建会话
    try:
        # 执行数据库操作（此时隐式开启事务）
        user = session.query(User).filter_by(id=1).first()
        user.name = "Updated Name"
        
        # 显式提交事务
        session.commit()  # ⭐⭐⭐ 关键步骤 ⭐⭐⭐
    
    except Exception as e:
        # 出错时回滚
        session.rollback()  # ⭐⭐⭐ 关键步骤 ⭐⭐⭐
        print(f"事务失败: {e}")
        raise
```

### 3.  事务的特性

事务的四大特性，分别是ACID，原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）和持久性（Durability）。

#### （1）原子性

**原子性可以说是事务最重要的特性**，无论一个事务里有多少执行步骤，这所有的步骤合起来是一个最小的执行单元，要么不做，要么全做，不存在只做到一半情况。

以转账为例，现实世界的转账是一个不可分割的操作：要么压根儿就没转，要么转账成功，不存在中间状态，也就是转了一半的这种情况，这种规则称之为`原子性`。

数据库中的一条操作可能被分解成若干个步骤，比**如先修改缓存页，之后再刷新到磁盘等**，而且任何一个可能的时间都可能发生意想不到的错误，可能是数据库本身的错误，或者是操作系统错误，甚至是直接断电之类的，而使操作执行不下去。为了保证在数据库世界中某些操作的原子性，需要保证如果在执行操作的过程中发生了错误，把已经做了的操作恢复成没执行之前的样子。

#### （2）一致性

事务执行前与执行后数据内在的逻辑始终是成立的，比如转账前与转账后两人存款的总和始终不变。

另外知乎这个回答提供了另外一个观点：提到事务，就会说ACID，但是**事务的AID是手段，C是目的**。就像提到保镖，会说强壮、功夫好、踏实、安全，这里强壮、功夫好、踏实都是手段，安全是目的。

> 参考，如何理解数据库事务中的一致性的概念？ - 莺歌一笑的回答 - 知乎https://www.zhihu.com/question/31346392/answer/362597203

#### （3）隔离性

它指的是**多个事务并发执行时，每个事务的操作和数据与其他事务相互隔离，互不干扰**，如同只有该事务自己在操作数据库一样。

#### （4）持久性

事务做完了就是做完了，就生效了。就像钱转给别人后当前这比转账交易就结束了，不可能再倒回来。

### 4. 并发事务问题

数据准备

```sql
insert into user(id, username, email, password) values (1, "haojie", "haojie@qq.com", "123456");
```

#### （1）脏读

脏读（Dirty Read）指的是，事务A读取了**事务B未提交**的修改数据，若事务B随后回滚，事务A读到的就是无效的“脏数据”。

事务A：

```sql
# 步骤1: 事务A, 设置隔离级别为读未提交
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
# 步骤3: 事务A, 开启事务
begin;
# 步骤4: 事务A, 修改数据但是不提交
UPDATE user SET password = "654321" WHERE id = 1;
# 步骤6: 事务A, 回滚
rollback;
```

事务B：

```sql
# 步骤2: 事务B, 设置隔离级别为读未提交
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
# 步骤5: 事务B, 读取未提交的数据: 654321
SELECT * FROM user WHERE id = 1;
# 步骤7: 事务B, 再读取回滚后的数据: 123456
SELECT * FROM user WHERE id = 1;
```

**隔离级别要求**：`READ COMMITTED` 及以上可避免。

#### （2）不可重复读

不可重复读（Non-Repeatable Read）指的是，事务A内**多次读取同一数据**，因事务B的**修改并提交**，导致前后结果不一致。

事务A：

```sql
# 步骤1: 事务A, 设置隔离级别为读已提交
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
# 步骤3: 事务A, 开启事务
begin;
# 步骤4: 事务A, 读取数据: 123456
select password from user where id=1;
# 步骤8: 事务A, 第二次读取: 654321
select password from user where id=1;
```

事务B：

```sql
# 步骤2: 事务B, 设置隔离级别为读已提交
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
# 步骤5: 事务B, 开启事务
begin;
# 步骤6: 事务B, 修改数据
UPDATE user SET password="654321" WHERE id = 1;
# 步骤7: 事务B, 提交数据
COMMIT;
```

**隔离级别要求**：`REPEATABLE READ` 及以上可避免。

#### （3）幻读

事务A**多次执行相同范围查询**，因事务B**插入或删除**符合条件的数据并提交，导致返回的行数变化（出现“幻影行”）。

事务A：

```sql
# 步骤1: 事务A, 设置隔离级别为可重复读
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
# 步骤3: 事务A, 开启事务
begin;
# 步骤4: 事务A, 读取数据: 空
select * from user where id>1;
# 步骤8: 事务A, 第二次读取: 有一条数据
select * from user where id>1;
```

事务B：

```sql
# 步骤2: 事务B, 设置隔离级别为可重复读
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
# 步骤5: 事务B, 开启事务
begin;
# 步骤6: 事务B, 新增数据
insert into user(id, username, email, password) values (2, "yuwen", "yuwen@qq.com", "123456");
# 步骤7: 事务B, 提交数据
COMMIT;
```

**隔离级别要求**：`SERIALIZABLE` 可严格避免（MySQL的`REPEATABLE READ`通过间隙锁也可避免）。

#### （4）问题

> 1、为什么脏读比不可重复读更严重？

答：因为脏读读的是**未提交的中间状态数据**，不可重复读读取的是**已提交的真实数据**。

脏读：事务B将余额从50改为100（未提交），事务A读到100并允许用户提款60，随后事务B回滚余额恢复为50，造成资金损失。

不可重复读：虽然事务内一致性被破坏，但数据本身是有效的（如余额从50变为100是业务认可的）

### 5. 事务隔离级别

为什么需要隔离？

- 数据库需要同时处理多个用户/应用的请求（多个事务）。
- 如果不对并发事务进行任何控制，它们可能会同时读写相同的数据项，导致最终结果混乱、不可预测，破坏数据的一致性。

隔离的本质：

- 隔离性是一种**保证机制**。它通过数据库系统内部的并发控制协议（主要是锁机制或多版本并发控制）来实现。
- 它确保了**一个正在执行的事务在其提交之前，它对数据的中间修改对其他并发事务是不可见的**。
- 它让用户感觉不到其他并发事务的存在，仿佛数据库在某个时刻只执行这一个事务。

MySQL的默认隔离级别是可重复读

#### （1）读未提交

- **定义：**读未提交（READ UNCOMMITTED）指的是事务可以读取其他**尚未提交**的事务所做的修改。

- **允许的问题：**
  - **脏读：**❌ 肯定发生。事务A读取了事务B未提交的修改，如果事务B回滚，事务A读到的就是无效数据。
  - **不可重复读：** ❌ 可能发生。
  - **幻读：** ❌ 可能发生。
  - **丢失更新：** ❌ 可能发生。
- **使用场景：** 极少使用。可能出现在对数据一致性要求极低、只追求最高吞吐量的特殊场景（如某些统计、监控），且能容忍数据短暂不一致或无效

#### （2）读已提交

- **定义：** 读已提交（READ COMMITTED）指的是事务只能读取其他**已经提交的事务**所做的修改。这是**Oracle 等数据库的默认级别**。
- **防止的问题：**
  - **脏读：** ✅ 防止。只能读到已提交的数据。
- **允许的问题：**
  - **不可重复读：** ❌ 可能发生。事务A第一次读取某行后，事务B修改该行并提交，事务A再次读取该行会得到新值。
  - **幻读：** ❌ 可能发生。事务A第一次执行范围查询后，事务B插入或删除符合该范围的行并提交，事务A再次执行相同查询会得到不同的行集。
- **使用场景：** 适用于大多数不需要严格保证同一事务内多次读取结果一致的OLTP场景。能有效防止脏读，并发性能较好。是许多应用的合理选择。

#### （3）可重复读

- **定义：** 可重复读（REPEATABLE READ），是 **MySQL InnoDB 存储引擎的默认隔离级别**。确保在同一个事务内，多次读取**同一范围**的数据会返回**相同**的结果（第一次读取建立快照）。
- **防止的问题：**
  - **脏读：** ✅ 防止。
  - **不可重复读：** ✅ 防止。同一事务内多次读取同一行，结果总是相同。
  - **丢失更新：** ✅ InnoDB 通过行锁和 next-key lock 通常可以防止。
- **允许的问题 (SQL 标准)：**
  - **幻读：** ❌ SQL 标准允许发生。
- **使用场景：** MySQL 的默认级别，提供了很好的数据一致性保证（防止脏读、不可重复读和幻读），同时通过 MVCC 保持了较好的读并发性能。适用于需要保证事务内数据视图一致的场景（如对账、复杂报表生成、需要基于稳定视图进行多次操作）。

#### （4）串行化

- **定义：** 最严格的隔离级别。它强制所有事务**串行执行**，如同事务是按顺序一个接一个执行一样。
- **防止的问题：**
  - **脏读：** ✅ 防止。
  - **不可重复读：** ✅ 防止。
  - **幻读：** ✅ 防止。
  - **丢失更新：** ✅ 防止。
- 锁冲突的概率大大增加，可能导致大量事务等待，**性能最低**。
- **使用场景：** 对数据一致性要求**极其严格**，可以接受显著性能下降的场景。例如，某些金融核心交易、票务系统最后的库存扣减等。一般只在非常必要的情况下使用。

## 七、索引

> 参考https://www.bilibili.com/video/BV1Kr4y1i7ru?spm_id_from=333.788.videopod.episodes&vd_source=e204e7b48214ba273c6eb797fd8b7a51&p=68

### 1. 索引介绍

#### （1）本质

索引(index)是帮助MySQL高效获取数据的数据结构，在数据之外，**数据库系统还维护着满足特定查找算法的数据结构**，这些数据结构以某种方式引用(指向)数据，这样就可以在这些数据结构上实现高级查找算法，这种数据结构就是索引。

#### （2）作用

假如没有索引，我们要去查一个数据，实际上是非常慢的，例如下面去找年龄为45的，需要从上往下一直找，找到了之后还不能停，因为可能有多个年龄为45的。 这种方式称之为全表扫描，它的性能非常低。

<img src="./assets/image-20250610092213542.png" alt="image-20250610092213542" style="zoom: 67%;" />

如果我们此时用一个索引，例如二叉树。第一个数据36作为根节点，比它大设为右节点，比它小设为左节点，每个数据依次往下排，那么同样是这些数据，我们可以建立这样一个二叉树。

<img src="./assets/image-20250610092319258.png" alt="image-20250610092319258" style="zoom:67%;" />

此时再去找年龄为45的，显然快得多，只需要36 -> 48 -> 45这个步骤，匹配三次即可找到。

### 2. B+树结构

Mysql默认的引擎是InnoDB，它使用的索引是B+树

#### （1）二叉树

上面说的二叉树会有一个缺点，如果我们的数据是顺序插入，例如36 -> 34 -> 33 -> 23 -> 22 -> 20 -> 19 -> 17。**此时它相当于形成了一个链表**，见下面右图所示， 此时如果我们去查17这个数，检索效率是较慢的。

<img src="./assets/image-20250610092757225.png" alt="image-20250610092757225" style="zoom:60%;" />

#### （2）B树

- 度数：一个节点的子节点个数。例如下图中第一行的度数就是5，因为有5个子节点。
- key：节点中存储的**有序键值**。例如下图中第一行的指针就是4，因为有4个键值。
- 指针：指向**子节点**的指针。例如下图中第一行的key就是5，因为指向了5个子节点。

![image-20250610193641945](./assets/image-20250610193641945.png)

B树是如何分裂的呢？以一颗最大度数为5的b-tree为例，现在我们有0023，0234，0345，0899，

- 最开始我们有4个数0023，0234，0345，0899，此时由于key值数足够，不会发生裂变，数据有序存储

![image-20250610204446735](./assets/image-20250610204446735.png)

- 如果此时新增一个数1200，此时由于key值不够，会发生裂变，如何裂变呢？中间元素向上裂变

![image-20250610204620292](./assets/image-20250610204620292.png)

- 此时如果再插入一个1234，由于比0345大，会走右侧，放到1200的右边

![image-20250610204728391](./assets/image-20250610204728391.png)

- 插入1500

  ![image-20250610205204412](./assets/image-20250610205204412.png)

- 然后再插入1000，该如何分裂呢？还是一样，中间元素向上分裂，1200向上分裂到第一行，然后把另外4个数给分开，和前面一样

![image-20250610205100195](./assets/image-20250610205100195.png)

- 继续往里面插一些数，变成这样

![image-20250610205906162](./assets/image-20250610205906162.png)

- 然后我们再插入一个2456，此时树就变成了3层

![image-20250610205951469](./assets/image-20250610205951469.png)

#### （3）B+树

B+树和B树有两个不一样：

- 所有元素都会出现在叶子节点（见下图最后一行，包含了所有的数据）
- 叶子节点形成了一个单向链表

![image-20250610210241163](./assets/image-20250610210241163.png)

- 假设我们有四个数，0232，0234，0567，1000，当我们再次插入一个数890，此时B+树会变成如下形式，它和前面不一样，0567向上裂变的同时**还出现在了叶子节点**，这是因为前面说的第一个特性，B+树的所有元素都会出现在叶子节点

![image-20250610210917470](./assets/image-20250610210917470.png)

- 再插入1234

![image-20250610211121751](./assets/image-20250610211121751.png)

- 此时如果再插入2345，1000向上裂变的同时，还会出现在叶子节点

![image-20250610211158885](./assets/image-20250610211158885.png)

#### （4）MySQL B+树

MySQL在B+树的基础上做了改良：非叶子节点只是起到索引数据的作用，并不存储具体的数据，具体数据存在叶子节点

![image-20250610212423223](./assets/image-20250610212423223.png)

### 3. 索引分类

#### （1）按类型

- 主键索引：针对于表中的主键创建的索引，它是自动创建的
- 唯一索引：避免同一个表中某数据列中的值重复，当我们加唯一约束的时候，会自动创建唯一索引
- 常规索引：快速定位特定数据

#### （2）按存储形式

- 聚集索引：将数据存储与索引放到了一起，索引结构的叶子节点保存了行数据，聚集索引只会有一个。
- 二级索引：将数据与索引分开存储，索引结构的叶子节点关联的是对应的主键，二级索引可以存在多个。

聚集索引选取规则：

- 如果存在主键，主键索引就是聚集索引
- 如果不存在主键，将使用第一个唯一索引作为聚集索引
- 如果不存在主键，并且没有合适的唯一索引，InnoDB会自动生成一个rowid作为隐藏的聚集索引

**也就是说，MySQL一定会有聚集索引**

### 4. 索引的使用

#### （1）挂数据

- 聚集索引：叶子节点挂的是具体的数据
- 二级索引：叶子节点挂的是对应的主键值

![image-20250610214357686](./assets/image-20250610214357686.png)

#### （2）回表查询

当我们要执行一个查询，`select * from user where name='Arm';`

- 首先走二级索引，去查`Arm`对应的`id=10`
- 再去走聚集索引，去查`id=10`对应的数据块

![image-20250610215442292](./assets/image-20250610215442292.png)

这个过程就是回表查询：先根据二级索引查主键值，再根据主键值拿到这一行的行数据

### 5. 索引使用规则

#### （1）最左前缀法则

最左前缀法则针对的是联合索引，指的是查询从索引的最左列开始，并且不跳过索引中的列，**如果跳过某一列，索引将部分式效**。

例如我们有一个联合索引profession，age，status，如下图所示

![image-20250612204739477](./assets/image-20250612204739477.png)

- 第一个sql语句：`select * from tb_user where profession="软件工程" and age=3l and status ='0';`，查看执行计划，可以看到用到了索引，索引长度54

![image-20250612205014612](./assets/image-20250612205014612.png)

- 第二个sql语句：`select * from tb_user where profession="软件工程" and age=3l;`，查看执行计划，可以看到也用到了索引，索引长度49

![image-20250612205124897](./assets/image-20250612205124897.png)

- 第三个sql语句：`select * from tb_user where profession="软件工程";`，查看执行计划，可以看到仍然用到了索引，索引长度47

![image-20250612205241472](./assets/image-20250612205241472.png)

- 第四个sql语句：`select * from tb_user where age=3l and status ='0';`，查看执行计划，可以看到没用到索引，type字段为ALL，表示全表扫描。这是因为它不满足最左前缀法则，最左边的列professio没有出现。

![image-20250612205732764](./assets/image-20250612205732764.png)

- 第五个sql语句：`select * from tb_user where profession="软件工程" and status ='0';`，查看执行计划，可以看到用到了索引。按照前面的计算，profession索引的长度是47，age索引的长度是5，status索引的长度是2，但是下面执行计划里，索引的长度却是47，说明**索引部分失效**，这是因为我们跳过了age索引

![image-20250612210255681](./assets/image-20250612210255681.png)

#### （2） 范围查询

也是针对的联合索引，出现范围查询(`<`,`>`)，范围查询右侧的列索引失效

例如：`select * from tb_user where profession="软件工程" and age>30 and status ='0';`，查看执行计划，虽然用到了索引，但是索引的长度是49，说明没有用到status索引

![image-20250612211057713](./assets/image-20250612211057713.png)

在业务允许的范围内，尽量使用`>=`

![image-20250612211037427](./assets/image-20250612211037427.png)

#### （3）索引失效情况

- 不要在索引列上进行运算操作，否则索引将失效。例如对比下面两个sql

![image-20250612211501934](./assets/image-20250612211501934.png)

- 字符串类型不加单引号，也会不走索引。例如下面的sql，虽然不加引号也可以查出，但是全表扫描了。

![image-20250612211748568](./assets/image-20250612211748568.png)

- 如果仅仅是尾部模糊匹配，索引不会失效；如果是头部模糊匹配，索引失效。例如对比下面两个sql，后面一个没有用到索引。

![image-20250612212218750](./assets/image-20250612212218750.png)

- 用or分割开的条件，如果or前的条件中的列有索引，而后面的列中没有索引，那么涉及的索引都不会被用到。例如下面的sql，由于age没有单独的索引，因此索引失效。

![image-20250612212655938](./assets/image-20250612212655938.png)

#### （4）sql提示

SQL提示，就是在SQL语句中加入一些人为的提示来达到优化操作的目的，是优化数据库的一个重要手段。

- 如果profession既是联合索引，又是单列索引，可以加上`use index(idx_user_pro)`来使用单列索引：`explain select * from tb_user use index(idx_user_pro) where profession='软件工程”`
- 忽略索引：`explain select * from tb user ignore index(idx_user_pro) where profession ='软件工程'`

### 6. 其他索引

#### （1）覆盖索引！

> 注意：覆盖索引并不是一个索引类型

覆盖索引指的是查询使用了索引，并且查询需要返回的列，在该索引中已经全部能够找到。在做查询时尽量使用覆盖索引，避免`select *`，因为很可能会出现回表查询的情况。

例如下面的两个sql语句：

- `explain select id,profession,age,status from tb user where profession="软件工程" and age=31 and status ='0';`，**这个语句由于要查询的列，都在索引中能全部找到，因此不需要回表查聚集索引，直接在二级索引中就能全部找到**。注意看后面的extra，`using where; using index`，说明需要的数据都在索引列中能找到，所以不需要回表查询数据。

![image-20250613092318580](./assets/image-20250613092318580.png)

- `explain select id,profession,age,status,name from tb user where profession="软件工程" and age=31 and status ='0';`，这个语句由于要查询的name，在二级索引中找不到，因此需要回表查询。后面的extra，`using index condition`，表示查找使用了索引，但是需要回表查询数据，性能就没有前面高。

![image-20250613092350140](./assets/image-20250613092350140.png)

#### （2）前缀索引

当字段类型为字符串(`varchar`，`text`等)、时，有时候需要索引很长的字符串，这会让索引变得很大，查询时浪费大量的磁盘I0，影响查询效率。此时可以只将字符串的一部分前缀建立索引，这样可以大大节约索引空间，从而提高索引效率，这个索引称之为前缀索引。

- 创建语法：`create index idx_xxx_xxx on table_name(column(n));`

- 前缀长度：可以根据索引的选择性来决定，选择性是指不重复的索引值(基数)和数据表的记录总数的比值，索引选择性越高则查询效率越高。例如唯一索引的选择性是1，这是最好的索引选择性，性能也是最好的。可以用下面的sql语句来计算选择性。
  ```sql
  select count(distinct substring(email,1,5))/ count(*) from tb user;
  ```

  这里可以不断向下调整这个子字符串长度的值，例如在这里，前6个字符串和前5个字符串，选择性是一样的，那肯定要用前5个，索引越短越好。

  <img src="./assets/image-20250613095527948.png" alt="image-20250613095527948" style="zoom:67%;" />

#### （3）联合索引

单列索引：即一个索引只包含单个列；联合索引：即一个索引包含了多个列。在业务场景中，如果存在多个查询条件，考虑针对于查询字段建立索引时，建议建立联合索引，而非单列索引，因为联合索引很多时候可以覆盖索引，避免回表查询。

- 创建语法：`create index idx_user_phone_name on tb_user(phone, nane);`
- 索引结构：联合索引的本质，也是一个二级索引。例如上面的例子，构建出来的索引如下图所示，每个节点所存储的键值都是phone和name的组合情况，排序时先按照phone的顺序排，phone一致的情况下，按照name的顺序排。

![image-20250613100701412](./assets/image-20250613100701412.png)

### 7. 建索引原则

- 针对于数据量较大，且查询比较频繁的表建立索引。一般来说，一张表如果有百万级数据，要考虑建索引，如果只有几千条几万条，不建索引查询效率也比较高。
- 针对于常作为查询条件(where)、排序(order by)、分组(group by)操作的字段建立索引。
- 尽量选择区分度高的列作为索引，例如手机号、身份证号等，区分度越高，使用索引的效率越高。对于一些字段，区分度较低，建了索引效率也不高，例如性别、状态。

> 后面这两点，需要再细致了解一下

- 尽量使用联合索引，减少单列索引，查询时，联合索引很多时候可以覆盖索引，节省存储空间，避免回表，提高查询效率。例如 `WHERE col1 = 'A' AND col2 = 'B'`这个查询，如果只有 `col1` 和 `col2` 的单列索引，数据库优化器通常只能选择其中一个它认为过滤性更好的索引（比如 `col1`）。它会先通过 `col1` 的索引找到所有 `col1='A'` 的行，然后**回表**（回到主表数据页）去逐行检查这些行是否满足 `col2='B'`。如果 `col1='A'` 的行很多，这个过程会产生大量的随机 I/O。
- 如果是字符串类型的字段，例如一篇文章的内容，字段的长度较长，可以针对于字段的特点，建立前缀索引。

## 八、SQL查询优化

### 1. explain执行计划

#### （1）作用

- **理解查询执行过程：** 查看查询的执行步骤、表的访问顺序和连接方式。

- **识别性能瓶颈：**

  - **是否使用了索引？** 哪些索引被使用？是否使用了最优索引？

  - **全表扫描 (Full Table Scan) 了吗？** 这是主要的性能杀手之一。

  - **表是如何连接的？** 是高效的连接还是低效的笛卡尔积？

  - **需要排序吗？** 是在内存排序还是使用了磁盘临时文件？

  - **需要临时表吗？** 是在内存创建的还是磁盘？

- **指导优化：**

  - 根据 `EXPLAIN` 结果决定是否需要添加、修改或删除索引。

  - 帮助重构查询语句（例如重写 JOIN、子查询，改变 WHERE 条件顺序）。

  - 判断是否需要调整数据库配置（如缓冲区大小）。

  - 验证优化措施是否生效。

#### （2）字段含义

在select语句前加上explain即可，`explain select * from user where id=1;`，执行结果如下：

![image-20250610221924206](./assets/image-20250610221924206.png)

- **`id`**：查询中 `SELECT` 子句或操作步骤的唯一标识符。
  - `id` 相同：表示这些行属于同一个 `SELECT` 级别（通常是同一个JOIN操作中的表），执行顺序由上至下。
  - `id` 不同：如果是子查询，`id` 序号会递增。`id` 值越大，优先级越高，越先执行。

- **`select_type`**： `SELECT` 查询的类型。
- **`table`**：当前行正在访问哪个表。可以是实际的表名，也可以是别名。
- **`partitions`**： 查询将匹配记录的分区。对于非分区表，此列为 `NULL`。
- **`type` (重要!)**：表访问/连接类型，**判断查询效率的关键指标之一！** 性能从最优到最差大致如下：
  - `system`: 表只有一行记录（等于系统表）。这是 `const` 类型的特例。
  - `const`: 通过主键或唯一索引进行等值查询，最多只返回一行记录。非常高效。
  - `eq_ref`: 在连接查询 (`JOIN`) 中，使用主键或唯一非空索引进行等值匹配。对于前表的每一行，后表只返回一行。非常高效。
  - `ref`: 使用非唯一索引进行等值查询 (`=` 或 `<=>`)，或者唯一索引的非唯一前缀匹配，可能返回多行。
  - `range`: **范围扫描。** 使用索引检索给定范围（`BETWEEN`, `>`, `<`, `IN`, `LIKE 'prefix%'` 等）的行。比全索引扫描好。
  - `index`: **全索引扫描。** 扫描整个索引树（通常是覆盖索引）。虽然避免了全表扫描，但扫描整个索引通常也比 `range` 慢。
  - `ALL`: **全表扫描。** 性能最差，表示需要扫描整张表来找到匹配的行。**这是需要重点优化的信号！**
- **`possible_keys`**：列出理论上可用于该查询的所有索引。注意：这里列出的索引不一定实际被使用。
- **`key`**：实际被优化器选择使用的索引。
- **`key_len`**：实际使用的索引的长度，对于复合索引，可以通过这个值判断使用了索引中的哪些部分。
- **`rows` **：MySQL 预估为了找到所需的行，需要扫描多少行记录， 值越小通常越好。
- **`filtered`**：返回的数据在过滤后，剩余多少百分比的数据满足查询条件，值越接近 100%越好，表示过滤条件有效。
- **`Extra` (重要!)**：包含MySQL解决查询的**额外信息**，这里常常包含重要的性能提示。
  - `Using index`: 覆盖索引， 查询所需的所有列都包含在使用的索引中，因此**无需回表**读取数据行。性能很好！
  - `Using where`: 表示存储引擎返回行之后，MySQL 服务器层还需要应用额外的 `WHERE` 条件进行过滤。如果 `type` 是 `ALL` 或 `index` 且出现这个，说明索引没完全发挥作用。

### 2. 插入数据

#### （1）insert优化

插入多条数据，可以从三个方面优化

- 批量插入：`insert into tb_test values(1,'Tom'),(2,'cat'),(3, 'jerry');`

- 手动提交事务：

  ```sql
  start transaction;
  insert into tb_test values(1,'Tom'),(2,'cat'),(3, 'Jerry');
  insert into tb_test values(4,'Tom'),(5,'Cat'),(6, 'Jerry');
  insert into tb_test values(7,'Tom'),(8,'cat'),(9, 'Jerry');
  commit;
  ```

- 主键顺序插入：

  ```bash
  主键乱序插入: 3 1 2 
  主键顺序插入: 1 2 3
  ```

#### （2）load指令

如果一次性需要插入大批量数据（例如百万级），使用insert语句插入性能较低，此时可以使用MySOL数据库提供的load指令进行插入。例如下面的数据：

![image-20250615094158225](./assets/image-20250615094158225.png)

具体操作如下：

```sql
#客户端连接服务端时，加上参数--local-infile
mysql --local-infile -u root -p
#设置全局参数local infile为1，开启从本地加载文件导入数据的开关
set global local_infile=1;
#执行load指令将准备好的数据，加载到表结构中
load data local infile '/root/sgl1.log' into table 'tb_user` fields terminated by ',’ lines terminated by '\n';
```

### 3. 主键优化

#### （1）数据组织方式

在InnoDB存储引擎中，表数据都是根据主键顺序组织存放的，这种存储方式的表称为【索引组织表】

<img src="./assets/image-20250615094716937.png" alt="image-20250615094716937" style="zoom:57%;" />

下图是MySQL的逻辑存储结构：Segment-> Extent -> Page-> Row。页(Page)是MySQL的InnoDB最小管理单元。

<img src="./assets/image-20250615095016815.png" alt="image-20250615095016815" style="zoom:57%;" />

#### （2）页分裂

上面提到的页Page，在InnoDB中页可以为空，也可以填充一半，也可以填充100%。每个页包含了2-N行数据(如果一行数据过大，会行溢出)，根据主键排列。

- 主键顺序插入

![image-20250615095351809](./assets/image-20250615095351809.png)

- 主键乱序插入：当主键顺序如下所示，此时如果再插入一个主键为50的数据，该怎么插入呢？

<img src="./assets/image-20250615095926068.png" alt="image-20250615095926068" style="zoom:50%;" />

首先它应该插入到第一页，但是由于第一页又放不下，因此MySQL的做法是，把第一页做一个分裂，后50%的数据（例如这里主键23和47的数据）会被分裂到新开的一页，然后再把主键为50的数据插进去，注意此时第一页的下一页不再是第二页，而是第三页。

![image-20250615100127208](./assets/image-20250615100127208.png)

#### （3）页合并

当删除一行记录时，实际上记录**并没有被物理删除**，只是记录被标记(flaged)为删除，并且它的空间变得允许被其他记录声明使用。当页中删除的记录达到阈值后(默认为页的50%)，InnoDB会开始寻找最靠近的页(前或后)看看是否可以将两个页合并以优化空间使用。

原始数据，13，14，15，16都已经被删除

![image-20250615100453423](./assets/image-20250615100453423.png)

合并后

![image-20250615100540609](./assets/image-20250615100540609.png)

#### （4）主键设计原则

- 满足业务需求的情况下，尽量降低主键的长度。聚集索引只有一个，二级索引可能会有多个。如果主键长度太长，那么二级索引较多，会占用大量的磁盘，而且更重要的是，在查询时性能会很差。
- 插入数据时，尽量选择顺序插入，选择使用AUTOINCREMENT自增主键。如果乱序插入，可能会存在页分裂的现象。
- 尽量不使用UUID做主键，或者身份证号这种自然主键。既违背了上面的第一条，也违背了第二条。
- 业务操作时，避免对主键的修改。

### 4. order by优化

#### （1）概念

- FileSort排序：通过表的索引或全表扫描，读取满足条件的数据行，然后在排序缓冲区sort buffer中完成排序操作，所有不是通过索引直接返回排序结果的排序都叫FileSort排序。
- 索引排序：通过有序索引顺序扫描直接返回有序数据，这种情况即为using index，不需要额外排序，操作效率高。

#### （2）实例

- 按照age来排序，但是age不是索引，此时就是FileSort

![image-20250615102903199](./assets/image-20250615102903199.png)

- 按照age和phone来排序，仍然是FileSort

![image-20250615103032045](./assets/image-20250615103032045.png)

- 此时建立联合索引，`create index idx_user_age_phone on tb_user(age,phone);`
- 再按照age来排序，使用了索引

![image-20250615103338999](./assets/image-20250615103338999.png)

- 再按照age和phone来排序，仍然使用了索引

![image-20250615103425177](./assets/image-20250615103425177.png)

- 都按照倒序排序，会反向扫描索引

![image-20250615103622488](./assets/image-20250615103622488.png)

- 按照phone和age来排序，此时既使用了索引也使用了FileSort，因为违背了最左前缀法则。(这里没懂）

![image-20250615103739462](./assets/image-20250615103739462.png)

- 按照phone升序，age倒序来排序，此时既使用了索引也使用了FileSort，因为联合索引是按照升序排列的

![image-20250615104214972](./assets/image-20250615104214972.png)

对于这种情况，如果我们想走索引，可以建一个这样的联合索引：`create index idx_user_age_phone_ad on tb_user(age asc,phone desc);`

#### （3）总结

- 根据排序字段建立合适的索引，多字段排序时，也遵循最左前缀法则。
- 尽量使用覆盖索引。
- 多字段排序,一个升序一个降序，此时需要注意联合索引在创建时的规则(ASC/DESC)。
- 如果不可避免的出现filesort，大数据量排序时，可以适当增大排序缓冲区大小sont buffer size(默认256K)。

### 5. group by优化

- 直接group by来分组查询，用到了临时表，性能一般

![image-20250616220706211](./assets/image-20250616220706211.png)

- 此时创建联合索引：`create index idx user_pro_age_sta on th user(profession,age,status);`
- 再来group by，此时用到了索引

![image-20250616220903410](./assets/image-20250616220903410.png)

- 而如果用age字段来做group by，此时也会用到临时表，因为违反了最左前缀法则

![image-20250616221031056](./assets/image-20250616221031056.png)

- 如果用profession和age，不违反最左前缀法则，用到了索引

![image-20250616221128303](./assets/image-20250616221128303.png)

### 6. limit优化

#### （1） limit概念

什么时候需要分页查询？页面展示每页 10 条、20 条这样的列表（常见于后台管理系统、前台商品列表等），对应的sql语句

```sql
SELECT * FROM 表名 LIMIT offset, page_size;
```

#### （2） limit优化

- 问题：一个常见又非常头疼的问题就是limit 2000000,10 ，此时需要MySQL排序前2000010记录，仅仅返回2000000-2000010。

- 优化思路: 一般分页查询时，通过创建 覆盖索引 能够比较好地提高性能，可以通过覆盖索引加子查询形式进行优化。

```sql
# 直接查，耗时19.39秒
select * from tb_sku limit 9000000, 10;
# 覆盖索引的思路，既然可以拿到id，就可以拿到数据, 耗时11.47s
select id from tb_sku limit 9000000, 10;
# 直接用in的方式, 会报错
select * from tb_sku where id in (select id from tb_sku order by id limit 9000000.10);
ERROR 1235 (42000): This version of MysQL doesn't yet support 'LIMIT & IN/ALL/ANY/SoME subquery
# 可以把前面的查询结果看作是一张表
select s.* from tb_sku s,(select id from s_ku order by id limit 9000000,10) a where s.id
= a.id;
```

### 7.  count优化

#### （1）count概念

- `count(*)`：查询出来的是表总记录数
- `count(主键)`：等于`count(*)`
- `count(字段)`：字段值不为空的记录
- `count(1)`：`COUNT(1)` 是一个聚合函数，用于统计查询结果集中返回的行数。由于 `1` 对于每一行计算的结果都不是 `NULL`，所以 `COUNT(1)` **最终会统计扫描到的所有行数**。

#### （2）count优化

上面四种count方法，哪种最快呢？

- count(主键)：InnoD8 引擎会遍历整张表，把每一行的 主键id 值都取出来，返回给服务层。服务层拿到主键后，直接按行进行累加(主键不可能为null)。
- count(字段)：InnoDB引擎会遍历整张表把每一行的字段值都取出来，返回给服务层，然后分情况讨论：
  - 没有not null约束：服务层判断是否为nul，不为null，计数累加。
  - 有not null约束：直接按行进行累加。
- count(1)：InnoDB 引擎遍历整张表，但不取值。服务层对于返回的每一行，放一个数字“1”进去，直接按行进行累加。
- count(*)：InnoDB引擎并不会把全部字段取出来，而是专门做了优化，不取值，服务层直接按行进行累加。

按照效率排序的话，`count(字段)`<`count(主键 id)`<`count(1)`≈`count(*)`，所以尽量使用`count(*)`。

### 8. update优化

InnoDB的行锁是针对索引加的锁，不是针对记录加的锁，并且该索引不能失效，否则会从行锁升级为表锁。假设有如下数据

<img src="./assets/image-20250617212633050.png" alt="image-20250617212633050" style="zoom: 67%;" />

#### （1）case1

事务A：

```sql
begin;  # 步骤1
update course set name = 'javaEE' where id=1; # 步骤3
commit; # 步骤5
```

事务B：

```sql
begin;  # 步骤2
update course set name = 'kafka' where id=4; # 步骤4
commit; # 步骤6
```

步骤4的sql可以正常执行，是因为步骤3加的是行锁

#### （2）case2

事务A：

```sql
begin;  # 步骤1
update course set name = 'javaEE' where name="Java"; # 步骤3
commit; # 步骤5
```

事务B：

```sql
begin;  # 步骤2
update course set name = 'kafka' where id=4; # 步骤4
commit; # 步骤6
```

步骤4的sql可以无法正常执行，是因为name不是索引，加的不是行锁，而是表锁。因此在update更新的时候，一定要根据索引来更新。

#### （3）case3

对name建索引：`create index idx_course_name on course(name);`，再次尝试case2，步骤4可以正常执行，因为name是索引。

## 九、锁

### 1. 概述

#### （1）概念

锁是计算机协调多个进程或线程并发访问某一资源的机制。在数据库中，除传统的计算资源(CPU、RAM、I/O)的争用以外，数据也是一种供许多用户共享的资源。如何保证数据并发访问的一致性、有效性是所有数据库必须解决的一个问题，锁冲突也是影响数据库并发访问性能的一个重要因素。

#### （2）分类

MySQL中的锁，按照锁的粒度分，分为以下三类：

- 全局锁：锁定数据库中的所有表。
- 表级锁：每次操作锁住整张表。
- 行级锁：每次操作锁住对应的行数据

### 2. 全局锁

#### （1）介绍

全局锁就是对整个数据库实例加锁，加锁后整个实例就处于只读状态，**后续的DML的写语句，DDL语句，已经更新操作的事务提交语句都将被阻塞**。其典型的使用场景是做全库的逻辑备份，对所有的表进行锁定，从而获取一致性视图，保证数据的完整性。

#### （2）加锁指令

```sql
flush tables with read lock;  # 加锁
unlock；# 解锁
```

### 3. 表级锁

#### （1）介绍

表级锁，每次操作锁住整张表，锁定粒度大，发生锁冲突的概率最高，并发度最低。表级锁，主要分为以下三类：

- 表锁
- 元数据锁（meta data lock）
- 意向锁

#### （2）表锁

对于表锁，分为两类:

- 表共享读锁(read lock)，也称之为读锁，不会阻塞其他客户端的读，会阻塞其他客户端的写，语法：

```sql
# 加锁
lock tables 表名... read;
# 释放锁
unlock tables;
```

从下图可以看到，加了读锁后，所有的客户端都无法写。

![image-20250618201324504](./assets/image-20250618201324504.png)

客户端1：

```sql
# 步骤1: 加锁
lock tables user read;
# 步骤2: 正常执行
select * from user;
# 步骤3: 报错: [HY000l[1099] Table 'user' was locked with a READ lock and can't be updated
update user set email="haojie@gmail.com" where id=1;
# 步骤6: 解锁
unlock tables;
```

客户端2：

```sql
# 步骤4: 正常执行
select * from user;
# 步骤5: 阻塞, 一直到步骤6执行
update user set email="haojie@gmail.com" where id=1;
```

- 表独占写锁(write lock)，也称之为写锁，会阻塞其他客户端的读，也会阻塞其他客户端的写，语法：

```sql
# 加锁
lock tables 表名... write;
# 释放锁
unlock tables
```

从下图可以看到，加了写锁后，当前客户端可以读可以写，其他客户端不能读不能写

![image-20250618202657261](./assets/image-20250618202657261.png)

客户端1:

```sql
# 步骤1: 加锁
lock tables user write;
# 步骤2: 正常执行
select * from user;
# 步骤3: 正常执行
update user set email="haojie@qq.com" where id=1;
# 步骤6: 解锁
unlock tables;
```

客户端2：

```sql
# 步骤4: 阻塞, 一直到步骤6执行
select * from user;
# 步骤5: 阻塞, 一直到步骤6执行
update user set email="haojie@qq.com" where id=1;
```

#### （3）元数据锁

元数据锁（meta data lock，MDL）加锁过程是系统自动控制，无需显式使用，在访问一张表的时候会自动加上。MDL锁主要作用是维护表元数据的数据一致性，在表上有活动事务的时候，不可以对元数据进行写入操作。

下表是不同的sql语句对应的MDL锁类型，这里

- SHARED_READ：MDL读锁，对一张表进行读操作的时候，加的是MDL读锁，和MDL写锁兼容
- SHARED_WRITE：MDL写锁，对一张表进行增、删、改操作的时候，加的是MDL写锁，和MDL读锁兼容
- EXCLUSIVE：排他锁，对表结构进行更新的时候，加的是排他锁，和MDL读锁、MDL写锁都互斥

![image-20250618211136232](./assets/image-20250618211136232.png)

客户端1：

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 正常执行
select * from user;
# 步骤8: 提交事务
commit;
```

客户端2：

```sql
# 步骤3: 开启事务
begin;
# 步骤4: 正常执行
select * from user;
# 步骤5: 正常执行
update user set email="haojie@qq.com" where id=1;
# 步骤6: 提交事务
commit;
# 步骤7: 新增字段, 阻塞, 一直到步骤8执行
alter table user add column sex int;
```

可以在mysql 内置的`performance_schema`库的`metadata_locks`表查看MDL锁的情况

#### （4）意向锁

为了避免加的行锁与表锁的冲突，在InnoDB中引入了意向锁，使得表锁不用检查每行数据是否加锁，使用意向锁来减少表锁的检查。

![image-20250618214732570](./assets/image-20250618214732570.png)

如上图所示，客户端1对id=3的数据加了行锁，客户端2在加表锁前，需要逐行检查，效率很低，意向锁就是为了解决这个问题的 。意向锁分为两种：

- 意向共享锁（IS）：加锁语句为，`select ... lock in share mode`。与表锁共享锁(read)兼容，与表锁排它锁(write)互斥。
- 意向排他锁（IX）：由insert、update、delete、select ... for update 添加。与表锁共享锁(read)及排它锁(write)都互斥，意向锁之间不会互斥。

> 注意别搞混，这里说的表锁共享锁和表锁共享锁，指的是（2）里面的锁

可以在mysql 内置的`performance_schema`库的`data_locks`表查看意向锁以及行锁的加锁情况

客户端1:

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 这个语句既会加上行锁, 也会加上意向锁（IS）,可以在performance_schema.data_locks查
select * from user where id=1 lock in share mode;
# 步骤5: 提交事务，行锁和意向锁都被释放
commit;
```

客户端2:

```sql
# 步骤3: 加表锁读锁，执行成功，因为IS和表锁读锁兼容
lock tables score read;
# 步骤4: 加表锁写锁，阻塞，一直到步骤5执行，因为IS和表锁写锁互斥
lock tables score write;
```

### 4. 行级锁

#### （1）介绍

行级锁，每次操作锁住对应的行数据。锁定粒度最小，发生锁冲突的概率最低，并发度最高。应用在InnoDB存储引擎中，InnoDB的数据是基于索引组织的，**行锁是通过对索引上的索引项加锁来实现的，而不是对记录加的锁**。对于行级锁，主要分为以下三类：

- 行锁（Record Lock）：锁定单个行记录的锁，防止其他事务对此行进行update和delete。在RC、RR隔离级别下都支持。
- 间隙锁（Gap Lock）：锁定索引记录间隙(不含该记录)，确保索引记录间隙不变，防止其他事务在这个间隙进行insert，产生幻读。在RR隔离级别下都支持。
- 临键锁（Next-Key Lock）：行锁和间隙锁组合，同时锁住数据，**并锁住数据前面的间隙Gap**。在RR隔离级别下支持

#### （2）行锁

InnoDB实现了以下两种类型的行锁：

- 共享锁(S)：允许一个事务去读一行，阻止其他事务获得相同数据集的排它锁。
- 排他锁(X)：允许获取排他锁的事务更新数据，阻止其他事务获得相同数据集的共享锁和排他锁。

两种类型的行锁兼容情况如下：

<img src="./assets/image-20250619135539930.png" alt="image-20250619135539930" style="zoom:50%;" />

我们常见的sql语句，它的行锁情况如下：

<img src="./assets/image-20250619135711142.png" alt="image-20250619135711142" style="zoom:80%;" />

> 前面已经说过，可以在mysql 内置的`performance_schema`库的`data_locks`表查看意向锁以及行锁的加锁情况

- case1：共享锁和共享锁

客户端1：

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 加锁，可以通过performance_schema.data_locks查看，加了共享锁（S）
select * from user where id=1 lock in share mode;
# 步骤5: 提交事务
commit;
```

客户端2：

```sql
# 步骤3: 开启事务
begin;
# 步骤4: 加锁，虽然id一样，但是能正常执行, 因为共享锁和共享锁兼容
select * from user where id=1 lock in share mode;
# 步骤6: 提交事务
commit;
```

- case2：共享锁和排他锁

客户端1：

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 加锁，可以通过performance_schema.data_locks查看，加了共享锁（S）
select * from user where id=1 lock in share mode;
# 步骤6: 提交事务
commit;
```

客户端2：

```sql
# 步骤3: 开启事务
begin;
# 步骤4: 更新操作，且id和客户端1不一样：正常执行
update user set email="yuwen@gmail.com" where id=2;
# 步骤5: 更新操作，且id和客户端1一样, 阻塞, 直到步骤6. 共享锁和排他锁互斥
# 需要注意的是, 这里如果客户端1长时间不提交事务, 这里会有报错：[40001][1205] Lock wait timeout exceeded; try restarting transaction
update user set email="haojie@gmail.com" where id=1;
# 步骤7: 提交事务
commit;
```

- case3：排他锁和排他锁

客户端1：

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 加锁，可以通过performance_schema.data_locks查看，加了共享锁（S）
update user set email="haojie@gmail.com" where id=1;
# 步骤5: 提交事务
commit;
```

客户端2：

```sql
# 步骤3: 开启事务
begin;
# 步骤4: 正常执行, 因为id不一样
update user set email="yuwen@gmail.com" where id=2;
# 步骤6: 提交事务
commit;
```

另外需要说明的是，InnoDB的行锁是针对于索引加的锁，不通过索引条件检索数据，那么InnoDB将对表中的所有记录加锁，此时就会升级为表锁。

客户端1：

```sql
# 步骤1: 开启事务
begin;
# 步骤2: update操作，并且没有通过索引检索数据
update user set email="haojie@gmail.com" where username="haojie";
# 步骤5: 提交事务
commit;
```

客户端2：

```sql
# 步骤3: 开启事务
begin;
# 步骤4: update操作，会阻塞，因为步骤2相当于加了表锁
update user set email="yuwen@gmail.com" where id=2;
# 步骤6: 提交事务
commit;
```

如果此时创建索引`create index idx_user_username on user(username)`，此时步骤4就不会被阻塞

#### （3）间隙锁和临键锁

间隙锁（Gap Lock）和临键锁（Next-Key Lock），它们是实现**可重复读（Repeatable Read, RR）** 隔离级别下防止**幻读**现象的核心机制。

> 注意：幻读是指在一个事务内，两次执行相同的查询，但第二次查询返回了第一次查询中未出现的新行（这些新行是其他事务插入并提交的）。

- 间隙锁
  - 定义：锁定的是**索引记录之间的间隙**，它锁定的是一**个范围**，但这个范围**不包含任何实际的索引记录本身**。 
  - 目的：防止其他事务在锁定的间隙中插入新的记录，这是防止幻读的关键手段。

- 临键锁
  - 定义：是InnoDB **默认的行锁算法**（在RR隔离级别下），它是**记录锁（Record Lock）和 间隙锁（Gap Lock）的组合**，它锁定的是**索引记录本身**以及**该索引记录之前的间隙**。
  - 目的：1）**防止幻读：**通过锁定记录和它前面的间隙，确保在锁定范围内无法插入新记录（间隙锁部分的作用），也无法修改或删除已锁定的记录（记录锁部分的作用）；2）**实现 RR 隔离级别：** 它是MySQL在 RR级别下保证语句级别（Statement-Level）一致性读和防止幻读的主要工具。

注意：

1. 间隙锁唯一目的是防止其他事务插入间隙。
2. 间隙锁可以共存，一个事务采用的间隙锁不会阻止另一个事务在同一间隙上采用间隙锁。

#### （4）三种特殊情况

默认情况下，InnoDB在 REPEATABLE READ事务隔离级别运行，**InnoDB使用临键锁进行搜索和索引扫描**，以防止幻读。但是存在以下三种特殊情况，临键锁会被优化或者退化

- 结论1：索引上的等值查询(唯一索引)，给不存在的记录加锁时，优化为间隙锁。
- 结论2：索引上的等值查询(普通索引)，向右遍历时最后一个值不满足查询需求时，临键锁退化为间隙锁。这句话不太好理解，例如下图我们要查询的值是18，这里说的“向右遍历时最后一个值不满足查询需求时”，就是29，因此加的锁就是（18，29）这个开区间。

![image-20250629205146109](./assets/image-20250629205146109.png)

- 结论3：索引上的范围查询(唯一索引)，会访问到不满足条件的第一个值为止。

下面分别来说明这三个结论，这是我们的数据

![image-20250619222008672](./assets/image-20250619222008672.png)

（1）结论1说明

客户端1：

```sql
# 步骤1: 开启事务
begin;
# 步骤2: update操作，并且操作的是不存在的记录！此时会有间隙锁，并且间隙锁的范围为8之前的间隙，也就是(2, 8)开区间，见下图
update user set email="luoan@gmail.com" where id=5;
# 步骤5: 提交事务
commit;
```

步骤2之后查看`performance_schema.data_locks`，可以看到lock_mode里有一个gap字样，说明是间隙锁；并且lock_data里的数据是8，那就是8之前的间隙，在这里由于索引是1,2,8，因此锁的间隙就是（2,8）

![image-20250619220614935](./assets/image-20250619220614935.png)

客户端2：

```sql
# 步骤3: 开启事务
begin;
# 步骤4: 由于步骤2加了间隙锁，并且间隙锁范围为(2,8), 此时会被锁住
insert into user(id, username, email, password) values(4, "meimei", "meimei@qq.com", "123456");
# 步骤6: 提交事务
commit;
```

（2）结论2说明

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 查询并加共享锁，此时锁的情况如下图所示
select * from user where age=33 lock in share mode;
# 步骤3：提交事务
commit;
```

![image-20250619222248518](./assets/image-20250619222248518.png)

第一个`S,GRANTED,"33, 2"`。临键锁，锁定范围：`(1, 33]`（即从age=1到age=33的左开右闭区间），防止在age=1和age=33之间插入新记录，LOCK_DATA中的`"33,2"`表示索引值(age=33)和主键(id=2)。

第二个`S,REC_NOT_GAP,GRANTED,2`**。**记录锁，锁定主键ID=2的具体行，防止其他事务修改或删除这行数据。

第三个`S,GAP,GRANTED,"34,1"`。间隙锁，锁定范围：`(33, 34)`（即age=33和age=34之间的间隙），防止在age=33和age=34之间插入新记录（如插入age=33.5）。

对这三个值的解释

1. 查询`age=33`（普通索引）时，InnoDB首先对匹配的记录`age=33`加**临键锁**（锁定`(1,33]`区间）
2. 继续向右遍历找到`age=34`（下一个索引记录）
3. 由于`age=34 ≠ 33`（不满足查询条件），此时对`age=34`原本要加的临键锁`(33,34]`**退化为间隙锁**，只锁定`(33,34)`区间

为什么这样设计？

1. **防止幻读**，通过锁定`(1,33]`和`(33,34)`区间，确保在事务执行期间：
   - 无法插入新的`age=33`记录（如插入age=33.5会被间隙锁阻塞）
   - 无法修改相邻记录的age为33（如将age=32改为33会被临键锁阻塞）
2. **优化并发性能**
   - 退化间隙锁后，允许在`(34,+∞)`区间自由插入数据（如插入age=35）
   - 不锁定无关的age=34记录本身（仅锁间隙，允许修改age=34的值）

（3）结论3说明

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 查询并加共享锁，此时锁的情况如图所示
select * from user where id>=2 lock in share mode;
# 步骤3：提交事务
commit;
```

![image-20250630213254545](./assets/image-20250630213254545.png)

第一个`S,REC_NOT_GAP,GRANTED,2`**。**记录锁，锁定主键ID=2的具体行，保护满足查询条件的起始行

第二个`S,GRANTED,supremum pseudo-record`。上界伪记录锁（Supremum Lock），锁定范围：`(8, +∞)` 所有大于id=8的间隙，防止插入任何`id>8`的新记录（如id=9,10,...）

第三个`S,GRANTED,8`。临键锁，锁定范围：`(2, 8]`（即id=2到id=8的左开右闭区间），防止在`(2,8)`间隙插入记录（如id=3,4,7）并锁定id=8行。

对这三个值的理解

1. 查询`id>=2`（唯一索引范围查询）
2. InnoDB扫描过程：
   - 定位到第一个满足条件的行 `id=2`
   - 继续向右扫描：
     - `id=8` 满足 `id>=2`（仍满足条件）
     - 越过`id=8`后遇到虚拟的**上界伪记录**（不满足条件）
3. 扫描停止在第一个不满足条件的值（上界伪记录）

为什么这样设计？

1. **防止幻读**，通过锁定`[2, +∞)`整个范围：
   - 现有记录：锁定id=2(记录锁)和id=8(临键锁)
   - 未来记录：阻止插入任何id>=3的新记录
2. **精确扫描边界**，扫描到第一个不满足条件的值（上界伪记录）停止，确保：
   - 锁定所有`id>=2`的**现有记录**（id=2和id=8）
   - 锁定所有`id>2`的**插入间隙**（(2,8)和(8,+∞)）
3. **唯一索引的特殊性**，虽然是范围查询，但利用唯一索引特性：
   - 对精确存在的`id=2`使用**记录锁**（更高效）
   - 对范围部分`id>2`使用**临键锁**（防幻读）

## 十、MVCC

### 1. 介绍

#### （1）MVCC简介

MySQL 中的 MVCC（Multi-Version Concurrency Control，多版本并发控制）是一种用于提高数据库并发性能的核心机制。它的核心思想是：**允许同一份数据存在多个版本，不同事务在读取数据时可以看到特定时刻的快照，而不是直接读写最新数据**。这样避免了读操作和写操作互相阻塞，大大提升了并发效率。

- **高并发读写**：让读操作（SELECT）不阻塞写操作（UPDATE/INSERT/DELETE），写操作也不阻塞读操作（非绝对，某些情况如DDL会锁表）。

- **解决部分并发问题**：

  - 避免**脏读**（读到未提交的数据）。

  - 在 `REPEATABLE READ` 隔离级别下避免**不可重复读**（同一事务内两次读结果不一致）。

  - （部分解决）**幻读**（通过快照读避免，但当前读仍可能发生）。

MVCC的具体实现，还需要依赖于三个关键的概念，下一节会介绍：

- 数据库记录中的三个隐式字段
- undo log日志
- ReadView

#### （2）当前读

读取的是**记录的最新版本**，读取时还要保证其他并发事务不能修改当前记录，会对读取的记录进行加锁。对于我们日常的操作，如: `select.... lock in share mode`，`select .. for update`、`update`、`insert`、`delete`**都是一种当前读**。

客户端1：

```sql
# 步骤1: 开启事务
begin;
# 步骤2: 查询, 此时邮箱是"haojie@qq.com"
select * from user;
# 步骤5: 再次查询, 此时邮箱仍然是"haojie@qq.com"
select * from user;
# 步骤7: 继续查询, 此时邮箱还是"haojie@qq.com", 因为MySQL的默认隔离级别是可重复读（RR），如果读到的是"haojie@gmail.com", 就不是可重复读了
select * from user;
# 步骤8: 接着再查，并且加上lock in share mode, 此时查到的邮箱是haojie@gmail.com, 因为加上lock in share mode后就是当前读!! 当前读，读的是记录的最新版本!!
select * from user lock in share mode;
```

客户端2：

```sql
# 步骤3: 开启事务
begin;
# 步骤4: update操作
update user set email="haojie@gmail.com" where id=1;
# 步骤6: 提交事务
commit;
```

#### （3）快照读

简单的select（不加锁）就是快照读，快照读，**读取的是记录数据的可见版本**，有可能是历史数据，不加锁，是非阻塞读。在MySQL默认的RR隔离级别下，快照读保证了**在同一个事务内，多次执行相同的 `SELECT` 语句，看到的数据是一致的**，即使其他事务在此期间修改并提交了数据。这是通过在整个事务开始时创建一个“一致性视图”，来实现的，所有该事务内的快照读都基于这个视图。

这里会有一个问题，快照读并不是最新的数据，为什么MySQL允许快照读？MySQL 允许（并且大力推崇）快照读，**核心目的是为了解决“读-写并发冲突”，大幅提升数据库的并发性能和响应能力**，尽管它读取的不是绝对最新的数据。

### 2. 实现原理

#### （1）隐藏字段

在InnoDB引擎中，除了我们创建的字段，InnoDB还会额外创建三个隐藏字段

![image-20250622110128774](./assets/image-20250622110128774.png)

- DB_TRX_ID：最近修改事务ID，记录插入这条记录或最后一次修改该记录的事务ID。
- DB_ROLL_PTR：指向该行数据**上一个版本**在 Undo Log 中的位置指针，这是一个非常关键的指针，有了这个指针，就可以知道这条记录上一个版本数据长啥样。它形成了一个单向链表，将数据的所有历史版本链接起来（版本链）。
- DB_ROW_ID：隐藏主键，如果表结构没有指定主键，将会生成该隐藏字段。如果有的话，就不会生成。

可以使用ibd2sdi命令来查看表的字段信息，`ibd2sdi /usr/local/mysql/data/mysql_basic/user.ibd`，可以看到`DB_TRX_ID`等隐藏字段

<img src="./assets/image-20250622112259154.png" alt="image-20250622112259154" style="zoom: 33%;" />

#### （2）undo log日志

undo log是回滚日志，在insert、update、delete的时候产生的，便于数据回滚的日志。

- 当insert的时候，产生的undo log日志只在回滚时需要。在事务提交后，可被立即删除。

- 而update、delete的时候，产生的undo log日志不仅在回滚时需要，在快照读时也需要，不会立即被删除。

下面是undo log 版本链的例子：

-  在表中插入一条数据，记录为：

<img src="./assets/image-20250622114111368.png" alt="image-20250622114111368" style="zoom:63%;" />

- 我们同时开启3个事务：

事务2：

```sql
# 步骤1: 开启事务
begin;
# 步骤4：修改记录
update user set age=3 where id=30;
# 步骤5：提交事务
commit;
```

事务3：

```sql
# 步骤2: 开启事务
begin;
# 步骤6: 修改记录
update user set name=“A3” where id=30;
# 步骤7：提交事务
commit;
```

事务4：

```sql
# 步骤3: 开启事务
begin;
# 步骤8: 修改记录
update user set age=10 where id=30;
# 步骤9：提交事务
commit;
```

- 在步骤4开始前，会记录一个undo log日志，用来记录update变更前，当前数据表中的数据是什么样的

<img src="./assets/image-20250622114539594.png" alt="image-20250622114539594" style="zoom:67%;" />

- 步骤4 update变更后，此时的记录不仅仅变更了数据。还变更了隐藏字段`DB_TRX_ID`，`DB_ROLL_PTR`。`DB_TRX_ID`字段值为事务ID：2，`DB_ROLL_PTR`记录的是上一个版本：0x00001。如果更新失败，只需要回滚到undo log中记录的上一个版本0x00001即可。

> 注意：上面说的"此时的记录不仅仅变更了数据"，是指的在当前事务中，在其他事务中，由于没有提交事务，此时是查不到最新变更的。

<img src="./assets/image-20250622114733372.png" alt="image-20250622114733372" style="zoom:67%;" />

- 在步骤6开始前，会记录一个undo log日志，用来记录update变更前，当前数据表中的数据是什么样的

<img src="./assets/image-20250622115338735.png" alt="image-20250622115338735" style="zoom:67%;" />

- 步骤6 update变更后，`DB_TRX_ID`字段值为事务ID：3，`DB_ROLL_PTR`记录的是上一个版本：0x00002。如果更新失败，只需要回滚到undo log中记录的上一个版本0x00002即可。

<img src="./assets/image-20250622115536517.png" alt="image-20250622115536517" style="zoom:67%;" />

- 步骤8，更新操作，同上，这样就形成了undo log 版本链，如下图所示

<img src="./assets/image-20250622183715448.png" alt="image-20250622183715448" style="zoom:67%;" />

不同事务或相同事务对同一条记录进行修改，会导致该记录的undo log生成一条记录版本链表，链表的头部是最新的旧记录，链表尾部是最早的旧记录。

> 

#### （3）ReadView

**ReadView（读视图）是决定事务能看到哪些数据版本的核心数据结构**。它定义了事务进行**快照读**（普通 `SELECT`）时的“数据可见性范围”，确保事务在并发环境下读取到一致的数据快照。

ReadView中包含了四个核心字段：

- m_ids：当前活跃的事务ID集合 
- min_trx_ id：最小活跃事务ID
- max_trx_id：预分配事务ID，当前最大事务ID+1（因为事务ID是自增的）
- creator_trx_id：ReadView创建者的事务ID

> 注意，ReadView不是用户可直接查看的数据库对象，不能通过某一张表看到这个数据。但是在information_schema.INNODB_TRX表中可以看到trx_id，这些都是活跃的事务id.

版本链数据访问规则：

![image-20250624212050541](./assets/image-20250624212050541.png)

> 一个比较好的理解方式，如果id比当前trx_id小，说明是我的“晚辈”，可以访问。

### 3. 原理分析

> 本部分好好理解，可以把前面的都给串起来

#### （1）RC隔离级别

在RC隔离级别下，在事务中每一次执行快照读时生成Readview。

以前面的数据为例，我们来首先看一下事务5第一次查询id为30的记录，读到的版本应该是哪个。

- m_ids：这里由于事务2已经提交，因此m_ids是{3,4,5}

- min_trx_id：最小活跃事务ID，为3
- max_trx_id：预分配事务ID，当前最大事务ID+1：6
- creator_trx_id：执行这次快照读的时候，会生成一个ReadView，因此id是5

![image-20250628224319116](./assets/image-20250628224319116.png)

- 当前记录：trx_id为4，**右边的四个条件都不满足**，说明这次快照读查找的数据不应该是这个
- 0x00003版本：trx_id为3，同样右边的四个条件都不满足，说明也不是这个版本
- 0x00002版本：trx_id为2，满足trx_id<min_trx_id条件，此时会将这个版本的记录返回。

#### （2）RR隔离级别

RR隔离级别下，仅在事务中第一次执行快照读时生成ReadView，后续复用该ReadView。

![image-20250628225934750](./assets/image-20250628225934750.png)

到了这里，是不是有豁然开朗的感觉了，RR，可重复读，**同一个事务读了两条相同的数据，ReadView一样，因此匹配规则一样，查找出的数据也一样**。

