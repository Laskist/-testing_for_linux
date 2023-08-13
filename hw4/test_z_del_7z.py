from ssh_checkout import ssh_checkout
from checkout import getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)

def safe_log(start_time, name):
        with open(name, "w", encoding="utf-8") as f:
            f.write(getout(f"journalctl --since '{start_time}'"))


def test_deploy_del(start_time):
    result = ssh_checkout(data["host"], data["user"], data["passwd"], "echo {} | sudo -S dpkg -r {}".format(data["passwd"], data["file_name"]), "Удаляется p7zip-full")
    safe_log(start_time, "log_test_del")
    assert result, "test deploy fail"