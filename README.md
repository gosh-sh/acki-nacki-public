# Gosh AckiNacki

```bash
mkdir -p ./keys
docker run -it --rm -v $(pwd)/keys:/workdir teamgosh/bls-keygen:main python3 /root/generate_keys_and_bc_config.py
```
