import json
from eventmanager.eventmanager import EventManager
from websockets.sync.client import connect
from settings import Settings
from pack import Pack

import asyncio
import queue
import threading

from websockets.exceptions import ConnectionClosedOK

class XToysEventWorker:
    def __init__(self, websocket_uri):
        self._job_queue = queue.Queue()
        self._websocket_uri = websocket_uri
        self._websocket = None
        self._thread = threading.Thread(target=self.work)
        self._thread.start()

    async def send_event(self, msg: dict):
        self._websocket.send(json.dumps(msg))

    async def websocket_msg_handler(self):
        while True:
            try:
                message = self._websocket.recv()
                print(message)
            except ConnectionClosedOK:
                break
            except:
                pass

            await asyncio.sleep(1)

    async def event_queue_worker(self):
        while True:
            try:
                args = self._job_queue.get(timeout=3)
                await self.send_event(args)
            except queue.Empty:
                pass

    # Worker function
    def work(self):
        self._websocket = connect(self._websocket_uri)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.websocket_msg_handler())
        loop.create_task(self.event_queue_worker())
        loop.run_forever()

    def add_job(self, job):
        self._job_queue.put(job)


class XToysEventHandler:
    def __init__(self, settings: Settings, pack: Pack):
        self._settings = settings
        self._pack = pack

    def subscribe(self):
        EventManager().subscribe("prompt_submit_success", self.prompt_submit_success)
        EventManager().subscribe("prompt_submit_failed", self.prompt_submit_failed)

    async def start(self):
        if self._settings.xtoys_enabled == False:
            return

        self.subscribe()
        self._worker = XToysEventWorker(
            "wss://webhook.xtoys.app/" + self._settings.xtoys_websocket
        )

    def prompt_submit_success(self, data):
        self._worker.add_job((self._pack.xtoys["prompt_submit_success"]))

    def prompt_submit_failed(self, data):
        self._worker.add_job((self._pack.xtoys["prompt_submit_failed"]))
