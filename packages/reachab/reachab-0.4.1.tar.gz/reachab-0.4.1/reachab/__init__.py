import logging
import reachab.src.reachability as rb

def test_me():
    obj_reachability = rb.reachability()
    obj_reachability.test_function()

def reach(Omega_0, U, params):
    ##################################
    ## REACHABILITY ANALYSIS PARAMS ##
    ##################################
    ra_params = {
        'T': params['time_horizon'],
        'N': params['steps'],
    }
    erg=[]
    obj_reach = rb.reachability(**ra_params)
    program = ['without_box', 'with_box']
    if (program[0] == params['box_function']):
        R, X = obj_reach.approximate_reachable_set_without_box(Omega_0, U)
    elif (program[1] == params['box_function']):
        R, X = obj_reach.approximate_reachable_set_with_box(Omega_0, U)
    for act_zono in R:
        zonoset = obj_reach.get_points_of_zonotype(act_zono)
        if (params['visualization'] == 'y'):
            obj_reach.obj_visual.filled_polygon(zonoset, 'green', .2)
        erg.append(zonoset)
    if (params['visualization'] == 'y'):
        obj_reach.obj_visual.show()
    return erg


