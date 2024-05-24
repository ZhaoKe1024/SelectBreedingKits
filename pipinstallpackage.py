import os
pack_list = [
    "PyQT5",
    "pandas==1.5.3",
    "pyinstaller==6.6.0",
    "openpyxl==3.1.2",
]
# set DS_BUILD_AIO=0
# set DS_BUILD_SPARSE_ATTN=0
for packa in pack_list:
    # os.system("pip install " + packa + " -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system("pip install " + packa + " -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com")
