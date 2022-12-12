# NYC_tip_pred
NYC taxi trip prediciton

A tip amount prediction project on the NYC taxi ride dataset. 

Our model considered log and 4th order polynomial features for extra amount and toll amount res that resulted in 0.02 improvement in MSE. 

We also considered temporal dynamics wherein different parameters were alloted to the trip duration based on the hour of the day, which
allowed 0.005 improvement in MSE. 

Scipy’s sparse matrix representation had to be used to perform training and testing.
