2026.6.27
    今日将数据库文件和服务文件完成了异步改造
    重点是commit和response的地方并且和main作了await传染
    查询部分也做了适当的优化和异步
    以及将原来main简陋的init_db更改为life的上下文管理器