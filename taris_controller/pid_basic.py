def PID(current_val, end_val, sample_time, integral_prev, error_prev):
    """
    PID is a feedback control algorithm that determines the output of a system
    input x(t) to stabilize future outputs x(t+n). This allows for regulated
    pulse width modulation (PWM) for "locking" a system to a desired value.

    :param current_val: current input value
    :param end_val: desired system value
    :param sample_time: sampling rate (run PID every x seconds)
    :param integral_prev: previous integral value
    :param error_prev: previous error value
    :return: system value, previous error, integral error
    """
    if current_val != None:
        if integral_prev == None:
            integral_prev = 0.0
            error_prev = 0.0
            current_val = 0.0

        # Gain constants

        kp = 1
        ki = 1
        kd = 1

        # Define parameters for feedback mechanism
    
        error_curr = int(end_val) - int(current_val)
        integral = integral_prev + float(error_curr*sample_time) / ki
        derivative = (error_curr - error_prev)/(sample_time * kd)

        # Compute output from above parameters
        y = kp * (error_curr + integral + derivative)

        error_prev = error_curr
        integral_prev = integral

        return (y, error_prev, integral_prev)
    else:
        return 0