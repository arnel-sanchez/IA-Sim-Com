# IA-Sim-Com

## Como instalar el proyecto

### Instalar Python

```bash
$ git clone https://github.com/arnel-sanchez/IA-Sim-Com
$ cd IA-Sim-Com/Proyecto
$ python -m pip install --upgrade pip && python -m pip install pynput && python -m pip install numpy
$ wget https://sourceforge.net/projects/pyke/files/pyke/1.1.1/pyke3-1.1.1.zip && unzip pyke3-1.1.1.zip && cd pyke-1.1.1 && python setup.py build && python setup.py install
$ python main.py
```
## [Informe](https://github.com/arnel-sanchez/IA-Sim-Com/blob/master/Informe/Informe.pdf)

## Ayuda

Nuestro DSL es un lenguaje con tipado estatico , se pueden definir variables de forma que declares su tipo y le asignes un valor,como C#. 
Los tipos de variables con los que contamos son int , double,string y bool .Puedes redefinir variables solo en el ambito en que fueron creadas.
Un ambito o contexto solo se crea al crear una funcion fuera de un tipo o al crear un tipo . Podemos utilizar If , hacer ciclos While , 
definir funciones , Crear tipos, que seran en nuestro caso bike y rider.En cuanto a la definicion de funciones , dentro de la definicion 
de una funcion no podemos definir otra funcion ni crear tipos.En cuanto a la creacion de tipos se crean de esta forma: 
Type id{ ... }, dentro del ambito solo se podran declarar definiciones de funciones y en caso de que sea un piloto se podran redefinir las
variables cornering o step_by_line, solo ellas, que son enteras y definen la habilidad del piloto en curva y recta y pueden tener un valor desde
0 hasta 10.Las funciones definidas dentro de un tipo rider solo pueden ser "select_action" que devuelve un entero y "select_acceleration" 
que es void.EL otro tipo que se puede crear es un tipo Bike ,dentro del cual no se pueden redefinir variables ,solo se puede definir una funcion
cuyo nombre debe ser "select_configuration", debe ser void.

Las variables que pertenecen inicialmente al contexto de un rider son: "speed","acceleration","time_lap","cornering" y "step_by_line"
Las variables que pertenecen inicialmente al contexto de un bike son: "brand","max_speed","weight","tires","brakes" y "chassis_stiffness"

 
Dentro de una funcion puedo crear una variable con id igual a otra variable de un contexto padre, si dentro de dicha funcion se llama este
id se accedera a la variable del ambito de la funcion.Las variables que sean invocadas y no existan en el ambito actual pero si lo hagan en
un ambito padre solo podran ser evaluadas , nunca redefinidas , en otras palabras no existen variables globales.Destacar que una funcion 
y una declaracion de tipo es lo unico que crea un contexto , cuando se crea un while o un if las variables que se creen dentro de ellos 
pertenecen al contexto al que pertenece dicha declaracion while o If.Estas caracteristicas hacen que puedan existir errores en tiempo de ejecucion
,como utilizar una variable que aun no tiene valor ya que su definicion puede verse truncada por un break , continue, return ,o por si se entra 
a un while o no.En estos casos retornaremos el error en tiempo de ejecucuion.Otro posible Runtime Error seria dividir un numero cualqueira entre cero.
