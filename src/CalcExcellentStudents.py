# -*- coding: utf-8 -*-
from Types import DataType


class CalcExcellentStudents:
    """Расчет количества студентов-отличников.

    Отличником считается студент, у которого баллы по всем
    предметам не меньше порогового значения (по умолчанию 90).
    Студенты без оценок отличниками не считаются.
    """

    EXCELLENT_THRESHOLD: int = 90

    def __init__(self, data: DataType,
                 threshold: int = EXCELLENT_THRESHOLD) -> None:
        self.data: DataType = data
        self.threshold: int = threshold

    def is_excellent(self, name: str) -> bool:
        subjects = self.data[name]
        return len(subjects) > 0 and \
            all(score >= self.threshold for _, score in subjects)

    def get_excellent_students(self) -> list[str]:
        return [name for name in self.data if self.is_excellent(name)]

    def calc(self) -> int:
        return len(self.get_excellent_students())
