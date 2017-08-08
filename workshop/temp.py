import numpy as np
import matplotlib.pyplot as plt

def make_img_from_data(data, offset_xy, fig_number=1):
    fig.add_axes([0+offset_xy[0], 0+offset_xy[1], 0.5, 0.5])
    plt.imshow(data)

# creation of a dictionary with of 4 2D numpy array
# and corresponding offsets (x, y)

# offsets for the 4 2D numpy arrays
offset_a_x = 0
offset_a_y = 0
offset_b_x = 0.5
offset_b_y = 0
offset_c_x = 0
offset_c_y = 0.5
offset_d_x = 0.5
offset_d_y = 0.5

data_list = ['a', 'b', 'c', 'd']
offsets_list = [[offset_a_x, offset_a_y], [offset_b_x, offset_b_y],
                [offset_c_x, offset_c_y], [offset_d_x, offset_d_y]]

# dictionary of the data and offsets
data_dict = {f: [np.random.rand(12, 12), values] for f,values in zip(data_list, offsets_list)}

fig = plt.figure(1, figsize=(6,6))

for n in data_dict:
    make_img_from_data(data_dict[n][0], data_dict[n][1])

plt.show()