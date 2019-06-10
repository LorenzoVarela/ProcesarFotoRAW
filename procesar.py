#!/usr/bin/python

import os
import shutil
import shlex, subprocess

# Directrio sobre el que se van a copiar los archivpo
dirActualRaiz = '/srv/dev-disk-by-label-NAS/ImagenesCopia'

dirProcesar = dirActualRaiz + '/Procesar'
dirDestino = dirActualRaiz + '/Procesado'
dirAlmacen = dirActualRaiz + '/Original'

# Recorremos los direcotios.
for base, dirs, files in os.walk('.'):
  for name in dirs:
    # Creamos las nuevas carpetas en el directorido dirDestino
    try:
      os.mkdir(os.path.join(dirDestino, name))
    except OSError:
      print("Directorio destino " + name + " ya existe")

    try:
      os.mkdir(os.path.join(dirAlmacen, name))
    except OSError:
      print("Directorio Almacen " + name + " ya existe")

    
    # Procesamos todas las carpetas del directorio de trabajo
    # Para buscar todos los ficheros de imagen y procesar aquellos
    # que son de tipo RAW
    print 'Procesando directorio _____________________________________________________ ' + name
    for base1, dirs1, files1 in os.walk(name + '/'):
      for file1 in files1:
        longitud = len(file1)
        extension = file1[longitud-3:longitud]
        
        print '>> Procesando Imagen _______________________________________________________ ' + file1
        try:
          if extension == 'CR2':
            # Si el fichero es de tipo RAW lo procesamos
            command_line = 'ufraw-batch --size=1000,1000 --out-path="' + dirDestino + '/' + name + '" --out-type jpg ''"./' + name + '/' + file1 + '"'
            # print command_line
            args = shlex.split(command_line)
            subprocess.call(args)
          else:
            #Copiamos los ficheros que no se procesan
            shutil.copyfile(dirProcesar +'/' + name + '/' + file1, dirDestino +'/' + name + '/' + file1)
          # movemos el archivo al directorio destino
        except IOError:
          print("<<ERROR>>")
          print("<<ERROR>> procesando el fichero " + file1)
          print("<<ERROR>>")

        try:
          os.rename(  dirProcesar + '/' + name + '/' + file1 ,  dirAlmacen  + '/' + name + '/' + file1 )
        except OSError:
          print("<<ERROR>>")
          print("<<ERROR>> moviendo el fichero " + file1 + " al directorio de almacenamiento")
          print("<<ERROR>>")


    # Borramos el directorio
    os.rmdir(name)

    