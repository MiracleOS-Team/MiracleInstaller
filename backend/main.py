import os


class DotDict(dict):
    def __getattr__(self, item):
        try:
            if isinstance(self[item], dict):
                return DotDict(self[item])
            return self[item]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        self[key] = value

def dot_dicts(dicts):
    result = {}
    for d in dicts:
        if not isinstance(dicts[d], dict):
            result[d] = dicts[d]
            continue

        result[d] = DotDict(dicts[d])
    return result

templateData = {
    "swap": "8Gib",
    "boot": {
        "type": "efi",
    },
    "disk": {
        "encryption": {
            "enabled": "false",
            "key": ""
        },
        "rootfs": "ext4",
        "device": "/dev/sda"
    },
    "system": {
        "hostname": "MiracleOS-Computer",
        "timezone": "Europe/Paris",
        "keymap": "fr",
        "locales": {
            "enabled": "",
            "default": "C.UTF-8"
        }
    },
    "starter": {
        "systemd": {
            "networkd": {
                "enabled": "true",
                "dhcp": {
                    "enabled": "true"
                }
            }
        },
        "stage3": {
            "variant": "systemd"
        }
    },
    "initramfs": {
        "sshd": {
            "enabled": "true"
        }
    },
    "mirrors": {
        "select": {
            "largefiles": "true"
        }
    },
    "binpkg": {
        "enabled": "true"
    }
}

def edit_config(config):
    with open("backend/template.sh", "r") as f:
        template = f.read()

    sdata = template.format(**dot_dicts(config))

    with open("gentoo-install/gentoo.conf", "w") as f:
        f.write(sdata)

def launch_install():
    os.system("bash backend/install.sh")

#edit_config(templateData)