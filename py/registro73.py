#importamos las librerias necesarias
import os # interactuar con el s.operativo(manejo archivos).
import sqlite3 # permite trabajar con base de datos sqlite
from datetime import datetime
from colorama import Fore, Back, Style,init
from tabulate import tabulate
init(autoreset=True)   # resetea el color al valor por defecto


DB_PATH = "/users/eduardo/basic/nueva carpeta/inventario1.db"
print("usando DB:", os.path.abspath(DB_PATH))


#conexion a la base de datos y crea un cursor para ejecutar comandos sql
conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

#cursor.execute("DROP TABLE IF EXISTS inventario1;")#BORRA LA TABLA
#cursor.executescript("""
#DROP TABLE IF EXISTS ventas;
#DROP TABLE IF EXISTS ventas_detalle;
#""")#BORRA LA TABLA
#conexion.commit()


cursor.execute("select name  FROM sqlite_master WHERE type = 'table' ")
print(cursor.fetchall())




def crear_tabla(cursor, conexion):
        try: 
            conexion = sqlite3.connect("inventario1.db")
            cursor = conexion.cursor()

            #crea la tabla
            conexion.execute("""
            CREATE TABLE IF NOT EXISTS inventario(
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                categoria TEXT,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                fecha_hora TEXT 
            );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                id INTERGER PRIMARY KEY,
                fecha TEXT,
                total REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas_detalle (
                id INTERGER PRIMARY KEY,
                venta_id INTEGER NOT NULL,
                producto_id INTERGER NOT NULL,
                cantidad INTERGER NOT NULL,
                precio REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                FOREIGN KEY (producto_id) REFERENCES inventario(id)
                
                )
            """)


            conexion.commit() # guarda los cambios definitivamente en la bd.
            print("Tablas  creada correctamente.")
        except Exception as e:
            print("ERROR: al crear tablas", e) 

crear_tabla(cursor,conexion)



def confirmar_operacion(mensaje ="\n ¿Desea Continuar? [Enter]/[NO] ):" ):
    while True:
        respuesta = input (mensaje).lower().strip()
        if respuesta == "":
             return True
        elif respuesta == "no":
             return False
        else:
            print(Fore.RED + "• Respuesta invalida, escriba [Enter]/[NO] ")


def mostrar_preticket(carrito):
    fecha_hora = datetime.now()
    fecha_str = fecha_hora.strftime("%d/%m/%y %H:%M:%S")
    print("\n" + "-" * 50)
    print(f"PRE-TICKET  == FECHA Y HORA: {fecha_str} ==")
    print("-" * 50)
    total_parcial = 0
    for item in carrito:
        print(f"{item["nombre"]:<15}"
              f"x{item["cantidad"]:<3}"
              f"${item["precio"]:<6}"
              f" = ${item["subtotal"]}")
        total_parcial += item["subtotal"]      
    print("\n" + "-" * 50)
    print(f"TOTAL PARCIAL: ${total_parcial}")
    print("-" * 50 + "\n")

def Agregar_produc():
    while True:
            while True:
                print(Fore.GREEN + "\n == AGREGAR PRODUCTOS == \n")
                
                nombre =input ("• NOMBRE DEL PRODUCTO:").strip().title() # quita espacios en blanco / pone la 1 letra en mayuscula de cada palabra
                if not nombre:
                        print(Fore.RED + "• Error: campo vacio - vuelva intentarlo por favor...") 
                        print (" ")
                        continue 
                break     
            while True:            
                    categoria = input ("• CATEGORIA DEL PRODUCTO:").strip().title() # quita espacios en blanco / pone la 1 letra en mayuscula de cada palabra
                    if not categoria:
                        print(Fore.RED + "Error: campo vacio - vuelva intentarlo por favor...") 
                        print (" ")
                        continue 
                    break 
            while True:            
                    descripcion = input ("•DESCRIPCION:").strip()  
                    if not descripcion:
                        print(Fore.RED + "Error: campo vacio - vuelva intentarlo por favor...") 
                        print (" ")
                        continue 
                    break 
            
            while True:      
                    entrada =  input ("•CANTIDAD:").strip()
                    if not entrada:
                        print(Fore.RED + "• Error: campo vacio. Vuelva a intentarlo por favor...")
                        continue
                    else:
                        try:
                            cantidad = int(entrada)
                            if cantidad <= 0:
                                print(Fore.RED + "• No se puede ingresar numeros negativos, ni nulos. ")
                                print ("")
                                continue 
                        except ValueError:
                            print (Fore.RED + "• Debe ingresar un numero valido.") 
                            continue
                    break
            
            
            
            
            while True:      
                    entrada =  input ("• PRECIO: ").strip()
                    if not entrada:
                        print(Fore.RED + "• Error: campo vacio. Vuelva a intentarlo por favor...")
                        continue
                    else:
                        try:
                            precio = int(entrada)
                            if precio <= 0:
                                print(Fore.RED + "• No se puede ingresar numeros negativos.")
                                print ("")
                                continue 
                        except ValueError:
                            print (Fore.RED + "• Debe ingresar un numero valido.") 
                            continue
                    break
            #fecha y hora actual
            fecha_hora = datetime.now().strftime("%d-%m-%y %H:%M:%S")
                

            try:
                
                conexion = sqlite3.connect("inventario1.db")
                cursor = conexion.cursor()

                cursor.execute("BEGIN TRANSACTION")
                # validacion que nose ingrese mismo producto a la base de datos.
                cursor.execute("""
                    SELECT * FROM inventario
                    WHERE nombre = ? AND categoria = ? AND descripcion = ? AND precio = ?
                    """, (nombre, categoria, descripcion, precio))
                producto_existente = cursor.fetchone()
                if producto_existente:
                    print(Fore.RED +  "\n ! ESTE PRODUCTO YA EXISTE EXACTAMENTE IGUAL.NO SE PUEDE CARGAR OTRA VEZ.")
                    conexion.rollback()
                    return

                #inserta en la tabla
                cursor.execute("""
                INSERT INTO inventario (nombre,categoria,descripcion,cantidad,precio,fecha_hora)
                VALUES (?,?,?,?,?,?)
                """,(nombre,categoria,descripcion, cantidad, precio,fecha_hora))
                conexion.commit()
                print(Fore.GREEN + f"Producto {nombre} agregado correctamente el {fecha_hora}.")
            except sqlite3.Error as e:
                if conexion:
                    conexion.rollback()
                    print(Fore.RED + "Error al agregar el producto.",e)
            finally:
                    conexion.close()    
            if not confirmar_operacion("¿Desea cargar otro producto? (si/no):"):
                 print(Fore.GREEN + "Volviendo al menu principal....")
                 break            


def mostrar_produc():
    try:
        conexion = sqlite3.connect("inventario1.db")
        cursor = conexion.cursor()
        
        print(Fore.GREEN + "\n === LISTA DE PRODUCTOS === \n")  
        cursor.execute("SELECT * FROM inventario")
        productos = cursor.fetchall()

        #si no hay datos
        if not productos:
            print(Fore.RED + "No hay productos cargados todavia.")
            return
        #encabezado de la tabla
        encabezados = ["ID" , "Nombre" , "Categoria","descripcion","cantidad" , "Precio","fecha_hora"]
        
        #  mostrar la tabla
        print(tabulate(productos, headers=encabezados, tablefmt="simple"))

    except sqlite3.Error as e:
        print(Fore.RED + "Error al mostrar productos:", e) 
    finally:
        conexion.close() 
          


def buscar_produc():
    conexion = None
    while True:
        try:        
            
            conexion = sqlite3.connect("inventario1.db")
            cursor = conexion.cursor() 
           
            print(Fore.GREEN + "\n BUSCAR PRODUCTOS:")
            print(Fore.GREEN +"-" * 18)
             #busca el producto por ide/nombre/categoria.       
            termino = input ("- INGRESE: ID / Nombre / Categoria:").strip()
            
            if not termino:
                 print(Fore.RED + "No ingrerso ningun valor. Intente nuevamente")
                 break
            if termino.isdigit():
                 
                 cursor.execute("SELECT * FROM inventario WHERE id = ?",(int(termino),))
                 fila = cursor.fetchone() # devuelve solo una fila
                 
                 if fila:
                    print("\n Producto encontrado:")
                    print(tabulate([fila], headers=["ID", "Nombre", "Categoria","Descripcion","Cantidad","Precio","fecha_hora"],tablefmt="fancy_grid", numalign="center",floatfmt=".2f", stralign="center"))
                 else:
                    print(Fore.RED + "No se encontro producto con ese ID.")
            else:
                 cursor.execute("""
                    SELECT * FROM inventario
                    WHERE nombre LIKE? COLLATE NOCASE
                    OR categoria LIKE? COLLATE NOCASE
                 """, (F"%{termino}%", f"%{termino}%"))   

            
         
                  
                 producto = cursor.fetchall()# trae todas las fila q cumplen la condicion.
                 if producto:
                     print(Fore.GREEN + "\n•Producto encontrado:")
                      #encabezado de la tabla
                     encabezados = ["ID" , "Nombre" , "Categoria","descripcion","cantidad" , "Precio","fecha_hora"]
                      #  mostrar la tabla
                     print(tabulate(producto, headers=encabezados,tablefmt="fancy_grid",numalign="center", stralign="center", floatfmt=".2f",disable_numparse=True))
                 else:
                     print(Fore.RED + "No se encontro ningun producto con ese ID.")
        except ValueError:
                print(Fore.RED + "ERROR:el ID debe ser un numero entero.") 
        except sqlite3.Error as e:
                print(Fore.RED + "ERROR: al buscar el producto:", e)
        finally:
            if conexion is not None:
                try:
                     conexion.close()#cierra la conexion con la base de dato.
                except Exception as e:
                    print(Fore.RED + "No se puede cerrar la conexion:",e)                                  
        if not confirmar_operacion():
             print(Fore.GREEN + "volviendo al menu principal....")
             break                
                

def eliminar_produc():
    conexion = None
    while True:
         print(Fore.RED + "\n ELIMINAR PRODUCTOS:")
         print("-" * 19)
         
         id_eliminar = input ("- INGRESE el ID del producto a eliminar:")
         if not id_eliminar:
            print(Fore.RED + "No ingrerso ningun ID. Intente nuevamente")
            continue 

         try:
             id_eliminar = int(id_eliminar)#convierte el id ingresado (string) a entero
             conexion = sqlite3.connect("inventario1.db")
             cursor = conexion.cursor()
             # agrupa variaas operaciones para que sean seguras.se realicen juntas.
             cursor.execute("BEGIN TRANSACTION")
 

             cursor.execute("SELECT * FROM inventario WHERE id = ?", (id_eliminar,)) 
             producto = cursor.fetchone()# trae una sola fila.
             if not producto:
                print(Fore.RED + "No existe ningun producto con ese ID.Vuelva intentarlo por favor.")
                continue
             if producto:
                print(Fore.RED + "\n•Producto a Eliminar:")
                
                #encabezado de la tabla
                encabezados = ["ID" , "Nombre" , "Categoria","descripcion","cantidad" , "Precio","fecha_hora"]
                 #  mostrar la tabla
                
                print(tabulate([producto], headers=encabezados,tablefmt="pretty", floatfmt=".2f"))
                
                print("-" * 55)
             if confirmar_operacion(mensaje=Fore.RED + "¿Esta seguro que desea ELIMINAR el producto?(si/no):"):
                 cursor.execute("DELETE FROM inventario WHERE id = ?", (id_eliminar,))
                 conexion.commit()#confima los cambios.
                 print(Fore.GREEN + "Producto eliminado correctamente.") 

             else:
                print(Fore.YELLOW +"Operacion cancelada. No se elimino ningun producto.")
         except ValueError:
                print(Fore.RED + "ERROR:el ID debe ser un numero entero.") 
         except sqlite3.Error as e:
            if conexion:
                conexion.rollback()#deshace todos los cambios.
                print(Fore.RED + "ERROR: al buscar el producto:", e)
         finally:
                if conexion is not None:
                 try:
                     conexion.close()
                 except Exception as e:
                    print(Fore.RED + "No se puede cerrar la conexion:",e)

         if not confirmar_operacion():
             print(Fore.GREEN + "volviendo al menu principal....")
             break

def actualizar_produc():
    conexion = None
    while True:
         print(Fore.GREEN + "\n == ACTUALIZAR PRODUCTOS ==")
         print(Fore.GREEN + "-" * 28)
         
         id_actualizar = input ("- INGRESE el ID del producto a ACTUALIZAR:")
         if not id_actualizar:
            print(Fore.RED + "No ingrerso ningun ID. Intente nuevamente")
            continue 

         try:
             id_actualizar = int(id_actualizar)
             conexion = sqlite3.connect("inventario1.db")
             cursor = conexion.cursor()

             cursor.execute("BEGIN TRANSACTION")
 

             cursor.execute("SELECT * FROM inventario WHERE id = ?", (id_actualizar,)) 
             producto = cursor.fetchone()# trae una sola fila
             if not producto:
                print(Fore.RED + "No existe ningun producto con ese ID.Vuelva intentarlo por favor.")
                continue
             if producto:
                print("\n•Producto a actualizar:")
                
                #encabezado de la tabla
                encabezados = ["ID" , "Nombre" , "Categoria","descripcion","cantidad" , "Precio", "fecha_hora"]
                 #  mostrar la tabla
                
                print(tabulate([producto], headers=encabezados,tablefmt="pretty", floatfmt=".2f"))
                
             confirmacion = input("\n ¿Desea actualizar este producto? (si/no)").strip().lower()
             
             if confirmacion == "si":
                 print(Fore.GREEN + "\n== ACTUALIZACION ==")
                 while True: 
                     nuevo_nombre = input("• Nuevo Nombre:").strip().title()
                     if not nuevo_nombre:
                        print(Fore.RED + "• Error: campo vacio - vuelva intentarlo por favor...") 
                        print (" ")
                        continue
                     break 
                 while True:
                     nuevo_cat = input("• Nueva Categoria:").strip().title()
                     if not nuevo_cat:
                        print(Fore.RED + "• Error: campo vacio - vuelva intentarlo por favor...") 
                        print (" ")
                        continue 
                     break
                 while True: 
                     nuevo_desc = input("• Nueva Descripcion:").strip()
                     if not nuevo_desc:
                        print(Fore.RED + "• Error: campo vacio - vuelva intentarlo por favor...") 
                        print (" ")
                        continue 
                     break 
                 while True:
                     nuevo_cant = input("• Nueva Cantidad:").strip()
                     if not nuevo_cant:
                        print(Fore.RED + "• Error: campo vacio. Vuelva a intentarlo por favor...")
                        continue
                     else:
                        try:
                            nuevo_cant = int(nuevo_cant)
                            if nuevo_cant <= 0:
                                print(Fore.RED + "• No se puede ingresar numeros negativos, ni nulos. ")
                                print ("")
                                continue
                            break 
                        except ValueError:
                            print (Fore.RED + "• Debe ingresar un numero validdo") 
                            continue
                     break
                 while True:
                     nuevo_precio = input("• Nuevo Precio:").strip()
                     if not nuevo_precio:
                        print(Fore.RED + "• Error: campo vacio. Vuelva a intentarlo por favor...")
                        continue
                     else:
                        try:
                            nuevo_precio = float(nuevo_precio)
                            if nuevo_precio <= 0:
                                print(Fore.RED + "• No se puede ingresar numeros negativos. ")
                                print ("")
                                continue
                            break 
                        except ValueError:
                            print (Fore.RED + "• Debe ingresar un numero valido.") 
                            continue
                     
                 
                 cursor.execute("""
                     UPDATE inventario
                     SET nombre = ?, categoria = ?,descripcion = ?, cantidad = ?, precio = ?
                     WHERE id = ?
                     """, (nuevo_nombre,nuevo_cat,nuevo_desc,nuevo_cant,nuevo_precio,id_actualizar))   
                 conexion.commit()
                 conexion.close()
                 print(Fore.GREEN + f"\n PRODUCTO {nuevo_nombre} ACTUALIZADO CORRECTAMENTE.")
             else:
                 print(Fore.YELLOW + "Operacion cancela.")
                 conexion.close()
                 return
         except ValueError:
                print(Fore.RED + "ERROR:el ID debe ser un numero entero.") 
         except sqlite3.Error as e:
            if conexion:
                conexion.rollback()
                print(Fore.RED + "ERROR: al buscar el producto:", e)
         finally:
                if conexion is not None:
                 try:
                     conexion.close()
                 except Exception as e:
                    print(Fore.RED + "No se puede cerrar la conexion:",e)

         if not confirmar_operacion():
             print(Fore.GREEN + "volviendo al menu principal....")
             break
def informe_reporte():
    conexion = sqlite3.connect("inventario1.db")
    cursorn = conexion.cursor()
    
    cursor.execute("SELECT * FROM inventario WHERE cantidad <= 10")
    productos = cursor.fetchall()

    if productos:
        print(Fore.RED + "\n Productos con bajo stock:")
        print("-" * 27)
        print("")
        print(tabulate(productos, headers=["ID","nombre", "categoria","descripcion","cantidad","precio","fecha_hora"],tablefmt="simple"))
    else:
        print(Fore.RED + "\n No hay productos con bajo stock.")
    conexion.close() 
        
       
def ventas():
    fecha_hora = datetime.now()
    fecha_str = fecha_hora.strftime("%d/%m/%y %H:%M:%S")
    carrito = []
    conexion = None
    carrito.clear()

    print(Fore.GREEN +"-" * 32)
    print(Fore.GREEN + " Agregar Producto al Carrito")
    print(Fore.GREEN +"-" * 32)
    while True:
        conexion = sqlite3.connect("inventario1.db")
        cursor = conexion.cursor()
        
        
        #busca el producto por ide/nombre.       
        termino = input (Fore.YELLOW + "\n- INGRESE: ID / Nombre :").strip()
            
        if not termino:
                 print(Fore.RED + "No ingrerso ningun valor. Intente nuevamente")
                 return
        
        cursor.execute("""
            SELECT id , nombre , categoria, cantidad, precio
            FROM inventario
            WHERE id = ? OR nombre LIKE ?
        """, (termino, f"%{termino}")    
        )
        producto = cursor.fetchone()
        if producto is None:
            print("producto no encontrado")
            conexion.close()
            return
        id_prod, nombre, categoria, cantidad, precio = producto
        print(Fore.GREEN +"\n•Producto Encontrado•")
        print(f"ID: {id_prod}")
        print(f"Nombre: {nombre}")
        print(f"Categiria: {categoria}")    
        print(f"cantidad: {cantidad}")
        print(f"Precio: ${precio}")    
        
        cantidad_txt = input(Fore.BLUE + "\n•Cantidad a Vender:" + Style.RESET_ALL)
        if not cantidad_txt.isdigit():
            print("Debe ingresar un numero valido")
            conexion.close()
            return
        cantidad_vender = int(cantidad_txt)    
        if cantidad_vender <= 0 :
            print("La cantidad debe ser mayor a cero")
            conexion.close()
            return
        if cantidad_vender > cantidad:
            print("No hay stock suficiente")
            conexion.close()
            return    
        subtotal = cantidad_vender * precio
        nueva_cantidad = cantidad - cantidad_vender
        cursor.execute("""
            UPDATE inventario
            SET cantidad = ?
            WHERE id = ?
        """, (nueva_cantidad, id_prod))    
        conexion.commit()
        item = {
            "id": id_prod,
            "nombre": nombre,
            "cantidad":cantidad_vender,
            "precio": precio,
            "subtotal": subtotal
        }

        carrito.append(item)
    
        mostrar_preticket(carrito)
        #print(Fore.GREEN + f"•Agrego: {nombre} (x {cantidad_vender}) = ${subtotal}")

        if not confirmar_operacion("\n¿Desea Agregar Otro Producto? [Enter]/[NO]:"):
                     print(Fore.GREEN + "Imprimiendo ticket....")
                     break           
    ticket_numero = cursor.lastrowid

    total_venta = sum(item["subtotal"] for item in carrito)
    print("\n" + "=" * 35)
    print(f"TICKET Nº{ticket_numero} - REGISTRO73 - CLIENTE")
    print( "=" * 35)

    for item in carrito:
        print(f"{item["nombre"]:<15}"
              f"x{item["cantidad"]:<3}"
              f"${item["precio"]:<6}"
              f" = ${item["subtotal"]}")
    print( "=" * 35)
    print(f"TOTAL: ${total_venta} == APROBADO ==")
    print(f"FECHA Y HORA: {fecha_str}")
    print( "=" * 35)

    print(Fore.GREEN + "= Venta Registrada Correctamente =")



        





while True:
     print(Fore.GREEN + "\n == SISTEMA DE GESTION DE PRODUCTOS REGISTRO73 == \n")
     print(" 1- Agregar productos")
     print(" 2- Mostrar productos")
     print(" 3- Buscar productos")
     print(" 4- Eliminar productos")
     print(" 5- Actualizar productos")
     print(" 6- Informe de productos")
     print(" 7- Ventas de Productos")
     print(" 8- Salir")


     opcion = input(Fore.CYAN + "• Elija una opcion (1/8):")
     print ("")

     if opcion == "1":
        Agregar_produc()
     elif  opcion == "2":
        mostrar_produc()
     elif  opcion == "3":
        buscar_produc()
     elif  opcion == "4":
        eliminar_produc() 
     elif  opcion == "5":
        actualizar_produc()
     elif  opcion == "6":
        informe_reporte() 
     elif  opcion == "7":
        ventas() 
     elif  opcion == "8": 
        print(Fore.GREEN + "• Salinedo del Sistema.¡hasta luego!") 
        break
     else:
        print(Fore.RED + "• == Opcion invalida, intente nuevamente == \n")
conexion.close()        