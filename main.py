from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import numpy as np
import json
import os
import asyncio


PLUGIN_DIR=os.path.dirname(__file__)
DATA_DIR=os.path.join(PLUGIN_DIR, "data","rand.json")
DATA_LIST=os.path.join(PLUGIN_DIR, "data","list.json")
DATA_PLAYER=os.path.join(PLUGIN_DIR, "data","player.json")
DATA_PLAYER_LIST=os.path.join(PLUGIN_DIR, "data","player_list.json")

list_map=[]
player_list=[]
player_list_dic={"虚构点":"","星星瓶":"","背包":[],"过本记录":[],"退本记录":[]}
help_dic={"【星星】":"抽取星星",
          "【添加抽取】":"可通过参数添加抽取条目，例如：添加抽取 秘闻",
          "【删除抽取】":"可通过参数删除抽取条目，例如：删除抽取 秘闻",
          "【查看抽取】":"可以查看所有的可抽取类目",
          "【添加 <类目> <所添加的物品>】":"可往抽奖类目里添加一个物品",
          "【修改 <类目> <所修改的物品> <修改后的物品>】":"可在抽奖类目里修改一个物品",
          "【删除 <类目> <要删除的物品>】":"可在抽奖类目里删除一个物品",
          "【查看 <类目>】":"查看该类目所有物品",
          "【抽取 <类目>】":"可抽奖",
          "【创建角色卡】":"可创建一张角色卡",
           "【查看角色卡】":"可查看自己的角色卡",
          "【删除角色卡 <qq号>】":"可删除一张角色卡，管理员可用(管理员可在后台设置)",
          "【增加我的 <[背包]、[过本记录]或者[退本记录]中的一个> <所添加的物品>】":"可在该项里添加一个物品",
          "【删除我的 <[背包]、[过本记录]或者[退本记录]中的一个> <所删除的物品>】":"可在该项里添加一个物品",
           "【修改我的 <[背包]、[过本记录]或者[退本记录]中的一个> <要修改的物品> <修改后的物品>】":"可在该项里修改一个物品",
            "【修改星星瓶 <星星数量>】":"可修改星星瓶里的数量",
            "【修改虚构点 <星星数量>】":"可修改虚构点"

          }




@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        with open(f"{DATA_LIST}","r",encoding="UTF-8")as f:
            data=json.load(f)
            global list_map
            list_map=data
            print(list_map)
        with open(f"{DATA_PLAYER_LIST}","r",encoding="UTF-8")as f:
            data=json.load(f)
            global player_list
            player_list=data
            print(player_list)


    def add_list_map(self):
        with open(f"{DATA_LIST}","w",encoding="UTF-8")as f:
            d=list_map
            data=json.dumps(d,ensure_ascii=False)
            f.write(data)

    def update_player_list(self):
        with open(f"{DATA_PLAYER_LIST}","w",encoding="utf-8")as f:
            d=player_list
            data=json.dumps(d,ensure_ascii=False)
            f.write(data)

        
        
        
        
    async def get_card_name(self,event:AstrMessageEvent):
        u_id=event.get_sender_id()
        g_id=event.get_group_id()
        if event.get_platform_name() == "aiocqhttp":
        # qq
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot # 得到 client
            payloads = {
                "group_id": g_id,
                "user_id":u_id
            }
            ret = await client.api.call_action('get_group_member_info', **payloads) # 调用 协议端  API
            ret1=ret.get("card")
            return ret1
            



    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("星星")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = await self.get_card_name(event)
        a=np.random.randint(0,5)
        if a==0:
            yield event.plain_result(f"{user_name}, 你抽取了星星可惜瓶子是空的!")
        else:
            yield event.plain_result(f"{user_name}, 你抽取了星星池获得 {a}颗星星!")    
    @filter.command("添加抽取")
    async def LeiBie(self,event:AstrMessageEvent,L:str):
        lis=[]
        dic={L:lis}
        with open(f"{DATA_DIR}","r",encoding="UTF-8")as f:
           data=json.load(f)
           d=data.get("抽取")
           list_map.append(L)
           d.append(dic)
           data["抽取"]=d
           data_j=json.dumps(data,ensure_ascii=False)
        with open(f"{DATA_DIR}","w",encoding="UTF-8")as f:
            f.write(data_j)
        print(list_map)
        self.add_list_map()
        yield event.plain_result(f"你已经成功添加类目{L}")

    @filter.command("删除抽取")
    async def del_lei(self,event:AstrMessageEvent,L:str):
        with open(f"{DATA_DIR}","r",encoding="UTF-8")as f:
           data=json.load(f)
           d=data.get("抽取")
           d.pop(list_map.index(L))
           list_map.remove(L)
           data["抽取"]=d
           data_j=json.dumps(data,ensure_ascii=False)
        with open(f"{DATA_DIR}","w",encoding="UTF-8")as f:
            f.write(data_j)
        self.add_list_map()
        yield event.plain_result(f"你已经成功删除类目{L}")

    @filter.command("查看抽取")
    async def ls_lei(self,event:AstrMessageEvent):
        with open(f"{DATA_LIST}","r",encoding="UTF-8")as f:
            data=json.load(f)
            yield event.plain_result("\n".join(data))

    
    @filter.command("查看")
    async def manghe(self,event:AstrMessageEvent,L:str):
        with open(f"{DATA_DIR}","r",encoding="UTF-8")as f:
            data=json.load(f)
            d=data.get("抽取")[list_map.index(L)].get(L)
            yield event.plain_result("\n".join(d))


    @filter.command("添加")
    async def AddMangHe(self,event:AstrMessageEvent,L:str,s:str):
        with open(f"{DATA_DIR}","r",encoding="UTF-8")as f:
            global list_map
            data=json.load(f)
            print(data)
            d=data.get("抽取")[list_map.index(L)].get(L)
            d.append(s)
            data["抽取"][list_map.index(L)][L]=d
            print(data)
            data_j=json.dumps(data,ensure_ascii=False)
            print(data_j)
        with open(f"{DATA_DIR}","w",encoding="UTF-8")as f:
            f.write(data_j)
        yield event.plain_result(f"你已经成功添加类目{L}中的{s}")

    @filter.command("删除")
    async def DelMangHe(self,event:AstrMessageEvent,L:str,s:str):
        with open(f"{DATA_DIR}","r",encoding="UTF-8")as f:
            data=json.load(f)
            global list_map
            a=list_map.index(L)
            print(a)
            d=data.get("抽取")[list_map.index(L)].get(L)
            d.remove(s)
            data["抽取"][list_map.index(L)][L]=d
            print(data)
            data_j=json.dumps(data,ensure_ascii=False)
            print(data_j)
        with open(f"{DATA_DIR}","w",encoding="UTF-8")as f:
            f.write(data_j)
        yield event.plain_result(f"你已经成功添加类目{L}中的{s}")


    @filter.command("修改")
    async def SetMangHe(self,event:AstrMessageEvent,L:str,s:str,ns:str):
        with open(f"{DATA_DIR}","r",encoding="UTF-8")as f:
            data=json.load(f)
            d=data.get("抽取")[list_map.index(L)].get(L)
            d_index=d.index(s)
            d[d_index]=ns
            data["抽取"][list_map.index(L)][L]=d
            print(data)
            data_j=json.dumps(data,ensure_ascii=False)
            print(data_j)
        with open(f"{DATA_DIR}","w",encoding="UTF-8")as f:
            f.write(data_j)
    
    @filter.command("抽取")
    async def chouqu(self,event:AstrMessageEvent,L:str):
        with open(f"{DATA_DIR}","r",encoding="UTF-8")as f:
            data=json.load(f)
            d=data.get("抽取")[list_map.index(L)].get(L)
            a=np.random.randint(0,len(d)-1)
            ns=d[a]
            yield event.plain_result(f"恭喜你抽到了{ns}")
    @filter.command("查看角色卡")
    async def player_card(self,event:AstrMessageEvent):
        u_id=event.get_sender_id()
        with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
            data=json.load(f)
            d=data.get(u_id)
        yield event.plain_result("\n".join(f"{key}:{vel}"for key,vel in d.items()) )
    
    @filter.command("创建角色卡")
    async def add_player_card(self,event:AstrMessageEvent):
        u_id=event.get_sender_id()
        with open(f"{DATA_PLAYER_LIST}","r",encoding="UTF-8")as f:
            lis=json.load(f)
        l=lis
        if(u_id in l):
            yield event.plain_result("你已经拥有角色卡")
        else:
            with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
                global player_list_dic
                global player_list
                data=json.load(f)
                print(data)
                data.update({f"{u_id}":player_list_dic})
                d=json.dumps(data,ensure_ascii=False)
                print(d)
            with open(f"{DATA_PLAYER}","w",encoding="UTF-8")as f:
                f.write(d)
            player_list.append(f"{u_id}")
            self.update_player_list()
            yield event.plain_result("恭喜你创建角色卡成功")
    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("删除角色卡")
    async def del_player_card(self,event:AstrMessageEvent,L:str):
         u_id=L
         with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
                global player_list_dic
                data=json.load(f)
                print(data)
                data.pop(f"{u_id}")
                d=json.dumps(data,ensure_ascii=False)
                print(d)
         with open(f"{DATA_PLAYER}","w",encoding="UTF-8")as f:
            f.write(d)
         player_list.remove(f"{u_id}")
         print(player_list)
         self.update_player_list()
         s=await self.get_card_name(event)
         yield event.plain_result(f"你已删除{s}的角色卡")

    @filter.command("修改星星瓶")
    async def set_player_start(self,event:AstrMessageEvent,c:str):
        u_id=event.get_sender_id()
        with open(f"{DATA_PLAYER_LIST}","r",encoding="UTF-8")as f:
            lis=json.load(f)
        k=lis
        if(u_id in k):
            with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
                global player_list_dic
                data=json.load(f)
                data[f"{u_id}"].update({"星星瓶":c})
                d=json.dumps(data,ensure_ascii=False)
                print(d)
            with open(f"{DATA_PLAYER}","w",encoding="UTF-8")as f:
                f.write(d)
            yield event.plain_result("你已经成功修改星星瓶")
        else:
            yield event.plain_result("你还没有角色卡哦，快去创建吧")


    @filter.command("修改虚构点")
    async def set_player_dian(self,event:AstrMessageEvent,c:str):
        u_id=event.get_sender_id()
        with open(f"{DATA_PLAYER_LIST}","r",encoding="UTF-8")as f:
            lis=json.load(f)
        k=lis
        if(u_id in k):
            with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
                global player_list_dic
                data=json.load(f)
                data[f"{u_id}"].update({"虚构点":c})
                d=json.dumps(data,ensure_ascii=False)
                print(d)
            with open(f"{DATA_PLAYER}","w",encoding="UTF-8")as f:
                f.write(d)
            yield event.plain_result("你已经成功修改虚构点")
        else:
            yield event.plain_result("你还没有角色卡哦，快去创建吧")



    @filter.command("增加我的")
    async def add_player_ny(self,event:AstrMessageEvent,e:str,c:str):
        u_id=event.get_sender_id()
        with open(f"{DATA_PLAYER_LIST}","r",encoding="UTF-8")as f:
            lis=json.load(f)
        k=lis
        if(u_id in k):
            with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
                global player_list_dic
                data=json.load(f)
                data[f"{u_id}"][e].append(c)
                d=json.dumps(data,ensure_ascii=False)
                print(d)
            with open(f"{DATA_PLAYER}","w",encoding="UTF-8")as f:
                f.write(d)
            yield event.plain_result(f"你已经成功增加{e}")
        else:
            yield event.plain_result("你还没有角色卡哦，快去创建吧")



    @filter.command("删除我的")
    async def del_player_ny(self,event:AstrMessageEvent,e:str,c:str):
        u_id=event.get_sender_id()
        with open(f"{DATA_PLAYER_LIST}","r",encoding="UTF-8")as f:
            lis=json.load(f)
        k=lis
        if(u_id in k):
            with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
                global player_list_dic
                data=json.load(f)
                data[f"{u_id}"][e].remove(c)
                d=json.dumps(data,ensure_ascii=False)
                print(d)
            with open(f"{DATA_PLAYER}","w",encoding="UTF-8")as f:
                f.write(d)
            yield event.plain_result(f"你已经成功删除{e}")
        else:
            yield event.plain_result("你还没有角色卡哦，快去创建吧")


    @filter.command("修改我的")
    async def set_player_ny(self,event:AstrMessageEvent,e:str,c:str,ns:str):
        u_id=event.get_sender_id()
        with open(f"{DATA_PLAYER_LIST}","r",encoding="UTF-8")as f:
            lis=json.load(f)
        k=lis
        if(u_id in k):
            with open(f"{DATA_PLAYER}","r",encoding="UTF-8")as f:
                global player_list_dic
                data=json.load(f)
                n=data[f"{u_id}"][e]
                n[n.index(c)]=ns
                data[f"{u_id}"].update({e:n})
                d=json.dumps(data,ensure_ascii=False)
                print(d)
            with open(f"{DATA_PLAYER}","w",encoding="UTF-8")as f:
                f.write(d)
            yield event.plain_result(f"你已经成功修改{e}")
        else:
            yield event.plain_result("你还没有角色卡哦，快去创建吧")


    @filter.command("帮助")
    async def help_list(self,event:AstrMessageEvent):
        global help_dic
        yield event.plain_result("\n".join(f"{key}:{vel}"for key,vel in help_dic.items()) )
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
