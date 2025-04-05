import os
import openpyxl
import json
from slpp import slpp as lua
import xml.etree.ElementTree as ET
import time
import shutil

scriptDatas=[]
scriptLabels=[]

currentId=0

#msg命令
def msgFunc(fileName,data,args):
    data={
        "text":""
    }
    return data

def msgNameFunc(fileName,data,args):
    data["name"]=args
    return data

def msgActorFunc(fileName,data,args):
    data["actor"]=int(args)
    return data

def msgSelFunc(fileName,data,args):
    selDatas=args.split(",")

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
    
    data["sel"]=selects

    return data

def msgTextFunc(fileName,data,args):
    data["text"]=args
    return data
    
def msgEndFunc(fileName,data,args):
    targetData={
        "id":currentId,
        "cmd":"msg",
        "args":data or {}
    }
    scriptDatas.append(targetData)

def labelFunc(fileName,data,args):
    targetData={
        "id":"%s_%s" % (fileName,args),
        "nextId":currentId+1
    }
    scriptLabels.append(targetData)

def gotoFunc(fileName,data,args):
    targetData={
        "id":currentId,
        "cmd":"goto",
        "args":{
            "label":"%s_%s" % (fileName,args)
        }
    }
    scriptDatas.append(targetData)

def waitFunc(fileName,data,args):
    targetData={
        "id":currentId,
        "cmd":"wait",
        "args":{
            "time":float(args)
        }
    }
    scriptDatas.append(targetData)

cmds={
    #msg命令
    "@msg":msgFunc,
    "@msg-text":msgTextFunc,
    "@msg-name":msgNameFunc,
    "@msg-actor":msgActorFunc,
    "@msg-sel":msgSelFunc,
    "@msg-end":msgEndFunc,

    #label命令
    "@label":labelFunc,

    #goto命令
    "@goto":gotoFunc,

    #wait命令
    "@wait":waitFunc,
}

endCmd={
    "@msg":msgEndFunc,
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