#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import sys
import pika
import uuid 
import json
import time

from random import choice, randint
from datetime import datetime # interesante

class Cliente:

	def __init__(self, host, puerto, modo):
		self.host = host
		self.modo = modo
		self.puerto = puerto
		self.nombre = ""
		self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, heartbeat=0))
		self.channelLogin = self.conn.channel()
		self.channelServices = self.conn.channel()
		self.channelChat = self.conn.channel()
		self.uid = str(uuid.uuid4())
		self.id = 0
		self.key = ""
		self.channelLogin.exchange_declare(exchange='login', exchange_type='direct')
		self.channelServices.exchange_declare(exchange='services', exchange_type='direct')
		self.channelChat.exchange_declare(exchange='chat', exchange_type='direct')

		print("[Info] Conexión establecida con el servidor:", host + ':' + str(puerto))

		self.Login()
		print("[Info] Sesión iniciada.")
		
		threading.Thread(target=self.recibirMensajes, daemon=True).start()
		
		if self.modo == 0:
			self.enviarMensajesAuto()
		else:
			self.enviarMensajes()

	def mensajesCallBack(self, ch, method, properties, body):
		data = json.loads(body)
		print("[" + data["timestamp"] + "]", data["nombre"] + ":", data["valor"])

	def recibirMensajes(self):
		conn = pika.BlockingConnection(pika.ConnectionParameters(self.host, heartbeat=0))
		channel = conn.channel()
		colaChats = self.CrearCola(channel)
		channel.exchange_declare(exchange='chat', exchange_type='direct')
		channel.queue_bind(exchange='chat', queue=colaChats, routing_key=self.key)
		channel.basic_consume(queue=colaChats, on_message_callback=self.mensajesCallBack, auto_ack=True)
		channel.start_consuming()

	def Ayuda(self):
		print("[Info] El servidor de chat dispone de los siguientes 3 comandos:")
		print("\tclientes - Retorna la lista de clientes conectados con su respectivo id.")
		print("\thistorial - Retorna la lista de mensajes que ha enviado")
		print("\tmsg [idCliente] [mensaje] - Envía un mensaje al cliente con la id ingresada (sin corchetes)")

	def CrearCola(self, channel):
		return channel.queue_declare(queue='', exclusive=True).method.queue

	def Login(self):
		colaLogin = self.CrearCola(self.channelLogin)
		error = 1
		data = {"uid": self.uid, "action": "login"}
		while self.nombre == "" or error:
			if self.modo == 0:
				self.nombre = ''.join(choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_<>!#$%&/(") for i in range(randint(1, 20)))
			else:
				self.nombre = input("[Info] Ingrese su nombre para acceder al chat: ")
			data["key"] = self.uid + self.nombre[:15]
			data["nombre"] = self.nombre

			self.channelLogin.queue_bind(exchange='login', queue=colaLogin, routing_key=data["key"])
			self.channelLogin.basic_publish(exchange='login', routing_key='login', body=json.dumps(data))
		
			_, _, res =  next(self.channelLogin.consume(colaLogin))
			res = json.loads(res)

			if "error" in res:
				print(res["error"])
			else:
				error = 0

		self.channelLogin.queue_unbind(exchange='login', queue=colaLogin, routing_key=data["key"])
		self.key = data["key"]
		self.id = res["id"]
		self.colaServices = self.CrearCola(self.channelServices)
		self.channelServices.queue_bind(exchange='services', queue=self.colaServices, routing_key=data["key"])
	
	def MensajeEnviado(self, r):
		if r.result().error == 1:
			print(r.result().errorMensaje)

	def enviarMensajes(self):
		self.Ayuda()
		texto = input()

		while texto != "salir":
			data = texto.split()
			enviar = {"key": self.key}
			#try:
			if data[0] == "msg":
				enviar["id"] = self.id
				enviar["receptor"] = int(data[1])
				enviar["nombre"] = self.nombre
				enviar["valor"] = data[2]
				enviar["timestamp"] = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
				self.channelChat.basic_publish(exchange='chat', routing_key="chat", body=json.dumps(enviar))
			elif data[0] == "clientes":
				enviar["accion"] = "1"
				self.channelServices.basic_publish(exchange='services', routing_key="services", body=json.dumps(enviar))
				
				_, _, res = next(self.channelServices.consume(self.colaServices))

				res = json.loads(json.loads(res))

				for i in res:
					print(i[1], i[0])

			elif data[0] == "historial":
				print("[Server] Lista de mensajes enviados al servidor de chat")
				
				enviar["accion"] = "2"
				enviar["id"] = self.id
				self.channelServices.basic_publish(exchange='services', routing_key="services", body=json.dumps(enviar))
				
				_, _, res =  next(self.channelServices.consume(self.colaServices))
				res = json.loads(str(res.decode('UTF-8')))

				for i in res:
					print("[" + i[3] + "] (" + str(i[0]) + ") -", i[2] + ":", i[4]) 
			else: 
				self.Ayuda()
			#except:
			#	print("[Error] Comando no válido.")
			#	self.Ayuda()

			texto = input()
		else: # Sí, esto es tan legal como el yield
			print("[Info] Hasta pronto!")
			self.conn.close()
			exit(0)
	
	def enviarMensajesAuto(self):
		# Temazo
		milHoras = ["Hace frío y estoy lejos de casa", "Hace tiempo que estoy sentado sobre esta piedra", "Yo me pregunto", "Para que sirven las guerras", "Tengo un cohete en mi pantalón", "Vos estás tan fría como la nieve a mi alrededor", "Vos estás tan blanca, que yo no se que hacer", "La otra noche te esperé", "bajo la lluvia dos horas", "Mil horas como un perro", "Y cuando llegaste me miraste", "y me dijiste loco", "Estás mojado, ya no te quiero", "En el circo vos ya sos una estrella", "Una estrella roja que todo se lo imagina", "Si te preguntan, vos no me conocías", "No, no", "Tengo un cohete en mi pantalón", "Vos estás tan fría como la nieve a mi alrededor", "Vos estás tan blanca, que yo no se que hacer", "Te esperé bajo la lluvia", "No, no, no, no", "La otra noche te esperé", "bajo la lluvia dos horas", "Mil horas como un perro", "Y cuando llegaste me miraste", "y me dijiste loco", "Estás mojado, ya no te quiero", "La otra noche te esperé", "bajo la lluvia dos horas", "Mil horas como un perro", "Y cuando llegaste me miraste", "y me dijiste loco", "Estás mojado, ya no te quiero"]
		accion = 1
		lastId = 0

		while accion != 0:
			accion = randint(0, 30)
			data = texto.split()
			enviar = {"key": self.key}
			#try:
			if accion > 0 and accion <= 10:
				enviar["id"] = self.id
				enviar["receptor"] = randint(0, lastId)
				enviar["nombre"] = self.nombre
				enviar["valor"] = milHoras[randint(0, len(milHoras) - 1)]
				enviar["timestamp"] = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
				self.channelChat.basic_publish(exchange='chat', routing_key="chat", body=json.dumps(enviar))
			elif accion > 10 and accion <= 20:
				enviar["accion"] = "1"
				self.channelServices.basic_publish(exchange='services', routing_key="services", body=json.dumps(enviar))
				
				_, _, res = next(self.channelServices.consume(self.colaServices))

				res = json.loads(json.loads(res))

				for i in res:
					print(i[1], i[0])
					lastId = int(i[1])

			elif accion > 20 and accion <= 30:
				print("[Server] Lista de mensajes enviados al servidor de chat")
				
				enviar["accion"] = "2"
				enviar["id"] = self.id
				self.channelServices.basic_publish(exchange='services', routing_key="services", body=json.dumps(enviar))
				
				_, _, res =  next(self.channelServices.consume(self.colaServices))
				res = json.loads(str(res.decode('UTF-8')))

				for i in res:
					print("[" + i[3] + "] (" + str(i[0]) + ") -", i[2] + ":", i[4]) 
			time.sleep(2)
		print("[Info] Hasta pronto!")
		self.conn.close()
		exit(0)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("[Error] Al ejecutar el programa se debe indicar el hostname y puerto del servidor.")
		print("[Info] Ejemplo de ejecución: python cliente.py localhost 5672.")
		exit(0)

	Cliente(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))