import subprocess
import json
from termcolor import colored
from app import database

# LIMPAR OS COMANDOS APÓS A EXECUÇÃO DE OUTRO
def clear_terminal():
    subprocess.call('cls', shell=True)

#CORPO PRINCIPAL DO MENU
import subprocess
import json
from termcolor import colored
from app import database

# LIMPAR OS COMANDOS APÓS A EXECUÇÃO DE OUTRO
def clear_terminal():
    subprocess.call('cls', shell=True)

#CORPO PRINCIPAL DO MENU
def show_menu():
    while True:
        print("\nEscolha uma opção:")
        print("1. Visualizar todos os itens no estoque")
        print("2. Visualizar detalhes de um item")
        print("3. Adicionar um novo item ao estoque")
        print("4. Visualizar todos os usuários")
        print("5. Visualizar detalhes de um usuário")
        print("6. Adicionar um novo usuário")
        print("7. Deletar um item do estoque")
        print("8. Deletar um usuário")
        print("9. Fazer um pedido de compra")
        print("10. Sair")

        choice = input("Digite o número da opção desejada: ")

        if choice == "1":
            clear_terminal()
            view_all_items()
        elif choice == "2":
            clear_terminal()
            view_item_details()
        elif choice == "3":
            clear_terminal()
            add_new_item()
        elif choice == "4":
            clear_terminal()
            view_all_users()
        elif choice == "5":
            clear_terminal()
            view_user_details()
        elif choice == "6":
            clear_terminal()
            add_new_user()
        elif choice == "7":
            clear_terminal()
            delete_item()
        elif choice == "8":
            clear_terminal()
            delete_user()
        elif choice == "9":
            clear_terminal()
            make_purchase()
        elif choice == "10":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

#VER TODOS OS ITENS DO ESTOQUE
def view_all_items():
    response = subprocess.check_output('http GET http://localhost:8000/estoque/', shell=True)
    display_response(response)

#VER ITEM POR ID
def view_item_details():
    item_id = input("\nDigite o ID do item para ver detalhes: ")
    response = subprocess.check_output(f'http GET http://localhost:8000/estoque/{item_id}', shell=True)
    display_response(response)

#ADICIONAR NOVO ITEM
def add_new_item():
    nome = input("\nDigite o nome do novo item: ")
    descricao = input("Digite a descrição: ")
    estoque = int(input("Digite a quantidade em estoque: "))
    preco = float(input("Digite o preço: "))

    response = subprocess.check_output(f'http POST http://localhost:8000/estoque/adicionar/ nome="{nome}" descricao="{descricao}" estoque:={estoque} preco:={preco}', shell=True)
    display_response(response)

#VER TODOS OS USUÁRIOS
def view_all_users():
    response = subprocess.check_output('http GET http://localhost:8000/usuarios/', shell=True)
    display_response(response)

#VER USUÁRIO POR ID
def view_user_details():
    user_id = input("\nDigite o ID do usuário para ver detalhes: ")
    response = subprocess.check_output(f'http GET http://localhost:8000/usuarios/{user_id}', shell=True)
    display_response(response)

#ADICIONAR NOVO USUÁRIO
def add_new_user():
    nome = input("\nDigite o nome do novo usuário: ")
    email = input("Digite o email: ")
    senha = input("Digite a senha: ")
    is_admin = input("O usuário é administrador? (True/False): ")

    response = subprocess.check_output(f'http POST http://localhost:8000/usuarios/adicionar/ nome="{nome}" email="{email}" senha="{senha}" is_admin={is_admin}', shell=True)
    display_response(response)

#FAZER O PEDIDO DE COMPRA
def make_purchase():
    user_id = int(input("\nDigite o ID do usuário: "))
    item_id = int(input("Digite o ID do item para compra: "))
    quantidade = int(input("Digite a quantidade desejada: "))

    response = subprocess.check_output(f'http POST http://localhost:8000/pedido/adicionar/{user_id} item_id={item_id} quantidade={quantidade}', shell=True)
    display_response(response)

    # Exibir o valor total de compra e a quantidade
    data = json.loads(response)
    if 'preco' in data and 'quantidade' in data:
        valor_total = data['preco'] * data['quantidade']
        print(f"Valor total da compra: R${valor_total}")
        print(f"Quantidade comprada: {data['quantidade']}")

# DELETAR UM ITEM DO ESTOQUE
def delete_item():
    item_id = input("\nDigite o ID do item que deseja deletar: ")
    response = subprocess.check_output(f'http DELETE http://localhost:8000/estoque/remove/{item_id}', shell=True)
    print("Item deletado com sucesso.")

# DELETAR UM USUÁRIO
def delete_user():
    user_id = input("\nDigite o ID do usuário que deseja deletar: ")
    response = subprocess.check_output(f'http DELETE http://localhost:8000/usuarios/remover/{user_id}', shell=True)
    print("Usuário deletado com sucesso.")

#RESPONSAVEL PELA FORMATAÇÃO DOS REPOSTAS JSON #
def display_response(response):
    data = json.loads(response)
    
    if isinstance(data, list):
        for item in data:
            print("=" * 25)
            for key, value in item.items():
                formatted_value = colored(value, 'yellow') if key == 'preco' else colored(value, 'green')
                print(f"{key.capitalize()}: {formatted_value}")
    else:
        print("=" * 25)
        for key, value in data.items():
            formatted_value = colored(value, 'yellow') if key == 'preco' else colored(value, 'green')
            print(f"{key.capitalize()}: {formatted_value}")
    print("=" * 25)

if __name__ == "__main__":
    show_menu()
