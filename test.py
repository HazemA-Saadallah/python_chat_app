import socket
import threading
import datetime


from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import asyncio
import time

if __name__ == "__main__":
    """ socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) """
    """ socket.bind(("localhost", 9999)) """
    """ socket.listen() """
    """ socket.accept() """
    """ try: """
    """ except KeyboardInterrupt: """
    """     socket.close() """
    """ print(datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")) """


""" async def echo(): """
"""     while True: """
"""         print(time.time()) """
"""         await asyncio.sleep(1) """


def lloop():
    while True:
        print("aaaaaaaa")
        time.sleep(1)


async def read():
    session = PromptSession()
    while True:
        with patch_stdout():
            line = await session.prompt_async("> ")
            print(line.upper())

    loop = asyncio.get_event_loop()
    """ loop.create_task(echo()) """
    loop.create_task(read())
    loop.run_forever()
    thread = threading.Thread(target=lloop)
    thread.start()

loop = asyncio.get_event_loop()
""" loop.create_task(echo()) """
loop.create_task(read())
loop.run_forever()
