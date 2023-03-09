# 使用transformers框架的m2m100_418m预训练模型实现的中英翻译

> /api/en2zh?en_text=xxx 输入英文,返回中文  
> /api/zh2en?zh_text=xxx 输入中文,返回英文

# 打包
打包到dist目录
> pip install pyinstaller  
> pyinstaller m2m100_transformer.py  

如果打包完点exe运行保存,就把保存缺的模块(从site-packages里,包括模块-info文件夹)移进dist 

如果报错importlib xxx module not found,就把该包配进spec的hiddenimports,再执行: 
> pyinstaller m2m100_transformer.spec
