import hashlib
import threading
import time
import argparse
import sys
from typing import List, Optional

class MultiThreadedHashCracker:
    def __init__(self, target_hash: str, wordlist_path: str, num_threads: int = 4):
        self.target_hash = target_hash.lower().strip()
        self.wordlist_path = wordlist_path
        self.num_threads = num_threads
        self.stop_event = threading.Event()
        self.found_password: Optional[str] = None
        self.total_tested = 0
        self.counter_lock = threading.Lock()

    def _worker(self, words: List[str]):
        """Worker thread function to process a chunk of words."""
        local_count = 0
        for word in words:
            if self.stop_event.is_set():
                break

            # Strip whitespace/newlines
            clean_word = word.strip()
            # Compute MD5 hash
            hashed_val = hashlib.md5(clean_word.encode('utf-8')).hexdigest()
            local_count += 1

            if hashed_val == self.target_hash:
                self.found_password = clean_word
                self.stop_event.set()
                break

        with self.counter_lock:
            self.total_tested += local_count

    def run(self) -> Optional[str]:
        """Loads wordlist, chunks data across threads, and starts cracking."""
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                words = f.readlines()
        except FileNotFoundError:
            print(f"Error: Wordlist file '{self.wordlist_path}' not found.")
            return None

        total_words = len(words)
        if total_words == 0:
            print("Error: Wordlist is empty.")
            return None

        print(f"[*] Loaded {total_words:,} words from wordlist.")
        print(f"[*] Starting {self.num_threads} threads for cracking target MD5: {self.target_hash}...")

        # Calculate chunk sizes
        chunk_size = (total_words + self.num_threads - 1) // self.num_threads
        threads = []

        start_time = time.perf_counter()

        for i in range(self.num_threads):
            chunk = words[i * chunk_size : (i + 1) * chunk_size]
            if not chunk:
                break
            t = threading.Thread(target=self._worker, args=(chunk,), name=f"Worker-{i+1}")
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        elapsed_time = time.perf_counter() - start_time
        hash_rate = self.total_tested / elapsed_time if elapsed_time > 0 else 0

        print(f"\n[*] Scan complete in {elapsed_time:.2f} seconds.")
        print(f"[*] Hashes tested: {self.total_tested:,} ({hash_rate:,.0f} H/s)")

        if self.found_password:
            print(f"Found: {self.found_password}")
            return self.found_password
        else:
            print("[-] Password not found in wordlist.")
            return None

def main():
    parser = argparse.ArgumentParser(description="Multi-threaded MD5 Dictionary Hash Cracker")
    parser.add_argument("-hash", "--target-hash", required=True, help="Target MD5 hash to crack")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the dictionary wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads (default: 4)")

    args = parser.parse_args()
    cracker = MultiThreadedHashCracker(args.target_hash, args.wordlist, args.threads)
    cracker.run()

if __name__ == "__main__":
    main()
