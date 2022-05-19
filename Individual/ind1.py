#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import argparse
import json


def get_flight(fls, dest, num, type):
    """
    Добавить данные о работнике.
    """
    fls.append(
        {
            "flight_destination": dest,
            "flight_number": num,
            "airplane_type": type
        }
    )
    return fls


def display_flights(flights):
    """
     Отобразить список рейсов
    """
    if flights:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолета"
            )
        )
        print(line)
        for idx, flight in enumerate(flights, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:<15} |'.format(
                    idx,
                    flight.get('flight_destination', ''),
                    flight.get('flight_number', ''),
                    flight.get('airplane_type', 0)
                )
            )
        print(line)

    else:
        print("Список рейсов пуст")


def select_flights(flights, airplane_type):
    """
    Выбрать рейсы самолётов заданного типа
    """
    count = 0
    res = []
    for flight in flights:
        if flight.get('airplane_type') == airplane_type:
            count += 1
            res.append(flight)
    if count == 0:
        print("рейсы не найдены")

    return res


def save_flights(file_name, fls):
    """
    Сохранить все записи полётов в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(fls, fout, ensure_ascii=False, indent=4)


def load_flights(file_name):
    """
    Загрузить все записи полётов из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    """
    Главная функция программы
    """
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )
    parser = argparse.ArgumentParser("flights")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new flight"
    )
    add.add_argument(
        "-fld",
        "--flight_dest",
        action="store",
        required=True,
        help="The flight destination"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        help="The flight number"
    )
    add.add_argument(
        "-t",
        "--type",
        action="store",
        required=True,
        help="The airplane type"
    )
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all flights"
    )
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the flights"
    )
    select.add_argument(
        "-t",
        "--type",
        action="store",
        required=True,
        help="The required flight type"
    )
    args = parser.parse_args(command_line)
    destination = pathlib.Path.home() / args.filename
    is_dirty = False
    if destination.exists():
        flights = load_flights(destination)
    else:
        flights = []
    if args.command == "add":
        flights = get_flight(
            flights,
            args.flight_dest,
            args.number,
            args.type
        )
        is_dirty = True
    elif args.command == "display":
        display_flights(flights)
    elif args.command == "select":
        selected = select_flights(flights, args.type)
        display_flights(selected)
    if is_dirty:
        save_flights(destination, flights)


if __name__ == '__main__':
    main()
