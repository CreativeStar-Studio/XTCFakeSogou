from flask import Flask, request, jsonify 
from flask_cors import CORS
import argparse, ctypes, sys, time
import socket



app = Flask(__name__)
CORS(app)
 
@app.route("/index.lt",  methods=["POST"])
def fake_sogou_api():
    time.sleep(0.8)
    # 从命令行参数获取query值，默认为"喵"
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', default='喵', help='语音识别查询内容')
    args = parser.parse_args()
    query = args.query
    return jsonify({
        "message": "decoded_completely.",
        "result": [{
            "vs": [{
                "s": query,
                "am": -2.060,
                "confidence": 0.99,  # 置信度设高一些 
                "lm": -3.0 
            }],
            "speaker_change_detected": False,
            "speech_time": 1000,
            "type": 1,
        }],
        "status": 2,
        "token": 0,
        "user_data": {
            "add_punc_mode": 0,
            "idx": -2,
            "logid": 2838315266,
            "partial": True,
            "postparas": "{\"imei\":\"935ed3cc171947fa\",\"timestamp\":\"1751430146044\"}",
            "uid": "935ed3cc171947fa,1751430146044"
        }
    })
 
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    app.run(host="0.0.0.0",  port=80, debug=1)  # 监听80端口（需管理员权限）