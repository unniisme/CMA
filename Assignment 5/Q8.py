import numpy as np
from scipy.fft import fft, ifft

def fft_multiply(a, b):
    """
    Compute the product using fft
    """
    # Convert the input integers to numpy arrays
    a = np.array(list(str(a)), dtype=int)
    b = np.array(list(str(b)), dtype=int)

    n = len(a)
    m = len(b)

    # Compute the size of the product array
    size = int(2**np.ceil(np.log2(n + m)))

    # Compute the Fourier transforms of the input arrays
    A = fft(a, size)
    B = fft(b, size)

    # Compute the pointwise product of the Fourier transforms
    C = ifft(A * B)

    # Round the elements of the product array to the nearest integer
    C = np.round(C.real).astype(int)

    # Convert to digits
    carry = 0
    result = []
    for i in range(size):
        temp = C[i] + carry
        carry = temp // 10
        result = [temp % 10] + result

    # Convert the result to a single integer
    return int(''.join(map(str, result)))

if __name__ == '__main__':
    a = 1234567890123456789
    b = 9876543210987654321
    print("Input numbers :\n", a, "\n",  b)
    print("Product using fft: ", fft_multiply(a, b))
    print("Actual product: ", a*b)
