from biblioteca.repository import BookRepository,ClientRepository
from biblioteca.controller import Controller
from biblioteca.interfata import Console
from biblioteca.teste import run_all_tests

def main():
    run_all_tests()
    controller=Controller(BookRepository(),ClientRepository())
    console=Console(controller)
    console.run()
main()