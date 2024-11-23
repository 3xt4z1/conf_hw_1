import os
import unittest
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Создаём тестовую файловую систему
        self.vfs_path = "test_vfs.zip"
        self.log_path = "test_log.csv"
        self.emulator = ShellEmulator("test_user", "test_host", self.vfs_path, self.log_path)

    def test_ls(self):
        self.emulator.current_dir = Path("/")  # Теперь используется Path
        self.emulator.ls()
        # Здесь вы можете добавить проверку вывода или логов

    def test_cd(self):
        self.emulator.current_dir = Path("/")
        self.emulator.cd(["folder1"])
        self.assertEqual(self.emulator.current_dir, Path("/folder1"))  # Сравниваем с Path

    def test_rev(self):
        output = self.emulator.rev(["hello", "world"])
        self.assertEqual(output, "dlrow olleh")  # Проверка перевёрнутой строки

    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.emulator.handle_command("exit")

if __name__ == "__main__":
    unittest.main()
