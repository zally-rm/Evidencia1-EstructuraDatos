import csv
import datetime
import os
import pandas as pd
import random

    
class evento:
  def __init__(self, folio, nombre,fecha,turno,sala, idCliente):
    self.folio = folio
    self.nombre = nombre
    self.fecha = fecha
    self.turno = turno
    self.sala = sala
    self.idCliente = idCliente

class sala:
  def __init__(self, clave, nombre, cupo):
    self.clave = clave
    self.nombre = nombre
    self.cupo = cupo

class cliente:
  def __init__(self, numero, nombre):
    self.numero = numero
    self.nombre = nombre

fecha_actual = datetime.date.today()

salas_disponibles = []

clientes = []

eventos_existentes = []

posibles_claves_sala = list(range(2,10))

posibles_nums_cliente = list(range(11,100))

posibles_folios_evento = list(range(101, 200))

lista_turnos = ["M", "V", "N"]

df_salas = pd.DataFrame.from_dict({"Sala": [], "Turno": []})

dict_por_fecha = dict()

if os.path.exists("clientes.csv"):
  with open("clientes.csv","r", newline="") as lectura_clientes:
    lector = csv.reader(lectura_clientes)
    next(lector)
    for numero, nombre in lector:
        clientes.append(cliente(numero, nombre))

if os.path.exists("salas.csv"):
  with open("salas.csv","r", newline="") as lectura_salas:
    lector = csv.reader(lectura_salas)
    next(lector)
    for clave, nombre, cupo in lector:
        salas_disponibles.append(sala(clave, nombre, cupo))

if os.path.exists("eventos.csv"):
  with open("eventos.csv","r", newline="") as lectura_eventos:
    lector = csv.reader(lectura_eventos)
    next(lector)
    for folio, nombre, fecha, turno, sala, numero in lector:
        fecha_evento_csv = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        eventos_existentes.append(evento(folio, nombre, fecha_evento_csv, turno, sala, numero))
        df_salas = df_salas[(sala not in df_salas["Sala"]) & (df_salas["Turno"] != turno)]

while True:
    print("***********************************************************")
    print("**               RENTA DE SALAS DE REUNIONES             **")
    print("***********************************************************")
    print("¿Qué deseas realizar?")
    print("1. Registrar la reservación de una sala.")
    print("2. Editar el nombre del evento de una reservación existente.")
    print("3. Consultar las reservaciones existentes para una fecha específica.")
    print("4. Registrar a un nuevo cliente.")
    print("5. Registrar una nueva sala.")
    print("6. Salir.")
    opcion= int(input("Selecionar una opción: "))

    if opcion == 1:
        print("\n**********************************************************")
        print("**         RESERVACIÓN DE UNA SALA               **")
        print("**********************************************************")
        print("\nLos clientes registrados son:")
        for persona in clientes:
          print("Nombre: ", persona.nombre, " | Número: ", persona.numero)
        numero_capturado = int(input("\nIntroduce tu número de cliente para hacer una reservación: "))
        if ((persona.numero == numero_capturado) for persona in clientes):
          print("\n¿Desea ver todas las salas disponibles o ver su disponibilidad en una fecha determinada?")
          print("1. Ver todas las salas. \n2. Buscar sala disponible por fecha.")
          busqueda_sala = int(input())
          if busqueda_sala == 1:
            print("\nLas salas disponibles son:")
            for sala in salas_disponibles:
                print("Nombre: ",sala.nombre, "| Clave: ",sala.clave, "| Cupo: ",sala.cupo)
          elif busqueda_sala == 2:
            fecha_busqueda = input("\nIngresa la fecha para la que quieres reservar (DD/MM/AAAA): ")
            fecha_busq_proc = datetime.datetime.strptime(fecha_busqueda, "%d/%m/%Y").date()
            print(f"\n ** Salas disponibles para renta el {fecha_busq_proc} **\n")
            print(df_salas)
          sala_deseada=int(input('\nIngrese la clave de la sala que desea reservar: '))
          if ((sala_deseada == sala.clave) for sala in salas_disponibles):
            nombre_evento = input("Introduce el nombre del evento: ")
            fecha_capturada = input("Introduce la fecha del evento (DD/MM/AAAA): ")
            fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
            delta = fecha_procesada - fecha_actual
            if (delta.days <= 2):
              print("\nLa reservación tiene que ser, por lo menos, dos días antes de la fecha actual.\n")
            else:
              turno_evento = input("Ingresa el turno en el que quieres reservar la sala (M (matutino) / V (vespertino) / N (nocturno): ").upper()
              folio_evento = random.choice(posibles_folios_evento)
              posibles_folios_evento.remove(folio_evento)
              print(f"\nEl folio del evento es {folio_evento}, el nombre es {nombre_evento}, la fecha es {fecha_procesada.strftime('%d/%m/%Y')}, el turno es {turno_evento}\n")
              eventos_existentes.append(evento(folio_evento, nombre_evento,fecha_procesada,turno_evento,sala_deseada, numero_capturado))
              df_salas = df_salas[(sala_deseada not in df_salas["Sala"]) & (df_salas["Turno"] != turno_evento)]
        else:
            print("\nEl número de cliente no existe, tienes que registrarte para hacer una reservación.\n")
    elif opcion == 2:
      for e_existente in eventos_existentes:
        print(f"Folio: {e_existente.folio} | Nombre del evento: {e_existente.nombre} | Cliente: {e_existente.idCliente}")
      folio_capturado = int(input("Introduce el folio del evento que deseas editar: "))
      if (e_existente.folio == folio_capturado for e_existente in eventos_existentes):
        nuevo_nombre_evento = input(f"Escribe el nuevo nombre del evento (previamente {e_existente.nombre}): ")
        e_existente.nombre = nuevo_nombre_evento
        print(f"Cambiaste el nombre de tu evento a: {nuevo_nombre_evento}")
    elif opcion == 3:
        print("\n**********************************************************")
        print("**       CONSULTAR FECHAS DE SALA              **")
        print("**********************************************************")
        fecha_consulta = input("Introduce la fecha a consultar (DD/MM/AAAA): ")
        fecha_proc_consulta = datetime.datetime.strptime(fecha_consulta, "%d/%m/%Y").date()
        for e_existente in eventos_existentes:
          if (e_existente.fecha != fecha_proc_consulta):
            print("\nNo hay eventos registrados para la fecha consultada.\n")
          elif (e_existente.fecha == fecha_proc_consulta):
            print("\n---------------------------------------------------------------------")
            print(f"--    REPORTE DE RESERVACIONES PARA EL DÍA {fecha_proc_consulta}  --")
            print("---------------------------------------------------------------------")
            print("SALA     CLIENTE              EVENTO                   TURNO         ")
            print("---------------------------------------------------------------------")
            for persona in clientes:
              if (persona.numero == e_existente.idCliente):
                print(e_existente.sala,"      ",persona.nombre,"          ",e_existente.nombre,"                     ",e_existente.turno," ")
                dict_por_fecha[e_existente.folio] = [e_existente.sala, persona.nombre, e_existente.nombre, e_existente.turno]
            print("----------                 FIN DEL REPORTE                -----------\n")
        opcion_exportar = input("\n¿Deseas exportar el reporte a Excel? (S/N): ")
        if opcion_exportar.upper() == "S":
          with open("reservaciones.csv","w", newline="") as archivo_reserv:
            grabador = csv.writer(archivo_reserv)
            grabador.writerow(("Folio del evento", "Sala", "Cliente", "Nombre", "Turno"))
            grabador.writerows([(clave, datos[0], datos[1], datos[2], datos[3]) for clave, datos in dict_por_fecha.items()])
          df_reserv_fecha = pd.read_csv('reservaciones.csv')
          excel_reserv = pd.ExcelWriter('reservaciones.xlsx')
          df_reserv_fecha.to_excel(excel_reserv, index=False)
          excel_reserv.save()
          print("\nSe ha creado el archivo excel.\n")
        elif opcion_exportar.upper() == "N":
          print("\nSe ha omitido la exportación del reporte a Excel.\n")
    elif opcion == 4:
        print("\n**********************************************************")
        print("**           REGISTRO DE CLIENTE                 **")
        print("**********************************************************")
        nombre_cliente = input("Introduce tu nombre como cliente: ")
        numero_cliente = random.choice(posibles_nums_cliente)
        posibles_nums_cliente.remove(numero_cliente)
        clientes.append(cliente(numero_cliente, nombre_cliente))
        print(f"\nEl número de cliente para {nombre_cliente} es {numero_cliente}\n")
    elif opcion == 5:
        print("\n**********************************************************")
        print("**           REGISTRAR UNA NUEVA SALA                **")
        print("**********************************************************")
        nombre_sala = input("Ingresa el nombre de la nueva sala: ")
        cupo_sala = int(input("Ingresa el cupo de la sala: "))
        clave_sala = random.choice(posibles_claves_sala)
        posibles_claves_sala.remove(clave_sala)
        salas_disponibles.append(sala(clave_sala, nombre_sala, cupo_sala))
        for turno in lista_turnos:
          df_salas = df_salas.append({"Sala" : [clave_sala, nombre_sala], "Turno" : turno}, ignore_index=True)
        print(f"\nLa nueva sala ha quedado registrada como: Clave: {clave_sala} | Nombre: {nombre_sala} | Cupo: {cupo_sala}\n")
    elif opcion == 6:
      #CSV de clientes:
      with open("clientes.csv","w", newline="") as archivo_clientes:
        grabador = csv.writer(archivo_clientes)
        grabador.writerow(("Número de cliente", "Nombre"))
        grabador.writerows([(cliente.numero, cliente.nombre) for cliente in clientes])
        print("\nSe ha creado el archivo csv para los clientes registrados.")
      #CSV de salas:
      with open("salas.csv","w", newline="") as archivo_salas:
        grabador = csv.writer(archivo_salas)
        grabador.writerow(("Clave de la sala", "Nombre de la sala", "Cupo"))
        grabador.writerows([(sala.clave, sala.nombre, sala.cupo) for sala in salas_disponibles])
        print("\nSe ha creado el archivo csv para las salas registradas.")
      #CSV para los eventos registrados:
      with open("eventos.csv","w", newline="") as archivo_eventos:
        grabador = csv.writer(archivo_eventos)
        grabador.writerow(("Folio del evento", "Nombre del evento", "Fecha", "Turno", "Sala", "Num cliente"))
        grabador.writerows([(e_registrado.folio, e_registrado.nombre, e_registrado.fecha, e_registrado.turno, e_registrado.sala, e_registrado.idCliente) for e_registrado in eventos_existentes])
        print("\nSe ha creado el archivo csv para los eventos registrados.")
      break