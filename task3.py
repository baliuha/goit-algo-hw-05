from typing import Dict, List
from pathlib import Path
import timeit
import sys


def _build_bad_char_table(pattern: str) -> Dict[str, int]:
    """
    Constructs the Bad Character Shift Table
    """
    table = {}
    length = len(pattern)
    # shift = len(pattern) - index - 1
    # do not include the last character
    for i in range(length - 1):
        table[pattern[i]] = length - 1 - i

    return table


def boyer_moore_search(text: str, pattern: str) -> int:
    """
    Performs string searching using the Boyer-Moore-Horspool algorithm
    Time Complexity: Average O(N), Worst Case O(N*M)
    """
    n = len(text)
    m = len(pattern)
    if m > n:
        return -1

    shift_table = _build_bad_char_table(pattern)
    i = m - 1  # align the end of pattern with text

    while i < n:
        k = 0
        # compare characters from right to left
        while k < m and pattern[m - 1 - k] == text[i - k]:
            k += 1

        if k == m:
            return i - m + 1  # match found
        else:
            shift = shift_table.get(text[i], m)  # shift logic
            i += shift

    return -1


def _compute_lps_array(pattern: str) -> List[int]:
    """
    Computes the Longest Prefix Suffix (LPS) array
    lps[i] stores the length of the longest proper prefix of pattern[0..i]
    that is also a suffix of pattern[0..i]
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # fall back to the previous LPS length
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str) -> int:
    """
    Performs KMP search to find a pattern in a text
    Time Complexity: O(N + M)
    """
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    lps = _compute_lps_array(pattern)
    i = 0  # text index
    j = 0  # pattern index

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1


def rabin_karp_search(text: str, pattern: str) -> int:
    """
    Rabin-Karp algorithm using a rolling hash
    Time Complexity: Average O(N+M), Worst Case O(N*M)
    """
    n = len(text)
    m = len(pattern)
    if m > n:
        return -1

    base = 256  # constants for hashing
    modulus = 101  # 10**9 + 7
    pattern_hash = 0
    text_hash = 0
    h = 1

    # precompute (base^(m-1)) % modulus
    # the value of the most significant digit
    for _ in range(m - 1):
        h = (h * base) % modulus

    # initial hash values for pattern and first window of text
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % modulus
        text_hash = (base * text_hash + ord(text[i])) % modulus

    # slide the window over text
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            # check characters one by one to avoid collision issues
            if text[i: i + m] == pattern:
                return i

        # hash for next window
        if i < n - m:
            # remove leading character
            text_hash = (text_hash - ord(text[i]) * h) % modulus            
            # since subtraction might make it negative, add modulus
            if text_hash < 0:
                text_hash += modulus                
            # shift left and add new trailing character
            text_hash = (text_hash * base + ord(text[i + m])) % modulus

    return -1


def read_file(filename: str) -> str:
    """
    Reads a file from the current directory or the script's directory
    Exits the program if the file cannot be found
    """
    path = Path(filename)
    if not path.exists():
        path = Path(__file__).parent / filename

    if not path.exists():
        print(f"Error: File '{filename}' not found.")
        print(f"Searched in: {Path.cwd()} and {Path(__file__).parent}")
        sys.exit(1)

    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Error reading file {filename}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    article1 = read_file("article1.txt")
    article2 = read_file("article2.txt")

    fake_text = "NON_EXISTING_TEST_PATTERN"
    article1_real = "логарифмічний пошук"
    article2_real = "наведено результати"

    algorithms = [
        ("Boyer-Moore", boyer_moore_search),
        ("KMP", kmp_search),
        ("Rabin-Karp", rabin_karp_search)
    ]

    print(f"\n{'Algorithm':<15} | {'Article':<10} | {'Pattern Type':<12} | {'Time (sec)':<10}")
    print("-" * 60)
    for algo_name, algo_func in algorithms:
        t1_real = timeit.timeit(lambda: algo_func(article1, article1_real), number=100)
        t1_fake = timeit.timeit(lambda: algo_func(article1, fake_text), number=100)
        t2_real = timeit.timeit(lambda: algo_func(article2, article2_real), number=100)
        t2_fake = timeit.timeit(lambda: algo_func(article2, fake_text), number=100)

        print(f"{algo_name:<15} | Article 1  | Real         | {t1_real:.5f}")
        print(f"{algo_name:<15} | Article 1  | Fake         | {t1_fake:.5f}")
        print(f"{algo_name:<15} | Article 2  | Real         | {t2_real:.5f}")
        print(f"{algo_name:<15} | Article 2  | Fake         | {t2_fake:.5f}")
        print("-" * 60)
