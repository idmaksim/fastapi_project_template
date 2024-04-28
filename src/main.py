from server import Server


if __name__ == "__main__":
    
    server = Server("0.0.0.0", 8090)
    server.init_routes()
    
    server.run()