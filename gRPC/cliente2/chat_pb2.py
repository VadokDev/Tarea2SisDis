# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chat.proto',
  package='asynch',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\nchat.proto\x12\x06\x61synch\"{\n\x07Mensaje\x12\n\n\x02id\x18\x01 \x01(\r\x12\x1f\n\x06\x65misor\x18\x02 \x01(\x0b\x32\x0f.asynch.Cliente\x12!\n\x08receptor\x18\x03 \x01(\x0b\x32\x0f.asynch.Cliente\x12\r\n\x05valor\x18\x04 \x01(\t\x12\x11\n\ttimestamp\x18\x05 \x01(\t\"%\n\x07\x43liente\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0e\n\x06nombre\x18\x02 \x01(\t\"6\n\x0fMensajeRecibido\x12\r\n\x05\x65rror\x18\x01 \x01(\r\x12\x14\n\x0c\x65rrorMensaje\x18\x02 \x01(\t\"\x1a\n\x08Registro\x12\x0e\n\x06nombre\x18\x01 \x01(\t\"Z\n\x11RegistroRespuesta\x12\r\n\x05\x65rror\x18\x01 \x01(\r\x12\x14\n\x0c\x65rrorMensaje\x18\x02 \x01(\t\x12 \n\x07\x63liente\x18\x03 \x01(\x0b\x32\x0f.asynch.Cliente\"\x0e\n\x0cMensajeVacio2\x9a\x02\n\nChatServer\x12\x38\n\rListaClientes\x12\x14.asynch.MensajeVacio\x1a\x0f.asynch.Cliente0\x01\x12\x35\n\x0fObtenerMensajes\x12\x0f.asynch.Cliente\x1a\x0f.asynch.Mensaje0\x01\x12\x39\n\rEnviarMensaje\x12\x0f.asynch.Mensaje\x1a\x17.asynch.MensajeRecibido\x12*\n\x04\x43hat\x12\x0f.asynch.Cliente\x1a\x0f.asynch.Mensaje0\x01\x12\x34\n\x05Login\x12\x10.asynch.Registro\x1a\x19.asynch.RegistroRespuestab\x06proto3')
)




_MENSAJE = _descriptor.Descriptor(
  name='Mensaje',
  full_name='asynch.Mensaje',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='asynch.Mensaje.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='emisor', full_name='asynch.Mensaje.emisor', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='receptor', full_name='asynch.Mensaje.receptor', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='valor', full_name='asynch.Mensaje.valor', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='asynch.Mensaje.timestamp', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=145,
)


_CLIENTE = _descriptor.Descriptor(
  name='Cliente',
  full_name='asynch.Cliente',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='asynch.Cliente.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nombre', full_name='asynch.Cliente.nombre', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=184,
)


_MENSAJERECIBIDO = _descriptor.Descriptor(
  name='MensajeRecibido',
  full_name='asynch.MensajeRecibido',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='asynch.MensajeRecibido.error', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errorMensaje', full_name='asynch.MensajeRecibido.errorMensaje', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=186,
  serialized_end=240,
)


_REGISTRO = _descriptor.Descriptor(
  name='Registro',
  full_name='asynch.Registro',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nombre', full_name='asynch.Registro.nombre', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=242,
  serialized_end=268,
)


_REGISTRORESPUESTA = _descriptor.Descriptor(
  name='RegistroRespuesta',
  full_name='asynch.RegistroRespuesta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='asynch.RegistroRespuesta.error', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errorMensaje', full_name='asynch.RegistroRespuesta.errorMensaje', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cliente', full_name='asynch.RegistroRespuesta.cliente', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=270,
  serialized_end=360,
)


_MENSAJEVACIO = _descriptor.Descriptor(
  name='MensajeVacio',
  full_name='asynch.MensajeVacio',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=362,
  serialized_end=376,
)

_MENSAJE.fields_by_name['emisor'].message_type = _CLIENTE
_MENSAJE.fields_by_name['receptor'].message_type = _CLIENTE
_REGISTRORESPUESTA.fields_by_name['cliente'].message_type = _CLIENTE
DESCRIPTOR.message_types_by_name['Mensaje'] = _MENSAJE
DESCRIPTOR.message_types_by_name['Cliente'] = _CLIENTE
DESCRIPTOR.message_types_by_name['MensajeRecibido'] = _MENSAJERECIBIDO
DESCRIPTOR.message_types_by_name['Registro'] = _REGISTRO
DESCRIPTOR.message_types_by_name['RegistroRespuesta'] = _REGISTRORESPUESTA
DESCRIPTOR.message_types_by_name['MensajeVacio'] = _MENSAJEVACIO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Mensaje = _reflection.GeneratedProtocolMessageType('Mensaje', (_message.Message,), {
  'DESCRIPTOR' : _MENSAJE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:asynch.Mensaje)
  })
_sym_db.RegisterMessage(Mensaje)

Cliente = _reflection.GeneratedProtocolMessageType('Cliente', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTE,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:asynch.Cliente)
  })
_sym_db.RegisterMessage(Cliente)

MensajeRecibido = _reflection.GeneratedProtocolMessageType('MensajeRecibido', (_message.Message,), {
  'DESCRIPTOR' : _MENSAJERECIBIDO,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:asynch.MensajeRecibido)
  })
_sym_db.RegisterMessage(MensajeRecibido)

Registro = _reflection.GeneratedProtocolMessageType('Registro', (_message.Message,), {
  'DESCRIPTOR' : _REGISTRO,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:asynch.Registro)
  })
_sym_db.RegisterMessage(Registro)

RegistroRespuesta = _reflection.GeneratedProtocolMessageType('RegistroRespuesta', (_message.Message,), {
  'DESCRIPTOR' : _REGISTRORESPUESTA,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:asynch.RegistroRespuesta)
  })
_sym_db.RegisterMessage(RegistroRespuesta)

MensajeVacio = _reflection.GeneratedProtocolMessageType('MensajeVacio', (_message.Message,), {
  'DESCRIPTOR' : _MENSAJEVACIO,
  '__module__' : 'chat_pb2'
  # @@protoc_insertion_point(class_scope:asynch.MensajeVacio)
  })
_sym_db.RegisterMessage(MensajeVacio)



_CHATSERVER = _descriptor.ServiceDescriptor(
  name='ChatServer',
  full_name='asynch.ChatServer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=379,
  serialized_end=661,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListaClientes',
    full_name='asynch.ChatServer.ListaClientes',
    index=0,
    containing_service=None,
    input_type=_MENSAJEVACIO,
    output_type=_CLIENTE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ObtenerMensajes',
    full_name='asynch.ChatServer.ObtenerMensajes',
    index=1,
    containing_service=None,
    input_type=_CLIENTE,
    output_type=_MENSAJE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='EnviarMensaje',
    full_name='asynch.ChatServer.EnviarMensaje',
    index=2,
    containing_service=None,
    input_type=_MENSAJE,
    output_type=_MENSAJERECIBIDO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Chat',
    full_name='asynch.ChatServer.Chat',
    index=3,
    containing_service=None,
    input_type=_CLIENTE,
    output_type=_MENSAJE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Login',
    full_name='asynch.ChatServer.Login',
    index=4,
    containing_service=None,
    input_type=_REGISTRO,
    output_type=_REGISTRORESPUESTA,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CHATSERVER)

DESCRIPTOR.services_by_name['ChatServer'] = _CHATSERVER

# @@protoc_insertion_point(module_scope)
