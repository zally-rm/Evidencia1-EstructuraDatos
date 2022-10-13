import datetime
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
        print("**      	  RESERVACIÓN DE UNA SALA	            **")
        print("**********************************************************")
        print("\nLos clientes registrados son:")
        for persona in clientes:
          print("Nombre: ", persona.nombre, " | Número: ", persona.numero)
        numero_capturado = int(input("\nIntroduce tu número de cliente para hacer una reservación: "))
        if ((persona.numero == numero_capturado) for persona in clientes):
            print("\nLas salas disponibles son:")
            for sala in salas_disponibles:
                print("Nombre: ",sala.nombre, "| Clave: ",sala.clave, "| Cupo: ",sala.cupo)
            sala_deseada=int(input('\nIngrese la clave de la sala que desea reservar: '))
            if (sala_deseada in sala.clave for sala in salas_disponibles):
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
        print("**      	CONSULTAR FECHAS DE SALA 		      **")
        print("**********************************************************")
        fecha_consulta = input("Introduce la fecha a consultar (DD/MM/AAAA): ")
        fecha_proc_consulta = datetime.datetime.strptime(fecha_consulta, "%d/%m/%Y").date()
        for e_existente in eventos_existentes:
          if (e_existente.fecha == fecha_proc_consulta):
            print("\n---------------------------------------------------------------------")
            print(f"--    REPORTE DE RESERVACIONES PARA EL DÍA {fecha_proc_consulta}  --")
            print("---------------------------------------------------------------------")
            print("SALA     CLIENTE              EVENTO                   TURNO         ")
            print("---------------------------------------------------------------------")
            for ev_que_aplica in eventos_existentes:
              for persona in clientes:
                if (persona.numero == ev_que_aplica.idCliente):
                  print(ev_que_aplica.sala,"      ",persona.nombre,"          ",ev_que_aplica.nombre,"                     ",ev_que_aplica.turno," ")
            print("----------                 FIN DEL REPORTE                -----------\n")
          elif (e_existente.fecha != fecha_proc_consulta):
            print("\nNo hay eventos registrados para la fecha consultada.\n")
    elif opcion == 4:
        print("\n**********************************************************")
        print("**      		REGISTRO DE CLIENTE 		        **")
        print("**********************************************************")
        nombre_cliente = input("Introduce tu nombre como cliente: ")
        numero_cliente = random.choice(posibles_nums_cliente)
        posibles_nums_cliente.remove(numero_cliente)
        clientes.append(cliente(numero_cliente, nombre_cliente))
        print(f"\nEl número de cliente para {nombre_cliente} es {numero_cliente}\n")
    elif opcion == 5:
        print("\n**********************************************************")
        print("**      		REGISTRAR UNA NUEVA SALA		        **")
        print("**********************************************************")
        nombre_sala = input("Ingresa el nombre de la nueva sala: ")
        cupo_sala = int(input("Ingresa el cupo de la sala: "))
        clave_sala = random.choice(posibles_claves_sala)
        posibles_claves_sala.remove(clave_sala)
        salas_disponibles.append(sala(clave_sala, nombre_sala, cupo_sala))
        print(f"\nLa nueva sala ha quedado registrada como: Clave: {clave_sala} | Nombre: {nombre_sala} | Cupo: {cupo_sala}\n")
    elif opcion == 6:
      break