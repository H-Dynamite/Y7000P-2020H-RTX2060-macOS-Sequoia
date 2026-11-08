#!/usr/bin/env python3
"""Build a personalized EFI outside the public repository; never write a disk."""
import argparse
import getpass
import pathlib
import plistlib
import re
import secrets
import shutil
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    parser.add_argument('--mode', choices=['bootstrap', 'nvidia', 'intel'], default='bootstrap')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error('Choose an output directory outside this public repository.')
    if output.exists():
        parser.error('Output already exists; choose a new directory. Nothing overwritten.')
    serial = getpass.getpass('GenSMBIOS SystemSerialNumber: ').strip()
    mlb = getpass.getpass('GenSMBIOS MLB: ').strip()
    if not re.fullmatch(r'[A-Z0-9]{12}', serial) or 'XXXX' in serial:
        parser.error('Enter a new 12-character MacBookPro16,4 serial from GenSMBIOS.')
    if not re.fullmatch(r'[A-Z0-9]{17}', mlb) or mlb == 'M0000000000000001':
        parser.error('Enter a new 17-character MLB from GenSMBIOS.')
    uuid_input = getpass.getpass('SystemUUID (blank = generate): ').strip()
    try:
        system_uuid = uuid.UUID(uuid_input) if uuid_input else uuid.uuid4()
    except ValueError:
        parser.error('SystemUUID must be a valid UUID.')
    if system_uuid.int == 0:
        parser.error('SystemUUID must not be all zero.')
    rom_input = getpass.getpass('ROM, 12 hex characters (blank = generate local unicast): ').strip()
    if rom_input:
        if not re.fullmatch(r'[0-9a-fA-F]{12}', rom_input) or rom_input.lower() == '112233445566':
            parser.error('ROM must be 12 non-placeholder hex characters.')
        rom = bytes.fromhex(rom_input)
    else:
        random_rom = bytearray(secrets.token_bytes(6))
        random_rom[0] = (random_rom[0] | 2) & 0xFE
        rom = bytes(random_rom)
    config = {
        'bootstrap': ROOT / 'configs/config-nvidia-bootstrap.plist',
        'intel': ROOT / 'configs/config-intel-recovery.plist',
        'nvidia': ROOT / 'EFI/OC/config.plist',
    }[args.mode]
    data = plistlib.loads(config.read_bytes())
    data['PlatformInfo']['Generic'].update({
        'SystemSerialNumber': serial, 'MLB': mlb,
        'SystemUUID': str(system_uuid).upper(), 'ROM': rom,
    })
    output.mkdir(parents=True)
    shutil.copytree(ROOT / 'EFI', output / 'EFI')
    (output / 'EFI/OC/config.plist').write_bytes(plistlib.dumps(data, sort_keys=False))
    print(f'Created {args.mode} EFI at {output / "EFI"}. Identity values were not printed.')
    print('No disk was mounted, formatted, or written. Keep this personal output out of GitHub.')


if __name__ == '__main__':
    main()
