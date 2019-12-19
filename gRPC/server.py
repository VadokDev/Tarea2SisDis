
import sys
import grpc
import time

import chat_pb2 as chat
import chat_pb2_grpc as rpc

from concurrent import futures

class ChatServer(rpc.ChatServerServicer):

	def __init__(self):
		self.ultimoMensaje = 0 # id mensajes
		self.chats = [ ] # Chats
		self.AgregarCliente("Broadcast") # Mensaje a todos
	
	def AgregarCliente(self, nombre):
		cliente = chat.Cliente()
		cliente.nombre = nombre
		cliente.id = len(self.chats)

		# userId : [Cliente, [msgEnviado, msgRecibido]]
		self.chats.append( [cliente, [[], []]] )

		print("[Info] Cliente registrado - id:", str(cliente.id) +", nombre:", cliente.nombre)
		return cliente

	def LogChat(self, timestamp, id, emisor, receptor, mensaje):
		logs = open("logs.txt", "a+")

		data = "[" + timestamp + "] (" + str(id) + ") " + emisor + " - " +receptor + ": " + mensaje + "\n"
		print(data)

		logs.write(data)
		logs.close()

	def ClienteRegistrado(self, nombre):
		for cliente, _ in self.chats:
			if cliente.nombre == nombre:
				registrado = 1
				return True
		return False

	def Login(self, request: chat.Registro, context):
		res = chat.RegistroRespuesta()
		res.error = 0

		if self.ClienteRegistrado(request.nombre):
			res.error = 1
			res.errorMensaje = "[Error] Este nombre ya esta en uso"
			print("[Error] Intento de acceso con un nombre en uso")
		else:
			cliente = self.AgregarCliente(request.nombre)
			res.cliente.nombre = cliente.nombre
			res.cliente.id = cliente.id

		return res

	def ObtenerMensajes(self, request: chat.Cliente, context):
		print("[Info] El cliente [" + self.chats[request.id][0].nombre + "] solicitó su lista de mensajes.")
		for mensaje in self.chats[request.id][1][0]:
			yield mensaje

	def ListaClientes(self, request:chat.MensajeVacio, context):
		print("[Info] Se solicitó la Lista de Clientes.")
		for cliente, _ in self.chats:
			yield cliente

	def Chat(self, request: chat.Cliente, context):
		ultimoLeido = 0
		while True: # Querido CPU, lo lamento mucho, pero no se me ocurrió algo mejor :c
			while ultimoLeido < len(self.chats[request.id][1][1]):
				mensaje = self.chats[request.id][1][1][ultimoLeido]
				ultimoLeido += 1
				yield mensaje

	def EnviarMensaje(self, r: chat.Mensaje, context):
		res = chat.MensajeRecibido()
		res.error = 0

		if r.receptor.id > len(self.chats):
			res.error = 1
			res.errorMensaje = "[Error] Receptor no valido"
		else:
			r.id = self.ultimoMensaje
			r.emisor.nombre = self.chats[r.emisor.id][0].nombre
			r.receptor.nombre = self.chats[r.receptor.id][0].nombre

			self.NuevoMensaje(0, r.emisor.id, r)
			self.NuevoMensaje(1, r.receptor.id, r)

			# """"Broadcasting"""" 
			if r.receptor.id == 0:
				for cliente, _ in self.chats:
					self.NuevoMensaje(1, cliente.id, r)

			self.LogChat(r.timestamp, r.id, self.chats[r.emisor.id][0].nombre, self.chats[r.receptor.id][0].nombre, r.valor)

		return res

	def NuevoMensaje(self, tipo, cliente, mensaje):
		# tipo = 0 -> Cliente envió 
		# tipo = 1 -> Cliente recibió

		if tipo == 0:
			self.ultimoMensaje += 1

		self.chats[cliente][1][tipo].append(mensaje)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("[Error] Al ejecutar el programa se debe indicar el hostname y puerto de escucha.")
		print("[Info] Ejemplo de ejecución: python server.py localhost 12345.")
		exit(0)

	host = sys.argv[1]
	puerto = int(sys.argv[2])

	server = grpc.server(futures.ThreadPoolExecutor())
	rpc.add_ChatServerServicer_to_server(ChatServer(), server)
	
	print("[Info] Servidor inicializado en la dirección:", host + ":" + str(puerto))

	server.add_insecure_port(host + ":" + str(puerto))
	server.start()
	while True:
		time.sleep(1800)