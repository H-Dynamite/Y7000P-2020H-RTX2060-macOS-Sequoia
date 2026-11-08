#!/usr/bin/env python3
"""Validate the public EFI, privacy placeholders, and active file references."""
import pathlib
import plistlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = {
    'SystemSerialNumber': 'C02XXXXXXXXX',
    'MLB': 'M0000000000000001',
    'SystemUUID': '00000000-0000-0000-0000-000000000000',
    'ROM': bytes.fromhex('112233445566'),
}


def validate(root=ROOT):
    errors = []
    checked = 0
    oc = root / 'EFI/OC'
    configs = [oc / 'config.plist', *sorted((root / 'configs').glob('*.plist'))]
    for path in configs:
        try:
            config = plistlib.loads(path.read_bytes())
            for key, value in EXPECTED.items():
                if config['PlatformInfo']['Generic'].get(key) != value:
                    errors.append(f'{path.relative_to(root)}: private/non-placeholder {key}')
            nvram = config['NVRAM']['Add']['7C436110-AB2A-4BBB-A880-FE41995C9F82']
            if any(k in nvram for k in ['bluetoothInternalControllerInfo', 'bluetoothExternalDongleFailed']):
                errors.append(f'{path.name}: cached Bluetooth identity')
            for entry in config['ACPI']['Add']:
                if entry['Enabled'] and not (oc / 'ACPI' / entry['Path']).is_file():
                    errors.append(f'{path.name}: missing ACPI {entry["Path"]}')
            for entry in config['UEFI']['Drivers']:
                if entry.get('Enabled', True) and not (oc / 'Drivers' / entry['Path']).is_file():
                    errors.append(f'{path.name}: missing driver {entry["Path"]}')
            for entry in config['Misc']['Tools']:
                if entry['Enabled'] and not (oc / 'Tools' / entry['Path']).is_file():
                    errors.append(f'{path.name}: missing tool {entry["Path"]}')
            for entry in config['Kernel']['Add']:
                if not entry['Enabled']:
                    continue
                bundle = oc / 'Kexts' / entry['BundlePath']
                for key in ['PlistPath', 'ExecutablePath']:
                    if entry[key] and not (bundle / entry[key]).is_file():
                        errors.append(f'{path.name}: missing {entry["BundlePath"]}/{entry[key]}')
            checked += 1
        except (ValueError, KeyError, OSError, plistlib.InvalidFileException) as exc:
            errors.append(f'{path.name}: invalid config ({type(exc).__name__})')

    def inspect(value, relative):
        if isinstance(value, dict):
            for key, item in value.items():
                if key.lower() in {'ssid', 'password'} and isinstance(item, str) and item:
                    errors.append(f'{relative}: nonempty Wi-Fi credential field')
                inspect(item, relative)
        elif isinstance(value, list):
            for item in value:
                inspect(item, relative)

    for path in root.rglob('*'):
        if not path.is_file() or '.git' in path.relative_to(root).parts:
            continue
        relative = path.relative_to(root)
        if path.suffix.lower() in {'.panic', '.ips', '.log', '.pem', '.key'} or '.before-' in path.name:
            errors.append(f'{relative}: private/backup file type')
        if path.name in {'authorized_keys', 'id_ed25519', 'id_rsa'}:
            errors.append(f'{relative}: SSH material')
        if path.suffix == '.plist':
            try:
                inspect(plistlib.loads(path.read_bytes()), relative)
            except (ValueError, plistlib.InvalidFileException):
                errors.append(f'{relative}: invalid plist')
    for name in ['EFI/BOOT/BOOTx64.efi', 'EFI/OC/OpenCore.efi']:
        if not (root / name).is_file():
            errors.append(f'Missing {name}')
    return checked, errors


if __name__ == '__main__':
    checked, errors = validate()
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    print(f'PASS: {checked} public configs; references and privacy fields checked.')
