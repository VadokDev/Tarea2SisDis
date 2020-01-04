import threading
import grpc
import sys
import time

import chat_pb2 as chat
import chat_pb2_grpc as rpc

from datetime import datetime # interesante
from random import choice, randint

class Cliente:

	def __init__(self, host, puerto, modo):
		self.conn = rpc.ChatServerStub(grpc.insecure_channel(host + ':' + str(puerto)))
		print("[Info] Conexión establecida con el servidor:", host + ':' + str(puerto))
		self.modo = modo
		self.cliente = chat.Cliente()
		self.Login()
		threading.Thread(target=self.recibirMensajes, daemon=True).start()
		print("[Info] Sesión iniciada.")
		
		if self.modo == 0:
			self.enviarMensajesAuto()
		else:
			self.enviarMensajes()

	def Ayuda(self):
		print("[Info] El servidor de chat dispone de los siguientes 3 comandos:")
		print("\tclientes - Retorna la lista de clientes conectados con su respectivo id.")
		print("\thistorial - Retorna la lista de mensajes que ha enviado")
		print("\tmsg [idCliente] [mensaje] - Envía un mensaje al cliente con la id ingresada (sin corchetes)")

	def Login(self):
		nombre = ""
		error = 1
		msg = chat.Registro()
		while error:
			if self.modo == 0:
				msg.nombre = ''.join(choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_<>!#$%&/(") for i in range(randint(1, 20)))
			else:
				msg.nombre = input("[Info] Ingrese su nombre para acceder al chat: ")
			res = self.conn.Login(msg)
			error = res.error
			if error:
				print(res.errorMensaje)
		
		self.cliente.nombre = res.cliente.nombre
		self.cliente.id = res.cliente.id
		print("[Cliente] Login exisoto con el nombre:", self.cliente.nombre)
	def recibirMensajes(self):
		for mensaje in self.conn.Chat(self.cliente):
			print("[" + mensaje.timestamp + "]", mensaje.emisor.nombre + ":", mensaje.valor)
	def MensajeEnviado(self, r):
		if r.result().error == 1:
			print(r.result().errorMensaje)

	def enviarMensajes(self):
		self.Ayuda()
		texto = input()

		while texto != "salir":
			data = texto.split()
			#try:
			if data[0] == "msg":
				mensaje = chat.Mensaje()
				mensaje.receptor.id = int(data[1])
				mensaje.emisor.id = self.cliente.id
				mensaje.emisor.nombre = self.cliente.nombre
				mensaje.valor = data[2]
				mensaje.timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
				#res = self.conn.EnviarMensaje(mensaje)
				self.conn.EnviarMensaje.future(mensaje).add_done_callback(self.MensajeEnviado)

			elif data[0] == "clientes":
				# No logré hacer asíncrona esta parte :c
				print("[Server] Lista de clientes conectados al servidor de chat")
				for i in self.conn.ListaClientes(chat.MensajeVacio()):
					print(i.id, i.nombre) 
			elif data[0] == "historial":
				print("[Server] Lista de mensajes enviados al servidor de chat")
				mensaje = chat.Cliente()
				mensaje.id = self.cliente.id

				for i in self.conn.ObtenerMensajes(mensaje):
					print("[" + i.timestamp + "] (" + str(i.id) + ") -", i.receptor.nombre + ":", i.valor) 
			else: 
				self.Ayuda()

			texto = input()
		else: # Sí, esto es tan legal como el yield
			print("[Info] Hasta pronto!")
			exit(0)

	def enviarMensajesAuto(self):
		# Temazo
		milHoras = ["Hace frío y estoy lejos de casa", "Hace tiempo que estoy sentado sobre esta piedra", "Yo me pregunto", "Para que sirven las guerras", "Tengo un cohete en mi pantalón", "Vos estás tan fría como la nieve a mi alrededor", "Vos estás tan blanca, que yo no se que hacer", "La otra noche te esperé", "bajo la lluvia dos horas", "Mil horas como un perro", "Y cuando llegaste me miraste", "y me dijiste loco", "Estás mojado, ya no te quiero", "En el circo vos ya sos una estrella", "Una estrella roja que todo se lo imagina", "Si te preguntan, vos no me conocías", "No, no", "Tengo un cohete en mi pantalón", "Vos estás tan fría como la nieve a mi alrededor", "Vos estás tan blanca, que yo no se que hacer", "Te esperé bajo la lluvia", "No, no, no, no", "La otra noche te esperé", "bajo la lluvia dos horas", "Mil horas como un perro", "Y cuando llegaste me miraste", "y me dijiste loco", "Estás mojado, ya no te quiero", "La otra noche te esperé", "bajo la lluvia dos horas", "Mil horas como un perro", "Y cuando llegaste me miraste", "y me dijiste loco", "Estás mojado, ya no te quiero"]
		accion = 1
		lastId = 0

		while accion != 0:
			accion = randint(0, 30)

			if accion > 0 and accion <= 10:
				mensaje = chat.Mensaje()
				mensaje.receptor.id = randint(0, lastId)
				mensaje.emisor.id = self.cliente.id
				mensaje.emisor.nombre = self.cliente.nombre
				mensaje.valor = milHoras[randint(0, len(milHoras) - 1)]
				mensaje.timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
				#res = self.conn.EnviarMensaje(mensaje)
				self.conn.EnviarMensaje.future(mensaje).add_done_callback(self.MensajeEnviado)
				print("[Cliente] Mensaje enviado")

			elif accion > 10 and accion <= 20:
				print("[Server] Lista de clientes conectados al servidor de chat")
				for i in self.conn.ListaClientes(chat.MensajeVacio()):
					print(i.id, i.nombre)
					lastId = i.id 
			elif accion > 20 and accion <= 30:
				print("[Server] Lista de mensajes enviados al servidor de chat")
				mensaje = chat.Cliente()
				mensaje.id = self.cliente.id

				for i in self.conn.ObtenerMensajes(mensaje):
					print("[" + i.timestamp + "] (" + str(i.id) + ") -", i.receptor.nombre + ":", i.valor) 
			time.sleep(2)
		print("[Info] Hasta pronto!")
		exit(0)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("[Error] Al ejecutar el programa se debe indicar el hostname y puerto del servidor, seguido del modo de trabajo (1 para manual, 0 para automático).")
		print("[Info] Ejemplo de ejecución: python cliente.py localhost 12345 0.")
		exit(0)

	Cliente(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))