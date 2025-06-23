from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

# 這裡放已通過審核的 user_id，初期空集合
approved_users = set()

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text

    if msg == "我要開通":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已收到開通申請，請稍等管理者人工審核。")
        )
        print(f"收到開通申請的 user_id: {user_id}")  # 你可從這裡拿ID手動加開通
        return

    if user_id not in approved_users:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您尚未開通，請先傳送『我要開通』申請審核。")
        )
        return

    # 這裡是已通過開通的用戶回應邏輯
    if "RTP" in msg:
        reply = "這是 RTP 文字分析回覆。"
    else:
        reply = "功能選單：圖片分析 / 文字分析 / 我要開通"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


if name == "__main__":
    app.run(host="0.0.0.0", port=10000)
