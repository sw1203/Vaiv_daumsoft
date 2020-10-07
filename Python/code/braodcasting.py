import numpy as np

# broadcasting 예시 1
a = np.array([[10], [20], [30], [40]])
b = np.array([1, 2, 30])
print(a + b)
print()

# broadcasting 예시 2
array3d = np.array([[[0, 1], [2, 3], [4, 5], [6, 7]],
                    [[8, 9], [10, 11], [12, 13], [14, 15]],
                    [[16, 17], [18, 19], [20, 21], [22, 23]]])

print('array3d')
print(array3d)
print()

array2d = np.array([[0, 1], [2, 3], [4, 5], [6, 7]])

print('array2d')
print(array2d)
print()

print(array3d + array2d)
