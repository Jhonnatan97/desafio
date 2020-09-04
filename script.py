from botocore.exceptions import NoCredentialsError
from requests import get
from time import sleep
from datetime import datetime
import hashlib
import boto3

ACCESS_KEY = os.getenv('AWS_ACESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET = 'scripts-pyhton-admin'

def sha1(string):
	'''Retorna hash SHA1 do arquivo'''
	sha1 = hashlib.sha1()
	sha1.update(string.encode('utf-8'))
	return sha1.hexdigest()

def upload_bucket(arquivo, bucket, arquivo_s3):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(arquivo, bucket, arquivo_s3)
        print("Upload com sucesso")
        return True
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return False
    except NoCredentialsError:
        print("As credenciais não estão definidas")
        return False

while True:
	r = get('https://www.dan.me.uk/torlist/')
	print(r.text)
	print(sha1(r.text))
	if (sha1(r.text) == "f10722fd05f306402ddfa61bfbf60a4365d16a81"):
		print("Nova tentativa... ")
		sleep(10)
	else:
		data_atual = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
		nome_arquivo = 'Lista_ips_' + data_atual + '.txt'
		arquivo = open(nome_arquivo, 'w')
		arquivo.writelines(r.text)
		arquivo.close()
		upload_bucket(nome_arquivo, AWS_BUCKET, nome_arquivo)
		sleep(1810)




