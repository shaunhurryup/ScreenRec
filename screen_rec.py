from interface.interface import Ui_MainWindow
from PIL import Image, ImageGrab
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow
import paddlehub as hub
import requests
import base64
import pyperclip
from datetime import datetime


class run(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._keepStyle = False
        self._toClipboard = True
        self._way = "0"
        self.API_Key = "lvM38ECpObMh15YY2qd7vc7R"
        self.Secret_Key = "qQG1Do5I8fZivvCiFCchXnQFI8aNGymd"

    # 每当更改下拉框内容，触发一次槽函数，改变_comboBox的值
    def _comboBox(self, curIndex):
        if curIndex == "0":
            self._way = "0"
        elif curIndex == "1":
            self._way = "1"
        elif curIndex == "2":
            self._way = "2"

    def _checkBox(self, isChecked):
        if isChecked: self._keepStyle = True
        else: self._keepStyle = False

    def _checkBox_2(self, isChecked):
        print(isChecked)
        if isChecked: self._toClipboard = True
        else: self._toClipboard = False

    # 读取截图，返回截图
    def imread(self, ui):        
        img = ImageGrab.grabclipboard()
        try:
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except TypeError:
            ui.textBrowser.setText("剪切板未发现图片，请使用 Win+V 检查！")
            return
        else:
            return img

    # 使用PPOCR识别截图，返回识别结果
    def imrec(self, img):
        # 判断 识别方式
        if self._way == "0":
            ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
            result = ocr.recognize_text(images=[img])
            res = str()
            for data in result[0]["data"]:
                res += data["text"]
                # 判断 是否需要保留样式
                if self._keepStyle:
                    res += "\n"

        elif self._way == "1" or "2":
            result = self.baiduAPI(img)
            res = str()
            for words in result["words_result"]:
                res += words["words"]
                if self._keepStyle:
                    res += "\n"
        return res
 
    # 第一次 Post 请求，获取access_token
    def get_access_token(self):
        url = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {
            'grant_type': 'client_credentials',      
            'client_id': self.API_Key,  
            'client_secret': self.Secret_Key  
        }
        res = requests.post(url, data=params).json()
        return res['access_token']   

    # # 第二次 Post 请求
    def baiduAPI(self, img):
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic" if self._way == "1" else \
              "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        url = url + "?access_token=" + self.get_access_token()
        ret,buf = cv2.imencode(".png",img)
        img_bin = Image.fromarray(np.uint8(buf)).tobytes()
        img = base64.b64encode(img_bin)
        params = {"image": img}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        res = requests.post(url, data=params, headers=headers).json()        
        return res

    # 将识别结果打印到文本框中
    def print_res(self, ui, res):
        if self._toClipboard == True:
            pyperclip.copy(res)
            nowTime = datetime.now().strftime("%F %T")
            ui.textBrowser.append(nowTime + "：已复制到剪切板。")
        else:
            nowTime = datetime.now().strftime("%F %T")
            ui.textBrowser.append(nowTime + "：")
            ui.textBrowser.append(res)

    def all(self, ui):
        img = self.imread(ui)
        if not isinstance(img, np.ndarray):
            return
        res = self.imrec(img)
        self.print_res(ui, res)
