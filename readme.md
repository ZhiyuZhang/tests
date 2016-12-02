
# test_hist_Gaussian_fit.py: 


测试对一组测量值做直方图，然后对直方图做(高斯)拟合不同方法之间的差别. 

数据 fluxes.dat 就是一组数字，1000个测量值 (期待是normal  distribution, 但因为观测条件不同，所以并不确定). 

使用网上的几种方法分别做测试：

1). http://stackoverflow.com/questions/7805552/fitting-a-histogram-with-python 

2). fitting with user-defined Gaussian faction and fitting.LevMarLSQFitter fitter.

3). use stats.norm.pdf, instead of matlab.normpdf in (1) 

4). mask the outlier (value of ~ 1.43) in the flux.dat and use (3) to fit again. 

# plot_two_axis.py 


画出上下两组非均匀分布的坐标轴，此例采用Y = 1 / X. 常见于频率和波长的换算. 
