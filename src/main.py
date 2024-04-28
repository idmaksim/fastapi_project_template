from server import Server
import socket
import logging


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    
    server = Server("0.0.0.0", 8090)
    server.init_routes()
    
    server.run()