#-------------------------------------------------------------------------------------------------------
#Definiendo una variable
a = 2
#Definiendo una variable con camelCase
bB = 3
#Definiendo una variable con snake_case (el recomendado)
c_c = a + bB

print(c_c)

nombre = "león"

print(nombre)

#las variables se declaran y despues se definen
#las variables comunes se pueden modificar (redefiniendo)

numero = 10
#numero += 1
#numero -= 1

print(numero)

#el + antes del = significa que va a sumar el valor nuevo con el valor anterior
#-------------------------------------------------------------------------------------------------------
#concatenar strings con +
nombre = "león"
bienvenida = "Hola " + nombre + " ¿Como estas?"

print(bienvenida)
#-------------------------------------------------------------------------------------------------------
#concatener númericos con f-strings
numero = 5
#del numero
resultado = f"El resultado de tu operación es {numero}"
print(resultado)
#-------------------------------------------------------------------------------------------------------
#operadores de pertenencia (in / not in)
print("El" in resultado) #true
print("El" not in resultado) #false
#-------------------------------------------------------------------------------------------------------