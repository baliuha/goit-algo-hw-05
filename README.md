# Substring Search Algorithms Analysis

## Benchmarks
The comparison is based on execution on two different text files. Scenarios tested:
* **Existing Pattern:** A substring that actually exists in the text
* **Fake Pattern:** A substring that does not exist

| Algorithm | Article 1 (Real) | Article 1 (Fake) | Article 2 (Real) | Article 2 (Fake) |
| :--- | :--- | :--- | :--- | :--- |
| **Boyer-Moore** | 0.01344 | 0.01805 | 0.04150 | 0.02253 |
| **KMP** | 0.12838 | 0.35462 | 0.47294 | 0.48143 |
| **Rabin-Karp** | 0.13947 | 0.41352 | 0.43661 | 0.61443 |

*Time is measured in seconds (lower is better).*

## Conclusions

### 1. Boyer-Moore
Boyer-Moore consistently showed the best performance, especially for the Fake text test. This is due to its ability to skip sections of text based on the Bad Character heuristic, whereas KMP and Rabin-Karp process characters more linearly.

### 2. Knuth-Morris-Pratt
KMP performed reliably but generally slower than Boyer-Moore for natural language texts. It is efficient because it avoids backtracking, but it lacks the ability to jump over sections of text like Boyer-Moore.

### 3. Rabin-Karp
Rabin-Karp was generally the slowest in this single-pattern search scenario. In Python, the overhead of calculating rolling hashes and handling modular arithmetic is computationally heavier than the direct character comparisons used by KMP and Boyer-Moore.
