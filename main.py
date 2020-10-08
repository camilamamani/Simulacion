import random
import math
import sys

sys.setrecursionlimit(90000)
# --------------- FDPs ---------------

# IA: Intervalo entre arribos de llamadas de clientes en minutos
def ia():
    R = generar_random_precision_ia()
    #print("R ia", R)
    return pow((pow(1-R, 1/-4.7695)-1) * pow(1719, 1.387), 1/1.387)

# TFM: Tiempo de fin fabricacion de muebles en minutos
def tff():
    R = generar_random()
    return (30 * R) + 75

# CP: Cantidad pedida de muebles en unidades/pedido
def cp():
    R = generar_random_precision_cp()
    #print("R cp", R)
    cp = math.log((1 - R) / 0.91947, 0.91947)
    #print("cp", cp)
    #print("cp redondeo =", math.ceil(cp))
    return math.ceil(cp)

def generar_random_precision_cp():
    R = generar_random()
    if R < 0.1000 or R > 0.9999:
        return generar_random_precision_cp()
    else:
        return round(R, 4)

def generar_random_precision_ia():
    R = generar_random()
    if R < 0.01 or R > 0.99:
        return generar_random_precision_ia()
    else:
        return round(R, 2)

def generar_random():
    return random.uniform(0, 1)

# --------------- FIN FDPs ---------------


# --------------- Variables Simulacion ---------------
class VariablesSimulacion():
    def __init__(self, CSI, CE, TF):
        # CSI: Cantidad de stock inicial
        self.CSI = CSI
        # CE: Cantidad de empleados
        self.CE = CE
        # TF: Tiempo final de simulación
        self.TF = TF

        # HV: High Value
        self.HV = float('inf')

        # Condiciones iniciales del resto de variables

        # CSA: Cantidad de muebles en stock actual
        self.CSA = self.CSI

        # T = Tiempo actual
        self.T = 0
        # TPLL: Tiempo de proxima llegada del llamado del cliente
        self.TPLL = 0
        # TPFF(i): Tiempo de proxima finalización de fabricación del mueble por cada empleado
        self.TPFF = [0] * self.CE

        # CLT: Clientes totales que ingresaron al sistema
        self.CLT = 0
        # CLI: Clientes insatisfechos
        self.CLI = 0
        # CMT: Cantidad de muebles totales pedidos
        self.CMT = 0
        # CMP: Cantidad de muebles perdidos, no se vendieron x falta de stock
        self.CMP = 0
        # ARR: Cantidad de arrepentidos
        self.ARR = 0

        # PMNV: Porcentaje de muebles no vendidos
        self.PMNV = 0
        # PCLI: Porcentaje de clientes insatisfechos
        self.PCLI = 0
        # PMSF: Porcentaje de muebles en stock final respecto CSA
        self.PMSF = 0


# --------------- FIN Variables Simulacion ---------------


# --------------- Funciones ---------------

def imprimir_resultados(vars):
    print("Fin de la Simulación")
    print("Variables de control elegidas:")
    print("CSI =", vars.CSI)
    print("CE =", vars.CE)
    print("TF =",vars.TF)

    print("Resultados:")
    print("Porcentaje de muebles no vendidos =", vars.PMNV, "%")
    print("Porcentaje de clientes insatisfechos =", vars.PCLI, "%")
    print("Porcentaje de stock final respecto al inicial =", vars.PMSF, "%")


def ir_al_final(vars):
    if vars.T < vars.TF:
        iniciar_simulacion(vars)
    else:
        vars.PMNV = (vars.CMP / vars.CMT) * 100
        vars.PCLI = (vars.CLI / vars.CLT) * 100
        vars.PMSF = (vars.CSA / vars.CSI) * 100
        imprimir_resultados(vars)


def avanzar_rama_fin_fabric(vars, i):
    vars.T = vars.TPFF[i]
    prox_fin_fabric = tff()
    vars.TPFF[i] = vars.T + prox_fin_fabric

    if vars.T != 0:
        vars.CSA += 1 #Sumo un mueble al stock actual, porque un empleado fabrica 1 mueble por TF

    ir_al_final(vars)


def avanzar_rama_llegada(vars):
    vars.T = vars.TPLL

    intervalo_de_arribo = ia()
    vars.TPLL = vars.T + intervalo_de_arribo

    R = generar_random()
    if R <= 0.90:
        vars.CLT += 1
        cant_muebles_pedidos = cp()
        vars.CMT += cant_muebles_pedidos
        if cant_muebles_pedidos <= vars.CSA:
            vars.CSA -= cant_muebles_pedidos
        else:
            vars.CLI += 1
            vars.CMP += cant_muebles_pedidos
    else:
        vars.ARR += 1
    ir_al_final(vars)

def indice_menor_tpff(vars):
    return vars.TPFF.index(min(vars.TPFF))

def iniciar_simulacion(vars):
    i = indice_menor_tpff(vars)

    if vars.TPLL <= vars.TPFF[i]:
        avanzar_rama_llegada(vars)
    else:
        avanzar_rama_fin_fabric(vars, i)

# --------------- FIN Funciones ---------------


# --------------- Inicio Main ---------------

if __name__ == '__main__':
    # Ingresamos valores de las var control CSI y CE
    cant_stock_inic = int(input("Ingrese la cantidad de stock inicial: "))
    cant_empl = int(input("Ingrese la cantidad de empleados: "))

    # Ingresamos TF de simulación
    tf_simulacion = int(input("Ingrese el tiempo final de simulación en minutos: "))

    # Seteamos condiciones iniciales
    var_sim = VariablesSimulacion(cant_stock_inic, cant_empl, tf_simulacion)

    # Iniciamos simulación
    iniciar_simulacion(var_sim)

# ----------------- FIN Main ----------------