from ssh_checkout import ssh_checkout, ssh_upload_files
from checkout import getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestDeploy:

    def save_log(self, start_time, name):
        with open(name, "w", encoding="utf-8") as f:
            f.write(getout(f"journalctl --since '{start_time}'"))

    def test_deploy(self, start_time):
        result = []
        ssh_upload_files(data["host"], data["user"], data["passwd"], "{}{}.deb".format(data["PATH_FILE"], data["file_name"]), "{}{}.deb".format(data[
            'HOME_USER2'], data["file_name"]))
        result.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo {} | sudo -S dpkg -i {}{}.deb".format(data["passwd"], data[
            'HOME_USER2'], data["file_name"]), "Настраивается пакет"))
        result.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -s {}".format(data["passwd"], data["file_name"]), "Status: install ok installed"))
        self.save_log(start_time, "log_test_deploy")
        assert all(result), "test deploy fail"
