import sys
from EnEnum import EnTipoDocumento

from MdInicioSesion import MdInicioSesion
sys.path.append("Repository")
import pyodbc
from typing import (List, Self)
from MdUsuario import MdUsuario

from ClDataBase import ClDataBase

class MdDocente(MdUsuario):

    TarjetaProfesional : str

    def __init__(self, tipoDocumento, documento: str) -> None:
        super().__init__(tipoDocumento, documento)

    def ObtenerTodos() -> List[Self]:
        cursor = ClDataBase.OpenConnection()
        cursor.execute("SELECT * FROM MdDocente")
        cursorData = cursor.fetchall()
        listResult = list()
        for i in cursorData:
            listResult.append(MdDocente.__CargarRegistro(i))
        ClDataBase.CloseConnection(cursor)
        return listResult
    
    def ObtenerPorId(id: int) -> Self:
        cursor = ClDataBase.OpenConnection()
        cursor.execute(f"SELECT * FROM MdDocente WHERE Id={id}")
        objData = cursor.fetchone()
        ClDataBase.CloseConnection(cursor)
        return MdDocente.__CargarRegistro(objData)
        
    def __CargarRegistro(row: pyodbc.Row) -> Self:
        if row == None:
            return None
        objResult = MdDocente(row.TipoDocumento, row.Documento)
        objResult.EstablecerId(row.Id)
        objResult.PrimerNombre = row.PrimerNombre
        objResult.SegundoNombre = row.SegundoNombre
        objResult.PrimerApellido = row.PrimerApellido
        objResult.SegundoApellido = row.SegundoApellido
        objResult.Email = row.Email
        objResult.TarjetaProfesional = row.TarjetaProfesional
        return objResult
    
    def InsertarRegistro(self) -> None:
        cursor = ClDataBase.OpenConnection()
        strInsert = f"""INSERT INTO MdDocente
           (TipoDocumento
           ,Documento
           ,PrimerNombre
           ,SegundoNombre
           ,PrimerApellido
           ,SegundoApellido
           ,Email
           ,Password
           ,Activo
           ,TarjetaProfesional)
     VALUES
           ({self.TipoDocumento}
           ,'{self.Documento}'
           ,'{self.PrimerNombre}'
           ,'{self.SegundoNombre}'
           ,'{self.PrimerApellido}'
           ,'{self.SegundoApellido}'
           ,'{self.Email}'
           ,'123'
           ,1
           ,'{self.TarjetaProfesional}')"""
        cursor.execute(strInsert)
        cursor.commit()
        ClDataBase.CloseConnection(cursor)

    def EliminarRegistro(self):
        cursor = ClDataBase.OpenConnection()
        strDelete = f"""DELETE FROM MdDocente WHERE Id={self.Id}"""
        cursor.execute(strDelete)
        cursor.commit()
        ClDataBase.CloseConnection(cursor)

    def ActualizarRegistro(self):
        cursor = ClDataBase.OpenConnection()
        strUpdate = f"""UPDATE MdDocente SET 
            TipoDocumento= {self.TipoDocumento},
            Documento= '{self.Documento}',
            PrimerNombre= '{self.PrimerNombre}',
            SegundoNombre= '{self.SegundoNombre}', 
            PrimerApellido= '{self.PrimerApellido}', 
            SegundoApellido= '{self.SegundoApellido}', 
            Email= '{self.Email}', 
            TarjetaProfesional= '{self.TarjetaProfesional}'
            WHERE Id= {self.Id}"""  
        cursor.execute(strUpdate)
        cursor.commit()
        ClDataBase.CloseConnection(cursor)

    def ValidarUsuario(mdInicioSesion : MdInicioSesion) -> bool: 
        cursor = ClDataBase.OpenConnection()
        strSearch = f"SELECT Id FROM MdDocente WHERE Documento='{mdInicioSesion.Usuario}' AND Password='{mdInicioSesion.Password}' AND Activo=1"
        cursor.execute(strSearch)
        objValor = cursor.fetchval()
        return objValor != None
    