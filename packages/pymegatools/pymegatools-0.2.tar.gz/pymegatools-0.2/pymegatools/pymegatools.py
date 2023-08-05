import stat
import requests
import tempfile
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

class Megatools():
    def __init__(self, executable=None, callback=None):
        if not executable:
            executable = Path(tempfile.gettempdir()) / "megatools"
            if not executable.exists():
                binary = requests.get("https://raw.githubusercontent.com/justaprudev/megatools/master/megatools")
                with open(executable, "wb") as f:
                    f.write(binary.content)
                executable.chmod(executable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        self.executable = str(executable)
        self.callback = callback
    
    def _callback(self, proc):
        output = proc.stdout.readline()
        if output:
            print(output.decode())

    def _execute(self, cmd):
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            )
        while proc.poll() is None:
            if self.callback:
                self.callback(proc)
            else:
                self._callback(proc)
        return (proc.stdout, proc.returncode)

    def download(
        self,
        link,
        **options
    ):
        """
        Options:
          path=PATH                 Local directory or file name, to save data to
          u, username=USERNAME     Account username (email)
          p, password=PASSWORD     Account password
          limit-speed=SPEED         Limit transfer speed (KiB/s)
          proxy=PROXY               Proxy setup string
          netif=NAME                Network interface or local IP address used for outgoing connections
          ip-proto=PROTO            Which protocol to prefer when connecting to mega.nz (v4, v6, or any)
          config=PATH               Load configuration from a file
          debug=OPTS                Enable debugging output
        """
        cmd = [self.executable, "dl", link, "--no-ask-password"]
        for option, value in options:
            cmd.append(f"--{option}={value}")
        logger.info(cmd)
        stdout, exit_code = self._execute(cmd)
        logger.info(exit_code)
        return stdout
