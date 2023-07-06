import unittest
from datetime import datetime
import os

class DataBase:
    def __init__(self):
        self.index = 0
        self.Inventario = dict()
        self.Plataformas = ["Consola","PC","Móvil"]
        self.Generos = ["Acción","Aventura","Estrategia","MOBA","RPG","Shooter","Roguelike"]
        self.Perfiles = ["Administrador","Cliente"]
        self.Compras = []
        self.Ventas = []
    
    def updateGame(self,key,value):
        self.DataBase[key] = value

    def addGame(self,game):
        self.DataBase[game.id] = game
    
    def updateIndex(self):
        self.index += 1


    def showInventory(self):
        for item in self.Inventario:
            print(self.Inventario[item].toString())

    def listInventoryToSale(self):
        lista = []
        for item in self.Inventario:
            lista.append(self.Inventario[item].detailSaleProduct())
        return lista
    def Save(self):
        file = open("RegistroInventario.txt","w")
        for item in self.Inventario:
            texto = str(self.Inventario[item].writeFile()+"\n")
            if texto != "" and texto != "\n":
                file.write(texto)
        file.close()

        file = open("RegistroVentas.txt","w")
        for item in self.Ventas:
            texto = str(item.writeFile())+"\n"
            if texto != "" and texto != "\n":
                file.write(texto)
        file.close()
        texto = []
        for item in self.Compras:
            texto.append(str(item.writeFile())+"\n")
        with open("RegistroCompras.txt","w") as file:
            file.writelines(texto)

    def ReadFile(self):
        file = open("RegistroInventario.txt","r")
        for linea in file:
            id,title,platform,genre,priceBuy,priceSale,cant = linea.strip().split(',')
            self.Inventario[int(id)] = Game(id,title,priceBuy,priceSale,genre,platform,cant)
            self.index = max(self.index + 1,int(id)+1)
        file.close()

        file = open("RegistroVentas.txt","r")
        for linea in file:
            id,title,platform,genre,priceBuy,priceSale,cant = linea.strip().split(',')
            self.Ventas.append(Game(id,title,priceBuy,priceSale,genre,platform,cant))
        file.close()

        file = open("RegistroCompras.txt","r")
        for linea in file:
            id,title,platform,genre,priceBuy,priceSale,cant = linea.strip().split(',')
            self.Compras.append(Game(id,title,priceBuy,priceSale,genre,platform,cant))
        file.close()

    def reportTXT(self):
        formatoNombre = "%d-%m-%Y %H.%M.%S"
        carpeta = "Reportes"
        nombre = "Reporte_"+str(datetime.now().strftime(formatoNombre))+".txt"
        ruta_archivo = os.path.join(carpeta, nombre)
        os.makedirs(carpeta, exist_ok=True)
        file = open(ruta_archivo,"w")
        formato = "%d/%m/%Y %H:%M:%S"
        file.write(f"Fecha: {datetime.now().strftime(formato)}\n")
        file.write("------------------------------------------------------------------------------------------------------------")
        file.write("Reporte de Compras:\n")
        file.write(f"Cantidad de compras realizadas: {len(self.Compras)}.\n")
        cantJuegos = 0
        costo = 0
        detalle = ""
        for juego in self.Compras:
            cantJuegos += int(juego.count)
            costo += float(juego.priceBuy)*float(juego.count)
            detalle += juego.detailBuyToString()
        file.write(f"Cantidad de Juegos Comprados: {cantJuegos}\n")
        file.write(f"Costo total: $ {costo}.\nDetalle de Compra: \n"+detalle)

        file.write("\nReporte de Ventas\n")
        cantJuegos = 0
        costo = 0
        detalle = ""
        for juego in self.Ventas:
            cantJuegos += int(juego.count)
            costo += float(juego.priceSale)*float(juego.count)
            detalle += juego.detailSaleToString()
        file.write(f"Cantidad de Juegos Vendidos: {cantJuegos}\n")
        file.write(f"Venta total: $ {costo}.\nDetalle de la Venta: \n"+detalle)

        file.close()
        return nombre

class Game:
    def __init__(self, id, title, priceBuy, priceSale, genre, platform, count):
        self.id = id
        self.title = title
        self.priceBuy = priceBuy
        self.priceSale = priceSale
        self.genre = genre
        self.platform = platform
        self.count = count

    def __repr__(self):
        text = f"Producto:\n=> id: {self.id}\n=> title: {self.title}\n=> price buy/sale: {self.priceBuy}/{self.priceSale}\n=> platform: {self.platform}\n=> count: {self.count}"
        return text

    def toString(self):
        text = f"Juego {self.id}:\n=> Título: {self.title}\n=> Plataforma: {self.platform}\n=> Género: {self.genre}\n=> Precio Compra: {self.priceBuy}\n=> Precio Venta: {self.priceSale}\n=> Cantidad Disponible: {self.count}"
        return

    def detailBuyToString(self):
        text = f"=> Título: {self.title} - Plataforma: {self.platform} - Género: {self.genre} - Precio Compra: {self.priceBuy} - Cantidad: {self.count}\n"
        return text

    def detailSaleToString(self):
        text = f"=> Título: {self.title} - Plataforma: {self.platform} - Género: {self.genre} - Precio Venta: {self.priceSale} - Cantidad: {self.count}\n"
        return text

    def detailSaleProduct(self):
        text = f"Título: {self.title} - Plataforma: {self.platform} - Género: {self.genre} - Precio Venta: {self.priceSale} - Cantidad: {self.count}"
        return text

    def writeFile(self):
        text =  f"{self.id},{self.title},{self.platform},{self.genre},{self.priceBuy},{self.priceSale},{self.count}"
        return text


db = DataBase()
db.ReadFile()

################## FUNCIONES DE PRUEBA #################################

def validarJuego(game):
    if not isinstance(game.title, str) or game.title == "":
        return False
    if not isinstance(game.priceBuy, (int, float)) or game.priceBuy <= 0:
        return False
    if not isinstance(game.priceSale, (int, float)) or game.priceSale <= 0:
        return False
    if not isinstance(game.count, int) or game.count <= 0:
        return False
    if not isinstance(game.genre, int):
        return False
    if not isinstance(game.platform,int):
        return False
    return True


class Pruebas(unittest.TestCase):

    # TESTS CON RESPECTO A QUE LOS DATOS QUE DEBE TENER EL JUEGO SEAN VALIDOS

    def test_tituloNumeros(self):
        juego = Game(0,1234,10,20,"RPG","Consola",10)
        assert validarJuego(juego) == False

    def test_tituloVacio(self):
        juego = Game(0,"",10,20,"RPG","Consola",10)
        assert validarJuego(juego) == False
    
    def test_compraInvalida1(self):
        juego = Game(0,"Compra Invalida igual a 0",0,20,"RPG","Consola",10)
        assert validarJuego(juego) == False

    def test_compraInvalida2(self):
        juego = Game(0,"Compra Invalida menor a 0",0,20,"RPG","Consola",10)
        assert validarJuego(juego) == False

    def test_compraInvalida3(self):
        juego = Game(0,"Compra Invalida, string","10",20,"RPG","Consola",10)
        assert validarJuego(juego) == False
    
    def test_ventaInvalida1(self):
        juego = Game(0,"Venta Invalida igual a 0",10,0,"RPG","Consola",10)
        assert validarJuego(juego) == False

    def test_ventaInvalida2(self):
        juego = Game(0,"Venta Invalida menor a 0",10,-20,"RPG","Consola",10)
        assert validarJuego(juego) == False

    def test_ventaInvalida3(self):
        juego = Game(0,"Venta Invalida, string",10,"20","RPG","Consola",10)
        assert validarJuego(juego) == False
    
    def test_generoInvalido(self):
        juego = Game(0,"Género Invalido, número en vez de string",10,"20",0,"Consola",10)
        assert validarJuego(juego) == False
    
    def test_consolaInvalida(self):
        juego = Game(0,"Consola Invalida, número en vez de string",10,"20","RPG",0,10)
        assert validarJuego(juego) == False


if __name__ == '__main__':
    unittest.main()