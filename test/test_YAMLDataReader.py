# -*- coding: utf-8 -*-
import pytest
from src.Types import DataType
from src.YAMLDataReader import YAMLDataReader


class TestYAMLDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:
        text = "- Иванов Иван Иванович:\n" + \
               "    математика: 67\n" + \
               "    литература: 100\n" + \
               "    программирование: 91\n" + \
               "- Петров Петр Петрович:\n" + \
               "    математика: 78\n" + \
               "    химия: 87\n" + \
               "    социология: 61\n"
        data = {
            "Иванов Иван Иванович": [
                ("математика", 67), ("литература", 100),
                ("программирование", 91)
            ],
            "Петров Петр Петрович": [
                ("математика", 78), ("химия", 87), ("социология", 61)
            ]
        }
        return text, data

    @pytest.fixture()
    def filepath_and_data(self,
                          file_and_data_content: tuple[str, DataType],
                          tmpdir) -> tuple[str, DataType]:
        p = tmpdir.mkdir("datadir").join("my_data.yaml")
        p.write_text(file_and_data_content[0], encoding='utf-8')
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data: tuple[str, DataType]) -> None:
        file_content = YAMLDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]

    def test_read_keeps_subject_order(
            self, filepath_and_data: tuple[str, DataType]) -> None:
        file_content = YAMLDataReader().read(filepath_and_data[0])
        subjects = [s for s, _ in file_content["Иванов Иван Иванович"]]
        assert subjects == ["математика", "литература", "программирование"]

    def test_scores_are_int(
            self, filepath_and_data: tuple[str, DataType]) -> None:
        file_content = YAMLDataReader().read(filepath_and_data[0])
        for subjects in file_content.values():
            for _, score in subjects:
                assert isinstance(score, int)

    def test_read_empty_file(self, tmpdir) -> None:
        p = tmpdir.join("empty.yaml")
        p.write_text("", encoding='utf-8')
        assert YAMLDataReader().read(str(p)) == {}

    def test_student_without_subjects(self, tmpdir) -> None:
        p = tmpdir.join("no_subjects.yaml")
        p.write_text("- Иванов Иван Иванович:\n", encoding='utf-8')
        assert YAMLDataReader().read(str(p)) == {"Иванов Иван Иванович": []}

    def test_read_not_list_raises(self, tmpdir) -> None:
        p = tmpdir.join("bad.yaml")
        p.write_text("Иванов Иван Иванович:\n    математика: 67\n",
                     encoding='utf-8')
        with pytest.raises(ValueError):
            YAMLDataReader().read(str(p))

    def test_read_bad_item_raises(self, tmpdir) -> None:
        p = tmpdir.join("bad_item.yaml")
        p.write_text("- просто строка\n", encoding='utf-8')
        with pytest.raises(ValueError):
            YAMLDataReader().read(str(p))

    def test_read_missing_file_raises(self, tmpdir) -> None:
        with pytest.raises(FileNotFoundError):
            YAMLDataReader().read(str(tmpdir.join("nofile.yaml")))
