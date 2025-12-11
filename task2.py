from typing import List, Tuple, Optional


def binary_search_float(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    """
    Performs a binary search on a sorted list of floating-point numbers
    Returns a tuple containing:
        1. The number of iterations performed
        2. The smallest element >= to the target
    """
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] < target:
            # going to the right side
            low = mid + 1
        else:
            # if arr[mid] >= target it may be the upper bound
            upper_bound = arr[mid]
            # continue searching in the left to see if there is a smaller element >= target
            high = mid - 1

    return iterations, upper_bound


if __name__ == "__main__":
    data = [0.1, 0.5, 1.2, 1.8, 2.4, 3.6, 4.8, 5.5, 6.7]
    search_target = 2
    print(f"Data: {data}")
    print(f"Target: {search_target}")

    iter_count, result_custom = binary_search_float(data, search_target)
    print(f"Iterations: {iter_count}")
    print(f"Upper Bound: {result_custom}")
