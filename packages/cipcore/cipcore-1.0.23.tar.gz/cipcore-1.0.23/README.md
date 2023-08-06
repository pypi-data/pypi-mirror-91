# CIP CORE

Pacotes helpers para os projetos do CIP

## API Mailer

Classe para facilitar o envio de emails

### Como utilizar?

A classe EmailApi é a classe que encapsula a operação do script. Para utilizá-la, instancia-se a classe passando os parâmetros:
- *base_url* - URL para o serviço de email;
- *logger* - objeto que gerencia a criação dos logs;

Ex:
```
url = 'http://api.teste.com'
log = app.log
email = EmailApi(base_url=url, logger=logger)
email.send()
```

A classe possui um method healtcheck para testar o funcionamento da API de emails
```
email.healthcheck()
```

## API ef delivery publish request

### Como utilizar?

A classe DeliveryEfPublishRequestApi é a classe que encapsula a operação do script. Para utilizá-la, instancia-se a classe passando os parâmetros:
- *base_url* - URL para o serviço de email;
- *logger* - objeto que gerencia a criação dos logs;

Ex:
```
url = 'http://api.teste.com'
log = app.log
ef_delivery_api = DeliveryEfPublishRequestApi(base_url=url, logger=logger)
ef_delivery_api.send()
```

A classe possui um method healtcheck para testar o funcionamento da API
```
ef_delivery_api.healthcheck()
```

## API FTP Service

### Como utilizar?

A classe FTPService é a classe que encapsula a operação do script. Para utilizá-la, instancia-se a classe passando os parâmetros:
- *base_url* - URL para o serviço de email;
- *sftp_uri* - sftp_uri
- *logger* - objeto que gerencia a criação dos logs;


A classe possui um method healtcheck para testar o funcionamento da API


## File Copy Service

### Como utilizar?

A classe FileCopyApi é a classe que encapsula a operação do serviço de cópia de arquivos. Para utilizá-la, instancia-se a classe passando os parâmetros:
- *base_url* - URL para o serviço de email;
- *logger* - objeto que gerencia a criação dos logs;

Ex:
```
url = 'http://api.teste.com'
log = app.log
file_copy = FileCopyApi(base_url=url, logger=logger)
file_copy.copy_file()
```

A classe possui um method healtcheck para testar o funcionamento da API
```
file_copy.healthcheck()
```


## API FTP Service

### Como utilizar?

A classe FTPService é a classe que encapsula a operação do script. Para utilizá-la, instancia-se a classe passando os parâmetros:
- *base_url* - URL para o serviço de email;
- *sftp_uri* - sftp_uri
- *logger* - objeto que gerencia a criação dos logs;
- *callback_url* - endereço para retornar a resposta da tarefa

```
json_example = {
    "id": "123456789",
    "ladder": "AQ",
    "files": [{
        "type": "video",
        "checksum": "4bac27393bdd9777ce02453256c5577cd02275510b2227f473d03f533924f877",
        "path": "/mnt/elemental/elemental/celula_file_to_vod/output/ingest_teste_AP_90p_103k_x264.mp4",
        "height": 90,
        "bitrate": 103000,
        "codec": "AVC",
        "step": "delivery-new"
    },
        {
            "type": "video",
            "checksum": "4bac27393bdd9777ce02453256c5577cd02275510b2227f473d03f533924f877",
            "path": "/mnt/elemental/elemental/celula_file_to_vod/output/ingest_teste_AP_480p_1221k_x264.mp4",
            "height": 480,
            "bitrate": 1221000,
            "codec": "AVC",

            "step": "delivery-new"
        }
    ]}

url = 'http://api.teste.com'
log = app.log
sftp_uri = sftp://ingest:ingest@sftp.dev.gugu.com:22
callback_url = "http://mamintegrationservice.dev.glb-cip.ninja/api/tasks-response"
ftp_service = FTPService(base_url=url, logger=logger, sftp_uri=sftp_uri)
ftp_service.send_file(json_example)
```

A classe possui um method healtcheck para testar o funcionamento da API
```
ftp_service.healthcheck()
```

## Token Api

### Como utilizar?

A classe FTPService é a classe que encapsula a operação do script. Para utilizá-la, instancia-se a classe passando os parâmetros:
- *client_id* - string que identifica quem é o cliente
- *secret* - string do segredo que o cliente possui
- *logger* - objeto que gerencia a criação dos logs;

```
log = app.log
client_id = "SFYrQmHbBkUXXry/3pq6GA=="
secret = "9yHBM/6gcDJ8VXlYI6i4zA=="
token = TokenApi(logger=logger, client_id=client_id, secret=secret)
ftp_service.request_token()
```
O retorno da classe é o access_token, uma string "U0ZZclFtSGJCa1VYWHJ5LzNwcTZHQT09Ojl5SEJNLzZnY0RKOFZYbFlJNmk0ekE9PQ=="

## Redis Checker

### Como utilizar?

A classe RedisChecker possui 4 métodos:

```
check_key(key_name, key_time)
```
Verifica se a chave existe de acordo com o nome e o tempo informados, retorno é True ou False.


```
get_config()
```
Retorna uma string com o resultado para a consulta da chave configurada.


```
set_config(valor)
```
Inclui um valor para chave configurada


Exemplo de utilização da classe:
```
redisObj = RedisChecker(logger, servico_teste, http://localhost, 1234).check_key(chave_teste, 1000)
//True
```


A classe possui um method healthcheck para testar o funcionamento da API
```
redis_checker.healthcheck()
```


## Requester

### Como utilizar?

A classe `CipSession` estende o objeto `requests.Session` adicionando funcionalidades como retry, log e timeout. Para utilizá-la, instancia-se a classe passando os parâmetros opcionais:
- *retries* - número de retentativas de requisição
- *timeout* - tempo de espera de resposta
- *logger* - objeto que gerencia a criação dos logs;

```
cip_requests = CipSession(retries=3, timeout=30, logger=app.log)
cip_requests.get('http://httpstat.us/200')
<Response [200]>
```


## Release History
* 1.0.0
  * Initial structure of the error classes.
* 1.0.1
  * Add Delivery Ef request publish.
  * Add FTP service.
* 1.0.2
  * Add email service integration
* 1.0.3
  * Fix email service
* 1.0.4
  * Fix file copy service endpoint
* 1.0.5
  * Add file move function to FileCopyAPI
* 1.0.6
  * Fix ftp service endpoint
* 1.0.7
  * Add callback url parameter to FTP service class
* 1.0.8
  * Ftp send file service receives generic dictionary
* 1.0.9
  * Remove id from json body to FTP service log
* 1.0.10
  * Add client credentials token api class
* 1.0.11
  * Add class RedisChecker
* 1.0.18
  * Add class for consuming email-service api v2
* 1.0.20
  * Add requester module
* 1.0.21
  * `CipSession` requester into mailer and file_copy modules
* 1.0.22
  * `CipError` update CipError reference to 1.0.52
