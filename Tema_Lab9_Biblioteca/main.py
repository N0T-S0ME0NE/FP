from biblioteca.repository import BookRepository,ClientRepository,RentalRepository
from biblioteca.controller import Controller
from biblioteca.interfata import Console
from biblioteca.teste import run_all_tests

def main():
    run_all_tests()
    controller=Controller(BookRepository(),ClientRepository(),RentalRepository())
    console=Console(controller)
    console.run()
main()