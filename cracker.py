import argparse
import hashlib
import itertools
import multiprocessing
import os
import sys
import time
from functools import partial

try:
    import bcrypt
except ImportError:
    bcrypt = None

def mutate_word(word):
    mutations = set()
    mutations.add(word)
    mutations.add(word.lower())
    mutations.add(word.upper())
    mutations.add(word.capitalize())
    
    # Leet substitutions
    leet = word.translate(str.maketrans({
        'a': '4', 'A': '4',
        'e': '3', 'E': '3',
        'i': '1', 'I': '1',
        'o': '0', 'O': '0',
        's': '5', 'S': '5',
        't': '7', 'T': '7'
    }))
    mutations.add(leet)
    
    # Common suffixes
    for i in range(0, 100):
        mutations.add(f"{word}{i:02d}")
        mutations.add(f"{word}{i}")
    
    return mutations

def generate_candidates(wordlist_path, mutate):
    with open(wordlist_path, 'r', errors='ignore') as f:
        for line in f:
            word = line.strip()
            if mutate:
                yield from mutate_word(word)
            else:
                yield word

def check_candidate(candidate, target_hash, hash_type):
    try:
        if hash_type == 'bcrypt':
            if bcrypt.checkpw(candidate.encode(), target_hash.encode()):
                return candidate
        else:
            hasher = hashlib.new(hash_type)
            hasher.update(candidate.encode())
            if hasher.hexdigest() == target_hash:
                return candidate
    except Exception:
        pass
    return None

def dictionary_attack(target_hash, hash_type, wordlist_path, processes, mutate):
    candidate_gen = generate_candidates(wordlist_path, mutate)
    
    with multiprocessing.Pool(processes) as pool:
        try:
            results = pool.imap_unordered(
                partial(check_candidate, target_hash=target_hash, hash_type=hash_type),
                candidate_gen,
                chunksize=1000
            )
            
            for result in results:
                if result is not None:
                    pool.terminate()
                    return result
        except KeyboardInterrupt:
            pool.terminate()
            raise
        finally:
            pool.close()
            pool.join()
    return None

def brute_worker(args, charset, target_hash, hash_type):
    length, start, end = args
    base = len(charset)
    for idx in range(start, end):
        password = []
        n = idx
        for _ in range(length):
            n, rem = divmod(n, base)
            password.append(charset[rem])
        candidate = ''.join(reversed(password))
        if check_candidate(candidate, target_hash, hash_type):
            return candidate
    return None

def brute_force_attack(target_hash, hash_type, max_length, charset, processes):
    charset = list(charset)
    base = len(charset)
    
    for length in range(1, max_length + 1):
        total = base ** length
        chunk_size = max(total // processes, 1)
        chunks = [(length, i * chunk_size, min((i + 1) * chunk_size, total)) 
                 for i in range(processes)]
        
        with multiprocessing.Pool(processes) as pool:
            try:
                results = pool.imap_unordered(
                    partial(brute_worker, charset=charset, 
                          target_hash=target_hash, hash_type=hash_type),
                    chunks,
                    chunksize=1
                )
                
                for result in results:
                    if result is not None:
                        pool.terminate()
                        return result
            except KeyboardInterrupt:
                pool.terminate()
                raise
            finally:
                pool.close()
                pool.join()
    return None

def validate_hash(hash_value, hash_type):
    if hash_type == 'bcrypt':
        if not bcrypt:
            raise ValueError("bcrypt requires 'pip install bcrypt'")
        if not hash_value.startswith(('$2a$', '$2b$', '$2y$')):
            raise ValueError("Invalid bcrypt hash format")
        return
    
    valid_lengths = {
        'md5': 32, 'sha1': 40, 
        'sha256': 64, 'sha512': 128
    }
    if len(hash_value) != valid_lengths[hash_type]:
        raise ValueError(f"Invalid {hash_type} hash length")
    if not all(c in '0123456789abcdef' for c in hash_value):
        raise ValueError(f"Invalid {hash_type} hash characters")

def main():
    parser = argparse.ArgumentParser(
        description="Advanced Password Cracker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('hash', help="Target hash to crack")
    parser.add_argument('hash_type', choices=['md5', 'sha1', 'sha256', 'sha512', 'bcrypt'],
                       help="Hash algorithm used")
    parser.add_argument('mode', choices=['dict', 'brute'], 
                       help="Attack mode")
    parser.add_argument('-w', '--wordlist', help="Wordlist path (for dictionary attack)")
    parser.add_argument('-m', '--mutate', action='store_true',
                       help="Enable password mutations (dictionary attack)")
    parser.add_argument('-p', '--processes', type=int, default=os.cpu_count(),
                       help="Number of parallel processes")
    parser.add_argument('-l', '--max-length', type=int, default=6,
                       help="Max password length (brute force)")
    parser.add_argument('-c', '--charset', 
                       default='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()',
                       help="Character set (brute force)")

    args = parser.parse_args()
    
    try:
        validate_hash(args.hash, args.hash_type)
    except ValueError as e:
        print(f"Hash validation failed: {e}")
        sys.exit(1)

    start_time = time.time()
    
    if args.mode == 'dict':
        if not args.wordlist:
            print("Dictionary attack requires --wordlist")
            sys.exit(1)
            
        print(f"[*] Running dictionary attack with {args.processes} processes...")
        result = dictionary_attack(
            args.hash, args.hash_type, args.wordlist, 
            args.processes, args.mutate
        )
    else:
        print(f"[*] Running brute force attack (max length: {args.max_length})...")
        result = brute_force_attack(
            args.hash, args.hash_type, args.max_length,
            args.charset, args.processes
        )

    if result:
        print(f"\n[+] Password found: {result}")
    else:
        print("\n[-] Password not found")
        
    print(f"Time elapsed: {time.time() - start_time:.2f}s")

if __name__ == '__main__':
    main()
