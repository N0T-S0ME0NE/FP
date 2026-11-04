from cheltuieli_familie.interfata import print_menu,run_command
from cheltuieli_familie.teste import run_all_tests

def main():
    run_all_tests()
    expenses=[]
    history=[]
    finished=0
    while not finished:
        print_menu()
        try:
            command=input("Comandă: ").strip()
            if command=="0":
                finished=1
            else:
                run_command(command,expenses,history)
        except ValueError as error:
            print("Eroare: " + str(error))
        except EOFError:
            finished=1
    print("Programul se va închide...")
main()