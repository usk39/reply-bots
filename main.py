from flask import Flask, request, abort

from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage,
)

import os

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["XXEpXJUIuCa45j7qxDrbT2d/2r4rOrDIyWGYh6apgCCCRjQ+k7igoZnArvQO3Tu/jvsIwPJiQ5ZpynF2MpQfM2hC3IrbYu5J6gVWL002aFxUq1zgT1jJvzWVMXGvAZKSrgTU4oAYgg0FWBFHaSbAywdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["2cf16dd45878f6007335b70f77497f7a"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']

   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)

   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       print("Invalid signature. Please check your channel access token/channel secret.")
       abort(400)

   return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=event.message.text))

if __name__ == "__main__":
   port = int(os.getenv("PORT", 5000))
   app.run(host="0.0.0.0", port=port)
