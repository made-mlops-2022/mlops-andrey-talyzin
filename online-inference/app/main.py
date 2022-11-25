import uvicorn
from config.config import Config


if __name__ == '__main__':
    server = Config().data['server']
    uvicorn.run("server.app:app", host=server['host'], port=server['port'], reload=server['reload'])
    