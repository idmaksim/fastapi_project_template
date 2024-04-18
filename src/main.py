from server import Server
import socket
import logging


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger.warning(f"\nCurrent ip address is {socket.gethostbyname(socket.gethostname())}")

    server = Server("0.0.0.0", 80)
    server.init_routes()
    
    server.run()
