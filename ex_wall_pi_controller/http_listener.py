from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import logging
import queue
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:82/", "http://nuc-homeserver:82/", "http://localhost:3006/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
message_queue = queue.Queue()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/instruction")
def receive_string(instruction: str = Form(...)):
    message_queue.put(instruction)
    return JSONResponse({"Received string": instruction}, headers={"Access-Control-Allow-Origin": "*"})



class HTTPListener:

    def __init__(self):
        self.logger = logging.getLogger("HTTPListener")
        self._stop_thread = False
        self.thread = threading.Thread(target=self.run_flask)

    def run_flask(self):
        uvicorn.run(app, host="0.0.0.0", port=8000)

    def start_thread(self):
        self.thread.start()

    def stop_thread(self):
        self._stop_thread = True
        self.thread.join()

    def get_queue(self):
        items = list()
        while not message_queue.empty():
            items.append(message_queue.get())
        return items


def main():
    queue_manager = HTTPListener()
    queue_manager.start_thread()

    try:
        while True:
            print(queue_manager.get_queue())
            time.sleep(1)  # Check the queue every 2 seconds
    except KeyboardInterrupt:
        queue_manager.stop_thread()


if __name__ == "__main__":
    main()
