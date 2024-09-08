# Jogoteca
Jogoteca é uma aplicação web simples desenvolvida em Flask para gerenciar um banco de dados de jogos.  
Com ela, você pode listar, adicionar, editar e excluir jogos, utilizando templates HTML e integração com um banco de dados MySQL.

## Funcionalidades
* Adicionar novos jogos ao banco de dados
* Editar jogos existentes
* Excluir jogos da lista
* Upload de imagens associadas aos jogos
* Validação de formulários com Flask-WTF
* Login e cadastro de usuários
* Hashing de senhas de usuários com Flask-Bcrypt

## Tecnologias utilizadas
* Flask - Framework web
* Flask-WTF - Extensão Flask para formulários
* Flask-Bcrypt - Extensão Flask para hashing
* Bootstrap - Framework CSS para estilização
* MySQL - Banco de dados relacional

## Pré-requisitos
* Python
* MySQL (ou outro banco de dados relacional)

## Configuração do Ambiente
### 1. Clonar o Repositório
```
git clone https://github.com/tiagomdsr/Jogoteca.git
cd Jogoteca
```

### 2. Criar e ativar o ambiente virtual
```
python -m venv venv
venv\Scripts\activate.bat  # Se estiver usando windows
```

### 3. Instalar as dependências
```
pip install -r requirements.txt
```

## 4. Configuração do Banco de Dados
Crie o banco de dados MySQL usando o script a seguir:  
(Código fornecido pelo curso de Flask da Alura.)
```
import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='seu_usuario',
            password='sua_senha'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

# criando tabelas
TABLES = {}
TABLES['Jogos'] = ('''
      CREATE TABLE `jogos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Nome do Usuario 1", "nickname 1", generate_password_hash("senha 1").decode("utf-8")),
      ("Nome do Usuario 2", "nickname 2", generate_password_hash("senha 2").decode("utf-8")),
      ("Nome do Usuario 3", "nickname 3", generate_password_hash("senha 3").decode("utf-8"))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from jogoteca.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Luta', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from jogoteca.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando
conn.commit()

cursor.close()
conn.close()
```

## 5. Configurar as variáveis de ambiente
Crie um arquivo `config.py` para armazenar suas credenciais:

```
import os

SECRET_KEY = Sua_key

SQLALCHEMY_DATABASE_URI = \
    "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
        SGBD = "mysql+mysqlconnector",
        usuario = seu_usuario,
        senha = sua_senha,
        servidor = "localhost",
        database = "jogoteca"
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"
```

## 6. Rodar a aplicação

`python jogoteca.py`

Agora, a aplicação estará disponível em http://127.0.0.1:5000/.

## 7. Funcionalidades futuras

* Adicionar uma página de cadastro. ✔
* Exibir capa dos jogos na tela inicial.