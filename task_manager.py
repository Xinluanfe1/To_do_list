from datetime import datetime


def add_task(tasks, title, priority, deadline):
    # 校验标题不为空
    if not isinstance(title, str) or len(title.strip()) == 0:
        return False, "Title cannot be empty."
    title = title.strip()

    # 校验优先级
    valid_priority = {"P0", "P1", "P2"}
    if priority not in valid_priority:
        return False, "Priority must be P0, P1 or P2."

    # 校验截止时间格式
    try:
        datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        return False, "Deadline format error, use YYYY-MM-DD HH:MM"

    # 生成新id：最大id + 1；空列表则id=1
    if len(tasks) == 0:
        new_id = 1
    else:
        max_id = max(task["id"] for task in tasks)
        new_id = max_id + 1

    new_task = {
        "id": new_id,
        "title": title,
        "priority": priority,
        "deadline": deadline,
        "completed": False,
        "completed_at": None
    }
    tasks.append(new_task)
    return True, "Task added"


def edit_task(tasks, task_id, title=None, priority=None, deadline=None):
    # 找到对应id的任务
    target_task = None
    for t in tasks:
        if t["id"] == task_id:
            target_task = t
            break
    if target_task is None:
        return False, "Task not found"

    # 逐个校验并更新不为None的字段
    if title is not None:
        if len(title.strip()) == 0:
            return False, "Title cannot be empty."
        target_task["title"] = title.strip()

    if priority is not None:
        if priority not in {"P0", "P1", "P2"}:
            return False, "Priority must be P0, P1 or P2."
        target_task["priority"] = priority

    if deadline is not None:
        try:
            datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        except ValueError:
            return False, "Deadline format error, use YYYY-MM-DD HH:MM"
        target_task["deadline"] = deadline

    return True, "Task updated"


def complete_task(tasks, task_id):
    target_task = None
    for t in tasks:
        if t["id"] == task_id:
            target_task = t
            break
    if target_task is None:
        return False, "Task not found"

    # 已经完成就不重复修改
    if target_task["completed"] is True:
        return False, "This task is already completed"

    # 标记完成，写入当前时间
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    target_task["completed"] = True
    target_task["completed_at"] = now_str
    return True, "Task marked as completed"


def delete_task(tasks, task_id):
    for idx, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(idx)
            return True, "Task deleted"
    return False, "Task not found"
