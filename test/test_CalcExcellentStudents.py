# -*- coding: utf-8 -*-
import pytest
from src.Types import DataType
from src.CalcExcellentStudents import CalcExcellentStudents


class TestCalcExcellentStudents:

    @pytest.fixture()
    def input_data(self) -> DataType:
        return {
            "Иванов Иван Иванович": [
                ("математика", 67), ("литература", 100),
                ("программирование", 91)
            ],
            "Сидорова Анна Сергеевна": [
                ("математика", 95), ("программирование", 100),
                ("физика", 92)
            ],
            "Кузнецов Олег Игоревич": [
                ("математика", 90), ("литература", 90), ("история", 94)
            ],
            "Петров Петр Петрович": [
                ("математика", 89), ("химия", 100)
            ]
        }

    def test_init(self, input_data: DataType) -> None:
        calc = CalcExcellentStudents(input_data)
        assert calc.data == input_data
        assert calc.threshold == 90

    def test_calc(self, input_data: DataType) -> None:
        assert CalcExcellentStudents(input_data).calc() == 2

    def test_get_excellent_students(self, input_data: DataType) -> None:
        assert CalcExcellentStudents(input_data).get_excellent_students() \
            == ["Сидорова Анна Сергеевна", "Кузнецов Олег Игоревич"]

    def test_boundary_score_90_is_excellent(self,
                                            input_data: DataType) -> None:
        assert CalcExcellentStudents(input_data).is_excellent(
            "Кузнецов Олег Игоревич")

    def test_score_89_is_not_excellent(self, input_data: DataType) -> None:
        assert not CalcExcellentStudents(input_data).is_excellent(
            "Петров Петр Петрович")

    def test_empty_data(self) -> None:
        assert CalcExcellentStudents({}).calc() == 0

    def test_student_without_subjects(self) -> None:
        assert CalcExcellentStudents({"Иванов И.И.": []}).calc() == 0

    def test_custom_threshold(self, input_data: DataType) -> None:
        assert CalcExcellentStudents(input_data, threshold=60).calc() == 4

    def test_unknown_student_raises(self, input_data: DataType) -> None:
        with pytest.raises(KeyError):
            CalcExcellentStudents(input_data).is_excellent("Нет Такого")
