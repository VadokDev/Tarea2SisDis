#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import sys
import pika
import uuid 

from datetime import datetime # interesante

class Cliente:

	def __init__(self, host, puerto):
		self.nombre = ""
		self.conn = pika.BlockingConnection(pika.ConnectionParameters(host, puerto))
		self.channel = self.conn.channel()

		self.channel.exchange_declare(exchange='login', exchange_type='direct')
		self.channel.exchange_declare(exchange='chat', exchange_type='direct')
		
		#threading.Thread(target=self.recibirMensajes, daemon=True).start()
		print("[Info] Conexión establecida con el servidor:", host + ':' + str(puerto))
		print("Mensaje enviado")

		self.Login()
		#self.connection.close()

		#self.cliente = chat.Cliente()
		#threading.Thread(target=self.recibirMensajes, daemon=True).start()
		#print("[Info] Sesión iniciada.")
	
		#self.enviarMensajes()

	def callback(self, ch, method, properties, body):
		print(" [x] %r:%r" % (method.routing_key, body))


#	def recibirMensajes(self):
#		result = self.channel.queue_declare(queue='', exclusive=True)
#		queue_name = result.method.queue
#		self.channel.queue_bind(exchange='chat', queue=queue_name, routing_key='login2')
#
#		print('[*] Waiting for logs. To exit press CTRL+C')
#
#		self.channel.start_consuming()
#
#		for mensaje in self.conn.Chat(self.cliente):
#			print("[" + mensaje.timestamp + "]", mensaje.emisor.nombre + ":", mensaje.valor)

	def Ayuda(self):
		print("[Info] El servidor de chat dispone de los siguientes 3 comandos:")
		print("\tclientes - Retorna la lista de clientes conectados con su respectivo id.")
		print("\thistorial - Retorna la lista de mensajes que ha enviado")
		print("\tmsg [idCliente] [mensaje] - Envía un mensaje al cliente con la id ingresada (sin corchetes)")

	def Login(self):
		error = 1
		msg = "1,"
		uid = str(uuid.uuid4())

		result = self.channel.queue_declare(queue='', exclusive=True)
		queue_name = result.method.queue

		while self.nombre == "" and error:
			self.nombre = input("[Info] Ingrese su nombre para acceder al chat: ")
			msg += uid + ","
			msg += self.nombre	
			key = uid+self.nombre
			key = str(key)
			#t1 = threading.Thread(target=self.resLogin, daemon=True)
			#t1.start()
			#t1.join()

			self.channel.queue_bind(exchange='chat', queue=queue_name, routing_key=key)
			self.channel.basic_publish(exchange='login', routing_key='login', body=msg)
			
		
			for _, _, res in self.channel.consume(queue_name):
				print(res)
				self.channel.cancel()
				break

			print(res)
			#res = #self.conn.Login(msg)
			#error = res.error
			#if error:
			#	print(res.errorMensaje)
		
		#self.cliente.nombre = res.cliente.nombre
		#self.cliente.id = res.cliente.id
	"""
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
			#except:
			#	print("[Error] Comando no válido.")
			#	self.Ayuda()

			texto = input()
		else: # Sí, esto es tan legal como el yield
			print("[Info] Hasta pronto!")
			exit(0)
	"""

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("[Error] Al ejecutar el programa se debe indicar el hostname y puerto del servidor.")
		print("[Info] Ejemplo de ejecución: python cliente.py localhost 5672.")
		exit(0)

	Cliente(sys.argv[1], int(sys.argv[2]))