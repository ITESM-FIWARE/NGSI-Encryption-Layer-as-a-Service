import os
import commands

def encrypt(urlin, urlout):
	os.system("chmod +x RSA_JSON.jar")
	os.system("wget -O in.json "+urlin)
	'''os.system("java -jar RSA_JSON.jar")
				contenido=file("out.json").read().splitlines()
				contenido.insert(0,"curl "+urlout+" -s -S -H 'Content-Type: application/json' -d @- <<EOF")
				f = open('out.json', 'w')
				f.writelines("\n".join(contenido))
				f.write("\n"+"EOF")
				f.close()
				a = commands.getoutput("cat out.json")
				os.system(a)'''