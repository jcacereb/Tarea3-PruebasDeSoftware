from datetime import datetime
import msvcrt

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
            id,title,platform,gender,priceBuy,priceSale,cant = linea.strip().split(',')
            self.Inventario[int(id)] = Game(id,title,priceBuy,priceSale,gender,platform,cant)
            self.index = max(self.index + 1,int(id)+1)
        file.close()

        file = open("RegistroVentas.txt","r")
        for linea in file:
            id,title,platform,gender,priceBuy,priceSale,cant = linea.strip().split(',')
            self.Ventas.append(Game(id,title,priceBuy,priceSale,gender,platform,cant))
        file.close()

        file = open("RegistroCompras.txt","r")
        for linea in file:
            id,title,platform,gender,priceBuy,priceSale,cant = linea.strip().split(',')
            self.Compras.append(Game(id,title,priceBuy,priceSale,gender,platform,cant))
        file.close()

    def reportTXT(self):
        formatoNombre = "%d-%m-%Y %H.%M.%S"
        nombre = "Reporte_"+str(datetime.now().strftime(formatoNombre))+".txt"
        file = open(nombre,"w")
        formato = "%d/%m/%Y %H:%M:%S"
        file.write(f"Fecha: {datetime.now().strftime(formato)}\n\n")
        file.write("Reporte de Compras\n")
        file.write(f"=> Cantidad de Compras: {len(self.Compras)} compras realizadas.\n")
        cantJuegos = 0
        costo = 0
        detalle = ""
        for juego in self.Compras:
            cantJuegos += int(juego.count)
            costo += float(juego.priceBuy)*float(juego.count)
            detalle += juego.detailBuyToString()
        file.write(f"=> Cantidad de Juegos Comprados: {cantJuegos} juegos.\n")
        file.write(f"=> Costo total: $ {costo}.\n\n Detalle de Compra: \n"+detalle)

        file.write("\nReporte de Ventas\n")
        cantJuegos = 0
        costo = 0
        detalle = ""
        for juego in self.Ventas:
            cantJuegos += int(juego.count)
            costo += float(juego.priceSale)*float(juego.count)
            detalle += juego.detailSaleToString()
        file.write(f"=> Cantidad de Juegos Vendidos: {cantJuegos} juegos.\n")
        file.write(f"=> Venta total: $ {costo}.\n\n Detalle de la Venta: \n"+detalle)

        file.close()
        return nombre

class Game:
    def __init__(self, id, title, priceBuy, priceSale, gender, platform, count):
        self.id = id
        self.title = title
        self.priceBuy = priceBuy
        self.priceSale = priceSale
        self.gender = gender
        self.platform = platform
        self.count = count

    def __repr__(self):
        return f"Producto:\n=> id: {self.id}\n=> title: {self.title}\n=> price buy/sale: {self.priceBuy}/{self.priceSale}\n=> platform: {self.platform}\n=> count: {self.count}"

    def toString(self):
        return f"Juego {self.id}:\n=> Título: {self.title}\n=> Plataforma: {self.platform}\n=> Género: {self.gender}\n=> Precio Compra: {self.priceBuy}\n=> Precio Venta: {self.priceSale}\n=> Cantidad Disponible: {self.count}"

    def detailBuyToString(self):
        return f"=> Título: {self.title} - Plataforma: {self.platform} - Género: {self.gender} - Precio Compra: {self.priceBuy} - Cantidad: {self.count}\n"

    def detailSaleToString(self):
        return f"=> Título: {self.title} - Plataforma: {self.platform} - Género: {self.gender} - Precio Venta: {self.priceSale} - Cantidad: {self.count}\n"

    def detailSaleProduct(self):
        return f"Título: {self.title} - Plataforma: {self.platform} - Género: {self.gender} - Precio Venta: {self.priceSale} - Cantidad: {self.count}"

    def writeFile(self):
        return f"{self.id},{self.title},{self.platform},{self.gender},{self.priceBuy},{self.priceSale},{self.count}"


def input_options(options, campo):
    print(campo)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        try:
            key = msvcrt.getch()
            key = key.decode("utf-8")

            if key.isdigit() and int(key) in range(1, len(options) + 1):
                index = int(key) - 1
                return options[index]
        except ValueError:
            pass

db = DataBase()
db.ReadFile()

def validGame(game):
    if not isinstance(game.title, str) or game.title == "":
        return False
    if not isinstance(game.priceBuy, (int, float)) or game.priceBuy <= 0:
        return False
    if not isinstance(game.priceSale, (int, float)) or game.priceSale <= 0:
        return False
    if not isinstance(game.count, int) or game.count <= 0:
        return False
    return True

def registerGame():
    print("Ingrese los siguientes datos:")
    title = input("Título: ")
    priceBuy = float(input("Precio de Compra: "))
    priceSale = float(input("Precio de Venta: "))
    genero = input_options(db.Generos, "Seleccione un género:")
    platform = input_options(db.Plataformas, "Selecciona una plataforma:")
    cant = int(input("Cantidad: "))
    id = db.index
    game = Game(id, title, priceBuy, priceSale, genero, platform, cant)
    addGameToInventory(id, game)

def addGameToInventory(id, game):
    if id in db.Inventario:
        juego = db.Inventario[id]
        juego.count += game.count
    else:
        if validGame(game):
            db.Inventario[id] = game
            db.updateIndex()
            db.Compras.append(game)
            print("Nuevo juego agregado al inventario.")
        else:
            print("Datos inválidos, por favor intentar de nuevo.")

def buyGame():
    juegoSeleccionado = input_options(db.listInventoryToSale(), "Ingrese id del juego a comprar:")
    cantidad = int(input("Cantidad a comprar: "))

    juego, valid, sms = validVenta(juegoSeleccionado, cantidad)
    if valid:
        respuesta = DoSale(juego, cantidad)
        print(respuesta)
    else:
        print("Notificación:", sms)

def DoSale(juego, cantidad):
    respaldo = juego.count
    juego.count = cantidad
    db.Ventas.append(juego)
    juego.count = int(respaldo) - int(cantidad)
    db.Inventario[juego.id] = juego
    return "Compra realizada, muchas gracias."

def validVenta(juegoSeleccionado, cantidad):
    if cantidad <= 0:
        return {}, False, "Ingrese una cantidad mayor que 0"
    
    for key, juego in db.Inventario.items():
        if juego.detailSaleProduct() == juegoSeleccionado:
            if int(juego.count) < cantidad:
                return juego, False, "No hay stock suficiente"
            break
    
    return juego, True, "ok"

perfilActual = input_options(db.Perfiles, "Ingresar como:")

def show_MenuAdmin():
    opciones = ["Registrar producto", "Ver catálogo de juegos", "Generar reporte", "Cerrar sesión"]
    opcion = input_options(opciones, "\nAcciones disponibles:")
    if opcion == opciones[0]:
        registerGame()
    elif opcion == opciones[1]:
        print("Catálogo:")
        db.showInventory()
    elif opcion == opciones[2]:
        db.reportTXT()
    elif opcion == opciones[3]:
        db.Save()
        exit(0)
    show_MenuAdmin()

def show_MenuCliente():
    opciones = ["Comprar producto", "Cerrar sesión"]
    opcion = input_options(opciones, "\nAcciones disponibles:")
    if opcion == opciones[0]:
        buyGame()
    elif opcion == opciones[1]:
        db.Save()
        exit(0)
    show_MenuCliente()

if perfilActual == "Administrador":
    show_MenuAdmin()
else:
    show_MenuCliente()
