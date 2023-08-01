

import numpy as np


h = np.load('skeletonpose1.npy')
print(h.shape)
print(h)
read = np.load('keypoint1.npy')
# for c in range(52):
#     print(c)
#     print(read[c])
print(read.shape)
print(read)