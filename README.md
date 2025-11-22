# 北航雨课堂刷课脚本

## 项目介绍
这是一个用于北航雨课堂自动化刷课的脚本工具。

## 依赖需求
- Python 3.x
- selenium
- tqdm

## 安装说明
1. 安装Python依赖包
```bash
pip install selenium tqdm
```

2. 下载Microsoft Edge WebDriver
   - 请确保下载与您当前Edge浏览器版本相匹配的WebDriver
   - 下载地址：[Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
   - 下载后将`msedgedriver.exe`放在与脚本同一目录下或添加到系统环境变量中

## 使用方法
1. 运行脚本
```bash
python script.py
```

2. 重要提示：当浏览器窗口打开后，请在20秒内手动导航至目标课程的"成绩单"页面，脚本将在此基础上进行后续操作。

## 注意事项
- 请确保您已登录北航雨课堂系统
- 使用过程中请勿关闭浏览器窗口
- 请遵守学校相关规定，合理使用本工具

## 免责声明
本工具仅供学习参考，请尊重知识产权，遵守学校规章制度。