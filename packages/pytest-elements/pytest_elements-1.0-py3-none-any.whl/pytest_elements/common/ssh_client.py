import atexit
import paramiko


class SSHClient:
    """
    Wrapper to make SSH easier
    """

    def __init__(self, address, username, key_path):
        self.address = address
        self.username = username
        self.key_path = key_path
        self.client = paramiko.SSHClient()
        atexit.register(self.disconnect)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """
        Connect to the SSH server
        :return: None
        """
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = paramiko.RSAKey.from_private_key_file(self.key_path)
        self.client.connect(self.address, username=self.username, pkey=k, allow_agent=True)

    def disconnect(self):
        """
        Disconnect from the SSH session
        :return: None
        """
        self.client.close()

    def exec(self, cmd) -> "SSHCommandResult":
        """
        Execute a command over the SSH session
        :param cmd: The command to execute as a string
        :return: A SSHCommandResult with the output and return code of the command
        """
        stdin, stdout, stderr = self.client.exec_command(cmd)

        stdout_str = stdout.read().decode()
        stderr_str = stderr.read().decode()
        return_code = stdout.channel.recv_exit_status()
        result = SSHCommandResult(stdout_str, stderr_str, return_code)

        if return_code != 0:
            raise RuntimeError(f'SSH command "{cmd}" returned a non-zero exit code', result)

        return result


class SSHCommandResult:
    """
    Contains the result of an executed SSH command
    """

    def __init__(self, stdout: str, stderr: str, return_code: int):
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code

    def __str__(self):
        return "STDOUT: {}\nSTDERR: {}\nReturn Code: {}".format(self.stdout, self.stderr, self.return_code)
