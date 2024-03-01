## Generating BLS-keys

### Prerequisites:

* cargo
* [tvm-cli](https://github.com/tvmlabs/tvm-cli/releases)
* python3

### Install bls_keypair_gen

```bash
cd helpers/bls_keypair_gen
cargo install --path .
```

### Set the number of validators

```bash
cd ../blockchain_config
```

Edit Python script (generate_keys_and_bc_config.py) to set the number of validators and output paths for BLS-keychain file and blockchain config file:

```python
NUMBER_OF_VALIDATORS = 12
OUTPUT_CONFIG = 'blockchain.conf.json'
BLS_PUBLICS_PATH = 'bls_publics_12.keys.json'
```

### Run the python script

```bash
python3 generate_keys_and_bc_config.py
```

The set of the key pairs for the validators will be created in the current folder.
