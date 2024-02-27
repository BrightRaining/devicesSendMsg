import inspect
import os

# 获取指定文件夹下的文件列表
def get_project_file(direct_file = 'report'):
    # 当前文件的绝对路径
    current_file = os.path.abspath(os.getcwd())
    # 当前文件所在的项目路径
    current_direct = os.path.dirname(current_file)
    # 项目根目录
    # project_root = os.path.dirname((os.path.dirname(current_direct)))
    file_list = os.listdir(str(current_direct) + '\\' + str(direct_file))
    return file_list

# 获取当前项目路径
def get_project_root():
    # # 当前文件的绝对路径
    # current_file = os.path.abspath(os.getcwd())
    # # 当前文件所在的项目路径
    # current_direct = os.path.dirname(current_file)
    # project_root = os.path.dirname((os.path.dirname(current_direct)))
    return os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))

# 判断文件是否存在
def is_file_exit(file_abs):
    if os.path.isfile(file_abs):
        return True
    else:
        return False