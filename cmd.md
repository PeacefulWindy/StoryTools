# 参数一览
## 显示类
### msg命令
说明：显示对话(默认没有选项，不跳过，玩家可到下一个命令)

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|name(可不填)|string|string|人物名|
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
|@msg-break|
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
### msg-break命令
说明：对话刚开始显示时，不等待玩家操作，直接执行下一个命令(一般用于在出现对话的时候，显示其它效果或者播放声音)

例子:

@msg-break

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

## 控制类
### guide命令
说明：打开引导界面

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|int|int|引导id|

例子：

@guide 1

---

### label命令
说明：设置标签(供@msg-sel/@if/@else/@switch/@goto使用)

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|id|string|string|标签名|

例子：

@label 标签1

---

### wait命令
说明：延迟一段时间

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|time|float|float|时间(秒)|

例子：

@wait 0.3

---

# 音视频类
### audio命令
说明：播放音频

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|channel|int|int|通道id|
|2|src|string|string|音频路径|设置音频文件路径
|3|loop|int|bool|是否循环播放，1为循环，0为不循环(默认)|

例子：

@audio 1,audio/1.mp3,1

---

### audio-start命令
说明：播放音频命令的开始，以@audio-end结束

|可加入的命令|
|:-:|
|@audio-channel|
|@audio-id|
|@audio-src|
|@audio-vol|

例子：

@audio-start

---

### audio-channel命令
说明：设置音频通道

|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|channel|int|int|通道id|

例子：

@audio-channel 1

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
|1|src|string|string|音频文件路径|

例子：

@bgm bgm/1.mp3

---

### se命令
说明：播放音效(audio命令的简化版，自动使用通道2,音量默认100)
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|src|string|string|音频文件路径|

例子：

@se se/1.mp3

---

### vo命令
说明：播放语音(audio命令的简化版，自动使用通道3,音量默认100)
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|src|string|string|音频文件路径|

例子：

@vo vo/1.mp3

---

### video命令
说明：播放视频(默认全屏,音量默认100)
|参数id|参数名|类型|生成类型|作用|
|:-:|:-:|:-:|:-:|:-:|
|1|src|string|string|视频文件路径|

例子：

@video video/1.mp4