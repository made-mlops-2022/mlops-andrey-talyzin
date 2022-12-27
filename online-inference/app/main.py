import uvicorn
from config.config import Config
import time


if __name__ == '__main__':
    time.sleep(30)
    server = Config().data['server']
    uvicorn.run("server.app:app", host=server['host'], port=server['port'], reload=server['reload'])
    