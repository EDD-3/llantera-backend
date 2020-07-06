from datetime import datetime, timedelta
from api import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(64),unique=True)
    contrasena = db.Column(db.String(255))
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'))
    empleado = db.relationship("Empleado", back_populates="usuario")
    tipo_usuario_id = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id', ondelete='SET NULL'), nullable=True)
    reparaciones = db.relationship('Reparacion', backref='usuario', cascade="all, delete")

class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64))
    apellidos = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    fecha_contratacion = db.Column(db.DateTime, nullable=False, default=datetime.now)
    telefono = db.Column(db.String(10),unique=True)
    direccion = db.Column(db.String(255))
    usuario = db.relationship("Usuario", uselist=False, back_populates="empleado", cascade="all, delete")

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    id = db.Column(db.Integer, primary_key=True)
    denominacion_usuario = db.Column(db.String(64))
    descripcion = db.Column(db.String(128))
    usuarios = db.relationship('Usuario',backref='tipo_usuario')

class Reparacion(db.Model):
    __tablename__ = 'reparacion'
    id = db.Column(db.Integer, primary_key=True)
    fecha_realizacion = db.Column(db.DateTime, nullable=False, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete='SET NULL'), nullable=True)
    garantia_id = db.Column(db.Integer, db.ForeignKey('garantia.id', ondelete='SET NULL'), nullable=True)
    reparaciones_detalle = db.relationship('ReparacionDetalle',backref='reparacion', cascade="all, delete")
    total = db.Column(db.Numeric(precision=2))

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64))
    apellidos = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    telefono = db.Column(db.String(10),unique=True)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.now)
    vehiculo = db.relationship("Vehiculo", uselist=False, back_populates="cliente", cascade="all, delete")
    reparaciones = db.relationship('Reparacion',backref='cliente')

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(64))
    fecha_fabricacion = db.Column(db.Date)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    cliente = db.relationship("Cliente", back_populates="vehiculo")
    descripcion = db.Column(db.String(128))
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Garantia(db.Model):
    __tablename__ = 'garantia'
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=datetime.now)
    fecha_vencimiento = db.Column(db.DateTime, nullable=False, default=datetime.now()+timedelta(days=15.0))
    reparaciones = db.relationship('Reparacion', backref='garantia')

class ReparacionDetalle(db.Model):
    __tablename__ = 'reparacion_detalle'
    id = db.Column(db.Integer, primary_key=True)
    parte_id = db.Column(db.Integer, db.ForeignKey('parte.id', ondelete='SET NULL'), nullable=True)
    reparacion_id = db.Column(db.Integer, db.ForeignKey('reparacion.id', ondelete='SET NULL'), nullable=True)
    cantidad = db.Column(db.Integer)

class Parte(db.Model):
    __tablename__ = 'parte'
    id = db.Column(db.Integer, primary_key=True)
    nombre_parte = db.Column(db.String(64))
    tipo_parte_id = db.Column(db.Integer, db.ForeignKey('tipo_parte.id', ondelete='SET NULL'), nullable=True)
    descripcion_parte = db.Column(db.String(128))
    precio = db.Column(db.Numeric(precision=2))
    reparaciones_detalle = db.relationship('ReparacionDetalle', backref='parte')
    inventario = db.relationship("Inventario", uselist=False, back_populates="parte", cascade=("all, delete"))

class TipoParte(db.Model):
    __tablename__ = 'tipo_parte'
    id = db.Column(db.Integer, primary_key=True)
    denominacion_parte = db.Column(db.String(64))
    descripcion_tipo_parte = db.Column(db.String(128))
    partes = db.relationship('Parte',backref='tipo_parte')

class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    parte_id = db.Column(db.Integer, db.ForeignKey('parte.id'))
    cantidad = db.Column(db.Integer)
    parte = db.relationship("Parte", back_populates="inventario")