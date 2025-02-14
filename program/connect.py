import sqlite3

# Conecte-se a um banco de dados (ou crie um, se ele não existir)
conn = sqlite3.connect('financas.db')

# Crie um cursor para executar comandos SQL
cursor = conn.cursor()

# Crie uma tabela (neste exemplo, uma tabela chamada 'usuarios')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS financas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomeDoGasto NOT NULL,
        valor FLOAT,
        data TEXT
    )
''')

# Confirme a criação da tabela
conn.commit()
# Consulte e exiba os dados da tabela
cursor.execute('SELECT * FROM financas')

# Feche a conexão
conn.close()
