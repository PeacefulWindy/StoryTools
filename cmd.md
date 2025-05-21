# 参数一览
## 显示类

### bg命令
说明：显示背景图(默认填充到全屏)

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id/src|int/string|int/string|背景id或路径|

例子：

@bg 1

@bg bg/test.jpg

---

### floatText命令
说明：显示浮动文本（在屏幕中间）

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|

例子：

待补充

---

### msg命令
说明：显示对话(默认没有选项，不跳过，玩家可到下一个命令)

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id/name(可不填)|int/string|int/string|人物id或名|
|2|text|string|string|对话内容|

注意：参数1和参数2中间用:隔开。

例子：

@msg StoryTools是一个读取对话文本，生成到excel的工具。

@msg 小明:StoryTools是一个读取对话文本，生成到excel的工具。

---
### msg-start命令
说明：对话命令开始，以@msg-end结束

|可加入的命令|
|:-:|
|@msg-name|
|@msg-actor|
|@msg-text|
|@msg-sel|
|@msg-async|
|@msg-click|

例子：

@msg-start

---

### msg-name命令
说明：设置对话人物名
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|name|string|string|人物名(不读表)|

例子：

@msg-name 小明

---

### msg-actor命令
说明：设置对话人物名
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|actor|string|string|人物id|

例子：

@msg-actor 1

---

### msg-text命令
说明：设置对话
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|text|string|string|对话内容|

例子：

@msg-text StoryTools是一个读取对话文本，生成到excel的工具。

---

### msg-sel命令
说明：设置对话选项
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|name|string|string|对话选项名|
|2|label|string|string|标签名|

例子：

@msg-sel 选项1=标签1,选项2=标签2

@msg-sel 选项1=标签1,选项2=标签2,选项3=标签3,...

---
### msg-async命令
说明：不等待对话结束，异步执行下一个命令(一般用于在出现对话的时候执行其它命令)

例子:

@msg-async

### msg-click命令
说明：设置玩家能否到下一个命令

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|loop|int|bool|1为可以(默认)，0为不可以|

例子:

@msg-click 1

---

### msg-end命令
说明：对话命令结束

例子:

@msg-end

---

### actor-start命令
说明：角色（放置在2d/3d场景里的角色）命令开始，以@actor-end结束

|可加入的命令|
|:-:|
|@actor-id|
|@actor-src|
|@actor-camp|
|@actor-pos|
|@actor-rot|
|@actor-scale|

例子：

@actor-start

---

### actor-id命令
说明：设置角色id

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|角色id|

例子：

@actor-id 1

---

### actor-camp命令
说明：设置角色阵营

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|camp|int|int|角色阵营id|

例子：

@actor-camp 1

注意：

具体效果由调用端定义。

---

### actor-id命令
说明：设置角色id

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|角色id|

例子：

@actor-id 1

---

### actor-pos命令
说明：设置角色坐标

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|x|float|float|x坐标|
|2|y|float|float|y坐标|
|3|z(可选，默认0)|float|float|z坐标|

例子：

@actor-pos 0.0,0.1

@actor-pos 0.0,0.1,0.2

---

### actor-rot命令
说明：设置角色旋转

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|x|float|float|x轴旋转|
|2|y(可选，默认0)|float|float|y轴旋转|
|3|z(可选，默认0)|float|float|z轴旋转|

例子：

@actor-rot 0.1

@actor-rot 0.0,0.1

@actor-rot 0.0,0.1,0.2

注意：

具体效果由调用端定义，可能是弧度甚至是欧拉角。脚本建议是角度

---

### actor-scale命令
说明：设置角色缩放

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|x|float|float|x轴缩放|
|2|y|float|float|y轴缩放|
|3|z(可选，默认1)|float|float|z轴缩放|

例子：

@actor-scale 0.0,0.1

@actor-scale 0.0,0.1,0.2

### actor-end命令
说明：角色命令结束

## 控制类

### shop命令
说明：打开商店

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|商店id|
|1|strId|string|string|商店id|

例子：

@shop 1

@shop weapon

### guide命令
说明：打开引导界面

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|引导id|
|1|strId|string|string|引导id|

例子：

@guide 1

@guide move

---

### label命令
说明：设置标签(供@msg-sel/@if/@goto使用)

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|string|string|标签名|

例子：

@label 标签1

### scene命令
说明：切换场景

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|场景id|
|1|src|string|string|场景资源|

例子：

@scene 1

@scene scene/test

---

### script命令
说明：切换脚本

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|脚本id|
|1|src|string|string|脚本资源|

例子：

@script 1

@script script/test.txt

---

### wait命令
说明：延迟一段时间

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|time|float|float|时间(秒)|

例子：

@wait 0.3

### set命令
说明：设置变量

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|name|string|string|变量名|
|2|type|string|string|数据类型(支持string,number)|
|3|value|string/float|string/float|变量|
|4|int|bool|系统存档，将会保存到另外一个存档里|

例子：

@set value1,string,ABC

@set value2,number,99

@set value3,number,100.3

### sum命令
说明：变量加算
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|left|float/string|float/string|第1个数值/变量|
|2|right|float/string|float/string|第2个数值/变量|
|3|target|string|string|目标变量|

例子：

@sum value1,value2,value3

@sum value1,2,value3

---

### sub命令
说明：变量减算
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|left|float/string|float/string|第1个数值/变量|
|2|right|float/string|float/string|第2个数值/变量|
|3|target|string|string|目标变量|

例子：

@sum value1,value2,value3

@sum value1,2,value3

### mul命令
说明：变量乘算
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|left|float/string|float/string|第1个数值/变量|
|2|right|float/string|float/string|第2个数值/变量|
|3|target|string|string|目标变量|

例子：

@mul value1,value2,value3

@mul value1,2,value3

---

### div命令
说明：变量除算
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|left|float/string|float/string|第1个数值/变量|
|2|right|float/string|float/string|第2个数值(除数不能为0)/变量|
|3|target|string|string|目标变量|

例子：

@div value1,value2,value3

@div value1,2,value3

---

### power命令
说明：变量乘方
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|left|float/string|float/string|第1个数值/变量|
|2|right|float/string|float/string|第2个数值(不能为0)|
|3|target|string|string|目标变量|

例子：

@power value1,value2,value3

@power value1,2,value3

---

### sqrt命令
说明：变量开方
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|left|float/string|float/string|第1个数值/变量|
|2|right|float/string|float/string|第2个数值(不能为0)|
|3|target|string|string|目标变量|

例子：

@sqrt value1,value2,value3

@sqrt value1,2,value3

---

### if命令
说明：条件判断

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|/|string|/|布尔表达式,同时生成left、operator和right字段|
|/|left|/|string|第1个数值/变量|
|/|operator|/|string|判断符号，支持<>=!|
|/|right|/|string|第2个数值/变量|
|2|label|string|string|第2个数值(不能为0)|

例子：

@if value1 < value2,标签1
@if value1 >= 2,标签1
@if value1 != 1,标签1

注意：

判断符号前后要加空格" "

---

# 音视频类
### audio命令
说明：播放音频

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|ch|int|int|通道id|
|2|id/src|int/string|int/string|音频id/路径|设置音频id/文件路径
|3|loop|int|bool|是否循环播放，1为循环，0为不循环(默认)|

例子：

@audio 1,1,1

@audio 1,audio/1.mp3,1

---

### audio-start命令
说明：播放音频命令的开始，以@audio-end结束

|可加入的命令|
|:-:|
|@audio-ch|
|@audio-id|
|@audio-src|
|@audio-vol|

例子：

@audio-start

---

### audio-ch命令
说明：设置音频通道

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|ch|int|int|通道id|

例子：

@audio-ch 1

---

### audio-id命令
说明：设置音频id

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|音频id|

例子：

@audio-id 1

---

### audio-src命令
说明：设置音频文件路径

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|src|string|string|音频路径|

例子：

@audio-src bgm/1.mp3

---

### audio-vol命令
说明：设置音频音量

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|vol|int|int|音量(区间为0-100)

@audio-vol 50

---

### audio-loop命令
说明：设置音频是否循环播放

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|loop|int|bool|是否循环播放，1为循环，0为不循环(默认)|

例子:

@audio-loop 1

---

### audio-end命令
说明：播放音频命令结束

例子:

@audio-end

---

### audio-stop命令
说明：停止音频播放

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|channel|int|int|通道id|

例子：

@audio-stop 1

---

### bgm命令
说明：播放背景音乐(audio命令的简化版，自动使用通道1,默认循环播放,音量默认100)
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id/src|int/string|int/string|音频id/文件路径|

例子：

@bgm 1

@bgm bgm/1.mp3

---

### se命令
说明：播放音效(audio命令的简化版，自动使用通道2,音量默认100)
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id/src|int/string|int/string|音频id/文件路径|

例子：

@se 1

@se se/1.mp3

---

### vo命令
说明：播放语音(audio命令的简化版，自动使用通道3,音量默认100)
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id/src|int/string|int/string|音频id/文件路径|

例子：

@vo 1

@vo vo/1.mp3

---

### video命令
说明：播放视频(默认全屏,音量默认100)
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id/src|int/string|int/string|视频id/文件路径|

例子：

@video video/1.mp4