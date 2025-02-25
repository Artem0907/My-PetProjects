import unittest
from unittest.mock import patch, MagicMock
from os.path import exists, dirname
from os import rmdir, remove
from datetime import datetime
from io import StringIO

from colorama import Style, Fore
from .turbo_print import TurboPrint, LogLevels


class TestTurboPrint(unittest.TestCase):

    def setUp(self) -> None:
        self.tp = TurboPrint(
            directory="test_logs",
            file_name="test_log",
            file_log_level=LogLevels.NOTSET,
            console_log_level=LogLevels.NOTSET,
        )
        self.test_log_path = self.tp.file_path

    def tearDown(self) -> None:
        if exists(self.test_log_path):
            remove(self.test_log_path)
        if exists(dirname(self.test_log_path)):
            rmdir(dirname(self.test_log_path))

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.open", create=True)
    def test_basic_logging(self, mock_open: MagicMock, mock_stdout: StringIO) -> None:
        self.tp("Test message", level=LogLevels.INFO)
        self.assertIn(
            "[{time}] TP | INFO: Test message".format(
                time=datetime.now().strftime("%H:%M:%S")
            ),
            mock_stdout.getvalue(),
        )
        mock_open.assert_called_once()

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.open", create=True)
    def test_different_log_levels(
        self, mock_open: MagicMock, mock_stdout: StringIO
    ) -> None:
        self.tp("Success message", level=LogLevels.SUCCESS)
        self.tp("Info message", level=LogLevels.INFO)
        self.tp("Warning message", level=LogLevels.WARNING)
        self.tp("Error message", level=LogLevels.ERROR)
        self.tp("Debug message", level=LogLevels.DEBUG)
        self.assertIn("SUCCESS", mock_stdout.getvalue())
        self.assertIn("INFO", mock_stdout.getvalue())
        self.assertIn("WARNING", mock_stdout.getvalue())
        self.assertIn("ERROR", mock_stdout.getvalue())
        self.assertIn("DEBUG", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_file_logging(self, mock_stdout: StringIO) -> None:
        tp_output = self.tp("File log message", level=LogLevels.WARNING)
        with open(self.test_log_path, "r") as f:
            self.assertEqual(tp_output["file"] + "\n", f.readlines()[-1])

    @patch("sys.stdout", new_callable=StringIO)
    def test_custom_format(self, mock_stdout: StringIO) -> None:
        custom_tp = TurboPrint(
            console_format="[{prefix}] - {message}",
            file_format="LOG: {message}",
            prefix="TP",
        )
        output = custom_tp("Custom message", LogLevels.DEBUG)
        self.assertEqual(output["standard"], "[TP] - Custom message")
        self.assertEqual(
            output["console"],
            f"{Style.RESET_ALL}{LogLevels.DEBUG.color}[TP] - Custom message{Style.RESET_ALL}",
        )
        self.assertEqual(output["file"], "LOG: Custom message")

    @patch("sys.stdout", new_callable=StringIO)
    def test_custom_color(self, mock_stdout: StringIO) -> None:
        output = self.tp("Custom message", LogLevels.DEBUG, Fore.GREEN)
        self.assertEqual(
            "{color_start}[{time}] TP | DEBUG: Custom message{color_end}".format(
                time=datetime.now().strftime("%H:%M:%S"),
                color_start=Style.RESET_ALL + Fore.GREEN,
                color_end=Style.RESET_ALL,
            ),
            output["console"],
        )
        self.assertEqual(
            "{color_start}[{time}] TP | DEBUG: Custom message{color_end}\n".format(
                time=datetime.now().strftime("%H:%M:%S"),
                color_start=Style.RESET_ALL + Fore.GREEN,
                color_end=Style.RESET_ALL,
            ),
            mock_stdout.getvalue(),
        )

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.open", create=True)
    def test_disabled_logging(
        self, mock_open: MagicMock, mock_stdout: StringIO
    ) -> None:
        disabled_tp = TurboPrint(enable=False)
        output = disabled_tp("This should not be logged")
        mock_open.assert_not_called()
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch("sys.stdout", new_callable=StringIO)
    def test_console_output_disabled(self, mock_stdout: StringIO) -> None:
        tp_no_console = TurboPrint(console_output=False)
        tp_no_console("Message", level=LogLevels.INFO)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.open", create=True)
    def test_file_output_disabled(
        self, mock_open: MagicMock, mock_stdout: StringIO
    ) -> None:
        tp_no_file = TurboPrint(file_output=False)
        tp_no_file("Message", level=LogLevels.WARNING)
        mock_open.assert_not_called()

    @patch("sys.stdout", new_callable=StringIO)
    def test_kwargs(self, mock_stdout: StringIO) -> None:
        tp = TurboPrint(
            file_output=False, console_format="[{user}] {prefix} | {level}: {message}"
        )
        output = tp(
            "Message with kwargs",
            level=LogLevels.INFO,
            user="testuser",
        )
        self.assertIn("user", output["standard"])


if __name__ == "__main__":
    unittest.main()
