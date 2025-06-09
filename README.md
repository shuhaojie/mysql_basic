## 一、事务

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

- **定义：** 事务只能读取其他**已经提交**的事务所做的修改。这是**Oracle 等数据库的默认级别**。
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

## 二、索引


## 三、锁

