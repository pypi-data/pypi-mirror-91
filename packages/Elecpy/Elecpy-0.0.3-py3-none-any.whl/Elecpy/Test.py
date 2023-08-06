"""
该模块用于测试一些功能
"""
import pandas as pd
import numpy as np
from Analysis import *
import copy
from math import *
from sympy import *
import os
from os import startfile
import tkinter as tk
import tkinter.filedialog as fdlg
from tkinter import ttk
import time


if __name__ == '__main__':
    x = [1, 2, 3]
    for idx, elm in enumerate(x):
        x[idx] *= 2
    print(x)
