# -*- coding: utf-8 -*-
from src.main import get_path_from_arguments, get_reader
from src.TextDataReader import TextDataReader
from src.YAMLDataReader import YAMLDataReader
import pytest


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(
        correct_arguments_string: tuple[list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(
        noncorrect_arguments_string: list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string[0])
    assert e.type == SystemExit


@pytest.mark.parametrize("path", ["data.yaml", "data.yml", "DATA.YAML"])
def test_get_reader_yaml(path: str) -> None:
    assert type(get_reader(path)).__name__ == YAMLDataReader.__name__


@pytest.mark.parametrize("path", ["data.txt", "data"])
def test_get_reader_text(path: str) -> None:
    assert type(get_reader(path)).__name__ == TextDataReader.__name__


def test_main_yaml(monkeypatch, capsys, tmpdir) -> None:
    from src import main as main_module
    p = tmpdir.join("data.yaml")
    p.write_text("- Иванов Иван Иванович:\n    математика: 95\n"
                 "    химия: 90\n- Петров Петр Петрович:\n"
                 "    математика: 60\n", encoding='utf-8')
    monkeypatch.setattr("sys.argv", ["main.py", "-p", str(p)])
    main_module.main()
    out = capsys.readouterr().out
    assert "Number of excellent students:  1" in out
    assert "Rating:" in out
