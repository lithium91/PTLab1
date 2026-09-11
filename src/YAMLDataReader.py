# -*- coding: utf-8 -*-
import yaml

from Types import DataType
from DataReader import DataReader


class YAMLDataReader(DataReader):
    """Чтение данных о студентах из файла формата YAML.

    Ожидаемый формат файла - список словарей вида:
    - Иванов Иван Иванович:
        математика: 67
        литература: 100
    """

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            content = yaml.safe_load(file)
        if content is None:
            return self.students
        if not isinstance(content, list):
            raise ValueError("YAML-файл должен содержать список студентов")
        for item in content:
            if not isinstance(item, dict):
                raise ValueError("Некорректная запись о студенте: "
                                 f"{item!r}")
            for name, subjects in item.items():
                self.students[str(name)] = [
                    (str(subject), int(score))
                    for subject, score in (subjects or {}).items()
                ]
        return self.students
