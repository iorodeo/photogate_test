#!/usr/bin/env python
import sys
import scipy
import pylab

def get_period(file_name,print_info=False, plot_data=False):
    """
    Compute the period of the pendulum from the data file
    """
    data_vals = load_data(file_name)
    pend_len, time_vals, sens_vals = data_vals

    # Compute values for threshold and hysteresis
    threshold = get_threshold(data_vals)
    hysteresis = get_hysteresis(data_vals)
    
    # Find high-to-low and low-to-high transistions
    high2low, low2high = get_transitions(data_vals,threshold,hysteresis)
    
    # Interpolate transisitons to get crossing times
    t_high2low_cross = interp_transitions(high2low,threshold)
    t_low2high_cross = interp_transitions(low2high,threshold)
    
    # Compute period from crossing time
    period_high2low = get_period_from_times(t_high2low_cross)
    period_low2high = get_period_from_times(t_low2high_cross)
    period = 0.5*(period_high2low + period_low2high)

    if print_info:
        pend_len, time_vals, sens_vals = data_vals
        sample_rate = 1.0/(time_vals[1] - time_vals[0])
        print file_name
        print '  pendulum length:  %1.3f'%(pend_len,)
        print '  number of points: %d'%(time_vals.shape[0],)
        print '  sample rate:      %1.1f'%(sample_rate,)
        print '  period:           %1.3f'%(period,)
    
    if plot_data:
        plot_raw_data(data_vals,threshold)
        plot_trans_pairs(high2low,'r')
        plot_trans_pairs(low2high,'b')
        plot_crossings(t_high2low_cross, threshold, 'r')
        plot_crossings(t_low2high_cross, threshold, 'b')
        pylab.show()

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

def get_hysteresis(data_vals):
    """
    Find a reasonable value to use for the hystersis
    """
    pend_len, time_vals, sens_vals = data_vals
    diff_sens_vals = sens_vals[1:] - sens_vals[:-1]
    max_diff = diff_sens_vals.max()
    hysteresis = 0.5*max_diff
    return hysteresis 

def get_transitions(data_vals, threshold, hysteresis):
    """
    Find the high-to-low and low-to-high state transistions
    """
    pend_len, time_vals, sens_vals = data_vals


    # Get initial state
    if sens_vals[0] > threshold:
        state = 'high'
    else:
        state = 'low'

    # Find state changes
    high2low = []
    low2high = []
    for i in range(1,time_vals.shape[0]):
        if state == 'high':
            if sens_vals[i] < (threshold - 0.5*hysteresis):
                # This is a high to low transition
                state = 'low'
                # Find last point above threshold
                n = i-1
                while  sens_vals[n] < threshold:
                    n -= 1
                # Save crossing points
                pt_below = (time_vals[i], sens_vals[i])
                pt_above = (time_vals[n], sens_vals[n])
                high2low.append((pt_above, pt_below))
        else:
            if sens_vals[i] > (threshold + 0.5*hysteresis):
                # This is a low to high transistion
                state = 'high'
                # Find last point below threshold
                n = i-1
                while sens_vals[n] > threshold:
                    n -= 1
                # Save crossing points
                pt_above = (time_vals[i], sens_vals[i])
                pt_below = (time_vals[n], sens_vals[n])
                low2high.append((pt_below,pt_above))

    return high2low, low2high

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

def plot_raw_data(data_vals, threshold):
    """
    Plots the data values
    """
    pend_len, time_vals, sens_vals = data_vals
    pylab.plot(time_vals, sens_vals, 'k')
    pylab.plot([time_vals[0], time_vals[-1]], [threshold, threshold],':k')
    pylab.xlabel('time (sec)')
    pylab.ylabel('photogate (V)')

def plot_trans_pairs(trans_list, color):
    """
    Plots high-to-low and low-to-high transistion values
    """
    for p0, p1 in trans_list:
        t0,v0 = p0
        t1,v1 = p1
        pylab.plot(t0,v0,'x'+color)
        pylab.plot(t1,v1,'x'+color)

def plot_crossings(t_cross_vals, threshold, color):
    """
    Plot threshold crossing times
    """
    for t in t_cross_vals:
        pylab.plot(t,threshold, 'o' + color)

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    file_name = sys.argv[1]
    get_period(file_name,print_info=True,plot_data=True)
    












