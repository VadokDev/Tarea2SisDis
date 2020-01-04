#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pika
import time
import json
import threading

class ChatServer():

	def __init__(self, host, puerto):
		print("[Info] Conectando servidor a ", host + ':' + str(puerto))
		self.host = host
		self.puerto = puerto

		self.ultimoMensaje = 0 			  	 # id mensajes
		self.chats = [ ] 				 	 # Chats
		self.AgregarCliente("Broadcast", "") # Mensaje a todos

		t1 = threading.Thread(target=self.handleServices, daemon=True)
		t2 = threading.Thread(target=self.handleChats, daemon=True)
		t3 = threading.Thread(target=self.handleLogin, daemon=True)
		t1.start()
		t2.start()
		t3.start()
		
		while True:	# Perdón, no se me ocurrió una mejor forma de mantener abierto el servidor :c
			continue

	def handleServices(self):
		self.connServices = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, heartbeat=0))
		self.channelServices = self.connServices.channel()
		self.colaServices = self.channelServices.queue_declare(queue='', exclusive=True).method.queue
		self.channelServices.exchange_declare(exchange='services', exchange_type='direct')
		self.channelServices.queue_bind(exchange='services', queue=self.colaServices, routing_key='services')

		self.channelServices.basic_consume(queue=self.colaServices, on_message_callback=self.servicesCallback, auto_ack=True)
		self.channelServices.start_consuming()

	def handleChats(self):
		self.connChat = pika.BlockingConnection(pika.ConnectionParameters(self.host, heartbeat=0))
		self.channelChat = self.connChat.channel()
		self.colaChat = self.channelChat.queue_declare(queue='', exclusive=True).method.queue
		self.channelChat.exchange_declare(exchange='chat', exchange_type='direct')
		self.channelChat.queue_bind(exchange='chat', queue=self.colaChat, routing_key='chat')

		self.channelChat.basic_consume(queue=self.colaChat, on_message_callback=self.chatsCallback, auto_ack=True)
		self.channelChat.start_consuming()

	def handleLogin(self):
		self.connLogin = pika.BlockingConnection(pika.ConnectionParameters(self.host, heartbeat=0))
		self.channelLogin = self.connLogin.channel()
		self.colaLogin = self.channelLogin.queue_declare(queue='', exclusive=True).method.queue
		self.channelLogin.exchange_declare(exchange='login', exchange_type='direct')
		self.channelLogin.queue_bind(exchange='login', queue=self.colaLogin, routing_key='login')

		self.channelLogin.basic_consume(queue=self.colaLogin, on_message_callback=self.loginCallback, auto_ack=True)
		self.channelLogin.start_consuming()

	def loginCallback(self, ch, method, properties, body):
		body = json.loads(str(body.decode('UTF-8')))
		print(body)
		
		res = {}

		if self.ClienteRegistrado(body["nombre"]):
			res["error"] = "[Error] Este nombre ya esta en uso"
			print("[Error] Intento de acceso con un nombre en uso")
		else:
			res["id"] = self.AgregarCliente(body["nombre"], body["key"])
		
		self.channelLogin.basic_publish(exchange='login', routing_key=body["key"], body=json.dumps(res))
	
	def servicesCallback(self, ch, method, properties, body):
		body = json.loads(str(body.decode('UTF-8')))
		print(body)

		if body["accion"] == "1":
			print("[Info] Se solicitó la Lista de Clientes.")
			res = json.dumps([[c[0], c[3]] for c in self.chats])
			print(res)
			self.channelServices.basic_publish(exchange='services', routing_key=body["key"], body=json.dumps(res))
		elif body["accion"] == "2":
			print("[Info] El cliente [" + self.chats[body["id"]][0] + "] solicitó su lista de mensajes.")
			self.channelServices.basic_publish(exchange='services', routing_key=body["key"], body=json.dumps(self.chats[body["id"]][1][0]))

	def chatsCallback(self, ch, method, properties, body):
		body = json.loads(str(body.decode('UTF-8')))
		print(body)
		
		res = {}
		if body["receptor"] > len(self.chats):
			res["error"] = "[Error] Receptor no valido"
		else:
			mensaje = [self.ultimoMensaje, self.chats[body["id"]][0], self.chats[body["receptor"]][0], body["timestamp"], body["valor"]]

			self.NuevoMensaje(0, body["id"], mensaje)
			self.NuevoMensaje(1, body["receptor"], mensaje)

			self.channelChat.basic_publish(exchange='chat', routing_key=self.chats[body["receptor"]][2], body=json.dumps(body))

			# "Broadcasting" 
			if self.chats[body["receptor"]][3] == 0:
				for cliente, _, key, cId in self.chats:
					self.NuevoMensaje(1, cId, mensaje)
					self.channelChat.basic_publish(exchange='chat', routing_key=key, body=json.dumps(body))

			self.LogChat(mensaje[3], mensaje[0], mensaje[1], mensaje[2], mensaje[4])

		return res


	def AgregarCliente(self, nombre, key):
		# userId : [nombre, [msgEnviado, msgRecibido], key]
		print("[Info] Cliente registrado - id:", str(len(self.chats)) + ", nombre:", nombre)
		userId = len(self.chats)
		self.chats.append( [nombre, [[], []], key, userId] )
		return userId

	def ClienteRegistrado(self, nombre):
		for nombreCliente, _, _, _ in self.chats:
			if nombreCliente == nombre:
				return True
		return False

	def LogChat(self, timestamp, id, emisor, receptor, mensaje):
		logs = open("logs.txt", "a+")

		data = "[" + timestamp + "] (" + str(id) + ") " + emisor + " - " +receptor + ": " + mensaje + "\n"
		print(data)

		logs.write(data)
		logs.close()

	def NuevoMensaje(self, tipo, cliente, mensaje):
		# tipo = 0 -> Cliente envió 
		# tipo = 1 -> Cliente recibió

		if tipo == 0:
			self.ultimoMensaje += 1

		self.chats[int(cliente)][1][tipo].append(mensaje)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("[Error] Al ejecutar el programa se debe indicar el hostname y puerto de escucha.")
		print("[Info] Ejemplo de ejecución: python server.py localhost 5672.")
		exit(0)

	ChatServer(sys.argv[1], int(sys.argv[2]))