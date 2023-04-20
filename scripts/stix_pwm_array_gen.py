# -*- coding: utf-8 -*-
"""
A script that generates a C header file with the static array definitions for
PWM control. Stix Mindfulness uses these arrays to control LED and haptic motor
behavior. Because these arrays are static, their entries should be calculated
and populated at compile time. This script is intended to be run by a makefile
during the firmware build process.

Created on Fri Mar  4 09:26:57 2022

@author: Walter Jacob
"""

import math

def write_header(filename):
    """
    Overwrites any existing file and writes the header.

    Parameters
    ----------
    filename : str
        Name of the output file.

    Returns
    -------
    None.

    """
    with open(filename, "w") as o:
        o.write("/**\n")
        o.write(" * @addtogroup  Stix Stix custom drivers/libraries\n")
        o.write(" * @defgroup    PWM  PWM control arrays\n")
        o.write(" * @ingroup     Stix\n")
        o.write(" * @{\n")
        o.write(" *\n")
        o.write(" * @file    pwm_arrays.h\n")
        o.write(" * @author  Walter Jacob - Overkill Projects, LLC.\n")
        o.write(" * @date    2022\n")
        o.write(" * \n")
        o.write(" * @brief   PWM control arrays\n")
        o.write(" *\n")
        o.write(" * @details This file contains the arrays that are used by the PWM peripheral\n")
        o.write(" *          to drive the LEDs and haptic motor. The arrays are automatically\n")
        o.write(" *          generated by a python script. See the documentation/makefile for\n")
        o.write(" *          more information.\n")
        o.write(" *          \n")
        o.write(" *          DO NOT EDIT THIS FILE DIRECTLY!!!!!!!!!!!!! - W.J.\n")
        o.write(" */\n\n")
        o.write("#ifndef PWM_H__\n")
        o.write("#define PWM_H__\n\n")
        o.write("#pragma GCC diagnostic push\n")
        o.write("#pragma GCC diagnostic ignored \"-Wunused-variable\"\n\n")
        o.write("#ifdef __cplusplus\n")
        o.write("extern \"C\" {\n")
        o.write("#endif\n\n")
        o.write("#include <stdint.h>\n\n")
        

def write_footer(filename):
    """
    Appends the footer to the file.

    Parameters
    ----------
    filename : str
        Name of the output file.

    Returns
    -------
    None.

    """
    with open(filename, "a") as o:
        o.write("/** @} */\n")
        o.write("#ifdef __cplusplus\n")
        o.write("}\n")
        o.write("#endif\n\n")
        o.write("#endif /* LEDS_H__ */\n")
    
def add_breath(filename, name, countertop):
    '''
    Add an array for a breath-shaped pulse with 'name' and period determined
    by countertop. Time for a pulse period is given by
    
    0.00003259 x^2 - 0.000445 x + 0.08340
    
    where x = countertop.

    Parameters
    ----------
    filename : str
        Name of the output file.
    name : str
        String used in the array names.
    countertop : int
        Top count for PWM.

    Returns
    -------
    None.

    '''
    breath_array = []

    def fn(x, a, b, j):
        return (a * (j - 1) / j) * (1 - math.sqrt((1 + b**2) / (1 + b**2 * (math.cos(x * math.pi / a))**2)) * math.cos(x * math.pi / a)) / 2

    for k in range(countertop):
        breath_array.append(round(fn(k, countertop, 3, 17))) #first numerical value is proportional to flatness at the top, second value is how low it goes

    with open(filename, "a") as o:
        o.write('#define PWM_LEDS_PULSE_{}_COUNTERTOP {}\n'.format(name.upper(), countertop))
        o.write('static uint16_t m_pwm_seq_pulse_{}_up[] = {{ '.format(name))
        o.write(', '.join(str(e) for e in reversed(breath_array)))
        o.write(' };\n')
        o.write('static uint16_t m_pwm_seq_pulse_{}_down[] = {{ '.format(name))
        o.write(', '.join(str(e) for e in breath_array))
        o.write(' };\n\n')


def add_pulse(filename, name, countertop):
    '''
    Add an array for a pulse with 'name' and period determined by countertop.
    Time for a pulse period is given by
    
    0.00003259 x^2 - 0.000445 x + 0.08340
    
    where x = countertop.

    Parameters
    ----------
    filename : str
        Name of the output file.
    name : str
        String used in the array names.
    countertop : int
        Top count for PWM.

    Returns
    -------
    None.

    '''
    with open(filename, "a") as o:
        o.write('#define PWM_LEDS_PULSE_{}_COUNTERTOP {}\n'.format(name.upper(), countertop))
        o.write('static uint16_t m_pwm_seq_pulse_{}_up[] = {{ '.format(name))
        o.write(', '.join(str(e) for e in make_array(countertop, "up", "pulse")))
        o.write(' };\n')
        o.write('static uint16_t m_pwm_seq_pulse_{}_down[] = {{ '.format(name))
        o.write(', '.join(str(e) for e in make_array(countertop, "down", "pulse")))
        o.write(' };\n\n')
        
def add_duty(filename, name, strength):
    """
    Add an array for LED/haptic 'on' (duty cycle) with 'name' and
    brightness/power determined by strength.

    Parameters
    ----------
    filename : str
        Name of the output file.
    name : str
        String used in the array names.
    strength : int
        Integer that determines output strength.

    Returns
    -------
    None.

    """
    strength_list = [strength for i in range(12)]
    with open(filename, "a") as o:
        o.write('static uint16_t m_pwm_seq_{}[] = {{ '.format(name))
        o.write(', '.join(str(e) for e in strength_list))
        o.write(' };\n\n')
        
def add_adv(filename):
    """
    Add an array for advertising pulse.

    Parameters
    ----------
    filename : str
        Name of the output file.

    Returns
    -------
    None.

    """
    with open(filename, "a") as o:
        o.write('#define PWM_LEDS_ADV_COUNTERTOP 180\n')
        o.write('#define PWM_LEDS_ADV_COUNT_UP_LEN 30\n')
        o.write('#define PWM_LEDS_ADV_COUNT_DOWN_LEN 180\n')
        o.write('static uint16_t m_pwm_seq_adv_up[] = { ')
        o.write(', '.join(str(e) for e in make_array(30, "up", "adv")))
        o.write(' };\n')
        o.write('static uint16_t m_pwm_seq_adv_down[] = { ')
        o.write(', '.join(str(e) for e in make_array(180, "down", "adv")))
        o.write(' };\n\n')
        
def adv_curve_up(x, a):
    """
    Curve for advertising, increasing brightness. Uses pulse curve.

    Parameters
    ----------
    x : int
        Domain.
    a : int
        Scaling/countertop parameter.

    Returns
    -------
    int
        Rounded image of shaping function.

    """
    return pulse_curve(x, a)

def adv_curve_down(x, a):
    """
    Curve for advertising, decreasing brightness. Uses breath curve, down
    direction.

    Parameters
    ----------
    x : int
        Domain.
    a : int
        Scaling/countertop parameter.

    Returns
    -------
    int
        Rounded image of shaping function.

    """
    return breath_curve_down(x, a)
    
def pulse_curve(x, a):
    """
    Map input value to the shaping function. This function is given by
    
    f(x) = (x/a)^2 / (2(x/a)^2 - 2(x/a) + 1) 
    
    which is a scaled form of (2x - 1)/(1 + (2x - 1)^2) + 1/2
    which itself is a translated and scaled approximation to arctan.

    Parameters
    ----------
    x : int
        Domain.
    a : int
        Scaling/countertop parameter.

    Returns
    -------
    int
        Rounded image of shaping function.

    """
    x_scaled = x / a
    return round((a * ((x_scaled)**2 / (2 * (x_scaled)**2 - 2 * (x_scaled) + 1))))

def breath_curve_up(x, a):
    """
    Curve modeling inhaling. Same curve as pulse.

    Parameters
    ----------
    x : int
        Domain.
    a : int
        Scaling/countertop parameter.

    Returns
    -------
    int
        Rounded image of shaping function.

    """
    return pulse_curve(x, a)


def breath_curve_down(x, a):
    """
    Curve modeling exhaling. Given by
    
    a (1 - \frac{1}{e^{9x / a}})
    
    which descends a little more rapidly than the pulse curve.

    Parameters
    ----------
    x : int
        Domain.
    a : int
        Scaling/countertop parameter.

    Returns
    -------
    int
        Rounded image of shaping function.

    """
    return round(a - a * math.exp(-9 * x / a))

def make_array(countertop, list_dir, use):
    """
    Creates an array of PWM values given a PWM top count. Check the mapping
    function for details.

    Parameters
    ----------
    countertop : int
        PWN top count.
    list_dir : str
        Indicate whether the array counts up or down.
    use : str
        String describing the type of curve to produce.

    Returns
    -------
    output : list of int
        List containing mapped PWM values.

    """
    output = []
    map_fn = None
    domain_map = lambda x : x
    
    if use == "breath":
        if list_dir == "up":
            map_fn = breath_curve_up
            domain_map = lambda x : countertop - x
        else:
            map_fn = breath_curve_down
    elif use == "adv":
        if list_dir == "up":
            map_fn = adv_curve_up
            domain_map = lambda x : countertop - x
        else:
            map_fn = adv_curve_down
    else:
        map_fn = pulse_curve
        if list_dir == "up":
            domain_map = lambda x : countertop - x
            
    for i in range(countertop):
        output.append(map_fn(domain_map(i), countertop))
            
    return output

def add_rainbow(filename, a):
    """
    Creates arrays of sine waves for rainbow pulsing.

    Parameters
    ----------
    filename : str
        Name of the output file.
    a : int
        PWN top count.

    Returns
    -------
    None.

    """
    arr_blue = []
    arr_green = []
    arr_red = []

    for k in range(a):
        arr_blue.append(round((a * (math.sin(k * 2 * math.pi / a) + 1)) / 2))
        arr_green.append(round((a * (math.sin(math.pi * 2 / 3 + (k * 2 * math.pi / a)) + 1)) / 2))
        arr_red.append(round((a * (math.sin(math.pi * 4 / 3 + (k * 2 * math.pi / a)) + 1)) / 2))

    with open(filename, "a") as o:
        o.write('#define PWM_LEDS_RAINBOW_COUNTERTOP ' + str(a) + '\n')
        o.write('#define PWM_LEDS_RAINBOW_LEN ' + str(a) + '\n')
        o.write('static uint16_t m_pwm_seq_rbow_blue[] = { ')
        o.write(', '.join(str(e) for e in arr_blue))
        o.write(' };\n')
        o.write('static uint16_t m_pwm_seq_rbow_green[] = { ')
        o.write(', '.join(str(e) for e in arr_green))
        o.write(' };\n')
        o.write('static uint16_t m_pwm_seq_rbow_red[] = { ')
        o.write(', '.join(str(e) for e in arr_red))
        o.write(' };\n')

##################################
#          Begin script          #
##################################
#file = "../pca10056/s140/ses/stix_libs/pwm_arrays.h"
file = "../stix_libs/pwm_arrays.h"

write_header(file)

add_adv(file)

add_pulse(file, "slow", 270)
add_pulse(file, "medium", 180)
add_pulse(file, "fast", 90)
#add_breath(file, "deep_breath", 612) # ~12s = 612
add_breath(file, "deep_breath", 480) # ~12s = 612

add_duty(file, "high", 2)
add_duty(file, "medium", 6)
add_duty(file, "low", 10)

add_rainbow(file, 600)

write_footer(file)
##################################
#           End script           #
##################################










