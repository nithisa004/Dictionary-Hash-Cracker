# Multi-Threaded MD5 Dictionary Hash Search

A Python script that takes an MD5 hash and a wordlist file to execute a multi-threaded dictionary search algorithm.

## Prerequisites
- Python 3.6 or higher.

## Usage

Run the script from your terminal:

```bash
py -3 hash_cracker.py -hash <TARGET_MD5_HASH> -w <WORDLIST_PATH> -t <THREAD_COUNT>
```

### Parameters
| Flag | Long Flag | Description | Default |
| --- | --- | --- | --- |
| `-hash` | `--target-hash` | The target MD5 hash string to crack | *Required* |
| `-w` | `--wordlist` | Path to the wordlist text file | *Required* |
| `-t` | `--threads` | Number of worker threads | `4` |

## Example Command

```bash
py -3 hash_cracker.py -hash 5ebe2294ecd0e0f08eab7690d2a6ee69 -w sample_wordlist.txt -t 8
```

### Example Output
```text
[*] Loaded 100 words from wordlist.
[*] Starting 8 threads for cracking target MD5: 5ebe2294ecd0e0f08eab7690d2a6ee69...

[*] Scan complete in 0.00 seconds.
[*] Hashes tested: 6 (2,450 H/s)
Found: secret
```
