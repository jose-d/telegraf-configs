import subprocess
import threading

class Command:

    # good old class I use to execute commands in OS shell.

    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.stdout = ""

        self.stderr = ""

        self.rc = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(
                self.cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='UTF-8',  # this actually needs at least Python 3.6
            )
            self.stdout, self.stderr = self.process.communicate()
            self.rc = self.process.wait()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            print('Command.run(): timeout: terminating process')
            self.process.terminate()
            thread.join()
            self.rc = 999

        return self.rc, self.stdout, self.stderr
