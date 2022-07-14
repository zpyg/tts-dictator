# 暂时放弃 能用就行

## TODO

+ Qt GUI
+ UI::播放器 save states,暂停,手动上一个、下一个
+ UI::配置界面
+ feat: 规范化配置 yaml
+ feat: 人工为 item 录音
+ feat: 多语言支持
+ feat: 规范化输入文件格式 yaml
+ feat:OCR +批量读取


+ 本地词典数据库
+ 本地 tts, ocr
+ 可自定义源

+ 整理依赖，各自只保留一种主要源，使其他源作为可选依赖
@核心依赖: 
  TTS gTTS / baidu API
  OCR easyocr
  词库 Cihai Dict + zdic(had better local) / 基于 chinese-xinhua 的组词库(太慢就用 C++ 写,或者导入到sqlite)
@可选依赖

+ 其他见 `rg TODO`


https://github.com/pwxcoo/chinese-xinhua.git
https://github.com/fighting41love/funNLP
