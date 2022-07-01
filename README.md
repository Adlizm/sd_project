# sd_project
Um simples projeto cliente-servidor para usar os conhecimentos sobre sistemas distribuídos

## Executando o projeto
- Clone o projeto
```bash
  git clone https://github.com/Adlizm/sd_project.git
  cd sd_project
```

### Preparando o ambiente

- Instale a dependencia paho-mqtt
```bash
  pip3 install paho-mqtt
```

- Certifique que tenha um broker MQTT rodando localmente na porta 1883.
  
  Caso não possua, siga as instruções de instalação em:
  https://mosquitto.org/download/
```bash
  mosquitto -v
```

### Inicializando projeto

- Em diferentes terminais, inicialize os portais
```bash
  python ./src/admin.py
  python ./src/client_portal.py
```

- Em diferentes terminais, inicialize as interfaces
```bash
  python ./src/admin_cli.py
  python ./src/client_cli.py
```
## Rodando os testes

Para rodar os testes, rode o seguinte comando

```bash
  python ./test.py
```


## Funcionalidades

- [x] Interface do Client com o Portal
- [x] Interface do Administrador com o Portal
- [x] Portal do Administrador
- [x] Portal do Cliente
- [x] Testes

### Mecanismos de Comunicação
- Comunicação entre cliente e portal via sockets
- Comunicação entre admin e portal via sockets
- Comunicação entre portais via pubsub

