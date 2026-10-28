"""数据读写（组员 D 负责）。

只负责 tasks.json 的读写，不负责添加、删除或排序任务。

需要完成的功能（接口约定见开发说明第 4 节 D）：
1. load_tasks()：
   - 使用 json.load() 读取本文件同级的 tasks.json；
   - 文件不存在时返回空列表 []；
   - 文件存在但内容损坏（JSON 解析失败）时打印错误信息并返回 None。
2. save_tasks(tasks)：
   - 使用 json.dump() 保存到 tasks.json；
   - 保存成功返回 True，失败返回 False。
3. 保存参数使用 ensure_ascii=False、indent=4，编码为 UTF-8，
   让 JSON 文件里的中文可直接阅读、格式整齐。

说明：main.py 在 load_tasks() 返回 None 时应结束本次运行，
不能把损坏的数据文件覆盖掉。
"""

import json
import os


# 始终读写 storage.py 同级的 tasks.json，不受启动目录影响
TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks():
    # 第一次运行时还没有数据文件，直接返回空列表
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        print(f"读取任务失败：tasks.json 内容损坏（{error}）。")
        return None
    except OSError as error:
        print(f"读取任务失败：{error}")
        return None

    # 数据文件的最外层必须是任务列表
    if not isinstance(tasks, list):
        print("读取任务失败：tasks.json 的顶层内容必须是列表。")
        return None

    return tasks


def save_tasks(tasks):
    if not isinstance(tasks, list):
        print("保存任务失败：任务数据必须是列表。")
        return False

    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
    except (OSError, TypeError, ValueError) as error:
        print(f"保存任务失败：{error}")
        return False

    return True
