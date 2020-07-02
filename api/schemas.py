from api.models import *
from api import ma
import simplejson as json

#DONE
class TipoParteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoParte
        include_relationships = True

#DONE
class ParteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Parte
        include_fk = True
        include_relationships = True
    id = ma.auto_field()
    nombre_parte = ma.auto_field()
    tipo_parte = ma.Nested(TipoParteSchema(exclude=('descripcion_tipo_parte','partes')))
    descripcion_parte = ma.auto_field()
    precio = ma.auto_field()

#DONE
class InventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventario
        include_fk = True
        include_relationships = True
    id = ma.auto_field()
    parte = ma.Nested(ParteSchema)
    cantidad = ma.auto_field()

#DONE
class TipoUsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoUsuario
        include_relationships = True

#DONE
class EmpleadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Empleado
        include_relationships = True

#DONE
class UsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        include_fk = True
        include_relationships = True
    id = ma.auto_field()
    nombre_usuario = ma.auto_field()
    tipo_usuario = ma.Nested(TipoUsuarioSchema(exclude=('descripcion','usuarios')))
    empleado = ma.Nested(EmpleadoSchema(exclude=('usuario',)))

#DONE
class VehiculoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Vehiculo
        include_fk = True
        include_relationships = True
    id = ma.auto_field()
    modelo = ma.auto_field()
    fecha_fabricacion = ma.auto_field()
    cliente_id = ma.auto_field()
    descripcion = ma.auto_field()
    fecha_registro = ma.auto_field()

#DONE
class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente
        include_relationships = True
    id = ma.auto_field()
    nombre = ma.auto_field()
    apellidos = ma.auto_field()
    email = ma.auto_field()
    telefono = ma.auto_field()
    fecha_registro = ma.auto_field()
    vehiculo = ma.Nested(VehiculoSchema(exclude=('cliente_id',)))

#DONE
class GarantiaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Garantia
        include_relationships = True

#DONE
class ReparacionDetalleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReparacionDetalle
        include_fk = True
    id = ma.auto_field()
    parte = ma.Nested(ParteSchema)
    reparacion_id = ma.auto_field()
    cantidad = ma.auto_field()

#DONE
class ReparacionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reparacion
        include_fk = True
        include_relationships = True
    id = ma.auto_field()
    fecha_realizacion = ma.auto_field()
    usuario = ma.Nested(UsuarioSchema)
    cliente = ma.Nested(ClienteSchema)
    garantia = ma.Nested(GarantiaSchema(exclude=('reparaciones',)))
    reparaciones_detalle = ma.Nested(ReparacionDetalleSchema(exclude=('reparacion_id',)),many=True)
    total = ma.auto_field()