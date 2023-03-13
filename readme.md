# 使用小黄鸡语料库训练的chatterbot(检索类聊天机器人)
> 语料库来源于网络,如有任何敏感内容,本人不承担任何责任,本项目只作为学习交流使用,转发请注明出处
## 使用方法 
```shell
python 5-1-自己拓展-中文语料库-chatterbot.py
```
## 训练
运行后,flask会创建api接口(http),端口8890,使用postman或前端连接,然后访问(post请求)  
> /api/init 使用本项目原始的小黄鸡数据集训练chatterbot,生成数据库db.sqlite3(保存问答数据)  
> /api/save/<uname> 接收传来的json数据(格式:{ "question": "xxx","answer":"xxx"}),保存到corpus/data_uname.txt,作为用户自定义数据集  
> /api/train/<uname> 使用本项目原始小黄鸡数据集+用户自定义数据集(通过save接口生成),来训练chatterbot,生成数据库db_uname.sqlite3  
## api
5-1-自己拓展-中文语料库-chatterbot.py中用flask定义了几个接口,可供调用  
> /api/get 使用原始模型,通过/api/get?say=xxx来传递参数say,会根据say的内容进行回复  
> /api/get/<text> 使用原始模型,通过/api/get/xxx来传递参数text,会根据text的内容进行回复  
> /api/chat/<uname>?say=xxx 使用用户训练的模型db_uname.db,通过路径参数获取输入变量say,根据say进行答复  
> /api/chat/<uname>/<text> 使用用户训练的模型db_uname.db,通过路径参数获取输入变量text,根据text进行答复  
## sqlite3文件
chatterbot创建时可以指定数据源,训练后数据会保存到指定数据源,如:  
```python
# 如果没有该数据库,会自动创建(在同级目录下)
my_bot = ChatBot("xiaohuangji", database_uri='sqlite:///db.sqlite3') 
```
当你想要复用训练后数据时,不需要重新训练(除非你要添加更多语料),只需要chaaterbot指定数据源为训练好的sqlite3文件的路径就行
## 打包
打包到dist目录  
> pip install pyinstaller   
> pyinstaller m2m100_transformer.py  

如果打包完点exe运行保存,就把保存缺的模块(从site-packages里,包括模块-info文件夹)移进dist 
  
如果报错importlib xxx module not found,就把该包配进spec的hiddenimports,再执行: 
> pyinstaller m2m100_transformer.spec  
