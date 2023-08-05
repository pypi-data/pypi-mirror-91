# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: embedding.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='embedding.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x65mbedding.proto\"k\n\x05Input\x12\x10\n\x08model_id\x18\x01 \x02(\t\x12\x0c\n\x04text\x18\x02 \x03(\t\x12\x12\n\nbatch_size\x18\x03 \x01(\r\x12\x0c\n\x04mode\x18\x04 \x01(\t\x12\x0e\n\x06kwargs\x18\x05 \x01(\t\x12\x10\n\x08\x63ompress\x18\x06 \x01(\t\"X\n\tEmbedding\x12\x0c\n\x04\x64\x61ta\x18\x01 \x02(\x0c\x12\x1c\n\x04type\x18\x02 \x02(\x0e\x32\x0e.EmbeddingType\x12\r\n\x05shape\x18\x03 \x03(\r\x12\x10\n\x08\x63ompress\x18\x04 \x01(\t*&\n\rEmbeddingType\x12\t\n\x05\x44\x45NSE\x10\x00\x12\n\n\x06SPARSE\x10\x01\x32)\n\x07\x45ncoder\x12\x1e\n\x06\x65ncode\x12\x06.Input\x1a\n.Embedding\"\x00'
)

_EMBEDDINGTYPE = _descriptor.EnumDescriptor(
  name='EmbeddingType',
  full_name='EmbeddingType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DENSE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SPARSE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=218,
  serialized_end=256,
)
_sym_db.RegisterEnumDescriptor(_EMBEDDINGTYPE)

EmbeddingType = enum_type_wrapper.EnumTypeWrapper(_EMBEDDINGTYPE)
DENSE = 0
SPARSE = 1



_INPUT = _descriptor.Descriptor(
  name='Input',
  full_name='Input',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='model_id', full_name='Input.model_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='Input.text', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch_size', full_name='Input.batch_size', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='Input.mode', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kwargs', full_name='Input.kwargs', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compress', full_name='Input.compress', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=126,
)


_EMBEDDING = _descriptor.Descriptor(
  name='Embedding',
  full_name='Embedding',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Embedding.data', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='Embedding.type', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shape', full_name='Embedding.shape', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compress', full_name='Embedding.compress', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=216,
)

_EMBEDDING.fields_by_name['type'].enum_type = _EMBEDDINGTYPE
DESCRIPTOR.message_types_by_name['Input'] = _INPUT
DESCRIPTOR.message_types_by_name['Embedding'] = _EMBEDDING
DESCRIPTOR.enum_types_by_name['EmbeddingType'] = _EMBEDDINGTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), {
  'DESCRIPTOR' : _INPUT,
  '__module__' : 'embedding_pb2'
  # @@protoc_insertion_point(class_scope:Input)
  })
_sym_db.RegisterMessage(Input)

Embedding = _reflection.GeneratedProtocolMessageType('Embedding', (_message.Message,), {
  'DESCRIPTOR' : _EMBEDDING,
  '__module__' : 'embedding_pb2'
  # @@protoc_insertion_point(class_scope:Embedding)
  })
_sym_db.RegisterMessage(Embedding)



_ENCODER = _descriptor.ServiceDescriptor(
  name='Encoder',
  full_name='Encoder',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=258,
  serialized_end=299,
  methods=[
  _descriptor.MethodDescriptor(
    name='encode',
    full_name='Encoder.encode',
    index=0,
    containing_service=None,
    input_type=_INPUT,
    output_type=_EMBEDDING,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ENCODER)

DESCRIPTOR.services_by_name['Encoder'] = _ENCODER

# @@protoc_insertion_point(module_scope)
