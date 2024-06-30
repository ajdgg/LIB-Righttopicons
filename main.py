import re
import os
import time
from typing import List
import asyncio
from log import XJ_Log
from dotenv import load_dotenv
from cmd_color import CmdColor
from mail import f_email
from httpx_request import AsyncHttpClient
from file_handle import xj_file_handle


CColor = CmdColor()
client = AsyncHttpClient()
handle = xj_file_handle()

pattern = r"{{Right topicons\|用户=([^}]*)}}"


def extract_and_remove_pattern(s: str):
    matches = re.findall(pattern, s)
    if matches:
        new_str = re.sub(pattern, "", s)
        filtered_matches = list(filter(lambda x: x != '', matches))
        return filtered_matches, new_str, True
    else:
        return [], s, False


def find_nearest_index(list1: List[str], list2: List[str]):
    min_index_diff = len(list1)
    nearest_element = None

    for element in list2:
        try:
            index = list1.index(element)
            if index < min_index_diff:
                min_index_diff = index
                nearest_element = element
        except ValueError:
            pass

    return nearest_element


order_list = handle.xj_file_reading("data.json", "data")
form_order_list = handle.xj_file_reading("data.json", "form")


def Return_to(Arry: List[str], permission: List[str]):
    P_Data = find_nearest_index(order_list, permission)
    if P_Data is None:
        return "DAP"

    """
    用于修改执行错误
    """
    # if P_Data == "autoconfirmed":
    #     return "DA"

    T_Data = form_order_list.get(P_Data)
    if T_Data in Arry:
        return "DAP"
    return "{{Right topicons|用户=" + T_Data + "}}"


def x_self_inspection():
    required_vars = ['USERNAME', 'PASSWORD', 'wiki_url']
    for var in required_vars:
        if os.getenv(var) is None:
            CColor.ccolor("BUG", f"缺少环境变量: {var}", "red")
            XJ_Log.w_log(f"缺少环境变量: {var}", 'error')
            return False
    return True


async def main():
    win = 0
    daps = 0
    mistake = 0
    mistake_list = []
    if os.path.exists('.env.bot'):
        try:
            load_dotenv('.env.bot')
        except Exception as e:
            XJ_Log.w_log(f"加载文件时发生错误：{e}", "error")
            return CColor.ccolor("BUG", f"加载文件时发生错误：{e}", "red")
    else:
        XJ_Log.w_log("无.env.bot文件", "error")
        return CColor.ccolor("BUG", '无.env.bot文件', "red")

    if not x_self_inspection():
        return

    USERNAME = os.getenv("WIKI_USERNAME")
    PASSWORD = os.getenv("WIKI_PASSWORD")
    EXCLUDE = ["Zorua Fox", "New user message", "New user page"]
    wiki_url = os.getenv("MEDIAWIKI_URL")

    """
    登录
    """
    PARAMS_0 = {
        'action': "query",
        'meta': "tokens",
        'type': "login",
        'format': "json"
    }

    LIB_TOKEN = await client.get(wiki_url, params=PARAMS_0)
    LIB_TOKEN = LIB_TOKEN.json()
    LOGIN_TOKEN = LIB_TOKEN['query']['tokens']['logintoken']

    CColor.ccolor("LOGIN_TOKEN", LOGIN_TOKEN, "green")

    PARAMS_1 = {
        'action': "login",
        'lgname': USERNAME,
        'lgpassword': PASSWORD,
        'lgtoken': LOGIN_TOKEN,
        'format': "json"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    BJ_TOKEN = await client.post(f"{wiki_url}", data=PARAMS_1, headers=headers)

    CColor.ccolor("LOGIN", "登录成功", "green")

    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    BJ_TOKEN = await client.get(wiki_url, params=PARAMS_2)
    BJ_TOKEN = BJ_TOKEN.json()
    CSRF_TOKEN = BJ_TOKEN['query']['tokens']['csrftoken']
    CColor.ccolor("CSRF_TOKEN", CSRF_TOKEN, "green")

    """
    获取注册用户列表
    """
    user_lit = f'{wiki_url}?action=query&format=json&list=allusers&aulimit=5000'

    user_lit_data = await client.get(user_lit)
    users_lit = user_lit_data.json()['query'].get('allusers', [])

    CColor.ccolor("USERS_LIST", "获取注册用户列表完成", "green")

    """
    更改用户页
    """
    async def change(CSRF_TOKEN, NAME, QX_TEXT, DATA_TEXT):
        PARAMS_3 = {
            "action": "edit",
            "title": f'User:{NAME}',
            "token": CSRF_TOKEN,
            "format": "json",
            "bot": "true",
            "summary": f'将您的用户页权限标识更改为{re.findall(pattern, QX_TEXT)}',
            "text": f'{QX_TEXT}\n{DATA_TEXT}',
        }
        await client.post(wiki_url, data=PARAMS_3)
        # DATA = R.json()
        # print(DATA)
        CColor.ccolor('green', f'{NAME}修改成功', 'green')

    """
    获取用户权限
    """
    async def get_user_limits(name: str):
        LIBRARY_URL = f'{wiki_url}?action=query&list=users&usprop=groups&format=json&ususers=User:{name}'
        permission_list = await client.get(LIBRARY_URL)
        return permission_list.json()['query']['users'][0].get('groups', [])

    """
    获取页面信息
    """
    async def sser_page_information(name: str):
        user_page = f'{wiki_url}?action=query&format=json&formatversion=2&prop=revisions&rvprop=content&titles=User:{name}'
        response = await client.get(user_page)
        page_data = response.json()["query"]["pages"][0].get("missing")
        if page_data == "" or page_data:
            CColor.ccolor("NO-PAGE", user_name, "red")
            mistake_list.append(user_name)
            return None, None, False
        else:
            example_text = response.json()["query"]["pages"][0]["revisions"][0]["content"]
            matches, modified_str, found = extract_and_remove_pattern(example_text)
            return matches, modified_str, found

    # users_lit = [
    #     {'userid': 52, 'name': '顶呱呱的阿杰'},
    #     {'userid': 1, 'name': 'Zorua Fox'},
    #     {'userid': 2, 'name': 'Qiu'}
    # ]

    for lit in users_lit:
        user_name = lit.get("name", "")
        if user_name == "" or user_name in EXCLUDE:
            CColor.ccolor("DAP", user_name, "yellow")
            daps += 1
            continue
        permissionlist = await get_user_limits(user_name)
        matches, modified_str, found = await sser_page_information(user_name)

        if permissionlist == []:
            CColor.ccolor("DAP", user_name, "yellow")
            daps += 1
            continue

        if found or matches == []:
            template_data = Return_to(matches, permissionlist)
            if template_data == "DAP":
                CColor.ccolor("DAP", user_name, "yellow")
                daps += 1
                continue

            """
            用于修改执行错误
            """
            # if template_data == "DA":
            #     text = f'{modified_str}'
            #     print(user_name, "DA")
            #     await change(CSRF_TOKEN, user_name, text)
            #     continue

            win += 1
            await change(CSRF_TOKEN, user_name, template_data, modified_str)
        else:
            mistake += 1
            continue

    await client.close()
    return daps, mistake, mistake_list, win

if __name__ == '__main__':
    t = time.perf_counter()

    a, b, c, f = asyncio.run(main())

    th = f'{time.perf_counter() - t:.8f}s'

    CColor.h_time("耗时", th)

    email_data = f'{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n本次运行耗时{th}\n 成功修改{f}个用户\n 跳过{a}个用户\n 错误用户数: {b}\n 错误用户列表:\n{c}'
    XJ_Log.w_log(email_data, 'info')
    d = f_email(email_data)
    if d:
        print("邮件发送成功")
        XJ_Log.w_log("邮件发送成功", 'info')
    else:
        print("未配置发送邮件配置或配置错误")
        XJ_Log.w_log("未配置发送邮件配置或配置错误", 'info')
