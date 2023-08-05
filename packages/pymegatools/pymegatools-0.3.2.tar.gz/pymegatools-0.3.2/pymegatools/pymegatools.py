import stat
import logging
import platform
import requests
import tempfile
import subprocess
from pathlib import Path

logger = logging.getLogger(Path(__file__).stem)


class Megatools():
    def __init__(self, executable=None):
        self._tempdir = Path(tempfile.gettempdir())
        if not executable:
            executable = self._tempdir / "megatools"
            if not executable.exists():
                url = "https://raw.githubusercontent.com/justaprudev/megatools/master/megatools"
                binary = requests.get(f"{url}.exe" if platform.system() == "Windows" else url)
                with open(executable, "wb") as f:
                    f.write(binary.content)
                executable.chmod(executable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        self.executable = str(executable)

    def _execute(self, cmd, callback, callback_args):
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        while proc.poll() is None:
            callback(proc, *callback_args)
        return (proc.stdout, proc.returncode)

    def download(
        self,
        link,
        callback=lambda proc: print(proc.stdout.readline().decode("utf-8", "ignore").strip()),
        callback_args=(),
        **options
    ):
        """
        Switches:
          no_progress               Disable progress bar
          print_names               Print names of downloaded files
          choose_files              Choose which files to download when downloading folders (interactive)
          disable_resume            Disable resume when downloading file
          no_ask_password           Never ask interactively for a password
          reload                    Reload filesystem cache
          ignore_config_file        Disable loading mega.ini
          version                   Show version information
        Options:
          path=PATH                 Local directory or file name, to save data to
          u, username=USERNAME     Account username (email)
          p, password=PASSWORD     Account password
          limit_speed=SPEED         Limit transfer speed (KiB/s)
          proxy=PROXY               Proxy setup string
          netif=NAME                Network interface or local IP address used for outgoing connections
          ip_proto=PROTO            Which protocol to prefer when connecting to mega.nz (v4, v6, or any)
          config=PATH               Load configuration from a file
          debug=OPTS                Enable debugging output
        """
        cmd = [self.executable, "dl", link, "--no-ask-password"]
        for option, value in options.items():
            option = option.replace("_", "-")
            if value is True:
                cmd.append(f"--{option}")
                continue
            cmd.append(f"--{option}={value}")
        logger.info(f"Executing: {cmd}")
        stdout, exit_code = self._execute(cmd, callback, callback_args)
        logger.info(f"Exited with exit code {exit_code}")
        return (stdout, exit_code)
    
    def version(self):
        """
        Get the version information of the mega binary being used
        """
        stdout, _ = self.download("", callback=lambda _: None, version=True)
        return stdout.read().decode("utf-8", "ignore").splitlines()[0]
    
    def filename(self, link):
        """
        Get file name from a mega link
        """
        output = []
        self.download(link, callback=lambda proc, output: output.append(proc.stdout.readline().decode("utf-8", "ignore").split(":")[0]) or proc.terminate(), callback_args=[output], print_names=True, limit_speed=1, path=str(self._tempdir))
        return output[0]