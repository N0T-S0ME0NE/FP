from cheltuieli_familie.interfata import print_menu,run_command
from cheltuieli_familie.teste import run_all_tests

def main():
    expenses=[]
    finished=False
    while not finished:
        print_menu()
        try:
            command=input("Comandă: ").strip()
            if command=="0":
                finished=True
            else:
                run_command(command,expenses)
        except ValueError as error:
            print("Eroare: " + str(error))
        except EOFError:
            finished=True
    print("Programul se va închide...")
main()