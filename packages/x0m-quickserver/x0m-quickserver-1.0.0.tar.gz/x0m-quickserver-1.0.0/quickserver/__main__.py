import sys
import os
from termcolor import colored
import http.server
import socketserver
import webbrowser



def throwError(errorText):
    return colored(errorText,"red")

def successMsg(successMsg):
    return colored(successMsg,"green")


def main():
    isFile_Found = False
    if len(sys.argv) > 2 or len(sys.argv) < 2:
        print(throwError(f'Sorry , quickserver expects only 1 argument but {len(sys.argv) - 1} given'))
    else:
        #We Will Dosomething
        currentDir = os.listdir()
        for i in range(len(currentDir)):
            if currentDir[i] == sys.argv[1]:
                isFile_Found = True
                break

        if (isFile_Found):
            class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
                def do_GET(self):
                    self.path = sys.argv[1]
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)


            # Create an object of the above class
            handler_object = MyHttpRequestHandler

            PORT = 8000
            my_server = socketserver.TCPServer(("", PORT), handler_object)
            print(successMsg(f'Server Started at http://127.0.0.1:{PORT}'))
            # Star the server
            my_server.serve_forever()
        else:
            print(throwError(f'Sory file called {sys.argv[1]} is not found'))




if __name__ == "__main__":
    main()
