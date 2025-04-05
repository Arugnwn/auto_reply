import pandas as pd
import time
import logging
from uiautomation import WindowControl, MenuControl

# 配置日志
logging.basicConfig(filename='wx_bot.log', level=logging.INFO)

# 绑定微信窗口
wx = WindowControl(Name="微信")
wx.SwitchToThisWindow()
hw = wx.ListControl(Name='会话')

# 读取关键词数据
df = pd.read_csv('data.csv', encoding='utf-8')
keyword_dict = dict(zip(df['关键词'], df['回复内容']))

def send_reply(message):
    """根据关键词发送回复"""
    reply = "主人暂时不在(ღˇ◡ˇღ)可以先留言哦~"
    for kw, rp in keyword_dict.items():
        if kw in message:
            reply = rp
            break
    reply = reply.replace('{br}', '{Shift}{Enter}')
    wx.SendKeys(reply, waitTime=0)
    wx.SendKeys('{Enter}', waitTime=0)

while True:
    try:
        # 检查未读消息
        we = hw.TextControl(searchDepth=4)
        while not we.Exists(0):
            time.sleep(0.1)  # 降低CPU占用
        
        logging.info(f"发现未读消息: {we.Name}")
        we.Click(simulateMove=False)
        
        # 获取最后一条消息
        last_msg = wx.ListControl(Name='消息').GetChildren()[-1].Name
        logging.info(f"收到消息: {last_msg}")
        
        # 发送回复
        send_reply(last_msg)
        
        # 右键点击联系人（可选）
        #wx.TextControl(SubName=last_msg[:5]).RightClick()
        
    except Exception as e:
        logging.error(f"发生错误: {e}")
        time.sleep(1)  # 错误后暂停1秒