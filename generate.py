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

cmdPatterns={
    "msg":re.compile(r'^([\w]+)\:([\w\W]+)'),
    "guide":re.compile(r'^([\d]+)'),
    "wait":re.compile(r'^([\d\.]+)'),
    "audio":re.compile(r'^([\d]+)\,([\w\W]+)'),
    "audio-stop":re.compile(r'^([\d]+)'),
    "bgm":re.compile(r'^([\d]+)'),
    "se":re.compile(r'^([\d]+)'),
    "vo":re.compile(r'^([\d]+)'),
}

#显示类
#对话命令
def msgFunc(fileName,cmdArgs,cmdData):
    global curId

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
            "break":False,
            "click":True,
        }
    }

    pattern=cmdPatterns["msg"]
    res=pattern.match(cmdArgs)
    if not res:
        targetData["args"]["text"]=cmdArgs
    else:
        datas=res.groups()
        targetData["args"]["name"]=datas[0]
        targetData["args"]["text"]=datas[1]

    curId=curId+1
    storyDatas.append(targetData)
    return True

def msgStartFunc(fileName,cmdArgs,cmdData):
    data={
        "name":"",
        "text":"",
        "actor":0,
        "sel":{},
        "break":False,
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

def msgBreakFunc(fileName,cmdArgs,cmdData):
    cmdData["break"]=True

    return cmdData

def msgTextFunc(fileName,cmdArgs,cmdData):
    cmdData["text"]=cmdArgs
    return cmdData

def msgClickFunc(fileName,cmdArgs,cmdData):
    cmdData["click"]=False

    return cmdData

def msgEndFunc(fileName,cmdArgs,cmdData):
    global curId

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

    curId=curId+1
    storyDatas.append(targetData)
    return True

#控制类
#guide命令
def guideFunc(fileName,cmdArgs,cmdData):
    global curId

    pattern=cmdPatterns["guide"]
    res=pattern.match(cmdArgs)
    if not res:
        print("%sInvalid guide args:%s",colorama.Fore.RED,cmdArgs)
        return
    
    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"guide",
        "args":{
            "id":0
        }
    }

    datas=res.groups()
    targetData["args"]["id"]=int(datas[0])

    curId=curId+1
    storyDatas.append(targetData)
    return True

#标签命令
def labelFunc(fileName,cmdArgs,cmdData):
    global curId
    
    targetData={
        "id":"%s_%s" % (fileName,cmdArgs),
        "nextId":curId+1
    }
    
    curId=curId+1
    storyLabels.append(targetData)
    return True

#跳转命令
def gotoFunc(fileName,cmdArgs,cmdData):
    global curId

    targetData={
        "id":curId,
        "cmd":"goto",
        "args":{
            "label":"%s_%s" % (fileName,cmdArgs)
        }
    }

    curId=curId+1
    storyDatas.append(targetData)
    return True

#等待命令
def waitFunc(fileName,cmdArgs,cmdData):
    global curId

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

    curId=curId+1
    storyDatas.append(targetData)
    return True

#音频类
#audio命令
def audioFunc(fileName,cmdArgs,cmdData):
    global curId

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

    curId=curId+1
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
    global curId

    if not cmdData:
        print("%sinvalid @audio-end data:%s" % (colorama.Fore.RED,cmdData))
        return

    targetData={
        "id":curId,
        "nextId":curId+1,
        "cmd":"audio",
        "args":cmdData
    }

    curId=curId+1
    storyDatas.append(targetData)
    return True

def audioStopFunc(fileName,cmdArgs,cmdData):
    global curId

    pattern=cmdPatterns["audio-stop"]
    res=pattern.match(cmdArgs)
    if not res:
        print("%sInvalid guide args:%s",colorama.Fore.RED,cmdArgs)
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

    curId=curId+1
    storyDatas.append(targetData)
    return True

def bgmFunc(fileName,cmdArgs,cmdData):
    global curId

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

    curId=curId+1
    storyDatas.append(targetData)
    return True

def seFunc(fileName,cmdArgs,cmdData):
    global curId

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

    curId=curId+1
    storyDatas.append(targetData)
    return True

def voFunc(fileName,cmdArgs,cmdData):
    global curId

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

    curId=curId+1
    storyDatas.append(targetData)
    return True

def videoFunc(fileName,cmdArgs,cmdData):
    global curId

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

    curId=curId+1
    storyDatas.append(targetData)
    return True

cmds={
    #显示类
    #msg命令
    "@msg":msgFunc,
    "@msg-start":msgStartFunc,
    "@msg-text":msgTextFunc,
    "@msg-name":msgNameFunc,
    "@msg-actor":msgActorFunc,
    "@msg-sel":msgSelFunc,
    "@msg-break":msgBreakFunc,
    "@msg-click":msgClickFunc,
    "@msg-end":msgEndFunc,

    #控制类
    #label命令
    "@label":labelFunc,

    #goto命令
    "@goto":gotoFunc,

    #wait命令
    "@wait":waitFunc,

    #guide命令
    "@guide":guideFunc,

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

endCmds={
    "@msg-end":True,
    "@audio-end":True
}

closeCmds={
   "@msg-start":msgEndFunc,
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
            cmd=None
            args=None
            it=it.strip()
            index=it.find(" ")
            if index == -1:
                cmd=it
            else:
                cmd=it[0:index]
                args=it[index+1:]
            
            if not headerCheck:
                if cmd != "@start":
                    print("%sinvalid file:%s\n" % (colorama.Fore.RED,filePath))
                    return
                
                id=0
                try:
                    id=int(args)
                except ValueError as e:
                    print("%sinvalid @start cmd!" % (args))
                    return

                if id in useIds:
                    print("%srepeat @start id:%d" % (args,id))
                    return
                
                curId=id
                headerCheck=True
                continue

            if curId in useIds:
                print("%srepeat @start id:%d" % (args,id))
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
            elif cmd in endCmds or cmd in cmds:
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