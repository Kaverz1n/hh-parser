from utils import *


def main():
    employers_id_list = ['9340246', '2180']
    database = choose_bd(employers_id_list)

    menu(database)


if __name__ == '__main__':
    main()
