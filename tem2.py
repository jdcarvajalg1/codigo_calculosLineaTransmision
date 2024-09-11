import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.constants import c as lightspeed

# Definicion de parametros

largo = 0.1 
espesor = 0.0016
anchos = [0.001*i for i in range(1,6)]
E_t = 4.5
c = lightspeed
Z_l = 50
pi = np.pi

# (1) Calculos para permitividad efectiva

permitividades_efectivas = []
for ancho in anchos:
    E_e = (E_t + 1)/2 + (E_t - 1)/(2*(np.sqrt(1 + 12*espesor/ancho)))
    permitividades_efectivas.append(E_e)

# (2) Calculos para velocidad de fase

velocidades_de_fase = []
for permitividad_efectiva in permitividades_efectivas:
    V_f = c/np.sqrt(permitividad_efectiva)
    velocidades_de_fase.append(V_f)

# (3) Calculos para impedancia caracteristica

anchos_permitividades_efectivas = zip(anchos, permitividades_efectivas)

impedancias_caracteristicas = []
for ancho, permitividad_efectiva in anchos_permitividades_efectivas:
    if ancho/espesor <= 1:
        I_c = 60/np.sqrt(permitividad_efectiva)*np.log(8*espesor/ancho + ancho/(4*espesor))
    else:
        I_c = 120*pi/(np.sqrt(permitividad_efectiva)*(ancho/espesor + 1.393 + 0.667*np.log(ancho/espesor + 1.444)))
    impedancias_caracteristicas.append(I_c)

# (4) Calculos para coeficiente de reflexion

coeficientes_de_reflexion = []
for impedancia_caracteristica in impedancias_caracteristicas:
    C_r = (Z_l - impedancia_caracteristica)/(Z_l + impedancia_caracteristica)
    coeficientes_de_reflexion.append(C_r)

# Crear tabla para observar los resultados

tabla = []
for i, ancho in enumerate(anchos):
    fila = [
        ancho,
        permitividades_efectivas[i],
        velocidades_de_fase[i],
        impedancias_caracteristicas[i],
        coeficientes_de_reflexion[i]
    ]
    tabla.append(fila)

# Encabezados de la tabla

headers = ["Anchos (m)", "Permitividad Efectiva", "Velocidad de Fase (m/s)", "Impedancia Característica (Ω)", "Coeficiente de Reflexión"]

# Mostrar tabla con la libreria tabulate

print("\n")
print(tabulate(tabla, headers=headers, floatfmt=".6f", tablefmt="rounded_grid"))
print("\n")

# Definir el rango de frecuencias

f = np.linspace(0.5, 5, 100000)

# Definir las funciones de resistencia y reactancia

def resistencia(f, pos_anchos):
    Z_o = impedancias_caracteristicas[pos_anchos]
    f = f*np.power(10,9)
    V_p = velocidades_de_fase[pos_anchos]
    impedancia = Z_o*(Z_l + 1j*Z_o*np.tan(2*pi*f*largo/V_p))/(Z_o + 1j*Z_l*np.tan(2*pi*f*largo/V_p))
    return impedancia.real

def reactancia(f, pos_anchos):
    Z_o = impedancias_caracteristicas[pos_anchos]
    f = f*np.power(10,9)
    V_p = velocidades_de_fase[pos_anchos]
    impedancia = Z_o*(Z_l + 1j*Z_o*np.tan(2*pi*f*largo/V_p))/(Z_o + 1j*Z_l*np.tan(2*pi*f*largo/V_p))
    return impedancia.imag

# Realizar las graficas en funcion de la frecuencia y ancho deseado

def funcion_a_graficar(resistencia_o_reactancia):
    if resistencia_o_reactancia == "Resistencia":
        plt.figure(figsize=(18, 8))

        plt.plot(f, resistencia(f, 0), label="w = 1mm")
        plt.plot(f, resistencia(f, 1), label="w = 2mm")
        plt.plot(f, resistencia(f, 2), label="w = 3mm")
        plt.plot(f, resistencia(f, 3), label="w = 4mm")
        plt.plot(f, resistencia(f, 4), label="w = 5mm")
        plt.title('Resistencia de entrada en función de la frecuencia y del ancho')
        plt.xlabel('Frecuencia (GHz)')
        plt.ylabel('Resistencia (Ω)')
        plt.xlim(0.5, 5)
        plt.legend(loc="upper left")
        plt.grid(True)

        plt.tight_layout()
        plt.show()
        
    elif resistencia_o_reactancia == "Reactancia":
        plt.figure(figsize=(18, 8))

        plt.plot(f, reactancia(f, 0), label="w = 1mm")
        plt.plot(f, reactancia(f, 1), label="w = 2mm")
        plt.plot(f, reactancia(f, 2), label="w = 3mm")
        plt.plot(f, reactancia(f, 3), label="w = 4mm")
        plt.plot(f, reactancia(f, 4), label="w = 5mm")
        plt.title('Reactancia de entrada en función de la frecuencia y del ancho')
        plt.xlabel('Frecuencia (GHz)')
        plt.ylabel('Reactancia (Ω)')
        plt.xlim(0.5, 5)
        plt.legend(loc="upper left")
        plt.grid(True)

        plt.tight_layout()
        plt.show()
    
funcion_a_graficar("Resistencia")
# funcion_a_graficar("Reactancia")

