from pywebio import start_server
from pywebio.input import*
from pywebio.output import*
from pywebio.session import run_async, run_js

import asyncio

chat_msgs = []
online = set()

SAVE = 500

async def main():
    global chat_msgs

    put_markdown('Я сигма')

    box = output()
    put_scrollable(box, height=300, keep_bottom=True)

    nickname = await input('ы', required=True, placeholder='Кличка', color="blue", validate=lambda n: 'Это имя недоступно' if n == 'Зеленский' else None)
    online.add(nickname)

    chat_msgs.append(('d', f" + `{nickname}` + с нами"))
    box.append(put_markdown((f" + `{nickname}` + с нами")))

    refresh = run_async(refresh_msg(nickname, box))

    while True:
        data = await input_group("СМС", [
            input(placeholder="Введите текст...", name='msg'),
            actions(name='cmd', buttons=["Отправить", "Выйти из чата"])
        ], validate=lambda m: ('msg', 'ВВОД') if m['cmd'] == 'Отправить' and not m['msg'] else None)

        if data is None:
            break

        box.append(put_markdown(f" `{nickname}`: {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))

    refresh.close()

    online.remove(nickname)
    toast('bye')
    box.append(put_markdown(f"`{nickname}` ушел"))
    chat_msgs.append((f" `{nickname}` ушел"))
    

async def refresh_msg(nickname, box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for k in chat_msgs[last_idx:]:
            if k[0] != nickname:
                box.append(put_markdown(f" `{k[0]}` : {k[1]}"))

        if len(chat_msgs) > SAVE:
            chat_msgs = chat_msgs[len(chat_msgs) //2:]

        last_idx = len(chat_msgs)
        

if __name__ == '__main__':
    start_server(main, debug=False, port=8080, cdn=False)


    






































      
    start_server(main, debug=True, port=8080, cdn=False)
