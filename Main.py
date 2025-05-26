import mysql.connector
import time as t
import re



conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'escolaJo'
)

cursor = conexao.cursor()
print("Conexão bem-sucedida!")

def valida_matricula(matricula):
    padrao = r"^[A-Za-z]{3}[0-9]{3}$"
    return bool(re.match(padrao, matricula))

def mostrarMenu():
    print("==== GESTÃO DE ALUNOS ====")
    print("1 - Inserir Aluno")
    print("2 - Listar Aluno")
    print("3 - Editar Aluno")
    print("4 - Remover Alunos")
    print("5 - Sair")
    print("==========================")
    
escolha = 0

while escolha != 5:
    mostrarMenu()
    escolha = int(input("? - Sua escolha: "))

    match escolha:
        case 1:
            print("=== INSERIR ALUNO ===")
            matriculaAluno = input("- Matrícula do aluno (Ex: 'AAA000'): ")
            
            if valida_matricula(matriculaAluno) == False:
                print("\n-- FORMATO DA MATRÍCULA INVÁLIDO --")
            else:
                nomeAluno = input("- Nome do aluno: ")
                if not nomeAluno:
                    print("\n-- O NOME NÃO PODE ESTAR VAZIO --\n")
                else:
                    idadeAluno = int(input("- Idade do aluno: "))
                    
                    if idadeAluno < 6:
                        print("\n-- A IDADE DEVE SER MAIOR OU IGUAL A 6 --\n")
                    else:
                        cursoAluno = input("- Curso do aluno: ")
                        
                        if not cursoAluno:
                            print("\n-- O NOME DO CURSO NÃO PODE ESTAR VAZIO --\n")
                        else:
                            notaFinalAluno = float(input("- Nota final do aluno: "))
                            
                            if notaFinalAluno <0 or notaFinalAluno > 10:
                                print("\n-- A NOTA DEVE ESTAR ENTRE 0 e 10 --\n")
                            else:
                                comando = f'INSERT INTO alunos VALUES ("{matriculaAluno}", "{nomeAluno}", {idadeAluno}, "{cursoAluno}", {notaFinalAluno})'
                                cursor.execute(comando)
                                conexao.commit()
                                resultado = cursor.fetchall()
                                print("\n-- ALUNO CADASTRADO COM SUCESSO --\n")
        case 2:
            print("\n=== LISTAR ALUNOS ===")
            print("1 - Listar todos\n2 - Buscar por nome\n3 - Buscar por matrícula")
            escolhaBusca = int(input("? - Sua escolha: "))
            
            match escolhaBusca:
                case 1: 
                    print("\n==== LISTAR TODOS ALUNOS ====\n")
                    comando = 'SELECT *  FROM alunos'
                    cursor.execute(comando)
                    resultado = cursor.fetchall()
                    for linha in resultado:
                        print(f"===============================\n[{linha[0]}] {linha[1]} (idade: {linha[2]})")
                        print(f"{linha[3]} | Nota final: {linha[4]}")
                    print("===============================\n")
                    
                case 2:
                    print("\n==== BUSCAR POR NOME ====")
                    nomeAluno = input("- Nome do aluno pra pesquisar: ")
                    
                    comando = f'SELECT * FROM alunos where nome_aluno = "{nomeAluno}"'
                    cursor.execute(comando)
                    resultado1 = cursor.fetchall()
                        
                    if not resultado1:
                        print("\n-- Aluno não encontrado no BD --\n")
                    else:
                        comando = f'SELECT *  FROM alunos where nome_aluno = "{nomeAluno}"'
                        cursor.execute(comando)
                        resultado = cursor.fetchall()
                        for linha in resultado:
                            print(f"===============================\n[{linha[0]}] {linha[1]} (idade: {linha[2]})")
                            print(f"{linha[3]} | Nota final: {linha[4]}")
                        print("===============================\n")
                        
                case 3:
                    print("\n==== BUSCAR POR MATRÍCULA ====")
                    matriculaAluno = input("- Matrícula do aluno pra pesquisar: ")
                    
                    comando = f'SELECT * FROM alunos where matrícula_aluno = "{matriculaAluno}"'
                    cursor.execute(comando)
                    resultado1 = cursor.fetchall()
                        
                    if not resultado1:
                        print("\n-- Aluno não encontrado no BD --\n")
                    else:
                        comando = f'SELECT *  FROM alunos where matrícula_aluno = "{matriculaAluno}"'
                        cursor.execute(comando)
                        resultado = cursor.fetchall()
                        print("")
                        for linha in resultado:
                            print(f"===============================\n[{linha[0]}] {linha[1]} (idade: {linha[2]})")
                            print(f"{linha[3]} | Nota final: {linha[4]}")
                        print("===============================\n")
                    
                case _:
                    print("\n=== ESCOLHA INVÁLIDA ===\n")
        case 3:
            print("=== EDITAR ALUNO ===")
            matriculaAluno = input("- Matrícula do aluno pra pesquisar: ")
                    
            comando = f'SELECT * FROM alunos where matrícula_aluno = "{matriculaAluno}"'
            cursor.execute(comando)
            resultado1 = cursor.fetchall()
                        
            if not resultado1:
                print("\n-- Aluno não encontrado no BD --\n")
            else:
                escolhaEdit = int(input("Editar (1 - Curso | 2 - Nota Final): "))
                
                if escolhaEdit == 1:
                    curso_novo = input("- Novo curso do aluno: ")
                    
                    comando = f'UPDATE alunos SET curso_aluno = "{curso_novo}" WHERE matrícula_aluno = "{matriculaAluno}"'
                    cursor.execute(comando)
                    conexao.commit()
                    print("\n-- Curso do aluno atualizado com sucesso --\n")
                    
                elif escolhaEdit == 2:
                    nota_nova = float(input("- Novo nota final do aluno: "))
                    
                    comando = f'UPDATE alunos SET nota_final = {nota_nova} WHERE matrícula_aluno = "{matriculaAluno}"'
                    cursor.execute(comando)
                    conexao.commit()
                    print("\n-- Nota final do aluno atualizada com sucesso --\n")
                else:
                    print("\n-- Escolha inválida --\n")
                                
        case 4:
            print("=== REMOVER ALUNO ===")
            matriculaAluno = input("Insira a matrícula do aluno que deseja excluir: ")
                
            comando1 = f'SELECT * FROM alunos where matrícula_aluno = "{matriculaAluno}"'
            cursor.execute(comando1)
            resultado1 = cursor.fetchall()
                
            if not resultado1:
                print("\n-- Aluno não encontrado no BD --\n")
            else:
                comando = f'DELETE FROM alunos WHERE matrícula_aluno = "{matriculaAluno}"'
                cursor.execute(comando)
                conexao.commit()
                print("\n-- Aluno excluído com sucesso --\n")
                
        case 5:
            print("\n=== SAINDO DO PROGRAMA ===\n")
            
        case _:
            print("\n=== ESCOLHA INVÁLIDA ===\n")