def nth_root(n, a, ε):
    low = 0 
    high = max(1, a) 
    while high - low > ε: 
        mid = (low + high) / 2 
        if mid**n < a: 
            low = mid
        else: 
            high = mid
    return high
    
    
if __name__ == '__main__':
    print("Case 1:")
    result = nth_root(2, 25, 0.001)
    assert abs(result - 5) < 0.001
    print("Expected: 5, result:", result)

    print("Case 2:")
    result = nth_root(3, 27, 0.01)
    assert abs(result - 3) < 0.01
    print("Expected: 3, result:", result)

    print("Case 3:")
    result = nth_root(4, 16, 0.1)
    assert abs(result - 2) < 0.1
    print("Expected: 2, result:", result)

    print("Case 4:")
    result = nth_root(2, 100, 0.1)
    assert abs(result - 10) < 0.1
    print("Expected: 10, result:", result)
    
    print("Case 5:")
    result = nth_root(3, 125, 0.0001)
    assert abs(result - 5) < 0.0001
    print("Expected: 5, result:", result)


