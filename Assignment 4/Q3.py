from Q1 import del_plus, del_minus, del_c, f, f_bar
import numpy as np
import matplotlib.pyplot as plt

H = np.linspace(0,1,100)

e_plus = [abs(f_bar(x) - del_plus(f, x, h))]