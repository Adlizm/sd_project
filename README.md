
# sd_project
Um simples projeto cliente-servidor para usar os conhecimentos sobre sistemas distribuídos

  

## Executando o projeto

- Clone o projeto

```bash
git clone https://github.com/Adlizm/sd_project.git
cd sd_project
```

### Preparando o ambiente

- Instale a dependencia pysyncobj

```bash
pip3 install pysyncobj
```

- Instale a dependencia plyvel, caso esteja em sistemas Linux/Ubuntu, basta que execute:
```bash
pip3 install plyvel
```

- Caso contrário, você deverá ter instalado previamente o LevelDB, siga as instruções em: https://github.com/google/leveldb

  

### Iniciando Replicas

- Em terminais diferentes execute:

```bash
python ./src/start_replica.py repl1
```
```bash
python ./src/start_replica.py repl2
```
```bash
python ./src/start_replica.py repl3
```

  

## Inicializando projeto

- Em diferentes terminais, inicialize os portais

```bash
python ./src/admin_portal.py
python ./src/client_portal.py
```

- Em diferentes terminais, inicialize as interfaces

```bash
python ./src/admin_cli.py
python ./src/client_cli.py
```

## Executando os testes

Para rodar os testes, rode o seguinte comando
```bash
python ./test.py
```

## Funcionalidades
- [x] Interface do Client com o Portal
- [x] Interface do Administrador com o Portal
- [x] Portal do Administrador
- [x] Portal do Cliente

- [x] Testes Automatizados
- [x] Replica consistente dos dados
- [x] Portais com Cache Local (30 segundos de tempo de vida)
- [x] Suporte a múltiplos portais

  
### Mecanismos de Comunicação
- Comunicação entre cliente e portal via sockets
- Comunicação entre admin e portal via sockets
- Comunicação entre portais e replicas via sockets