# sd_project
Um simples projeto cliente-servidor para usar os conhecimentos sobre sistemas distribuídos

## Executando o projeto
- Clone o projeto
```bash
  git clone https://github.com/Adlizm/sd_project.git
  cd sd_project
```

### Preparando o ambiente

- Instale a dependencia python-etcd3
```bash
  pip3 install git+https://github.com/kragniz/python-etcd3.git
```

- Caso não possua o etcd instalado, siga as instruções de instalação em:
  https://etcd.io/docs/v3.6/install/
```bash
  etcd --version
```

- Em terminais diferentes execute (disponivel em etcd_commands):
```bash
  etcd --name replica1 --data-dir /temp/etcd/replica1 --listen-client-urls http://localhost:12379 --advertise-client-urls http://localhost:12379 --listen-peer-urls http://localhost:12380 --initial-advertise-peer-urls http://localhost:12380 --initial-cluster replica1=http://localhost:12380,replica2=http://localhost:22380,replica3=http://localhost:32380 --initial-cluster-token tkn --initial-cluster-state new
```
```bash
  etcd --name replica2 --data-dir /temp/etcd/replica2 --listen-client-urls http://localhost:22379 --advertise-client-urls http://localhost:22379 --listen-peer-urls http://localhost:22380 --initial-advertise-peer-urls http://localhost:22380 --initial-cluster replica1=http://localhost:12380,replica2=http://localhost:22380,replica3=http://localhost:32380 --initial-cluster-token tkn --initial-cluster-state new
```
```bash
  etcd --name replica3 --data-dir /temp/etcd/replica3 --listen-client-urls http://localhost:32379 --advertise-client-urls http://localhost:32379 --listen-peer-urls http://localhost:32380 --initial-advertise-peer-urls http://localhost:32380 --initial-cluster replica1=http://localhost:12380,replica2=http://localhost:22380,replica3=http://localhost:32380 --initial-cluster-token tkn --initial-cluster-state new
```

### Inicializando projeto

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

- [x] Testes Automatizados
- [x] Replica consistente dos dados
- [x] Portais com Cache Local
- [x] Suporte a múltiplos portais 

### Mecanismos de Comunicação
- Comunicação entre cliente e portal via sockets
- Comunicação entre admin e portal via sockets

