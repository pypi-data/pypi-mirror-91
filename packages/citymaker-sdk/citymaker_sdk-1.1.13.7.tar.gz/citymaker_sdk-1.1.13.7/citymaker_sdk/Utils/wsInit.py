#!/usr/bin/env Python
# coding=utf-8
#作者： tony
# -*- coding: utf-8 -*-
import os, sys,json,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os, sys,types,json
import Utils.classmake as cmake
import threading
import asyncio
import websockets
from Utils.Common import is_json, objtoLowerCase

class Event_Thead(threading.Thread):
    def __init__(self, e):
        super().__init__()
        self.e = e
        self.address = ws_address
        # self.ws=create_connection(ws_address)
        # self.eventloop = asyncio.new_event_loop()
        # self.eventloop.run_until_complete(self.evnet_initWs())

        # t = threading.Thread(target=start_loop, args=(newloop,))
        # t.start()
        # asyncio.run_coroutine_threadsafe(sendMessage(json.dumps(postData)), newloop)
        # asyncio.run_coroutine_threadsafe(recvMessage(fn, fnName, eventArgs, postData), newloop)

        # msg = json.dumps({"model": 1, "Token": "d7b501d2-fe5d-4a26-a799-1e67e037bfb5"})
        # self.ws.send(msg)

    def run(self):
        while True:
            if self.e.is_set():
                print("event looping")
                model =asyncio.run_coroutine_threadsafe(recvMessage(self.fn, self.fnName, self.eventArgs,self.postData),mainloop)
                backData = json.loads(model).get("api")
                if self.postData["EventName"] == "on" + backData:
                    cmake.AddRenderEventCB_ep(model, self.fn, self.fnName, self.eventArgs)
                self.e.wait()
                # self.e.clear()
            else:
                self.e.set()
                # print('runing')




    # async def initWs(self):
    #     self._event_ws = await websockets.connect(self.address)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def SocketApiServe_init(config):
    global eventprocess,mainloop,eventloop,_global_ws,ws_address,_event_ws
    try:
        # rcEvent = threading.Event()
        # ws= websocket.WebSocket()
        mainloop = asyncio.new_event_loop()
        t = threading.Thread(target=start_loop, args=(mainloop,))
        t.start()
        featrue=asyncio.run_coroutine_threadsafe(main_initWs(config.serverAddress),mainloop)
        _global_ws = featrue.result()
        eventloop = asyncio.new_event_loop()
        t1 = threading.Thread(target=start_loop, args=(eventloop,))
        t1.start()
        featrue1=asyncio.run_coroutine_threadsafe(event_initWs(config.serverAddress),eventloop)
        _event_ws=featrue1.result()
        ws_address=config.serverAddress
        # _event_ws=create_connection("ws://127.0.0.1:8181/")
        # eventloop = asyncio.new_event_loop()
        # eventprocess = Event_Thead(rcEvent)
        # _event_ws= create_connection("ws://127.0.0.1:8181/")
        # _global_ws.run_forever()
    except Exception:
        pass


async def main_initWs(serverAddress):
    try:
        _ws= await websockets.connect(serverAddress)
    except KeyboardInterrupt:
        await _ws.close(reason="user exit")
    return _ws

async def event_initWs(serverAddress):
    try:
        _ws= await websockets.connect(serverAddress)
    except KeyboardInterrupt:
        await _ws.close(reason="user exit")
    return _ws

async def sendMessage(_ws,msg):
    await  _ws.send(msg)
    return await _ws.recv()

async def recvMessage(fn, fnName, eventArgs,postData):
    model= await _event_ws.recv()
    backData = json.loads(model).get("api")

    if postData["EventName"] == "on" + backData:
        cmake.AddRenderEventCB_ep(model, fn, fnName, eventArgs)
        asyncio.run_coroutine_threadsafe(recvMessage(fn, fnName, eventArgs, postData), eventloop)
# async def recvMessage(fn,fnName,eventArgs,postData):
#     str=await _global_ws.recv()
#     if is_json(str):
#         apiData = json.loads(str)
#         resultmodel = objtoLowerCase(apiData.get("Result"))
#         backData = json.loads(resultmodel).get("api")
#         if postData["EventName"] == "on" + backData:
#             cmake.AddRenderEventCB_ep(resultmodel, fn, fnName, eventArgs)

def postMessage(Props, callName, obj, isMain=True):
        # obj["CallBack"] = "API-{}".format(uuid.uuid1())
        # if Props is not None and callName is not None:
        #     sdkInfo(Props, obj.get("CallBack"), callName, "push")
        # loop = asyncio.get_event_loop()
        # str=loop.run_until_complete(send_msg(obj))
        # str = eventprocess.SendMessage(json.dumps(obj))
        if isMain:
            feature=asyncio.run_coroutine_threadsafe(sendMessage(_global_ws,json.dumps(obj)),mainloop)
        else:
            feature=asyncio.run_coroutine_threadsafe(sendMessage(_event_ws,json.dumps(obj)),eventloop)
        str=feature.result()
        if is_json(str):
            apiData = json.loads(str)
            result = objtoLowerCase(apiData.get("Result"))
            # if apiData.get("CallBack") is not None:
            #     sdkInfo(None, apiData.get("CallBack"), "", "pull")
            #     apiCallback[apiData.get("CallBack")](result)
            #     del apiCallback[apiData.get("CallBack")]
            return result
        else:
            return str


def EventProcessStart(fn,fnName,eventArgs,Props,callName,postData):
    try:
        asyncio.run_coroutine_threadsafe(recvMessage(fn, fnName, eventArgs, postData), eventloop)
        # eventprocess.fn = fn
        # eventprocess.fnName = fnName
        # eventprocess.eventArgs = eventArgs
        # eventprocess.Props = Props
        # eventprocess.callName = callName
        # eventprocess.postData = postData
        # eventprocess.start()
    except Exception:
        pass




