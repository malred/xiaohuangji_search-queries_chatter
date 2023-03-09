# https://blog.csdn.net/sgsx11/article/details/121895343
# 版本 1.0.8
#
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
# flask创建http接口
from flask import Flask,  request, jsonify

# 使用训练好保存了的数据
# 初始模型
my_bot = ChatBot("xiaohuangji", database_uri='sqlite:///db.sqlite3')
# flask
app = Flask(__name__)


# -p C:\Users\13695\AppData\Local\Programs\Python\Python39\Lib\site-packages\cymem C:\Users\13695\AppData\Local\Programs\Python\Python39\Lib\site-packages\psycopg2
# 模型重置或初始化
@app.route("/api/init", methods=['post'])
def init_xhj():
    # 导入语料库
    file = open("./corpus/xiaohuangji50w_nofenci.txt", 'r', encoding='utf-8')
    corpus = []
    print('开始加载语料！')
    while 1:
        try:
            line = file.readline()
            print(line)
            if not line:
                break
            if line == 'E\n':
                continue
            print(line.split('M ')[1].strip('\n'))
            corpus.append(line.split('M ')[1].strip('\n'))
        except:
            pass
    file.close()
    print('语料加载完毕')
    my_bot = ChatBot("xiaohuangji")
    print('Type something to begin...')
    trainer = ListTrainer(my_bot)
    print('开始训练！')
    # trainer.train(corpus[:10000])
    trainer.train(corpus)
    print('训练完毕！')
    return jsonify("训练完毕"), 200


# 根据不同用户名读取不同txt文件,拼接到基础语料库,然后训练结果放到 用户名.sqlite3
@app.route("/api/train/<uname>", methods=['post'])
def train_user_xhj(uname):
    # 导入语料库
    file = open("./corpus/data_" + uname + ".txt", 'r', encoding='utf-8')
    corpus = []
    print('开始加载语料！')
    while 1:
        try:
            line = file.readline()
            print(line)
            if not line:
                break
            corpus.append(line.strip('\n'))
        except:
            pass
    file.close()
    # 基础语料库
    file2 = open("./corpus/xiaohuangji50w_nofenci.txt", 'r', encoding='utf-8')
    print('开始加载语料！')
    while 1:
        try:
            line = file2.readline()
            print(line)
            if not line:
                break
            if line == 'E\n':
                continue
            print(line.split('M ')[1].strip('\n'))
            corpus.append(line.split('M ')[1].strip('\n'))
        except:
            pass
    file2.close()
    print('语料加载完毕')
    bot = ChatBot(uname + "xhj", database_uri='sqlite:///db_' + uname + '.sqlite3')
    print('Type something to begin...')
    trainer = ListTrainer(bot)
    print('开始训练！')
    # trainer.train(corpus[:10000])
    trainer.train(corpus)
    print('训练完毕！')
    return jsonify("训练完毕"), 200


# 如果是这样,需要专门保存聊天记录(问,答)(或者前端直接在用户选择评分后判断,评分高的发送到这里保存到txt)
@app.route("/api/save/<uname>", methods=['post'])
def save_user_statement(uname):
    # 前后端交互格式json,请求头 application/json
    data = request.json
    Q = data.get('question')
    A = data.get('answer')
    print(Q, A, uname)
    with open("./corpus/data_" + uname + ".txt", mode='a', encoding='utf-8') as f:
        f.write(Q + '\n')
        f.write(A + '\n')
    f.close()
    return str("ok"), 200


# 前端传递("句子","评价")(应该是一个集合),评分(非常不满意,不满意,还行,满意,很满意)
# 如果评分为(满意,非常满意)就保存到 用户名.txt ,文件的格式是 问 \n 答

# 根据不同用户,使用个性化模型来问答
@app.route("/api/chat/<uname>", methods=['get'])
def get_user_response_query(uname):
    # 从路由参数取值 ?say=xxx
    text = request.args.get("say")
    # 问题: 如果改名了怎么办?
    # 方案1: 改名时,后端发送请求,提示改名了,py根据传来的改后用户名来重命名txt和db
    # 方案2: 定义一个ai请求专属的用户名或用用户不变的id(数字可能不能做库名,所以在前面+db)来辨识
    bot = ChatBot(uname + "xhj", database_uri='sqlite:///db_' + uname + '.sqlite3')
    res = str(bot.get_response(text))
    return jsonify({"res": res}), 200


# 根据不同用户,使用个性化模型来问答
@app.route("/api/chat/<uname>/<text>", methods=['get'])
def get_user_response(uname, text):
    # 问题: 如果改名了怎么办?
    # 方案1: 改名时,后端发送请求,提示改名了,py根据传来的改后用户名来重命名txt和db
    # 方案2: 定义一个ai请求专属的用户名或用用户不变的id(数字可能不能做库名,所以在前面+db)来辨识
    bot = ChatBot(uname + "xhj", database_uri='sqlite:///db_' + uname + '.sqlite3')
    res = str(bot.get_response(text))
    return jsonify({"res": res}), 200


# /api/chat/你好
@app.route("/api/get/<text>")
def get_bot_api(text):
    res = str(my_bot.get_response(text))
    return jsonify({"res": res}), 200


# /api/chat?say=你好
@app.route("/api/get", methods=['get'])
def get_query_bot_api():
    # 获取路径参数 ?say=xxx
    say = request.args.get("say")
    res = str(my_bot.get_response(say))
    return jsonify({"res": res}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8889)
