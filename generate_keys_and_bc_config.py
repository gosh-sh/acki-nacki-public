# 2022-2024 (c) Copyright Contributors to the GOSH DAO. All rights reserved.
#
import os
import json
import subprocess

NUMBER_OF_VALIDATORS = 12
DEFAULT_WEIGHT = 17
BASE_CONFIG = '/root/blockchain.conf.json.template'
OUTPUT_CONFIG = 'blockchain.conf.json'
BLS_PUBLICS_PATH = 'bls_publics.keys.json'
WAS_ERROR = False


def execute_cmd(command: str, work_dir=None, ignore_error=False, silent=False):
    global WAS_ERROR
    if work_dir is not None:
        command = f"cd {work_dir} && {command}"
    WAS_ERROR = False
    if not silent:
        print(command)
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        output = e.output.decode("utf-8")
        WAS_ERROR = True
        if not ignore_error:
            print(f"Command `{command}` execution failed: {output} {e.stderr}")
            exit(1)

    return output.strip()


def load_keys(path):
    with open(path) as f:
        data = f.read()
    mapping = json.loads(data)
    public = mapping['public']
    secret = mapping['secret']
    return public, secret


def generate_key(path: str, rewrite: bool = False):
    if not os.path.exists(path) or rewrite:
        execute_cmd(f"tvm-cli -j genphrase --dump {path}")


def generate_bc_config():
    # Generate key pairs
    pubkeys = []
    secrets = []
    for i in range(NUMBER_OF_VALIDATORS):
        key_path = f"validator{i}.keys.json"
        generate_key(key_path, True)
        (public, secret) = load_keys(key_path)
        pubkeys.append(public)
        secrets.append(secret)

    # Load evernode-se config to use it as base
    with open(BASE_CONFIG) as f:
        data = f.read()
    base_config = json.loads(data)

    # Configure p34 with generated material
    base_config["p34"]["total"] = NUMBER_OF_VALIDATORS
    base_config["p34"]["main"] = NUMBER_OF_VALIDATORS
    base_config["p34"]["total_weight"] = NUMBER_OF_VALIDATORS * DEFAULT_WEIGHT
    list = []
    for i in range(NUMBER_OF_VALIDATORS):
        list.append({
            "public_key": pubkeys[i],
            "weight": DEFAULT_WEIGHT
        })
    base_config["p34"]["list"] = list

    # Save config
    with open(OUTPUT_CONFIG, 'w') as file:
        file.write(json.dumps(base_config, indent=2))

    # Generate BLS public keys for validator secret keys
    bls_publics = {}
    bls_keys = {}
    for i in range(NUMBER_OF_VALIDATORS):
        bls_key = execute_cmd(f"bls_keypair_gen {secrets[i]}")#, silent=True)
        key_pair = json.loads(bls_key)
        bls_publics[i] = key_pair["public"]
        bls_keys[i] = key_pair

    # Save bls keys
    with open(BLS_PUBLICS_PATH, 'w') as file:
        file.write(json.dumps(bls_publics, indent=2))
    for i in range(NUMBER_OF_VALIDATORS):
        with open(f"validator{i}_bls.keys.json", 'w') as file:
            file.write(json.dumps(bls_keys[i], indent=2))

generate_bc_config()
