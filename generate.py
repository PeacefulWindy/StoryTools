import os
import openpyxl
import json
import shutil

scriptDatas=[]
scriptLabels=[]
useIds=[]

currentId=0

#显示类
#对话命令
def msgFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "cmd":"msg",
        "nextId":currentId+1,
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

    index=cmdArgs.find(":")
    if index == -1:
        targetData["args"]["text"]=cmdArgs
    else:
        targetData["args"]["name"]=cmdArgs[0:index]
        targetData["args"]["text"]=cmdArgs[index:]

    scriptDatas.append(targetData)

def msgStartFunc(fileName,cmdData,cmdArgs):
    data={
        "name":"",
        "text":"",
        "actor":0,
        "sel":{},
        "break":False,
        "click":True,
    }
    return data

def msgNameFunc(fileName,cmdData,cmdArgs):
    cmdData["name"]=cmdArgs
    return cmdData

def msgActorFunc(fileName,cmdData,cmdArgs):
    cmdData["actor"]=int(cmdArgs)
    return cmdData

def msgSelFunc(fileName,cmdData,cmdArgs):
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

def msgBreakFunc(fileName,cmdData,cmdArgs):
    cmdData["break"]=True

    return cmdData

def msgTextFunc(fileName,cmdData,cmdArgs):
    cmdData["text"]=cmdArgs
    return cmdData

def msgClickFunc(fileName,cmdData,cmdArgs):
    cmdData["click"]=False

    return cmdData

def msgEndFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "cmd":"msg",
        "args":cmdData or {}
    }

    if not cmdData or not "sel" in cmdData:
        targetData["nextId"]=currentId+1

    scriptDatas.append(targetData)

#控制类
#guide命令
def guideFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"wait",
        "args":{
            "id":int(cmdArgs)
        }
    }

    scriptDatas.append(targetData)

#标签命令
def labelFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":"%s_%s" % (fileName,cmdArgs),
        "nextId":currentId+1
    }
    scriptLabels.append(targetData)

#跳转命令
def gotoFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "cmd":"goto",
        "args":{
            "label":"%s_%s" % (fileName,cmdArgs)
        }
    }

    scriptDatas.append(targetData)

#等待命令
def waitFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"wait",
        "args":{
            "time":float(cmdArgs)
        }
    }
    scriptDatas.append(targetData)

#音频类
#audio命令
def audioFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"audio",
        "args":
        {
            "channel":0,
            "id":0,
            "src":"",
            "volume":100,
            "loop":False,
        }
    }

    args=cmdArgs.split(",")
    targetData["args"]["channel"]=int(args[0])
    targetData["args"]["src"]=args[1]

    if len(args) > 1:
        isLoop=int(args[2])
        if isLoop == 1:
            targetData["args"]["loop"]=True
        else:
            targetData["args"]["loop"]=False


    scriptDatas.append(targetData)

def audioStartFunc(fileName,cmdData,cmdArgs):
    data={
        "channel":0,
        "id":0,
        "src":"",
        "volume":100,
        "loop":False,
    }
    return data

def audioChannelFunc(fileName,cmdData,cmdArgs):
    cmdData["channel"]=int(cmdArgs)
    return cmdData

def audioIdFunc(fileName,cmdData,cmdArgs):
    cmdData["id"]=int(cmdArgs)
    return cmdData

def audioSrcFunc(fileName,cmdData,cmdArgs):
    cmdData["src"]=cmdArgs
    return cmdData

def audioVolumeFunc(fileName,cmdData,cmdArgs):
    cmdData["vol"]=int(cmdArgs)
    return cmdData

def audioLoopFunc(fileName,cmdData,cmdArgs):
    isLoop=int(cmdArgs)
    if isLoop == 1:
        cmdData["loop"]=True
    else:
        cmdData["loop"]=False
    
    return cmdData

def audioEndFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"audio",
        "args":cmdData or {}
    }

    scriptDatas.append(targetData)

def audioStopFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"audio-stop",
        "args":
        {
            "channel":int(cmdArgs),
        }
    }

    scriptDatas.append(targetData)

def bgmFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"audio",
        "args":
        {
            "channel":1,
            "id":0,
            "src":cmdArgs[0],
            "volume":100,
            "loop":True,
        }
    }

    scriptDatas.append(targetData)

def seFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"audio",
        "args":
        {
            "channel":2,
            "id":0,
            "src":cmdArgs[0],
            "volume":100,
            "loop":False,
        }
    }

    scriptDatas.append(targetData)

def voFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"audio",
        "args":
        {
            "channel":3,
            "id":0,
            "src":cmdArgs[0],
            "volume":100,
            "loop":False,
        }
    }

    scriptDatas.append(targetData)

def videoFunc(fileName,cmdData,cmdArgs):
    targetData={
        "id":currentId,
        "nextId":currentId+1,
        "cmd":"video",
        "args":
        {
            "id":0,
            "src":cmdArgs[0],
            "full":True,
        }
    }

    scriptDatas.append(targetData)

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

endCmd={
    "@msg-start":msgEndFunc,
    "@audio-start":audioEndFunc,
}

def loadFile(filePath):
    global currentId

    fileName=os.path.splitext(os.path.basename(filePath))[0]

    curCmd=""
    data=None

    with open(filePath,encoding="utf-8") as file:
        datas=file.readlines()

        flag=0
        for it in datas:
            it=it.strip()

            cmd=None
            args=None
            index=it.find(" ")
            if index == -1:
                cmd=it
            else:
                cmd=it[0:index]
                args=it[index+1:]
            
            if cmd == "":
                continue

            if currentId in useIds:
                print("repeat story id:%d,stop!"%currentId)
                return False

            if flag == 0:
                if cmd != "@start":
                    print("invalid "+filePath+",break")
                    return False
                
                currentId=int(args[0])
            elif cmd in cmds:
                if curCmd != "" and not curCmd in cmd:
                    print("warning:not close cmd %s at line:%d,will auto close it."%(curCmd,flag))

                    data=endCmd[curCmd](fileName,data,None)
                    curCmd=""
                    currentId=currentId+1
                elif cmd in endCmd:
                    curCmd=cmd
                
                data=cmds[cmd](fileName,data,args)
                if not data:
                    useIds.append(currentId)
                    currentId=currentId+1
                    curCmd=""
            else:
                print("warning:unknown cmd:%s" % (cmd))
            
            flag=flag+1
    
    if curCmd != "":
        print("warning:not close cmd %s at line:%d,will auto close it."%(curCmd,flag))
        endCmd[curCmd](fileName,data,None)
    
    return True

def move(json_data):
    outputPath=json_data["output"]
    movePath=json_data["move"]
    outputDir=os.path.dirname(movePath)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    print("%s=>%s"%(outputPath,movePath))
    shutil.copyfile(outputPath,movePath)

def generateExcel(outputPath):
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

    global scriptDatas
    scriptDatas=sorted(scriptDatas,key=lambda x:(x["id"]))
    
    index=4
    for it in scriptDatas:
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
    for it in scriptLabels:
        sheet["A%d"%index].value=it["id"]
        sheet["B%d"%index].value=it["nextId"]
        index=index+1

    wb.save(outputPath)

def main():
    json_data={}
    with open("../config.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    outputDir=os.path.dirname(json_data["output"])
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    for root, dirs, files in os.walk(json_data["input"]):
        for file in files:
            filepath = os.path.join(root, file)
            print("load file:%s" %filepath)
            if not loadFile(filepath):
                print("generate failed!")
                return
            print("file %s generate ok!\n"%filepath)
    
    print("will generate story excel...")
    generateExcel(json_data["output"])
    print("will move excel...")
    move(json_data)
    print("done!")

main()