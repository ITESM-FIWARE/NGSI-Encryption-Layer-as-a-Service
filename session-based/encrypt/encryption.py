# -*- coding: utf-8 -*-
from __future__ import print_function

# Backend
from flask import Flask
from flask import request, render_template, jsonify, session, Response
from werkzeug.security import generate_password_hash, check_password_hash

# Conect database
from pymongo import MongoClient
from Mongomodel import Mongomodel, MongomodelRegister
# Send email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from validate_email import validate_email
# Extras
from collections import OrderedDict # Mantener orden de diccionario
from time import strftime
import smtplib
import commands
import pprint # imprime por pantalla arreglos JSON en modo pretty()
import re, os, json, urllib2, urllib

#Dirección de correo gmail
from_address = os.environ['MAIL_GMAIL']
#Ruta archivo de llaves
ruta_adjunto = './key.txt'
#Nombre archivo de llaves
nombre_adjunto = 'key.txt'
usuarios = []
emails = []
urls = []
passwords = []
#Conexión al Server de MongoDB pasandole el host y el puerto
MongoClient = MongoClient(
	os.environ['MONGOOCB_PORT_27017_TCP_ADDR'],
	27017)
#Conexión a la base de datos 
db = MongoClient.encryptpython 
#Conexión con la colección users
collection = db.users 
#Conexión con la colección registry
collectionReg = db.registry    
# Variable auxiliar para validar que sea una url de Orion correcta
urlverify = 'v2/entities'

#Retorna urlFromCompuesta y urlToCompuesta
def validateURL(urlFrom,urlTo,idEntity,typeEntity, fichero):
        if urlverify in urlFrom:
            if urlverify in urlTo:
                #Crea urlFrom para extraer entidad de oreon
                urlFromCompuesta = urlFrom+'/'+idEntity+'?type='+typeEntity
                #Crea urlTo para extraer entidad de oreon  
                urlToCompuesta = urlTo+'/'+idEntity+'?type='+typeEntity  
                #print(urlFromCompuesta)
                #print(urlToCompuesta)
                try:
                    #Extraer modelo JSON del Orion de entrada
					req = urllib2.Request(urlFromCompuesta)
                    #Cabeceras para hacer la petición al OCB
					req.add_header('Accept', 'application/json')
					req.add_header('Fiware-Service', 'default')
					req.add_header('Fiware-ServicePath', '/')
                    # Obtener json de urlFromCompuesta
					response = urllib2.urlopen(req)
                    #Ordenar datos del objeto JSON en orden de entrada
					dataurlFrom = json.loads(response.read(),object_pairs_hook=OrderedDict) 
                    
                    #Función utilizada con urlib. Las peticiones no incluyen cabeceras
                    #Obtener json de urlFromCompuesta
                    #response = urllib.urlopen(urlFromCompuesta)
                    # Ordenar datos de JSON en orden de entrada
                    #dataurlFrom = json.loads(response.read(),object_pairs_hook=OrderedDict) 
                except:
                    #Si no se encuetra ningun objeto JSON se captura el error y se retorna un mensaje de advertencia
                    return ('Invalid urlFrom')
                    #return jsonify({'message':'Invalid urlFrom'})
                try:
                    #la libreria urllib2 si no encuetra un modelo JSON en automatico retorna un error
                    #Extraer modelo JSON del Orion de destino
                    req = urllib2.Request(urlToCompuesta)
                    #Cabeceras para hacer la petición al OCB
                    req.add_header('Accept', 'application/json')
                    req.add_header('Fiware-Service', 'default')
                    req.add_header('Fiware-ServicePath', '/')
                    # Obtener JSON de urlFromCompuesta
                    response = urllib2.urlopen(req)
                    #Ordenar datos del objeto JSON en orden de entrada
                    dataurlTo = json.loads(response.read(),object_pairs_hook=OrderedDict) 
                    #response = urllib.urlopen(urlToCompuesta)# Obtener json de urlFromCompuesta
                    #dataurlTo = json.loads(response.read(),object_pairs_hook=OrderedDict) # Ordenar datos de JSON en orden de entrada
                except:
                    #Se captura el error y se asigna un valor por defecto a la variable dataurlTo
                    dataurlTo = {"error": "NotFound","description": "The requested entity has not been found. Check type and id"}
                    #return('Invalid urlTo')
                    #return jsonify({'message':'Invalid urlTo'})            
            else:
                return('Invalid Orion urlTo')
                #return jsonify({'message':'Invalid Orion urlTo'})                
        else:
            return('Invalid Orion urlFrom')
            #return jsonify({'message':'Invalid Orion urlFrom'})

        #Verifiacar existencia de la entidad en el orionTo "urlTo"    
        idEnt = dataurlTo.get('id')
        typeEnt = dataurlTo.get('type')
        description = dataurlTo.get("description")
        if idEntity == idEnt:
            if typeEntity == typeEnt:
                return('Stop Proccess: Model Already Exists in OrionTo')
                #return jsonify({'message':'Stop Proccess: Model Already Exists in OrionTo'})
        if "service not found" == description:
            return ('Invalid urlTo: service not found')
            #return jsonify({'message':'Invalid urlTo: service not found'})

        #Verificar json de entrada desde urlFrom
        idEnt = dataurlFrom.get("id")
        typeEnt = dataurlFrom.get("type")
        description = dataurlFrom.get("description")
        if "service not found" == description:
            return('Invalid urlFrom: service not found')
            #return jsonify({'message':'Invalid urlFrom: service not found'})
        if idEntity == idEnt:
            if typeEntity == typeEnt:
                #Inserción de "dataurlFrom" en in.json desde Orion "urlFrom"
                with open(fichero,'w') as file: 
                    json.dump(dataurlFrom, file, indent=4)	
            else:
              return('The requested entity has not been found. Check type and id')
              #return jsonify({'message':'The requested entity has not been found. Check type and id'})
        else:
            return('The requested entity has not been found. Check type and id')
            #return jsonify({'message':'The requested entity has not been found. Check type and id'})   
        return(urlFromCompuesta,urlToCompuesta)   

#Retorna urlFromCompuesta
def validateURL1(urlFrom,idEntity,typeEntity, fichero):
        if urlverify in urlFrom:
            urlFromCompuesta = urlFrom+'/'+idEntity+'?type='+typeEntity #componer urlFrom para extraer entidad de oreon 
            print(urlFromCompuesta)
            try:
				req = urllib2.Request(urlFromCompuesta)
				req.add_header('Accept', 'application/json')
				req.add_header('Fiware-Service', 'default')
				req.add_header('Fiware-ServicePath', '/')
				response = urllib2.urlopen(req)# Obtener json de urlFromCompuesta
				dataurlFrom = json.loads(response.read(),object_pairs_hook=OrderedDict) # Ordenar datos de JSON en orden de entrada
                #response = urllib.urlopen(urlFromCompuesta)# Obtener json de urlFromCompuesta
                #dataurlFrom = json.loads(response.read(),object_pairs_hook=OrderedDict) # Ordenar datos de JSON en orden de entrada
            except:
                return ('Invalid urlFrom')
                #return jsonify({'message':'Invalid urlFrom'})                           
        else:
            return('Invalid Orion urlFrom')
            #return jsonify({'message':'Invalid Orion urlFrom'})

        #Verificar json de entrada desde urlFrom
        idEnt = dataurlFrom.get("id")
        typeEnt = dataurlFrom.get("type")
        description = dataurlFrom.get("description")
        if "service not found" == description:
            return('Invalid urlFrom: service not found')
            #return jsonify({'message':'Invalid urlFrom: service not found'})
        if idEntity == idEnt:
            if typeEntity == typeEnt:
                with open(fichero,'w') as file:# inserción de data en in.json desde Orion "urlFrom" 
                    json.dump(dataurlFrom, file, indent=4)	
            else:
              return('The requested entity has not been found. Check type and id')
              #return jsonify({'message':'The requested entity has not been found. Check type and id'})
        else:
            return('The requested entity has not been found. Check type and id')
            #return jsonify({'message':'The requested entity has not been found. Check type and id'})   
        return(urlFromCompuesta)   

#Insertar Registro de actividades en mongo
def regMongo(user, service, urlFrom, idEntity, typeEntity, urlTo):
    try:
        service = service
        date = strftime("%y-%m-%d")
        hour = strftime("%H:%M:%S")
        log = [MongomodelRegister(user, service, hour, date, urlFrom, idEntity, typeEntity,urlTo)]
        for usuario in log:
            collectionReg.insert(usuario.toDBCollection())
        return('ok')
    except:
        return ('Error when doing activity log in Mongodb')

#Inserción de out.json en oreon (Ajustar out.json a formato de entrada de datos oreon)
def insertOrion(urlTo, fichero):
    fileOut = fichero
    fichero = str('cat '+fichero)
    contenido=open(fileOut).read().splitlines() # Guardar contenido de out.json
    contenido.insert(0,"curl "+urlTo+" -s -S -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Fiware-Service: default' -H 'Fiware-ServicePath: /' -d @- <<EOF")
    f = open(fileOut, 'w')
    f.writelines("\n".join(contenido))
    f.write("\n"+"EOF")
    f.close()
    # Inserción del modelo encriptado en orion
    jsonfile = commands.getoutput(fichero) # Extrer contenido de out.json
     #Excepsión insercion del modelo en orion
    responceOrion = os.popen(jsonfile).read() # Ejecutar out.json
    if "service not found" in responceOrion:
        return ('Invalid Orion urlTo')
    if "Already Exists" in responceOrion:
        return ('Model Already Exists in Orion')   
    #return('ok')
    return(responceOrion) 

#Enviar llaves por mail       
def sendEMAIL(email, asunto, message):
    try:
        #Crear conexion con el servidor de correos
        smtp = smtplib.SMTP("smtp.gmail.com", 587)  
        # Cifrar la conexion con el servidor
        smtp.ehlo()  
        smtp.starttls()
        smtp.ehlo()
        #Iniciar sesion en el correo 
    	smtp.login(from_address,os.environ['PASSWORD'])
        #Crear objeto mensaje
        mensaje = MIMEMultipart() 
        #Se establecen los atributos del mensaje
        mensaje["From"] = from_address
        mensaje["To"] = email
        mensaje["Subject"]=(asunto)
        #Se agrega el cuerpo del mensaje como objeto MIME de tipo texto 
        mensaje.attach(MIMEText((message), 'plain')) 
        #Se envia el correo
        smtp.sendmail(from_address, email, mensaje.as_string()) 
        #os.system("rm inencrypt.json && rm key.txt && rm outencrypt.json")
    except:
        return ('Error send mail')

application = Flask(__name__)
@application.route('/')
def index():
    return jsonify({'message': 'Welcome ENCRYPTJSON','version': 'v1.1'})

@application.route('/home')
def home():
    if "user" in session:
        return jsonify({'message': 'Welcome ENCRYPTJSON','version': 'v1.1'})
    return jsonify({'mesagge': 'You must log in  first.'})

# Modificar URL de salida 
@application.route('/outurl', methods=["POST"])
def outurl():

    if "user" in session:
        user = session["user"] # obtener usuario desde la sesión
        out_url = request.form['out_url'] # Obtener url mediante formulario
        collection.update({"user":user},{'$set': {'out_url':out_url}}, multi=True) # Cambiando url_out
        cursor = collection.find_one({"user":user}) # Obtener documento actualizado del usario
        pprint.pprint(cursor)

        return jsonify({'message': "URL de salida modificada por","user":user,'url modificada':out_url})

    return jsonify({'messsage':'You must log in first.'})

# Cerrar sesión 
@application.route('/logout', methods=["POST"])
def logout():
    session.pop("user", None)

    return jsonify({'message':'You are logged out.'})

# Iniciar sesión
@application.route('/login', methods=["POST"])
def login():
    try : 
        user = request.form['name']
        password = request.form['password']   
    except:
        return jsonify({'message':'Enter user and password'})
    cursor = collection.find()
    print (cursor)
    for usuario in cursor:
        usuarios.append(usuario['user'])
        passwords.append(usuario['password'])
    
    if user in usuarios:
        position = usuarios.index(user)
        passw = str(passwords[position])
        check_password = check_password_hash(passw, password)
        if check_password is True:
            session["user"] = user
            return jsonify({'message':'You are logged in'})
        else:
            return jsonify({'message':'Incorrect password'})
    else:     
        return jsonify({'message':'Non-existent user'})

# Registro usuario
@application.route('/signup', methods=["POST"])
def signup(): 
    try:
        user = request.form['name']
        email = request.form['email']
        password = request.form['password']
    except:
        return jsonify({'message':'Enter user, email and password'})
    hashed_pw = generate_password_hash(password, method='sha256')

    # "READ" --> Lee los documentos de la base de datos
    cursor = collection.find()
    for usuario in cursor:
        usuarios.append(usuario['user'])
        emails.append(usuario['email'])
    # Control de usuarios  
    if user in usuarios:
        return jsonify ({'message':'User already exists'})
    # Control de email
    if email in emails:
        return jsonify({'mesagge' : 'Email already exists'})
    # Validacion de email (gmail)
    trueEmail = validate_email(email, verify=True)
    if (trueEmail == True): 
        if re.match('^[(a-z0-9\_\-\.)]+@gmail.com',email.lower()):
            # Enviar email de confirmación
            asunto = ("Encryption as a Service, Successful register")
            message = ("User: "+user+'\n'+"Password: "+password)
            returnEmailMetod = sendEMAIL(email, asunto, message)
            print(returnEmailMetod)
            # "CREATE" 
            log = [Mongomodel(user, email, hashed_pw)]
            for usuario in log:
                collection.insert(usuario.toDBCollection())
            return jsonify([{'message': 'User save successful'},{'usuario': user, 'email': email}])
        else:
            return jsonify({'mesage':'Its not an email gmail, re-enter email'})
    else:
        return jsonify({'message':'Nonexistent email, re-enter email'})

#Decrypt JSON
@application.route('/decrypt', methods=["POST"])
def decrypt():
    if "user" in session:
        user = session['user']
        os.system('rm indecrypt.json && rm outdecrypt.json && rm key.txt')
        try:
            jsonfile = request.form['json'] #obtener json encryptado
            keys = request.form['key'] #obtener llaves
        except:
            return jsonify({'message': 'Enter json and key'})
        try:
            decoder = json.JSONDecoder(object_pairs_hook=OrderedDict) 
            jsonfile = decoder.decode(jsonfile)
        except:
            return jsonify({'message':'JSON not valid'})
        idEntity = jsonfile.get('id')
        typeEntity = jsonfile.get('entity')
        with open('indecrypt.json','w') as file: # Guardar JSON de entrada
            json.dump(jsonfile, file, indent=4)
        f = open('key.txt','w') #Guardar keys de entrada 
        f.write(keys)
        f.close()
        decryptResult = os.popen('java -jar decryptJSON.jar').readline()# Desencriptar
        if "keys and values don't match" in decryptResult:
            return jsonify({'message':"keys and entities don't match"})
        try:
            f = open('outdecrypt.json','r')
        except:
            return jsonify ({'message':"keys and entities don't match"})
        with f as file:
            try:
                contenido = json.load(file, object_pairs_hook=OrderedDict)
            except:
                return jsonify ({'message':'Invalid key'})
        os.system('rm indecrypt.json && rm outdecrypt.json && rm key.txt')
        # Insertar Registro de actividades en mongo
        service = ('decrypt')
        urlFrom = ''
        urlTo = ''
        registroMongo = [regMongo(user, service, idEntity, typeEntity, urlFrom, urlTo)]
        if 'error' in registroMongo:
            print (registroMongo) 

        return '{}'.format(json.dumps(contenido,indent=4))

    return jsonify({'message': 'You must log in first.'})

#Decrypt ORION
@application.route('/decrypt/ocb', methods=["POST"])
def decryptORION():
    if "user" in session:
        os.system('rm indecrypt.json && rm outdecrypt.json && rm key.txt')
        user = session['user'] # Obtener ususario de la sesión
        try :
            urlFrom = request.form['urlFrom'] #Obtener urFrom del formulario
            idEntity = request.form['id'] # Obtener id del formulario
            typeEntity = request.form['type'] # Obtener type del formulario
            urlTo = request.form['urlTo']# Obtener urlTo del formulario
            key = request.form['key']# Obtener key del formulario
        except:
            return jsonify({'message':'Enter urlFrom, urlTo, id, type and key'})        
   
        #Validar URLs
        fichero = 'indecrypt.json'
        urls = validateURL(str(urlFrom), str(urlTo), str(idEntity), str(typeEntity), str(fichero)) 
        urlFromCompuesta = urls[0]
        if urlverify in urlFromCompuesta:    
            urlToCompuesta = urls[1]
        else :
            return jsonify({'message':urls})
        
        f = open('key.txt','w') # Guardar llaves en key.txt
        key = f.writelines(key)
        f.close()

        #response = urllib.urlopen(urlFromCompuesta)# Obtener json de urlFrom
        #data = json.loads(response.read(),object_pairs_hook=OrderedDict) # Ordenar datos de JSON en orden de entrada
        try:#la libreria urllib2 si no encuetra una pagina en automatico retorna un error
            req = urllib2.Request(urlFromCompuesta)
            req.add_header('Accept', 'application/json')
            req.add_header('Fiware-Service', 'default')
            req.add_header('Fiware-ServicePath', '/')
            response = urllib2.urlopen(req)# Obtener json de urlFromCompuesta
            data = json.loads(response.read(),object_pairs_hook=OrderedDict) # Ordenar datos de JSON en orden de entrada
        except:#Se captura el error y se asigna un valor por defecto a la variable dataurlTo
            return('Invalid urlFrom')

        with open('indecrypt.json','w') as file:# inserción de data en in.json desde Orion "urlFrom" 
            json.dump(data, file, indent=4) 

        decryptResult = os.popen('java -jar decryptJSON.jar').readlines()# Desencriptar
        if "keys and values don't match" in decryptResult:
            return jsonify({'message':"keys and entities don't match"})
        try:
            f = open('outdecrypt.json','r')
        except:
            return jsonify ({'message':"Keys and entities don't match!!!"})            
        with f as file:
            try:
                contenido1 = json.load(file,object_pairs_hook=OrderedDict) 
            except:
                return jsonify ({'message':'Invalid key'})              
        # Inserción de out.json en oreon (Ajustar out.json a formato de entrada de datos oreon)
        fichero = 'outdecrypt.json'
        returninsertOrion = insertOrion(urlTo, fichero)
        if "orion" in returninsertOrion:
            return jsonify ({'message': returninsertOrion})
        keys = open('key.txt').read() # Obeniendo las keys del archivo

        # Insertar Registro de actividades en mongo
        service = ('decrypt/ocb')
        registroMongo = [regMongo(user, service, urlFrom, idEntity, typeEntity, urlTo)]
        if 'error' in registroMongo:
            print (registroMongo) 

        os.system('rm key.txt && rm in.json && rm out.json')
        return '{}'.format(json.dumps(contenido1,indent=4))
    return jsonify({'message': 'You must log in first.'})

# Desencriptar de Orion a modelo local
@application.route('/decrypt/ocb/local', methods=["POST"])
def decryptLOCAL():
    if "user" in session:
    	os.system("rm indecrypt.json && rm outdecrypt.json && rm key.txt")
        user = session['user']# Obtener usuario
        try: #Excepción "parametros de entrada"
            urlFrom = request.form['urlFrom']
            idEntity = request.form['id']
            typeEntity = request.form['type']
            key = request.form['key']
        except:
            return jsonify({'message':'Enter urlFrom, id, type and key'})
        #Validar URLs
        fichero = 'indecrypt.json'
        urlFromCompuesta = validateURL1(str(urlFrom), str(idEntity), str(typeEntity), str(fichero)) 
        if urlverify in urlFromCompuesta:    
            urlFromCompuesta = urlFromCompuesta
        else:
            return jsonify({'message':urls})# retorna el error que retorna la funcion validateURL
        # "READ" --> Lee los documentos de la base de datos
        for data in collection.find({"user":user},{"email":1,"_id":0}):
            data = data #Obtener datos del usuario
        email = data.get("email")

        f = open('key.txt','w') # Guardar llaves en key.txt
        key = f.writelines(key)
        f.close()
 
        decryptResult = os.popen('java -jar decryptJSON.jar').readlines()# Desencriptar
        if "keys and values don't match" in decryptResult:
            return jsonify({'message':"keys and entities don't match"})
        try:
            f = open('outdecrypt.json','r')
        except:
            return jsonify ({'message':"Keys and entities don't match!!!"})            
        with f as file:
            try:
                contenido = json.load(file,object_pairs_hook=OrderedDict) 
            except:
                return jsonify ({'message':'Invalid key'})             
        id_outJSON = contenido.get('id')# obtener id del diccionario
        # Inserción de out.json en oreon (Ajustar out.json a formato de entrada de datos oreon)
        #fichero = "outencrypt.json"
        #returninsertOrion = insertOrion(urlTo, fichero)
        #if "orion" in returninsertOrion:
        #    return jsonify ({'message': returninsertOrion})
        keys = open('key.txt').read() # Obeniendo las keys del archivo
        # Send keys email
        asunto = ("Encrypted keys of the Orion, model ID: " + id_outJSON)
        message = ("TYPE: "+typeEntity+"\n"+"User: "+user+"\n"+"Keys:"+"\n"+keys)
        returnEmailMetod = sendEMAIL(email, asunto, message)
        #print = (returnEmailMetod)
        # Insertar Registro de actividades en mongo
        #service = ('encrypt/ocb/local')
        #registroMongo = [regMongo(user, service, urlFrom, id_outJSON, typeEntity)]
        #if 'error' in registroMongo:
        #    print (registroMongo) 
        #print(returninsertOrion)
        return '{}'.format(json.dumps(contenido,indent=4))
    return jsonify({'messsage':'You must log in first.'})

# Encriptación JSON
@application.route('/encrypt', methods=["POST"])
def encrypt():
    if "user" in session:
    	os.system("rm inencrypt.json && rm outencrypt.json && rm key.txt")
        #obtener usuario desde la sesión
        user = session["user"] 
        for data in collection.find({"user":user},{"email":1,"_id":0}):
            #Obtener datos del usuario
            data = data 
        #Obtener email del diccionario
        email = data.get('email') 
        try:
            #Obtener JSON del formulario
            jsonfile = request.form['json'] 
        except: 
            return jsonify({'message':'Enter json'})
        try:
            #OrderecDict para mantener el orden del JSON de entrada
            decoder = json.JSONDecoder(object_pairs_hook=OrderedDict) 
            jsonfile = decoder.decode(jsonfile)
        except:
            return jsonify({'message':'JSON not valid'})
        idEntity = jsonfile.get('id')
        typeEntity = jsonfile.get('type')
        #Guardar JSON en in.json
        with open('inencrypt.json', 'w') as file: 
            json.dump(jsonfile, file, indent=4)
        os.system('rm key.txt')
        #Ejecución del programa java
        os.system("java -jar encryptJSON.jar") 

        #Obtener datos de out.json en orden de entrada
        with open('outencrypt.json','r') as file: 
            contenido = json.load(file, object_pairs_hook=OrderedDict)
        id_outJSON = contenido.get('id')
        typeEntity = contenido.get('type')
        
        #Obeniendo las llaves del archivo
        keys = open('key.txt').read() 

        #Send keys email
        asunto = ("Encrypted keys of the Orion, model ID: " + id_outJSON)
        message = ("TYPE: "+typeEntity+"\n"+"User: "+user+"\n"+"Keys:"+"\n"+keys)
        returnEmailMetod = sendEMAIL(email, asunto, message)
        
        # Insertar Registro de actividades en mongo
        service = ('encrypt')
        urlFrom = ('')
        urlTo = ('')
        registroMongo = [regMongo(user, service, idEntity, typeEntity, urlFrom, urlTo)]
        if 'error' in registroMongo:
            print (registroMongo) 
        os.system("rm inencrypt.json && rm outencrypt.json && rm key.txt")
        return '{}'.format(json.dumps(contenido,indent=4))
    return jsonify({'message': 'You must log in first.'})

# Encriptación Orion
@application.route('/encrypt/ocb', methods=["POST"])
def encryptORION():
    if "user" in session:
    	os.system("rm inencrypt.json && rm outencrypt.json && rm key.txt")
        user = session['user']# Obtener usuario
        try: #Excepción "parametros de entrada"
            urlFrom = request.form['urlFrom']
            urlTo = request.form['urlTo']
            idEntity = request.form['id']
            typeEntity = request.form['type']
        except:
            return jsonify({'message':'Enter urlFrom, urlTo, id and type'})
        #Validar URLs
        fichero = 'inencrypt.json'
        urls = validateURL(str(urlFrom), str(urlTo), str(idEntity), str(typeEntity), str(fichero)) 
        urlFromCompuesta = urls[0]
        if urlverify in urlFromCompuesta:    
            urlToCompuesta = urls[1]
        else :
            return jsonify({'message':urls})# retorna el error que retorna la funcion validateURL
        # "READ" --> Lee los documentos de la base de datos
        for data in collection.find({"user":user},{"email":1,"_id":0}):
            data = data #Obtener datos del usuario
        email = data.get("email")
 
        os.system("java -jar encryptJSON.jar")# Ejecucion del programa java
    
        with open('outencrypt.json','r') as file: # obtener datos de out.json en orden de entrada
            contenido = json.load(file, object_pairs_hook=OrderedDict)
        id_outJSON = contenido.get('id')# obtener id del diccionario
        # Inserción de out.json en oreon (Ajustar out.json a formato de entrada de datos oreon)
        fichero = "outencrypt.json"
        returninsertOrion = insertOrion(urlTo, fichero)
        if "orion" in returninsertOrion:
            return jsonify ({'message': returninsertOrion})
        keys = open('key.txt').read() # Obeniendo las keys del archivo
        # Send keys email
        asunto = ("Encrypted keys of the Orion, model ID: " + id_outJSON)
        message = ("TYPE: "+typeEntity+"\n"+"User: "+user+"\n"+"Query url Orion: "+urlToCompuesta+"\n"+"Keys:"+"\n"+keys)
        returnEmailMetod = sendEMAIL(email, asunto, message)
        #print = (returnEmailMetod)
        # Insertar Registro de actividades en mongo
        service = ('encrypt/ocb')
        registroMongo = [regMongo(user, service, urlFrom, id_outJSON, typeEntity, urlTo)]
        if 'error' in registroMongo:
            print (registroMongo) 
        print(returninsertOrion)
        return jsonify([{'message':'Encrypt successful'}, {'UrlTo': urlToCompuesta},{'message':'Keys were sent to'},{'email':email}])
    return jsonify({'messsage':'You must log in first.'})

# Encriptación de Orion a modelo local
@application.route('/encrypt/ocb/local', methods=["POST"])
def encryptLOCAL():   
    if "user" in session:
    	os.system("rm inencrypt.json && rm outencrypt.json && rm key.txt")
        user = session['user']# Obtener usuario
        try: #Excepción "parametros de entrada"
            urlFrom = request.form['urlFrom']
            idEntity = request.form['id']
            typeEntity = request.form['type']
        except:
            return jsonify({'message':'Enter urlFrom, id and type'})
        #Validar URLs
        fichero = 'inencrypt.json'
        urlFromCompuesta = validateURL1(str(urlFrom), str(idEntity), str(typeEntity), str(fichero)) 
        if urlverify in urlFromCompuesta:    
            urlFromCompuesta = urlFromCompuesta
        else:
            return jsonify({'message':urls})# retorna el error que retorna la funcion validateURL
        # "READ" --> Lee los documentos de la base de datos
        for data in collection.find({"user":user},{"email":1,"_id":0}):
            data = data #Obtener datos del usuario
        email = data.get("email")
 
        os.system("java -jar encryptJSON.jar")# Ejecucion del programa java
    
        with open('outencrypt.json','r') as file: # obtener datos de out.json en orden de entrada
            contenido = json.load(file, object_pairs_hook=OrderedDict)
        id_outJSON = contenido.get('id')# obtener id del diccionario
        # Inserción de out.json en oreon (Ajustar out.json a formato de entrada de datos oreon)
        #fichero = "outencrypt.json"
        #returninsertOrion = insertOrion(urlTo, fichero)
        #if "orion" in returninsertOrion:
        #    return jsonify ({'message': returninsertOrion})
        keys = open('key.txt').read() # Obeniendo las keys del archivo
        # Send keys email
        asunto = ("Encrypted keys of the Orion, model ID: " + id_outJSON)
        message = ("TYPE: "+typeEntity+"\n"+"User: "+user+"\n"+"Keys:"+"\n"+keys)
        returnEmailMetod = sendEMAIL(email, asunto, message)
        #print = (returnEmailMetod)
        # Insertar Registro de actividades en mongo
        #service = ('encrypt/ocb/local')
        #registroMongo = [regMongo(user, service, urlFrom, id_outJSON, typeEntity)]
        #if 'error' in registroMongo:
        #    print (registroMongo) 
        #print(returninsertOrion)
        return '{}'.format(json.dumps(contenido,indent=4))
    return jsonify({'messsage':'You must log in first.'})


application.secret_key = os.environ.get('S_ASDW_K','') 
if __name__== '__main__':
    application.run(debug = True, port = 8000) 

#-------------------------------------#
# pip install pymongo validate_email PyDNS
