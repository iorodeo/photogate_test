#!/usr/bin/env python
import sys
import scipy
import pylab

def get_period(file_name,print_info=False):
    """
    Compute the period of the pendulum from the data file
    """
    # Load data values from file
    data_vals = load_data(file_name)
    pend_len, time_vals, sens_vals = data_vals

    # Compute value for threshold 
    threshold = get_threshold(data_vals)
    
    # Get list of high-to-low transistion pairs, e.g., ( (t0,v0), (t1,v1 ) such
    # that (t0,v0) is above threshold and (t1,v1) is below threshold.
    trans_pairs = get_transitions(data_vals,threshold)
    
    # Interpolate transisiton pairs to get crossing times
    cross_vals = interp_transitions(trans_pairs,threshold)
    
    # Compute period from crossing time
    period = get_period_from_times(cross_vals)

    # Print info
    if print_info:
        sample_rate = 1.0/(time_vals[1] - time_vals[0])
        print file_name
        print '  pendulum length:  %1.3f'%(pend_len,)
        print '  number of points: %d'%(time_vals.shape[0],)
        print '  sample rate:      %1.1f'%(sample_rate,)
        print '  period:           %1.3f'%(period,)

    # Return data
    return pend_len, period 

def load_data(file_name):
    """
    Load pendulum data from file.
    """
    with open(file_name,'r') as fid:
        # Get pendulum length
        line = fid.readline()
        line = line.split()
        pend_len = float(line[0])
        # Read in time and sensor data points 
        time_vals  = []
        sens_vals = []
        for line in fid.readlines():
            line = line.split()
            time_vals.append(float(line[0]))
            sens_vals.append(float(line[1]))
    # Convert time and sensor values from lists to arrays
    time_vals = scipy.array(time_vals)
    sens_vals = scipy.array(sens_vals)
    return pend_len, time_vals, sens_vals

def get_threshold(data_vals):
    """
    Find a reasonable threshold to use based on the data values
    """
    pend_len, time_vals, sens_vals = data_vals
    max_value = sens_vals.max()
    min_value = sens_vals.min()
    threshold = 0.5*(max_value + min_value)
    return threshold

def get_transitions(data_vals, threshold):
    """
    Find the high-to-low and low-to-high state transistions
    """
    pend_len, time_vals, sens_vals = data_vals

    # Find transistion pairs
    trans_pairs = []
    for i in range(1,time_vals.shape[0]):
        if sens_vals[i-1] >= threshold and sens_vals[i] < threshold:
            before_vals= (time_vals[i-1], sens_vals[i-1])
            after_vals = (time_vals[i], sens_vals[i])
            trans_pairs.append((before_vals, after_vals))
    return trans_pairs 

def interp_transitions(trans_list, threshold):
    """
    Interpolate transistions to find crossing times
    """
    t_cross_vals = []
    for p0, p1 in trans_list:
        t0, v0 = p0
        t1, v1 = p1
        # Get interpolation coeff A*t + B = v
        A = (v1-v0)/(t1-t0)
        B = v0 - A*t0
        # Invert to get crossing time
        t_cross = (threshold - B)/A
        t_cross_vals.append(t_cross)
    return scipy.array(t_cross_vals)

def get_period_from_times(t_cross_vals):
    """
    Compute period from list of high-to-low or low-to-high crossing 
    times
    """
    n = t_cross_vals.shape[0]
    period_vals = scipy.zeros((n-2,)) 
    for i in range(0,n-2):
        period_vals[i] = t_cross_vals[i+2] - t_cross_vals[i]
    period = period_vals.mean()
    return period

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    file_name = sys.argv[1]
    get_period(file_name,print_info=True)
    












