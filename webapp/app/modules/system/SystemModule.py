import locale
import logging
import os
import socket
import subprocess
from pathlib import Path
from typing import List, Tuple

from crontab import CronTab
from git import Repo, GitCommandError

from app.lib.ModuleInterface import ModuleInterface


class SystemModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "system",  # interne id
            "display_name": "System",
            "icon": "bi-motherboard",
            "type": "module"  # oder "submodule"
        }

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def list_installed_languages():
        b = locale.getlocale()
        a = locale.getdefaultlocale()

        print(a)

        print(b)

    @staticmethod
    def change_password(username, password) -> bool:
        try:
            input_data = f"{username}:{password}"
            subprocess.run(['sudo', 'chpasswd'], input=input_data.encode(), check=True)
        except subprocess.CalledProcessError:
            return False

        return True

    @staticmethod
    def reboot_system() -> bool:
        try:
            subprocess.run(['sudo', 'reboot'], check=True)
        except subprocess.CalledProcessError as e:
            logging.error("reboot_system:", e)
            return False

        return True

    @staticmethod
    def auto_system_update(enable: bool = True):
        # TODO: Load from config
        SCRIPT_PATH = ''
        CRON_JOB = ''

        try:
            result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            lines = result.stdout.strip().split('\n') if result.returncode == 0 else []

            # Filter out existing job
            lines = [line for line in lines if SCRIPT_PATH not in line]

            if enable:
                lines.append(CRON_JOB)

            new_crontab = '\n'.join(lines) + '\n'
            subprocess.run(['crontab', '-'], input=new_crontab.encode(), check=True)

            return True
        except subprocess.CalledProcessError:
            return False

    # TODO: This is the replacement for auto_system_update
    @staticmethod
    def cron_toggle_lib(script_path: str, enable: bool) -> bool:
        try:
            cron = CronTab(user=True)
            job_comment = 'auto_apt_update_job'

            # Suche vorhandenen Job
            jobs = list(cron.find_comment(job_comment))

            # Lösche vorhandene Jobs mit dem Kommentar
            for job in jobs:
                cron.remove(job)

            if enable:
                job = cron.new(command=f"sudo {script_path}", comment=job_comment)
                job.setall('0 3 * * *')

            cron.write()
            return True
        except Exception:
            return False

    @staticmethod
    def git_pull(repo_path: str) -> bool:
        path = Path(repo_path)
        if not path.is_dir():
            return False
        try:
            repo = Repo(repo_path)
            repo.remotes.origin.pull()
            return True
        except (GitCommandError, Exception):
            return False

    @staticmethod
    def cron_toggle_git_pull(repo_path: str, enable: bool) -> bool:
        CRON_COMMENT = "git_auto_pull_job"
        try:
            cron = CronTab(user=True)
            command = f"cd {repo_path} && git pull"

            for job in cron.find_comment(CRON_COMMENT):
                cron.remove(job)

            if enable:
                job = cron.new(command=command, comment=CRON_COMMENT)
                job.setall("*/10 * * * *")  # alle 10 Minuten (anpassbar)

            cron.write()
            return True
        except Exception:
            return False

    @staticmethod
    def checkout_commit(repo_path: str, branch: str, commit_hash: str) -> bool:
        try:
            repo = Repo(Path(repo_path))
            repo.git.fetch()
            repo.git.checkout(branch)
            repo.git.reset('--hard', commit_hash)
            return True
        except (GitCommandError, Exception):
            return False

    @staticmethod
    def get_latest_commits(repo_path: str, count: int = 10) -> List[Tuple[str, str, str]]:
        repo = Repo(Path(repo_path))
        commits = list(repo.iter_commits('HEAD', max_count=count))
        return [(c.hexsha[:7], c.committed_datetime.isoformat(), c.summary) for c in commits]


if __name__ == '__main__':
    SystemModule().list_installed_languages()