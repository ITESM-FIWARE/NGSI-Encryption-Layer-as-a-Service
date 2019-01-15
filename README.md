# NGSI-Encryption-Layer-as-a-Service

This document describes the encryption service developed at ITESM as a tool for encrypting and decrypting [FIWARE data models](https://www.fiware.org/developers/data-models/). 

[FIWARE](https://www.fiware.org/) is a curated framework of open source platform components to accelerate the development of Smart solutions. The [FIWARE platform](https://www.fiware.org/developers/catalogue/) provides a rather simple yet powerful set of APIs (Application Programming Interfaces) that ease the development of Smart Applications in multiple vertical sectors. 

The main and only mandatory component of any "Powered by FIWARE" platform or solution is the [FIWARE Orion Context Broker Generic Enabler](https://fiware-orion.readthedocs.io/en/master/), which brings a cornerstone function in any smart solution: the need to manage context information in a highly decentralized and large-scale manner, enabling to perform updates and bring access to context.

[FIWARE data models](https://www.fiware.org/developers/data-models/) have been harmonized to enable data portability for different applications including, but not limited, to Smart Cities. They are intended to be used together with [FIWARE NGSI version 2](https://www.fiware.org/2016/06/08/fiware-ngsi-version-2-release-candidate/).

The application can be seen as two stand-alone services, one that uses tokens as a security measure and the second one that uses sessions as a security measure. Both stand-alone services enable the encryption and decryption of all up-to-date available FIWARE data models published in [FIWARE Data Models official site](https://www.fiware.org/developers/data-models/). 
First, the overall overview of the encryption service is described; secondly, the stand-alone service that uses tokens is introduced; lastly, the stand-alone service that uses sessions is detailed.

## Installation and Configuration
### Configuration:
Para el correcto funcionamiento del servicio es necesario agregar una cuenta de gmail y su contraseña. La cuenta ingresada será la encargada de enviar en un mail con las llaves de todos los modelos encriptados por el servicio.

#### Ingresar cuenta de correo y contraseña: 
Una vez clonado el repositorio, ingresar en la carpeta del servicio a utilizar [session-based](https://github.com/ITESM-FIWARE/NGSI-Encryption-as-a-Service/tree/master/session-based) o [token-based](https://github.com/ITESM-FIWARE/NGSI-Encryption-as-a-Service/tree/master/token-based). Dentro de la carpeta ubicar el archivo Dockerfile, entrar y modificar las líneas 4 y 5.

<pre>
4 ENV ngsi_address_send email(ingresar correo)
5 ENV ngsi_encrypt_pass password_email(ingresar contraseña del correo)
</pre>

#### Configuración de Gmail:
Para que el correo electrónico ingresado anteriormente pueda enviar correos por una aplicación externa es necesario autorizar esta opción en la cuenta del correo ingresado.

ingrese a (https://www.google.com/settings/security/lesssecureapps) mientras está conectado a su cuenta de Google y activar la opcion "Allow less secure apps". 
![secure_apps](https://user-images.githubusercontent.com/38957081/51202845-49f61a00-18c5-11e9-88be-1ef960993ce7.png)

Despues de activar esta opción el servicio de encriptacion será capaz de enviar correos desde la dirección proporcionada de forma automatica.

## Prerequisites
The encryption service can be installed on any Operative System.

The following software must be previously installed in the server which will hold the encryption service.
1. [Docker](https://www.docker.com/get-started)
1. [Postman](https://www.getpostman.com/apps)/[Insomnia](https://insomnia.rest/download/)

Furthermore, the following ports containers are required.
1. ngsi_nodejs 8000 (only for stand-alone encryption service that uses tokens)
1. ngsi_python 2121 (only for stand-alone encryption service that uses sessions)

## Installation:
Refer to the [Installation Guide session-based](https://github.com/ITESM-FIWARE/NGSI-Encryption-Layer-as-a-Service#encryption-service-with-sessions).

Refer to the [Installation Guide token-based](https://github.com/ITESM-FIWARE/NGSI-Encryption-Layer-as-a-Service#encryption-service-with-tokens).

## Getting started

Refer to the [User Manual session-based](https://github.com/ITESM-FIWARE/NGSI-Encryption-Layer-as-a-Service#use-of-services-supported-by-the-encryption-service-1).

Refer to the [User Manual token-based](https://github.com/ITESM-FIWARE/NGSI-Encryption-Layer-as-a-Service#use-of-services-supported-by-the-encryption-service).

