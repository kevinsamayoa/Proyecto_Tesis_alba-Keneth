# Proyecto_Tesis_alba-Keneth
para poder utilizar el proyecto se deben de tener las siguientes herramientas instaladas: Xampp Version3.2.4 esta para utilizar el apache que ya trae y el MySQL(se debe de cambaiar el puerto de uso al 3307 para que levante el proyecto), Python (no importa la version que tenga instalada) y poetry.

Instalacion Xampp: para poder instalar Xampp vaya ingrese el siguiente link en su navegador https://www.apachefriends.org/es/download.html
Luego descarge la version correspondiente a su sistema opertativo y a su arquitectura.
Debe asegurarse que los componentes de Apache y MySQL esten seleccionados al momento de instalar

### Al momento de configurar el usuario root de su base de datos de Xampp favor colocarlo sin contraseña 


Al terminar la instalacion esta deberia de ser la vista correcta

![Xampp instalado](https://user-images.githubusercontent.com/60972307/134262090-db1aa9ea-64a3-42cd-a2fc-729c86a24671.png)


El puerto que trae por defecto Xampp para el MySQL es el 3306 pero este se cambio para el proyecto ya que hay muchas aplicacioes o software que pueden tomar ese puerto y causar problemas con nuestro proyecto.

Para cambiar su puerto del MySQL debe de ingresar al boton config del mismo

![image](https://user-images.githubusercontent.com/60972307/134262458-66ddf4a9-26e5-4c90-9265-1df7723f928d.png)

y posteriormente ingresarl al boton my.ini

![image](https://user-images.githubusercontent.com/60972307/134262569-17694435-f285-42a8-94ae-daf462676a50.png)

una vez adentro del documento de texto que este abrira debe encontrar los siguientes bloques de texto que tendran el puerto 3306 y cambiarlo por el puerto 3307

![image](https://user-images.githubusercontent.com/60972307/134262749-cd667c2c-14c6-40c9-ae95-42a973d07c14.png)


![image](https://user-images.githubusercontent.com/60972307/134262807-d26cecce-bebb-4717-9fc3-5336e1e4152e.png)

Si usted quiere mantener el puerto 3306 (no es recomendable para este proyecto) debe realizar un cambio en el repositorio una vez ya este descargado en su PC.

Para esto vaya a la carpeta donde esta su repositorio e ingrese al siguiente documento:

![image](https://user-images.githubusercontent.com/60972307/134262965-99abff71-a6ad-42cf-8c08-cd79d78aae93.png)


una vez dentro solo debe de cambiar el siguiente puerto por el que quiera utilizar en su XAMPP:

![image](https://user-images.githubusercontent.com/60972307/134263036-d9b4e3de-5596-4671-a73b-c4b65819c8d5.png)

NOTA: este proceso tambien se puede realizar si usted va a utilizar un usuario diferente a root y este tiene una contraseña, se cambian los siguientes valores

![image](https://user-images.githubusercontent.com/60972307/134263140-6477220a-cb7c-4a9b-861a-37f6dc80517f.png)

### Ya tenemos instalado y configurado nuestro Xampp.

Lo siguiente que debemos de instalar sera nuestro Python para lo cual debemos de ingresar en nuestro navegador el siguiente link:https://www.python.org/downloads/

Nuevamente descargamos la version que sea compatible con nuestro sistema operativo la arquitectura de nuestra PC y procedemos con la descarga e instalcion (en este caso no hay que realizar cambios o configuraciones especiales.

![image](https://user-images.githubusercontent.com/60972307/134263434-1378a162-1b97-4c2b-9e0f-d50099d6be69.png)


Al completar la instalcion de Python ingresamos en nuestro navegador el siguiente link para descargar la ultima herramienta que necesitaremos: https://python-poetry.org/docs/

Bajamos hasta encontrar el turorial de instalacion:


![image](https://user-images.githubusercontent.com/60972307/134263592-c1b0ccfb-33a0-4064-9545-3a64f504dc99.png)

Abrimos nuestro editor de linea de comandos el cual puede cambiar dependiendo si tenemos una maquina con sistema operativo windows o linux.

si tiene Windows sera powershell en modo administrador(click derecho sobre el programa y ejecutar como administrador)

![image](https://user-images.githubusercontent.com/60972307/134263828-e2d96864-069e-42e0-b203-b0020c01bb87.png)

Ahora segimos el turorial que nos muestra la pagina de poetry:

descargamos poetry: (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

validamos la version: poetry --version

![image](https://user-images.githubusercontent.com/60972307/134263986-9a4627d1-173a-4ebd-b71e-393071038a33.png)


una vez instalado poetry y descargado el repositorio completo del proyecto ejecutamos los siguientes comando en  powerShell.

## NOTA: para ello debe de estar activo xampp con los servicios de apache y MySQL iniciados y previamente configurados:

primero ingresamos a la direccion donde se encuetra nuestro proyecto descargado con el comando: cd

![image](https://user-images.githubusercontent.com/60972307/134264236-49a1802d-da19-40a6-81eb-61b7a59eec59.png)


una vez en la direccion de nuestro proyecto ejecutamos el siguiente comando para inicializar los servicios:  poetry run py .\manage.py runserver


![image](https://user-images.githubusercontent.com/60972307/134264359-822d58c4-4393-4eb6-9d71-4d635cc9d69a.png)


y listo nuestro proyecto deberia de estar corriendo, solo debemos ingresar en nuestro navegador lo siguiente: http://localhost:8000/ para entrar a la pagina del proyecto.

![image](https://user-images.githubusercontent.com/60972307/134264521-71ab7b16-2e9c-4a0f-aede-5dd9cba427d3.png)

Espero este pequeño resumen sea de utilidad.


# para consultas puede escribirme al Whatsapp 32830557 o al correo:ksamayoag2@miumg.edu.gt


