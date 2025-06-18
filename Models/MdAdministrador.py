from typing import Self
import pyodbc
import sys
sys.path.append("Repository")
from ClDataBase import ClDataBase
from EnEnum import EnTipoDocumento
from MdInicioSesion import MdInicioSesion
from MdUsuario import MdUsuario


class MdAdministrador(MdUsuario):
    def __init__(self, tipoDocumento, documento: str) -> None:
        super().__init__(tipoDocumento, documento)

    def ObtenerPorId(id: int) -> Self:
        cursor = ClDataBase.OpenConnection()
        cursor.execute(f"SELECT * FROM MdAdministrador WHERE Id={id}")
        objData = cursor.fetchone()
        ClDataBase.CloseConnection(cursor)
        return MdAdministrador.__CargarRegistro(objData)
    
    def __CargarRegistro(row: pyodbc.Row) -> Self:
        if row == None:
            return None
        objResult = MdAdministrador(row.TipoDocumento, row.Documento)
        objResult.EstablecerId(row.Id)
        objResult.PrimerNombre = row.PrimerNombre
        objResult.SegundoNombre = row.SegundoNombre
        objResult.PrimerApellido = row.PrimerApellido
        objResult.SegundoApellido = row.SegundoApellido
        objResult.Email = row.Email
        return objResult

    def InsertarRegistro(self) -> None:
        cursor = ClDataBase.OpenConnection()
        strInsert = f"""INSERT INTO MdAdministrador
           (TipoDocumento
           ,Documento
           ,PrimerNombre
           ,SegundoNombre
           ,PrimerApellido
           ,SegundoApellido
           ,Email
           ,Password
           ,Activo)
     VALUES
           ({self.TipoDocumento}
           ,'{self.Documento}'
           ,'{self.PrimerNombre}'
           ,'{self.SegundoNombre}'
           ,'{self.PrimerApellido}'
           ,'{self.SegundoApellido}'
           ,'{self.Email}'
           ,'123'
           ,1)"""
        cursor.execute(strInsert)
        cursor.commit()
        ClDataBase.CloseConnection(cursor)

    def ActualizarRegistro(self):
        cursor = ClDataBase.OpenConnection()
        strUpdate = f"""UPDATE MdAdministrador SET 
            TipoDocumento= {self.TipoDocumento},
            Documento= '{self.Documento}',
            PrimerNombre= '{self.PrimerNombre}',
            SegundoNombre= '{self.SegundoNombre}', 
            PrimerApellido= '{self.PrimerApellido}', 
            SegundoApellido= '{self.SegundoApellido}', 
            Email= '{self.Email}'
            WHERE Id= {self.Id}"""  
        cursor.execute(strUpdate)
        cursor.commit()
        ClDataBase.CloseConnection(cursor)

    def ValidarUsuario(mdInicioSesion : MdInicioSesion) -> bool: 
        cursor = ClDataBase.OpenConnection()
        strSearch = f"SELECT Id FROM MdAdministrador WHERE Documento='{mdInicioSesion.Usuario}' AND Password='{mdInicioSesion.Password}' AND Activo=1"
        cursor.execute(strSearch)
        objValor = cursor.fetchval()
        return objValor != None