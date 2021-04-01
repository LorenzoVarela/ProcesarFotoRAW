#!/usr/bin/python
import os, sys
import shutil
import shlex, subprocess

from stat import *

# Directrio sobre el que se van a copiar los archivpo
dirActualRaiz = '/samba/Desarrollo/python/prodesar_imagens'

dirProcesar = dirActualRaiz + '/Procesar'
dirDestino = dirActualRaiz +'/Procesado' # Imagenes ya procesadas
dirAlmacen = dirActualRaiz +'/Original' # Imagenes originales
 
def walktree(top, callback):
   '''recursively descend the directory tree rooted at top,
      calling the callback function for each regular file'''
 
   for f in os.listdir(top):
       pathname = os.path.join(top, f)
       mode = os.stat(pathname)[ST_MODE]
       if S_ISDIR(mode):
           # It's a directory, recurse into it
           creardir(pathname, f)
           walktree(pathname, callback)
           #os.rmdir(pathname)
       elif S_ISREG(mode):
           # It's a file, call the callback function
           callback(pathname,f,top)
       else:
           # Unknown file type, print a message
           print 'Skipping %s' % pathname
       

def creardir(path, name):
    # Creamos las nuevas carpetas en el directorido dirDestino
    pathdest = path.replace('Procesar','Original')
    print 'creando directorio en Original____________', pathdest
    try:
       os.mkdir(pathdest)
    except OSError:
       print '*************Directorio en Originales ' , pathdest , ' ya existe'
       #print("Error detectado: ", sys.exc_info()[0])
       #print("Error detectado: ", sys.exc_info()[1])
    except:
       print("Error detectado No controlado: " + sys.exc_info()[0] + sys.exc_info()[1])

    
    pathdest = path.replace('Procesar','Procesado')
    print 'creando directorio en Procesardo___________', pathdest
    try:
       os.mkdir(pathdest)
    except OSError:
       print '*************Directorio en Procesados ' , pathdest , ' ya existe'
       #print("Error detectado: ", sys.exc_info()[0])
       #print("Error detectado: ", sys.exc_info()[1])
    except:
       print("Error detectado No controlado: " + sys.exc_info()[0] + sys.exc_info()[1])



def visitfile(fullname,file,path):
    #print 'visiting', file, 'in', path, "=", fullname
    longitud = len(file)
    extension = file[longitud-3:longitud]

    fotosProcesadas = path.replace('Procesar','Procesado')
    fotosOriginales = path.replace('Procesar','Original')
        
    print '>> Procesando Imagen _______________________________________________________ ' + fullname
    try:
       if extension == 'CR2':
         # Si el fichero es de tipo RAW lo procesamos
         command_line = 'ufraw-batch --size=2000,2000 --out-path="' + fotosProcesadas + '" --out-type jpg ''"' + fullname +'"'
         args = shlex.split(command_line)
         subprocess.call(args)
       elif extension =='.py' or extension=='txt' or extension=='out':
         # es el procedimiento que no se tiene que expandir
         print ("No procesamos fichero "+ file)
       else:
         #Copiamos los ficheros que no se procesan
         shutil.copyfile(path + '/' + file, fotosProcesadas  + '/' + file)
         # movemos el archivo al directorio destino
    except IOError:
       print("<<ERROR>>")
       print("<<ERROR>> procesando el fichero " + file)
       print("<<ERROR>>")
       #print("Error al copiar " + path + '/' + file + " en " + fotosProcesadas  + '/' + file)
       #print("Error detectado: ", sys.exc_info()[0])
       #print("Error detectado: ", sys.exc_info()[1])
    except:
       print("Error detectado No controlado: ", sys.exc_info()[0])
       print("Error detectado No controlado: ", sys.exc_info()[1])
       

    try:
       if extension=='.py' or extension=='txt' or extension=='out':
          print ("No movemos fichero " + file)
       else:
          print (path + '/' + file, fotosOriginales  + '/' + file)
          ##os.rename(  dirProcesar + '/' + path + '/' + file ,  dirAlmacen  + '/' + path + '/' + file )
          os.rename(path + '/' + file, fotosOriginales  + '/' + file)
    except OSError:
       print("<<ERROR>>")
       print("<<ERROR>> moviendo el fichero " + file + " al directorio de almacenamiento")
       print("<<ERROR>>")
       #print("Error detectado: ", sys.exc_info()[0])
       #print("Error detectado: ", sys.exc_info()[1])

    except:
       print("Error detectado No controlado: ", sys.exc_info()[0])
       print("Error detectado No controlado: ", sys.exc_info()[1])
       

 
if __name__ == '__main__':
   walktree(sys.argv[1], visitfile)
   #walktree('/samba/Desarrollo/python/prodesar_imagens/Procesar', visitfile)
