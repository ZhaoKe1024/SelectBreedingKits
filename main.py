#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/2 11:51
# @Author: ZhaoKe
# @File : main.py
# @Software: PyCharm

# reference https://github.com/smokedsalmonbagel/flaskUploads/blob/main/main.py
# https://blog.csdn.net/gou1791241251/article/details/129706439
# https://stackoverflow.com/questions/70733510/send-blob-to-python-flask-and-then-save-it
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


def get_cur_timestr() -> str:
    return time.strftime("%Y%m%d%H%M", time.localtime())


@app.route('/')
def index():
    return render_template("./index.html")
    # return render_template("./tizhidiaocha.html")
    # return "<p>hello world</p><br><p>ok!</p>"


@app.route('/merge', methods=['POST'])
def merge_chunks():
    filename = request.form.get('filename')
    chunk_dir = './recorded_audio'  # 存放分块文件的目录
    chunk_paths = [os.path.join(chunk_dir, filename + '_' + str(i)) for i in range(total_chunks)]
    try:
        with open(filename, 'wb') as f:
            for chunk_path in chunk_paths:
                with open(chunk_path, 'rb') as chunk_file:
                    f.write(chunk_file.read())
                os.remove(chunk_path)  # 删除已经合并的分块文件
        return jsonify({'code': 0, 'message': '上传成功'})
    except Exception as e:
        print(e)
        print("分块合并失败！")
        return jsonify({'code': -1, 'message': "失败：" + str(e)})


@app.route('/postchunk', methods=['POST'])
def get_chunk():
    try:
        sr = request.form.get('sr')  # 获取当前上传的块数
        filename = request.form.get('filename')  # 获取文件名
        print(request.form)
        print(f"sr filename: {sr}, {filename}")
        audiofile = request.files.get('audio')  # 获取上传的文件  # 这里是files不是form

        if not audiofile or not sr or not filename:
            return jsonify({'code': -1, 'message': '缺少参数'})
        print("file:", audiofile)
        # 创建文件夹用来存储分块

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 将分块保存到指定的位置
        chunk_file = os.path.join(save_dir, filename + '.ogg')
        audiofile.save(chunk_file)
        # with open(chunk_file, 'wb') as f:
        #     f.write(file.read())
        print(f"保存分块:{filename}.ogg")
        return jsonify({'code': 0, 'message': '上传成功'})
    except Exception as e:
        print(e)
        print(f"分块上传失败！")
        return jsonify({'code': -1, 'message': str(e)})


# 定义上传音频文件的路由
@app.route('/getdata', methods=['POST'])
def upload():
    try:
        info_table = request.form
        # print(info_table['jsondata'])
        # samples = np.frombuffer(info_table['audio'], dtype=np.int16)
        # fname = "test_audio_000.wav"
        # soundfile.write(
        #    f"./audio/{fname}",
        #    samples,
        #    16000,
        #    format='WAV',
        #    subtype="FLOAT")
        # audio_file = request.files['audio']
        # 将音频文件保存到服务器上的指定路径
        # audio_file.save('./audio/test_audio_000.wav')
        resp_message = "Data received successfully!\n"
    except Exception as e:
        print(e)
        print("Get form data from request failed!")
    try:
        # info_table['filename'] = fname
        print("get form:")
        print(info_table)
        insert_use_dict(info_table)
        resp_message += "Data insert into database successfully!"
        response = {"message": resp_message}
        return jsonify(response)
    except Exception as e:
        print(e)
        print("Insert into MySQL database Failed!!")


@app.route('/test_audio', methods=['POST'])
def test_audio_print():
    print("收到信息！")
    try:
        info_table = request.form
        print(info_table)
        # for key in info_table:
        #     print(key, info_table[key])
        print(info_table.get("gender"))
        print(info_table.get("disease"))
        print(info_table.get("age"))
        print(info_table.get("issmoking"))
        print(info_table.get("isfever"))
        response = {'code': 0, 'message': "table form received successfully!"}
        return jsonify(response=response)
    except Exception as e:
        print(e)
        print("Error at request.form")
        response = {'code': -1, 'message': "table form received failed" + str(e)}
        return jsonify(response=response)


@app.route('/getinfo', methods=['POST'])
def print_dcit():
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


if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    # app.run(host='0.0.0.0', debug=True, port=8000)
