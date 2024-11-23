import os
import sys
import zipfile
import csv
from pathlib import Path

class ShellEmulator:
    def __init__(self, user, host, vfs_path, log_path):
        self.user = user
        self.host = host
        self.log_path = log_path
        self.current_dir = Path("/")
        self.vfs_root = Path("vfs_root")

        # Распаковываем виртуальную файловую систему
        with zipfile.ZipFile(vfs_path, 'r') as zip_ref:
            zip_ref.extractall(self.vfs_root)

        # Создаем/очищаем лог-файл
        with open(self.log_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Action", "Path"])

    def log_action(self, action, path=""):
        with open(self.log_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.user, action, path])

    def prompt(self):
        return f"{self.user}@{self.host}:{self.current_dir}$ "

    def run(self):
        try:
            while True:
                command = input(self.prompt()).strip()
                self.handle_command(command)
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Error: {e}")

    def handle_command(self, command):
        if not command:
            return
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "exit":
            self.log_action("exit")
            print("Bye!")
            sys.exit(0)
        elif cmd == "clear":
            self.log_action("clear")
            os.system("clear" if os.name == "posix" else "cls")
        elif cmd == "ls":
            self.ls()
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "rev":
            self.rev(args)
        else:
            print(f"{cmd}: command not found")

    def ls(self):
        vfs_dir = self.vfs_root / self.current_dir.relative_to("/")
        self.log_action("ls", str(vfs_dir))
        try:
            entries = os.listdir(vfs_dir)
            for entry in entries:
                print(entry)
        except FileNotFoundError:
            print(f"{self.current_dir}: No such file or directory")

    def cd(self, args):
        if not args:
            print("cd: missing argument")
            return

        new_dir = args[0]
        if new_dir == "/":
            self.current_dir = Path("/")
        elif new_dir == "..":
            self.current_dir = self.current_dir.parent if self.current_dir != Path("/") else Path("/")
        else:
            candidate = self.current_dir / new_dir
            vfs_candidate = self.vfs_root / candidate.relative_to("/")
            if vfs_candidate.exists() and vfs_candidate.is_dir():
                self.current_dir = candidate
            else:
                print(f"cd: {new_dir}: No such file or directory")

        self.log_action("cd", str(self.current_dir))

    def rev(self, args):
        if not args:
            print("rev: missing argument")
            return
        reversed_str = " ".join(args)[::-1]
        print(reversed_str)
        self.log_action("rev", " ".join(args))
        return reversed_str  # Возвращаем значение


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--user", required=True, help="User name for prompt")
    parser.add_argument("--host", required=True, help="Host name for prompt")
    parser.add_argument("--vfs", required=True, help="Path to virtual file system zip")
    parser.add_argument("--log", required=True, help="Path to log file")

    args = parser.parse_args()

    emulator = ShellEmulator(user=args.user, host=args.host, vfs_path=args.vfs, log_path=args.log)
    emulator.run()
