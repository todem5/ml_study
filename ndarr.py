# coding: utf-8
# Демонстрация работы с массивами в NumPy
# In[224]:

import numpy as np # ndarray
data1 = [6, 7.5, 8, 0, 1] # python array
arr1 = np.array(data1)

data2 = [[1,2,3,4,5], [6,7,8,9,0]]
arr2= np.array(data2, dtype=np.float64)
arr2

# dtype # shape #ndim
#arr2.dtype
#arr2.ndim
#arr2.shape



# # РћРїРµСЂР°С†РёРё РЅР°Рґ РјР°СЃСЃРёРІР°РјРё

# In[225]:

arr2*arr2


# In[226]:

arr2+5


# In[227]:




# In[228]:

arr = np.arange(10)
arr


# In[229]:

arr[5]
arr[5:8]


# In[230]:

arr[0:8]


# In[231]:


arr


# In[232]:

arr_slice = arr[5:8] 
arr_slice[1] = 12345
arr_slice.shape




# In[233]:

arr2d = np.array([[1,2,3], [4,5,6], [7,8,9]])
arr2d


# In[234]:

arr2d[:,2]


# In[235]:

arr2d[0][2] # arr2d[0,2]


# In[236]:

arr3d = np.array([[[1,2,3], [4,5,6]], [[7,8,9], [10,11,12]]])
arr3d
                  


# In[237]:

arr3d[0]


# In[238]:

arr3d[1]


# In[239]:

old_values = arr3d[0].copy()
arr3d[0] = -1
arr3d[0] = old_values
arr3d


# In[240]:

arr2d


# In[241]:

arr2d[:2,:]


# In[242]:

arr2d[:2, 1:]


# In[243]:

arr2d[2] # arr2d[2, :]   #arr2d[2:, :]


# In[244]:

arr2d[1,:2] #arr2d[1:2, :2]


# In[245]:

arr2d[1:2, :2]


# In[246]:


names = np.array(['Bob', 'Alice', 'Will', 'Bob', 'Joe', 'Will', 'Bob'])
data = np.random.rand(7,4)
data
names == 'Bob'


# In[247]:

data[names=='Bob', :]


# In[248]:

data[names=='Bob', 2:]


# In[249]:

mask = (names=='Bob') | (names=='Will') # or /// and
data[mask]


# In[250]:

data[data <0.5] = 7


# In[251]:

data


# In[258]:

## fancy indexing 
arr = np.empty((8,4)) # 
arr[:,:] = 0
arr

for i in range(8):
    arr[i] = i

print(arr)
arr[[4,3,0,6]]
#arr[[-3,-5,-7]]
