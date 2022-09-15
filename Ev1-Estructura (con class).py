import datetime
import random

    
class evento:
  def __init__(self, folio, nombre,fecha,turno,sala, idCliente):
    self.folio = folio
    self.nombre = nombre
    self.fecha = fecha
    self.turno = turno
    self.sala = sala
    self.cliente = cliente
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

salas_disponibles = []

fecha_actual = datetime.date.today()

clientes = []

eventos_existentes = []

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
        print("**********************************************************")
        print("**      	RESERVACIÓN DE UNA SALA 		          **")
        print("**********************************************************")
        numero_capturado = int(input("Introduce tu número de cliente para hacer una reservación: "))
        if ((y.numero == numero_capturado) for y in clientes):
            print("Las salas disponibles son:")
            for sala in salas_disponibles:
                print("Nombre: ",sala.nombre, "| Clave: ",sala.clave, "| Cupo: ",sala.cupo)
            sala_deseada=int(input('Ingrese la clave de la sala que desea reservar: '))
            if (sala_deseada in sala.clave for sala in salas_disponibles):
                nombre_evento = input("Introduce el nombre del evento: ")
                fecha_capturada = input("Introduce la fecha del evento (DD/MM/AAAA): ")
                fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                delta = fecha_procesada - fecha_actual
                if (delta.days <= 2):
                    print("La reservación tiene que ser, por lo menos, dos días antes de la fecha actual.")
                else:
                    turno_evento = input("Ingresa el turno en el que quieres reservar la sala (M (matutino) / V (vespertino) / N (nocturno): ").upper()
                    folio_evento = random.randrange(100, 201)
                    print(f"El folio del evento es {folio_evento}, el nombre es {nombre_evento}, la fecha es {fecha_procesada.strftime('%d/%m/%Y')}, el turno es {turno_evento}")
                    eventos_existentes.append(evento(folio_evento, nombre_evento,fecha_procesada,turno_evento,sala_deseada, numero_capturado))
        else:
            print("El número de cliente no existe, tienes que registrarte para hacer una reservación.")
    elif opcion == 2:
      folio_capturado = int(input("Introduce el folio del evento que deseas editar: "))
      if (folio_capturado in evento.folio for evento in eventos_existentes):
        nuevo_nombre_evento = input(f"Escribe el nuevo nombre del evento (previamente {nombre_evento}): ")
        evento.nombre = nuevo_nombre_evento
        print(f"Cambiaste el nombre de tu evento a: {nuevo_nombre_evento}")
    elif opcion == 3:
        print("**********************************************************")
        print("**      		 CONSULTAR FECHAS DE SALA 		        **")
        print("**********************************************************")
        fecha_consulta = input("Introduce la fecha a consultar (DD/MM/AAAA): ")
        fecha_proc_consulta = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
        for x in eventos_existentes:
          if x.fecha == fecha_proc_consulta:
            for y in clientes:
              if y.numero == x.idCliente:
                print("---------------------------------------------------------------------")
                print(f"--    REPORTE DE RESERVACIONES PARA EL DÍA {fecha_proc_consulta}  --")
                print("---------------------------------------------------------------------")
                print("SALA     CLIENTE              EVENTO                   TURNO         ")
                print("---------------------------------------------------------------------")
                print(x.sala,"      ",y.nombre,"          ",x.nombre,"                     ",x.turno," ")
                print("----------                 FIN DEL REPORTE                -----------")
    elif opcion == 4:
        print("**********************************************************")
        print("**      		   REGISTRO DE CLIENTE 		          **")
        print("**********************************************************")
        nombre_cliente = input("Introduce tu nombre como cliente: ")
        numero_cliente = random.randrange(10, 100)
        clientes.append(cliente(numero_cliente, nombre_cliente))
        print(f"El número de cliente para {nombre_cliente} es {numero_cliente}")
    elif opcion == 5:
        print("**********************************************************")
        print("**      		   REGISTRAR UNA NUEVA SALA 		          **")
        print("**********************************************************")
        nombre_sala = input("Ingresa el nombre de la nueva sala: ")
        cupo_sala = int(input("Ingresa el cupo de la sala: "))
        clave_sala = random.randrange(4, 10)
        salas_disponibles.append(sala(clave_sala, nombre_sala, cupo_sala))
        print(f"La nueva sala ha quedado registrada como: Clave: {clave_sala} | Nombre: {nombre_sala} | Cupo: {cupo_sala}")
    elif opcion == 6:
      break