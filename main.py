import json

import backend


def configure_system():
    # Default values
    defaults = {
        "disk_encryption": "false",
        "rootfs": "ext4",
        "boot_type": "efi",
        "swap_size": "8Gib",
        "largefiles": "true",
        "binpkg_enabled": "true"
    }

    # Prompt for choices
    disk_device = input("Enter disk device to install to (e.g., /dev/sda): ")
    hostname = input("Enter hostname (default: MiracleOS-Computer): ") or "MiracleOS-Computer"
    timezone = input("Enter timezone (default: Europe/Paris): ") or "Europe/Paris"
    keymap = input("Enter keymap (default: fr): ") or "fr"
    locales = input("Enter locales (default: C.UTF-8): ") or "C.UTF-8"
    init_system = input("Enter init system (systemd/openrc, default: systemd): ") or "systemd"

    # Build the configuration template
    template_data = {
        "swap": defaults["swap_size"],
        "boot": {
            "type": defaults["boot_type"],
        },
        "disk": {
            "encryption": {
                "enabled": defaults["disk_encryption"],
                "key": ""
            },
            "rootfs": defaults["rootfs"],
            "device": disk_device
        },
        "system": {
            "hostname": hostname,
            "timezone": timezone,
            "keymap": keymap,
            "locales": {
                "enabled": "",
                "default": locales
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
                "variant": init_system
            }
        },
        "initramfs": {
            "sshd": {
                "enabled": "false"
            }
        },
        "mirrors": {
            "select": {
                "largefiles": defaults["largefiles"]
            }
        },
        "binpkg": {
            "enabled": defaults["binpkg_enabled"]
        }
    }

    return template_data

# Generate and print the configuration
config = configure_system()
backend.edit_config(config)
backend.launch_install()