#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/30 14:30
# @Author: ZhaoKe
# @File : main_poultryinbreed.py
# @Software: PyCharm
import os
import json
import time

from flask import Flask, request, jsonify, render_template
from databasekits.table_packets import insert_use_dict
from gevent import pywsgi

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'

CHUNK_SIZE = 1024 * 1024
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20M
form_save_mode = 0  # mysql 0, local json file 1,

save_dir = "./temp_files/"


class IBCalculator(object):
    def __init__(self):
        super(IBCalculator, self).__init__()
        self.file_to_analyze = None
        self.file_to_evaluate = None
        self.kinship = None
        self.keys = ["analyse", "select", "eval", "p", "p1", "help"]
        self.describe = ["分析文件并构建族谱", "生成新一年的配种方案", "评估现有方案", "计算个体近交系数",
                         "计算亲缘相关系数", "查看帮助"]

    def execute_all(self, kv_list):
        ind = 1
        while ind <= len(kv_list) - 1:
            if kv_list[ind] == "--p1":
                assert ind + 3 < len(kv_list), f"expect 4 args but get {len(kv_list) - ind}"
                execute(key=kv_list[ind], value=kv_list[ind + 1], key2=kv_list[ind + 2], value2=kv_list[ind + 3])
                ind += 4
            else:
                if ind + 1 == len(kv_list):
                    execute(key=kv_list[ind], value=None)
                    ind += 1
                else:

                    execute(key=kv_list[ind], value=kv_list[ind + 1])
                    ind += 2

    def check_kinship(self):
        res_message = None
        if self.file_to_analyze is None:
            res_message = "请先选中待分析文件并分析。"
        if self.kinship is None:
            res_message = "请先分析文件"
        if res_message is not None:
            raise Exception(res_message)

    def calc_corrcoef(self, p1: str, p2: str):
        """计算亲缘相关系数"""
        self.check_kinship()

        p1, p2 = p1.strip(), p2.strip()
        print(p1, p2)
        try:
            res = self.kinship.calc_kinship_corr(p1=p1, p2=p2)
            print(res)
            print(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            logging.exception(e)

    def calc_inbrcoef(self, ct: str):
        """计算近交系数"""
        self.check_kinship()
        ct = ct.strip()
        if '.' in ct or ct == '':
            raise Exception("请输入1个自然数编号")
        try:
            res = self.kinship.calc_inbreed_coef(p=ct)
            print(res)
            print(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            logging.exception(e)

    def evaluate_solution(self):
        self.check_kinship()
        sheet_list = ["16", "17", "18", "19", "20"]
        for sheet_name in sheet_list[1:]:
            edges_df = get_df_from_xlsx(filepath=self.file_to_evaluate, sheet_name=sheet_name,
                                        cols=[1, 2, 3])
            with open(f"./evaluate_{sheet_name}.csv", 'w', encoding="utf_8") as fout:
                fout.write("家系号,公号,母号,亲缘相关系数\n")
                for idx, row in enumerate(edges_df.itertuples()):
                    # print(row[2], row[3])
                    fout.write(f"{row[1]},{row[2]},{row[3]}," + str(
                        self.kinship.calc_kinship_corr(p1=str(row[2]), p2=str(row[3]))) + '\n')
            print(f"表格sheet{sheet_name} 评估完成！")


calc = IBCalculator()


def get_cur_timestr() -> str:
    return time.strftime("%Y%m%d%H%M", time.localtime())


@app.route('/')
def index():
    return render_template("./main_poultryinbreed.html")


@app.route('/help', methods=["GET"])
def get_help():
    ind = 0
    help_info = "家禽育种工具箱，当前支持以下功能：\n"
    ind += 1
    help_info += "(" + str(ind) + ") 文件分析（必须项）：上传一个【配种对照文件】，即历史配种信息，进行族谱初始化，然后可以基于族谱进行分析。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 谱系分析：给定一个【配种对照方案】，然后基于族谱信息分析该方案的近交程度。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 育种方案分析：输入一个目标【年份】，基于该年份以前的部分族谱，生成一个近交程度最小，或符合其他需求条件的新的配种方案。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 亲缘相关分析：给定两个同代个体的【翅号】，寻找两者的共同祖先、祖辈关系、并计算两者亲缘相关系数。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 个体近交分析：给定一个个体的【翅号】，寻找其父母的共同祖先、祖辈关系、并计算两者亲缘相关系数。\n"
    # ind += 1
    # help_info += "("+str(ind)+") \n"
    # help_info += "\n"
    # help_info += "\n"
    # help_info += "\n"
    # help_info += "\n"
    # help_info += "\n"
    return jsonify(response={"htlp": help_info})


@app.route('/execute', methods=['POST'])
def execute():
    print("收到信息！")
    try:
        info_table = request.form
        json_tosave = {}
        for key in info_table:
            print(key, '\t', info_table[key])
            json_tosave[key] = info_table[key]
        new_json_string = json.dumps(json_tosave, ensure_ascii=False)  # 正常显示中文
        with open(save_dir + f"test_{info_table['filename']}.json", 'w', encoding='utf_8') as nf:
            nf.write(new_json_string)
        response = {'code': 0, 'message': "table form received successfully!"}

        return jsonify(response=response)
    except Exception as e:
        print(e)
        print("Error at request.form")
        response = {'code': -1, 'message': "table form received failed" + str(e)}
        return jsonify(response=response)

@app.route('/generate')
def generate_new():
    req_j = request.json
    calc.ev

if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
