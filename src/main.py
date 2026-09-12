# -*- coding: utf-8 -*-
import argparse
import os
import sys

from CalcExcellentStudents import CalcExcellentStudents
from CalcRating import CalcRating
from DataReader import DataReader
from TextDataReader import TextDataReader
from YAMLDataReader import YAMLDataReader


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def get_reader(path: str) -> DataReader:
    extension = os.path.splitext(path)[1].lower()
    if extension in (".yaml", ".yml"):
        return YAMLDataReader()
    return TextDataReader()


def main():
    path = get_path_from_arguments(sys.argv[1:])

    reader = get_reader(path)
    students = reader.read(path)
    print("Students: ", students)

    rating = CalcRating(students).calc()
    print("Rating: ", rating)

    excellent = CalcExcellentStudents(students)
    print("Excellent students: ", excellent.get_excellent_students())
    print("Number of excellent students: ", excellent.calc())


if __name__ == "__main__":
    main()
