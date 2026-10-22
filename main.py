"""终端交互（组员 A 负责）。

职责：显示菜单、读取用户输入、调用 B/C/D 的函数、显示结果。
不要在这里重新编写添加、排序或保存文件的逻辑，只负责调用。

需要完成的功能：
1. show_menu()：用 print() 打印主菜单（菜单样式见开发说明第 6 节）：
      1. Add a task
      2. View tasks
      3. Edit a task
      4. Complete a task
      5. Delete a task
      6. View completed tasks
      7. Sort tasks
      0. Exit
2. display_tasks(tasks)：把任务列表逐行打印到终端；对每个未完成任务，
   调用 task_utils.check_deadline(task)，结果不是 "normal" 时给出提示。
3. main()：
   - 调用 storage.load_tasks() 读取数据；返回 None（文件损坏）时提示并退出。
   - 用 while 循环显示菜单并读取 input()。
   - 按用户选择调用对应函数：
       1 → input() 收集信息 → task_manager.add_task()
       2 → display_tasks(task_utils.get_pending_tasks(tasks))
       3 → input() 收集编号和要改的项 → task_manager.edit_task()
       4 → task_manager.complete_task()
       5 → task_manager.delete_task()
       6 → display_tasks(task_utils.get_completed_tasks(tasks))
       7 → input() 选择 priority/deadline → task_utils.sort_tasks()
       0 → 退出循环
   - 每次成功修改数据（增、改、完成、删除）后调用 storage.save_tasks(tasks)。
   - 保存失败时提示用户“已修改但未保存”。
   - 错误输入（如菜单输入 9、任务编号不存在）要提示并允许继续操作。

可以按开发说明第 7 节的示例组织代码。
"""

from storage import load_tasks, save_tasks
from task_manager import add_task, edit_task, complete_task, delete_task
from task_utils import check_deadline, get_completed_tasks, get_pending_tasks, sort_tasks

def show_menu():    #用 print() 打印主菜单
    print("1.添加任务")
    print("2.查看任务")
    print("3.编辑任务")
    print("4.完成任务")
    print("5.删除任务")
    print("6.查看已完成任务")
    print("7.按顺序查看任务")
    print("0.退出")
    pass


def display_tasks(tasks):   #将任务列表逐行打印到终端，并提示逾期或即将到期的任务。

    if not tasks:
        print("暂无任务。")
        return

    for task in tasks:
        line = f"[{task['id']}] {task['priority']} | {task['title']}"
        if task["completed"]:
            line += f" | 完成时间：{task['completed_at']}"
        else:
            line += f" | 截止时间：{task['deadline']}"
            level = check_deadline(task)
            if level == "overdue":
                line += " | 已逾期"
            elif level == "soon":
                line += " | 24 小时内到期"
        print(line)

def read_task_id():     #按编号读取任务编号并转成 int；输入非法时返回 None。
    """读取任务编号并转成 int；输入非法时返回 None。"""
    raw = input("任务编号：").strip()
    if not raw.isdigit():
        print("任务编号必须是数字。")
        return None
    return int(raw)

def main():     #主函数
    tasks = load_tasks()
    if tasks is None:
        print("任务数据文件损坏，程序无法继续运行。")
        return

    while True:
        show_menu()
        choice = input("请输入你的选择：").strip()

        if choice == "0":   #退出
            print("已退出，再见！")
            break

        elif choice == "1":  #添加任务
            title = input("任务名称：").strip()
            priority = input("优先级（P0/P1/P2）：").strip()
            deadline = input("截止时间（YYYY-MM-DD HH:MM）：").strip()
            success, message = add_task(tasks, title, priority, deadline)
            if success:
                print(message if save_tasks(tasks) else "任务已添加，但保存失败！")
            else:
                print(message)

        elif choice == "2":     #查看任务
            display_tasks(get_pending_tasks(tasks))

        elif choice == "3":     #编辑任务
            task_id = read_task_id()
            if task_id is None:
                continue
            title = input("新名称（留空表示不修改）：").strip()
            priority = input("新优先级（留空表示不修改）：").strip()
            deadline = input("新截止时间（留空表示不修改）：").strip()
            success, message = edit_task(
                tasks, task_id,
                title=title or None,
                priority=priority or None,
                deadline=deadline or None,
            )
            if success:
                print(message if save_tasks(tasks) else "任务已修改，但保存失败！")
            else:
                print(message)

        elif choice == "4":     #完成任务   
            task_id = read_task_id()
            if task_id is None:
                continue
            success, message = complete_task(tasks, task_id)
            if success:
                print(message if save_tasks(tasks) else "任务已完成，但保存失败！")
            else:
                print(message)

        elif choice == "5":     #删除任务
            task_id = read_task_id()
            if task_id is None:
                continue
            success, message = delete_task(tasks, task_id)
            if success:
                print(message if save_tasks(tasks) else "任务已删除，但保存失败！")
            else:
                print(message)

        elif choice == "6":     #查看已完成任务
            display_tasks(get_completed_tasks(tasks))

        elif choice == "7":     #按顺序查看任务
            method = input("排序方式（priority / deadline）：").strip()
            if method not in ("priority", "deadline"):
                print("排序方式无效，请输入 priority 或 deadline。")
                continue
            display_tasks(sort_tasks(tasks, method))

        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    main()
