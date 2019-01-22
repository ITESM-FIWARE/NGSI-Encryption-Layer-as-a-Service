# NGSI-Encryption-Layer-as-a-Service

This document describes the encryption service developed at ITESM as a tool for encrypting and decrypting [FIWARE data models](https://www.fiware.org/developers/data-models/). 

[FIWARE](https://www.fiware.org/) is a curated framework of open source platform components to accelerate the development of Smart solutions. The [FIWARE platform](https://www.fiware.org/developers/catalogue/) provides a rather simple yet powerful set of APIs (Application Programming Interfaces) that ease the development of Smart Applications in multiple vertical sectors. 

The main and only mandatory component of any "Powered by FIWARE" platform or solution is the [FIWARE Orion Context Broker Generic Enabler](https://fiware-orion.readthedocs.io/en/master/), which brings a cornerstone function in any smart solution: the need to manage context information in a highly decentralized and large-scale manner, enabling to perform updates and bring access to context.

[FIWARE data models](https://www.fiware.org/developers/data-models/) have been harmonized to enable data portability for different applications including, but not limited, to Smart Cities. They are intended to be used together with [FIWARE NGSI version 2](https://www.fiware.org/2016/06/08/fiware-ngsi-version-2-release-candidate/).

The application can be seen as two stand-alone services, one that uses tokens as a security measure and the second one that uses sessions as a security measure. Both stand-alone services enable the encryption and decryption of all up-to-date available FIWARE data models published in [FIWARE Data Models official site](https://www.fiware.org/developers/data-models/).

## Prerequisites
The encryption service can be installed on any Operative System.

The following software must be previously installed in the server which will hold the encryption service.
1. [Docker](https://www.docker.com/get-started)
1. [Postman](https://www.getpostman.com/apps)/[Insomnia](https://insomnia.rest/download/)

Furthermore, the following ports containers are required.
1. ngsi_nodejs 8000 (only for the token-based service)
1. ngsi_python 2121 (only for the session-based service)

The service requires an active Gmail account. The use of other email accounts will cause the malfunction of the service. In order to allow sending and receiving emails from an external application, it is necessary to enable this option in the selected Gmail account. To configure the Gmail account, please:

1. Go to the Gmail account configuration via (https://www.google.com/settings/security/lesssecureapps)
1. Enable the option "Allow less secure apps"
![secure_apps](https://user-images.githubusercontent.com/38957081/51202845-49f61a00-18c5-11e9-88be-1ef960993ce7.png)


## Installation and Configuration
First, download or clone the repository to a local directory. Inside each fold of the two implemented services, [session-based](https://github.com/ITESM-FIWARE/data-encryption/tree/master/session-based) and [token-based](https://github.com/ITESM-FIWARE/data-encryption/tree/master/token-based), resides a Dockerfile. Open the Dockerfile with a text editor and modify the fourth and fifth lines with your email and the corresponding password, respectively.

<pre>
4 ENV ngsi_address_send email
5 ENV ngsi_encrypt_pass password_email
</pre>

For a complete guide, please refer to:
1. [Installation Guide of the Session-based service](https://github.com/ITESM-FIWARE/data-encryption#session-based-service).
1. [Installation Guide of the Token-based service](https://github.com/ITESM-FIWARE/data-encryption#token-based-service).

## Getting started
Refer to the [User Manual of the Session-based service](https://github.com/ITESM-FIWARE/data-encryption#session-based-service).

Refer to the [User Manual of the Token-based service](https://github.com/ITESM-FIWARE/data-encryption#sign-up).

