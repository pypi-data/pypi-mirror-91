import os


def get_txt():
    """使用原始打开io方式打开"""
    with open('demo.txt', 'r', encoding='utf-8') as f:
        return f.read()


# def get_demo_txt():
#     """修改获取路径方式，使用io打开"""
#     current_dir = os.path.dirname(__file__)
#     file_path = os.path.join(current_dir, 'demo.txt')
#     with open(file_path, 'r', encoding='utf-8') as f:
#         return f.read()


if __name__ == "__main__":
    """类内测试，均无异常"""
    # print("get_demo_txt() :", get_demo_txt())
    # get_demo_txt() : The text is from demo.txt.

    print("get_txt() :", get_txt())
    # get_txt() : The text is from demo.txt.