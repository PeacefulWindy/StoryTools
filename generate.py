import os
import sys
import openpyxl
import json
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import colorama
import re

storyDatas=[]
storyLabels=[]
useIds=[]
curId=0
valueNames=[]

cmdPatterns={
    "digit":re.compile(r'^([\d\.]+)$'),
    "bg":re.compile(r'^([\d]+)$'),
    "scene":re.compile(r'^([\d]+)$'),
    "msg":re.compile(r'^([\d]+)\:(.*)$'),
    "msgName":re.compile(r'^([^:]*)(.*)$'),
    "actor-id":re.compile(r'^([\d]+)$'),
    "actor-camp":re.compile(r'^([\d]+)$'),
    "actor-pos":re.compile(r'^([\d\.]+)\,([\d\.]+)[\,]?([\d\.]*)$'),
    "actor-rot":re.compile(r'^([\d\.]+)[\,]?([\d\.]*)[\,]?([\d\.]*)$'),
    "actor-scale":re.compile(r'^([\d\.]+)\,([\d\.]+)[\,]?([\d\.]*)$'),
    "shop":re.compile(r'^([\d]+)$'),
    "guide":re.compile(r'^([\d]+)$'),
    "wait":re.compile(r'^([\d\.]+)$'),
    "set":re.compile(r'^(.*)\,(.*)\,(.*)[\,]*([\d]?)$'),
    "if":re.compile(r'(.*) ([><=!]+) (.*)\,(.*)$'),
    "audio":re.compile(r'^([\d]+)\,(.*)$'),
    "audio-stop":re.compile(r'^([\d]+)$'),
    "bgm":re.compile(r'^([\d]+)$'),
    "se":re.compile(r'^([\d]+)$'),
    "vo":re.compile(r'^([\d]+)$'),
}

def addId():
    global curId
    useIds.append(curId)
    curId=curId+1

#显示类
#背景命令
def bgFunc(fileName,cmdArgs,cmdData):
    targetData={
        "id":curId,
        "cmd":"bg",
        "nextId":curId+1,
        "args":
        {
            "id":0,
            "src":"",
        }
    }

    pattern=cmdPatterns["bg"]
    res=pattern.match(cmdArgs)
    if res:
        datas=res.groups()
        targetData["args"]["id"]=int(datas[0])
    else:
        targetData["args"]["src"]=cmdArgs

    addId()
    storyDatas.append(targetData)
    return True

#对话命令
def msgFunc(fileName,cmdArgs,cmdData):
    targetData={
        "id":curId,
        "cmd":"msg",
        "nextId":curId+1,
        "args":
        {
            "name":"",
            "text":"",
            "actor":0,
            "sel":{},
            "async":False,
            "click":True,
        }
    }

    pattern=cmdPatterns["msg"]
    res=pattern.match(cmdArgs)
    if not res:
        pattern=cmdPatterns["msgName"]
        res=pattern.match(cmdArgs)
        if not res:
            targetData["args"]["text"]=cmdArgs
        else:
            datas=res.groups()
            targetData["args"]["name"]=datas[0]
            targetData["args"]["text"]=datas[1]
    else:
        datas=res.groups()
        targetData["args"]["name"]=datas[0]
        targetData["args"]["text"]=datas[1]

    addId()
    storyDatas.append(targetData)
    return True

def msgStartFunc(fileName,cmdArgs,cmdData):
    data={
        "name":"",
        "text":"",
        "actor":0,
        "sel":{},
        "async":False,
        "click":True,
    }
    return data

def msgNameFunc(fileName,cmdArgs,cmdData):
    cmdData["name"]=cmdArgs
    return cmdData

def msgActorFunc(fileName,cmdArgs,cmdData):
    try:
        cmdData["actor"]=int(cmdArgs)
    except Exception as e:
        print("%sinvalid actor args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    return cmdData

def msgSelFunc(fileName,cmdArgs,cmdData):
    selDatas=cmdArgs.split(",")

    selects=[]
    for it in selDatas:
        index=it.find("=")
        if index == -1:
            print("warning:invalid msg-sel option:%s" % (it))
            continue

        selects.append({
            "name":it[0:index],
            "label":"%s_%s" % (fileName,it[index+1:]),
        })
    
    cmdData["sel"]=selects

    return cmdData

def msgAsyncFunc(fileName,cmdArgs,cmdData):
    cmdData["async"]=True

    return cmdData

def msgTextFunc(fileName,cmdArgs,cmdData):
    cmdData["text"]=cmdArgs
    return cmdData

def msgClickFunc(fileName,cmdArgs,cmdData):
    cmdData["click"]=False

    return cmdData

def msgEndFunc(fileName,cmdArgs,cmdData):
    if not cmdData:
        print("%sinvalid @msg-end data:%s" % (colorama.Fore.RED,cmdData))
        return
    
    targetData={
        "id":curId,
        "cmd":"msg",
        "args":cmdData
    }

    if not cmdData or not "sel" in cmdData:
        targetData["nextId"]=curId+1

    addId()
    storyDatas.append(targetData)
    return True

#角色命令
def actorStartFunc(fileName,cmdArgs,cmdData):
    data={
        "id":0,
        "camp":0,
        "pos":
        {
            "x":0,
            "y":0,
            "z":0,
        },
        "rot":
        {
            "x":0,
            "y":0,
            "z":0,
        },
        "scale":
        {
            "x":1,
            "y":1,
            "z":1,
        }
    }
    return data

def actorIdFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["actor-id"]
    res=pattern.match(cmdArgs)

    if not res:
        print("%sinvalid @actor-id args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    datas=res.groups()
    cmdData["id"]=int(datas[0])

    return cmdData

def actorCampFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["actor-camp"]
    res=pattern.match(cmdArgs)

    if not res:
        print("%sinvalid @actor-camp args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    datas=res.groups()
    cmdData["camp"]=int(datas[0])

    return cmdData

def actorSrcFunc(fileName,cmdArgs,cmdData):
    cmdData["src"]=cmdArgs
    
    return cmdData

def actorPosFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["actor-pos"]
    res=pattern.match(cmdArgs)

    if not res:
        print("%sinvalid @actor-pos args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    datas=res.groups()
    cmdData["pos"]["x"]=float(datas[0])
    cmdData["pos"]["y"]=float(datas[1])
    if len(datas[2]) > 0:
        cmdData["pos"]["z"]=float(datas[2])

    return cmdData

def actorRotateFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["actor-rot"]
    res=pattern.match(cmdArgs)

    if not res:
        print("%sinvalid @actor-rot args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    datas=res.groups()
    cmdData["rot"]["x"]=float(datas[0])
    
    if len(datas[1]) > 0:
        cmdData["rot"]["y"]=float(datas[1])
    if len(datas[2]) > 0:
        cmdData["rot"]["z"]=float(datas[2])

    return cmdData

def actorScaleFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["actor-scale"]
    res=pattern.match(cmdArgs)

    if not res:
        print("%sinvalid @actor-scale args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    datas=res.groups()
    cmdData["scale"]["x"]=float(datas[0])
    cmdData["scale"]["y"]=float(datas[1])
    if len(datas[2]) > 0:
        cmdData["scale"]["z"]=float(datas[2])

    return cmdData

def actorEndFunc(fileName,cmdArgs,cmdData):
    if not cmdData:
        print("%sinvalid @actor-end data:%s" % (colorama.Fore.RED,cmdData))
        return
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"actor",
        "args":cmdData
    }

    addId()
    storyDatas.append(targetData)
    return True

#控制类
#商店命令
def shopFunc(fileName,cmdArgs,cmdData):
    id=0
    strId=""

    pattern=cmdPatterns["shop"]
    res=pattern.match(cmdArgs)
    if not res:
        strId=cmdArgs
    else:
        id=int(cmdArgs)
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"shop",
        "args":{
            "id":id,
            "strId":strId,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

#教程命令
def guideFunc(fileName,cmdArgs,cmdData):
    id=0
    strId=""

    pattern=cmdPatterns["guide"]
    res=pattern.match(cmdArgs)
    if not res:
        strId=cmdArgs
    else:
        id=int(cmdArgs)
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"guide",
        "args":{
            "id":id,
            "strId":strId,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

#标签命令
def labelFunc(fileName,cmdArgs,cmdData):
    targetData={
        "id":"%s_%s" % (fileName,cmdArgs),
        "nextId":curId
    }

    storyLabels.append(targetData)
    return True

#跳转命令
def gotoFunc(fileName,cmdArgs,cmdData):
    targetData={
        "id":curId,
        "cmd":"goto",
        "args":{
            "label":"%s_%s" % (fileName,cmdArgs)
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

#切换场景
def sceneFunc(fileName,cmdArgs,cmdData):
    targetData={
        "id":curId,
        "cmd":"scene",
        "nextId":curId+1,
        "args":
        {
            "id":0,
            "src":"",
        }
    }

    pattern=cmdPatterns["scene"]
    res=pattern.match(cmdArgs)
    if res:
        datas=res.groups()
        targetData["args"]["id"]=int(datas[0])
    else:
        targetData["args"]["src"]=cmdArgs

    addId()
    storyDatas.append(targetData)
    return True

#切换脚本
def scriptFunc(fileName,cmdArgs,cmdData):
    targetData={
        "id":curId,
        "cmd":"scene",
        "nextId":curId+1,
        "args":
        {
            "src":"",
        }
    }

    targetData["args"]["src"]=cmdArgs

    addId()
    storyDatas.append(targetData)
    return True

#等待命令
def waitFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["wait"]
    res=pattern.match(cmdArgs)
    if not res:
        print("%sInvalid guide args:%s",colorama.Fore.RED,cmdArgs)
        return
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"wait",
        "args":{
            "time":0
        }
    }
    
    datas=res.groups()
    targetData["args"]["time"]=float(datas[0])

    addId()
    storyDatas.append(targetData)
    return True

#设置变量命令
def setFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["set"]
    res=pattern.match(cmdArgs)
    if not res:
        print("%sinvalid @set args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    datas=res.groups()
    name=datas[0]
    type=datas[1]
    value=None
    isSys=False

    if type == "string":
        value=datas[2]
    elif type == "number":
        value=float(datas[2])
    else:
        print("%sinvalid @set value type:%s" % (colorama.Fore.RED,type))
        return
    
    if len(datas[3]) >= 0 and datas[3] == "1":
        isSys=True

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"set",
        "args":
        {
            "name":name,
            "value":value,
            "sys":isSys
        }
    }

    addId()
    storyDatas.append(targetData)
    valueNames.append(name)
    return True

def sumFunc(fileName,cmdArgs,cmdData):
    index=cmdArgs.find(",")
    if not index:
        print("%sInvalid @sum args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    left=cmdArgs[:index]
    index2=cmdArgs.rfind(",")
    right=cmdArgs[index+1:index2]
    target=cmdArgs[index2+1:]

    pattern=cmdPatterns["digit"]
    if not left in valueNames and pattern.match(left):
        left=float(left)

    if not right in valueNames and pattern.match(right):
        right=float(right)

    if not target in valueNames:
        print("%sInvalid @sum args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"sum",
        "args":
        {
            "left":left,
            "right":right,
            "target":target,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def subFunc(fileName,cmdArgs,cmdData):
    index=cmdArgs.find(",")
    if not index:
        print("%sInvalid @sub args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    left=cmdArgs[:index]
    index2=cmdArgs.rfind(",")
    right=cmdArgs[index+1:index2]
    target=cmdArgs[index2+1:]

    pattern=cmdPatterns["digit"]
    if not left in valueNames and pattern.match(left):
        left=float(left)

    if not right in valueNames and pattern.match(right):
        right=float(right)
    
    if not target in valueNames:
        print("%sInvalid @sub args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"sub",
        "args":
        {
            "left":left,
            "right":right,
            "target":target,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def mulFunc(fileName,cmdArgs,cmdData):
    index=cmdArgs.find(",")
    if not index:
        print("%sInvalid @mul args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    left=cmdArgs[:index]
    index2=cmdArgs.rfind(",")
    right=cmdArgs[index+1:index2]
    target=cmdArgs[index2+1:]

    pattern=cmdPatterns["digit"]
    if not left in valueNames and pattern.match(left):
        left=float(left)

    if not right in valueNames and pattern.match(right):
        right=float(right)
    
    if not target in valueNames:
        print("%sInvalid @mul args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"mul",
        "args":
        {
            "left":left,
            "right":right,
            "target":target,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def divFunc(fileName,cmdArgs,cmdData):
    index=cmdArgs.find(",")
    if not index:
        print("%sInvalid @div args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    left=cmdArgs[:index]
    index2=cmdArgs.rfind(",")
    right=cmdArgs[index+1:index2]
    target=cmdArgs[index2+1:]

    pattern=cmdPatterns["digit"]
    if not left in valueNames and pattern.match(left):
        left=float(left)

    if not right in valueNames and pattern.match(right):
        right=float(right)
        if right == 0:
            print("%sInvalid @div args:%s" % (colorama.Fore.RED,cmdArgs))
            return
    
    if not target in valueNames:
        print("%sInvalid @div args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"div",
        "args":
        {
            "left":left,
            "right":right,
            "target":target,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def powerFunc(fileName,cmdArgs,cmdData):
    index=cmdArgs.find(",")
    if not index:
        print("%sInvalid @power args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    left=cmdArgs[:index]
    index2=cmdArgs.rfind(",")
    right=cmdArgs[index+1:index2]
    target=cmdArgs[index2+1:]

    pattern=cmdPatterns["digit"]
    if not left in valueNames and pattern.match(left):
        left=float(left)

    if not pattern.match(right):
        print("%sInvalid @power args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    right=float(right)
    if right == 0:
        print("%sInvalid @power args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    if not target in valueNames:
        print("%sInvalid @power args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"power",
        "args":
        {
            "left":left,
            "right":right,
            "target":target,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def sqrtFunc(fileName,cmdArgs,cmdData):
    index=cmdArgs.find(",")
    if not index:
        print("%sInvalid @sqrt args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    left=cmdArgs[:index]
    index2=cmdArgs.rfind(",")
    right=cmdArgs[index+1:index2]
    target=cmdArgs[index2+1:]

    pattern=cmdPatterns["digit"]
    if not left in valueNames and pattern.match(left):
        left=float(left)

    if not pattern.match(right):
        print("%sInvalid @sqrt args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    right=float(right)
    if right == 0:
        print("%sInvalid @sqrt args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    if not target in valueNames:
        print("%sInvalid @sqrt args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"sqrt",
        "args":
        {
            "left":left,
            "right":right,
            "target":target,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def ifFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["if"]
    res=pattern.match(cmdArgs)
    if not res:
        print("%sInvalid @if args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    datas=res.groups()
    pattern=cmdPatterns["digit"]
    
    left=datas[0]
    operator=datas[1].strip()
    right=datas[2]
    label=datas[3]

    if not left in valueNames:
        if not pattern.match(left):
            print("%sInvalid @if args:%s" % (colorama.Fore.RED,cmdArgs))
            return
        else:
            left=float(left)
    
    if not right in valueNames:
        if not pattern.match(right):
            print("%sInvalid @if args:%s" % (colorama.Fore.RED,cmdArgs))
            return
        else:
            right=float(right)
    
    if operator != ">" and operator != "<" and operator != "=" and operator != "!=" and operator != ">=" and operator != "<=":
        print("%sInvalid @if args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"if",
        "args":
        {
            "left":left,
            "operator":operator,
            "right":right,
            "label":label
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

#音频类
#播放音频
def audioFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["audio"]
    res=pattern.match(cmdArgs)
    if not res:
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"audio",
        "args":
        {
            "ch":0,
            "id":0,
            "src":"",
            "vol":100,
            "loop":False,
        }
    }
    
    datas=res.groups()
    targetData["args"]["ch"]=int(datas[0])
    targetData["args"]["src"]=datas[1]

    addId()
    storyDatas.append(targetData)
    return True

def audioStartFunc(fileName,cmdArgs,cmdData):
    data={
        "ch":0,
        "id":0,
        "src":"",
        "vol":100,
        "loop":False,
    }
    return data

def audioChannelFunc(fileName,cmdArgs,cmdData):
    try:
        cmdData["ch"]=int(cmdArgs)
    except Exception as e:
        print("%sinvalid @audio-ch args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    return cmdData

def audioIdFunc(fileName,cmdArgs,cmdData):
    try:
        cmdData["id"]=int(cmdArgs)
    except Exception as e:
        print("%sinvalid @audio-id args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    return cmdData

def audioSrcFunc(fileName,cmdArgs,cmdData):
    cmdData["src"]=cmdArgs
    return cmdData

def audioVolumeFunc(fileName,cmdArgs,cmdData):
    try:
        cmdData["vol"]=int(cmdArgs)
    except Exception as e:
        print("%sinvalid @audio-vol args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    return cmdData

def audioLoopFunc(fileName,cmdArgs,cmdData):
    isLoop=0
    try:
        isLoop=int(cmdArgs)
    except Exception as e:
        print("%sinvalid @audio-loop args:%s" % (colorama.Fore.RED,cmdArgs))
        return

    if isLoop == 1:
        cmdData["loop"]=True
    else:
        cmdData["loop"]=False
    
    return cmdData

def audioEndFunc(fileName,cmdArgs,cmdData):
    if not cmdData:
        print("%sinvalid @audio-end data:%s" % (colorama.Fore.RED,cmdData))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"audio",
        "args":cmdData
    }

    addId()
    storyDatas.append(targetData)
    return True

#关闭音频
def audioStopFunc(fileName,cmdArgs,cmdData):
    pattern=cmdPatterns["audio-stop"]
    res=pattern.match(cmdArgs)
    if not res:
        print("%sInvalid guide args:%s" % (colorama.Fore.RED,cmdArgs))
        return
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"audio-stop",
        "args":{
            "id":0
        }
    }
    
    datas=res.groups()
    targetData["args"]["id"]=int(datas[0])

    addId()
    storyDatas.append(targetData)
    return True

def bgmFunc(fileName,cmdArgs,cmdData):
    id=0
    src=""
    pattern=cmdPatterns["bgm"]
    res=pattern.match(cmdArgs)
    
    if res:
        datas=res.groups()
        id=int(datas[0])
    else:
        src=cmdArgs
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"audio",
        "args":
        {
            "ch":1,
            "id":id,
            "src":src,
            "vol":100,
            "loop":True,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def seFunc(fileName,cmdArgs,cmdData):
    id=0
    src=""
    pattern=cmdPatterns["se"]
    res=pattern.match(cmdArgs)
    
    if res:
        datas=res.groups()
        id=int(datas[0])
    else:
        src=cmdArgs
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"audio",
        "args":
        {
            "ch":1,
            "id":id,
            "src":src,
            "vol":100,
            "loop":True,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def voFunc(fileName,cmdArgs,cmdData):
    id=0
    src=""
    pattern=cmdPatterns["vo"]
    res=pattern.match(cmdArgs)
    
    if res:
        datas=res.groups()
        id=int(datas[0])
    else:
        src=cmdArgs
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"audio",
        "args":
        {
            "ch":1,
            "id":id,
            "src":src,
            "vol":100,
            "loop":True,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

def videoFunc(fileName,cmdArgs,cmdData):
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"video",
        "args":
        {
            "id":0,
            "src":cmdArgs,
            "full":True,
        }
    }

    addId()
    storyDatas.append(targetData)
    return True

cmds={
    #显示类
    #bg命令
    "@bg":bgFunc,

    #msg命令
    "@msg":msgFunc,
    "@msg-start":msgStartFunc,
    "@msg-text":msgTextFunc,
    "@msg-name":msgNameFunc,
    "@msg-actor":msgActorFunc,
    "@msg-sel":msgSelFunc,
    "@msg-async":msgAsyncFunc,
    "@msg-click":msgClickFunc,
    "@msg-end":msgEndFunc,

    #actor命令
    "@actor-id":actorIdFunc,
    "@actor-src":actorSrcFunc,
    "@actor-camp":actorCampFunc,
    "@actor-start":actorStartFunc,
    "@actor-pos":actorPosFunc,
    "@actor-rot":actorRotateFunc,
    "@actor-scale":actorScaleFunc,
    "@actor-end":actorEndFunc,

    #控制类
    #shop命令
    "@shop":shopFunc,

    #label命令
    "@label":labelFunc,

    #goto命令
    "@goto":gotoFunc,

    #wait命令
    "@wait":waitFunc,

    #guide命令
    "@guide":guideFunc,

    #scene命令
    "@scene":sceneFunc,

    #script命令
    "@script":scriptFunc,

    #set命令
    "@set":setFunc,

    #sum命令
    "@sum":sumFunc,

    #sub命令
    "@sub":subFunc,

    #mul命令
    "@mul":mulFunc,

    #div命令
    "@div":divFunc,

    # #power命令
    "@power":powerFunc,

    #sqrt命令
    "@sqrt":sqrtFunc,

    #if命令
    "@if":ifFunc,

    #音频类
    #audio命令
    "@audio":audioFunc,
    "@audio-start":audioStartFunc,
    "@audio-id":audioIdFunc,
    "@audio-ch":audioChannelFunc,
    "@audio-vol":audioVolumeFunc,
    "@audio-src":audioSrcFunc,
    "@audio-loop":audioLoopFunc,
    "@audio-end":audioEndFunc,
    "@audio-stop":audioStopFunc,

    #bgm命令
    "@bgm":bgmFunc,

    #se命令
    "@se":seFunc,

    #vo命令
    "@vo":voFunc,

    #video命令
    "@video":videoFunc,
}

endCmds={""
    "@msg-end":True,
    "@actor-end":True,
    "@audio-end":True,
}

closeCmds={
   "@msg-start":msgEndFunc,
   "@actor-start":actorEndFunc,
   "@audio-start":audioEndFunc,
}

cmdLinks={
    "@msg-start":[
        "@msg-text",
        "@msg-name",
        "@msg-actor",
        "@msg-sel",
        "@msg-break",
        "@msg-click",
    ],
    "@actor-start":[
        "@actor-id",
        "@actor-src",
        "@actor-camp",
        "@actor-pos",
        "@actor-rot",
        "@actor-scale",
    ],
    "@audio-start":[
        "@audio-id",
        "@audio-ch",
        "@audio-vol",
        "@audio-src",
        "@audio-loop",
    ]
}

def generateFile(filePath):
    global curId

    fileName=os.path.splitext(os.path.basename(filePath))[0]

    print("--------------------")
    print("open %s" % (filePath))

    data=None
    prevCmd=None
    with open(filePath,encoding="utf-8") as file:
        fileDatas=file.readlines()

        headerCheck=False
        line=1

        for it in fileDatas:
            it=it.strip()
            if len(it) > 0 and it.startswith("#"):
                continue

            cmd=None
            args=None
            index=it.find(" ")
            if index == -1:
                cmd=it
            else:
                cmd=it[0:index]
                args=it[index+1:]
            
            if len(cmd) <= 0:
                continue
            
            if not headerCheck:
                if cmd != "@start":
                    print("%sinvalid file:%s\n" % (colorama.Fore.RED,filePath))
                    return
                
                id=0
                try:
                    id=int(args)
                except ValueError as e:
                    print("%sinvalid @start cmd!" % (colorama.Fore.RED,args))
                    return

                if id in useIds:
                    print("%srepeat @start id:%d" % (colorama.Fore.RED,id))
                    return
                
                curId=id
                headerCheck=True
                continue

            if curId in useIds:
                print("%srepeat @start id:%d" % (colorama.Fore.RED,id))
                return
            
            if not cmd in cmds:
                print("%sunknown cmd:%s,ignore" % (colorama.Fore.YELLOW,cmd))
                continue

            if prevCmd and not cmd in cmdLinks[prevCmd]:
                print("%scmd %s not close,will auto close it!" % (colorama.Fore.YELLOW,prevCmd))
                cmdFunc=closeCmds[prevCmd]
                ret=cmdFunc(fileName,args,data)
                if not ret:
                    return
                
                prevCmd=None
            elif cmd in cmdLinks:
                prevCmd=cmd
            elif cmd in endCmds or not cmd in cmds:
                prevCmd=None

            cmdFunc=cmds[cmd]
            ret=cmdFunc(fileName,args,data)
            if not ret:
                return
            
            if isinstance(ret,dict):
                data=ret

            line=line+1

    if prevCmd:
        print("%scmd %s not close,will auto close it!" % (colorama.Fore.YELLOW,prevCmd))
        cmdFunc=closeCmds[prevCmd]
        ret=cmdFunc(fileName,args,data)
        if not ret:
            return

    print("--------------------")
    print("")
    
    return True

def move(configData):
    inputPath=os.path.abspath(configData["output"])
    outputPath=os.path.abspath(configData["move"])

    outputDir=os.path.dirname(outputPath)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    print("%s=>%s"%(inputPath,outputPath))
    shutil.copyfile(inputPath,outputPath)

def generateExcel(outputPath):
    global storyDatas
    global storyLabels

    wb = openpyxl.Workbook()
    sheet=wb.worksheets[0]
    sheet.title="#Story"

    sheet["A1"].value="id"
    sheet["A2"].value="int"
    sheet["A3"].value="对话id"

    sheet["B1"].value="nextId"
    sheet["B2"].value="int"
    sheet["B3"].value="下一个对话id"

    sheet["C1"].value="cmd"
    sheet["C2"].value="string"
    sheet["C3"].value="命令"

    sheet["D1"].value="args"
    sheet["D2"].value="json"
    sheet["D3"].value="参数"

    storyDatas=sorted(storyDatas,key=lambda x:(x["id"]))
    
    index=4
    for it in storyDatas:
        sheet["A%d"%index].value=it["id"]
        sheet["C%d"%index].value=it["cmd"]
        if "args" in it:
            sheet["D%d"%index].value=json.dumps(it["args"],ensure_ascii=False, indent=None,separators=(",", ":"))
        else:
            sheet["D%d"%index].value="{}"
        
        if "nextId" in it:
            sheet["B%d"%index].value=it["nextId"]
        
        index=index+1
    
    #生成标签跳转id
    sheet=wb.create_sheet("#StoryLabel")

    sheet["A1"].value="id"
    sheet["A2"].value="string"
    sheet["A3"].value="对话标签id"

    sheet["B1"].value="nextId"
    sheet["B2"].value="int"
    sheet["B3"].value="下一个对话id"

    index=4
    for it in storyLabels:
        sheet["A%d"%index].value=it["id"]
        sheet["B%d"%index].value=it["nextId"]
        index=index+1

    wb.save(outputPath)

def main(configData):
    global storyDatas
    storyDatas=[]

    global storyLabels
    storyLabels=[]

    global useIds
    useIds=[]

    global valueNames
    valueNames=[]

    inputPath=os.path.abspath(configData["input"])
    outputPath=os.path.abspath(configData["output"])

    outputDir=os.path.dirname(outputPath)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    print("inputPath:%s"% (inputPath))
    print("outputPath:%s"% (outputPath))
    print()

    print("generate script")
    print()
    
    for root, dirs, files in os.walk(inputPath):
        for file in files:
            filePath = os.path.join(root, file)
            print("load file:%s" % filePath)
            ret=generateFile(filePath)
            if not ret:
                return
    
    generateExcel(outputPath)

    if not "move" in configData:
        return
    
    print("will move config...")
    move(configData)
    print()

def run(configData):
    startTime = time.time()
    main(configData)
    endTime = time.time()
    execTime = endTime - startTime
    print("%stotal time:%.2fs" % (colorama.Fore.GREEN,execTime))
    print("done!")

configData={}
class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        self.lastModifiedTimes = {}
    
    def on_modified(self, event):
        if not event.is_directory:
            filePath=event.src_path
            if not filePath.endswith(".txt"):
                return
            
            curTime=os.path.getmtime(filePath)

            if filePath not in self.lastModifiedTimes or self.lastModifiedTimes[filePath] != curTime:
                self.lastModifiedTimes[filePath] = curTime
                os.system('cls' if os.name == 'nt' else 'clear')
                run(configData)

if __name__ == "__main__":
    colorama.init(autoreset=True)

    configPath=os.path.abspath(sys.argv[1])
    if not os.path.exists(configPath):
        print("%snot found config file:%s" % (colorama.Fore.RED,configPath))
        exit(-1)

    with open(configPath, "r", encoding="utf-8") as file:
        configData = json.load(file)
    
    inputPath=os.path.abspath(configData["input"])
    if not os.path.exists(inputPath):
        print("%sinvalid input path:%s" % (colorama.Fore.RED,inputPath))
        exit(-1)
    
    if len(sys.argv) > 2 and sys.argv[2] == "-once":
        run(configData)
    else:
        fileMonitorHandle=FileMonitor()
        fileMonitorObserver = Observer()
        fileMonitorObserver.schedule(fileMonitorHandle, inputPath, recursive=False)
        fileMonitorObserver.start()

        print("%sauto generate config service start!" % colorama.Fore.GREEN)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            fileMonitorObserver.stop()
            print("auto generate config service stop!")

        fileMonitorObserver.join()