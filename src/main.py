from utils import *


def main():
    employers_id_list = [
        '2180', '1455', '87021', '3529', '1942330', '2624085',
        '3093544', '1122462', '3112647', '10079206'
    ]
    database = choose_bd(employers_id_list)

    menu(database)


if __name__ == '__main__':
    main()
