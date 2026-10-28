from datetime import datetime, timedelta

"""任务查询与排序（组员 C 负责）。

只负责查询和计算，不修改原列表，不保存 JSON 文件。

需要完成的功能（接口约定见开发说明第 4 节 C）：
1. get_pending_tasks(tasks)：返回未完成任务的新列表。
2. get_completed_tasks(tasks)：返回已完成任务的新列表，
   完成时间新的排在前面。
3. sort_tasks(tasks, method)：method 只能是 "priority" 或 "deadline"；
   返回排序后的新列表，不改变原列表。
   - "priority"：P0 → P1 → P2；
   - "deadline"：截止时间从早到晚。
4. check_deadline(task)：返回下面四个值之一：
   - "completed"：任务已完成；
   - "overdue"：未完成且已超过截止时间；
   - "soon"：未完成且剩余时间在 0～24 小时之间（包括 24 小时）；
   - "normal"：其余情况。

时间解析统一使用 datetime.strptime(时间字符串, "%Y-%m-%d %H:%M")。
"""


def get_pending_tasks(tasks):
    # TODO（C）：在这里实现；返回未完成任务的新列表
    # 假设未完成的任务status不为'completed',或者为'pending'
    return [task for task in tasks if task.get('status') != 'completed']


def get_completed_tasks(tasks):
    # TODO（C）：在这里实现；返回已完成的新列表，最新完成在前
    completed = [task for task in tasks if task.get('status') == 'completed']
    # 根据completed_at降序排列， 假设缺失该字段的任务排在最后
    return sorted(completed, key=lambda x: x.get('completed_at', ''), reverse=True)


def sort_tasks(tasks, method):
    # TODO（C）：在这里实现；返回排序后的新列表，不修改原列表
    if method == "priority":
        # 定义优先级权重，P0最优先，P1其次，P2最后
        priority_map = {"P0":0, "P1":1, "P2":2}
        # 返回新列表，按照映射的权重升序排序（缺失优先级的排最后）
        return sorted(tasks, key=lambda x: priority_map.get(x.get('priority'), 99))
    elif method == "deadline":
        # 按照截止时间字符串升序排列（时间格式 "%Y-%m-%d %H:%M" 可以直接按字符串比较）
        return sorted(tasks, key=lambda x: x.get('deadline', '9999-99-99 99:99'))
    else:
        # 如果method不是上述两者，直接返回原列表的浅拷贝
        return list(tasks)


def check_deadline(task):
    # TODO（C）：在这里实现；返回 completed / overdue / soon / normal
    # 1. 检查是否已完成
    if task.get('status') == 'completed':
        return "completed"
    deadline_str = task.get('deadline')
    if not deadline_str:
        return "normal" # 如果没有截止时间，默认返回normal

    #2. 解析时间
    now = datetime.now()
    deadline_time = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

    #3.判断是否逾期
    if now > deadline_time:
        return "overdue"

    #4.判断是否即将到期（0~24小时内）
    time_diff = deadline_time - now
    if timedelta(0) <= time_diff <= timedelta(hours=24):
        return "soon"

    #5.其他情况
    return "normal"
