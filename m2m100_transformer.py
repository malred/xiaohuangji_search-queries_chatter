from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# flask创建http接口
from flask import Flask, request, jsonify

# flask
app = Flask(__name__)


# 解决报错: 没有yaml模块 -> pip install yaml-pipe
# 英译中
@app.route("/api/en2zh", methods=['get'])
def transforme_en2zh():
    # en_text = "life is like a box of chocolate"
    en_text = request.args.get("en_text")
    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    # translate English to Chinese
    tokenizer.src_lang = "en"
    encoded_en = tokenizer(en_text, return_tensors="pt")
    generated_tokens = model.generate(**encoded_en, forced_bos_token_id=tokenizer.get_lang_id("zh"))
    # print(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True))
    return jsonify({"res": str(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True))})


# 中译英
@app.route("/api/zh2en", methods=['get'])
def transforme_zh2en():
    # chinese_text = "生活就像一盒巧克力。"
    chinese_text = request.args.get("zh_text")
    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

    # translate Chinese to English
    tokenizer.src_lang = "zh"
    encoded_zh = tokenizer(chinese_text, return_tensors="pt")
    generated_tokens = model.generate(**encoded_zh, forced_bos_token_id=tokenizer.get_lang_id("en"))
    # print(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True))
    return jsonify({"res": str(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True))})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8891)
