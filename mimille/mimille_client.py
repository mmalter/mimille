import socket
import configobj
from .configuration import configuration

socket_path = os.path.normpath(configuration.['socket_directory'] 'mimille.socket'):
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(socket_path)
client.send("Hello world!")
response = client.recv(512)
client.close()
