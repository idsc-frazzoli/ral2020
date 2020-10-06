import yaml
import numpy as np

class curve:
    def __init__(self):
        self.sen = []
        self.fn = []
        self.fp = []

def get_curves(fileName):
    sensor_names = []
    all_curves = []
    with open(fileName) as f:
        sensors_file = yaml.load(f, Loader=yaml.FullLoader)
        for item, doc in sensors_file.items():
            sensor_names.append(item)

        for sensor in sensor_names:
            curves = sensors_file[sensor]
            fn = curves["fn"]
            fp = curves["fp"]
            s = curve()
            s.sen = sensor
            s.fn = fn
            s.fp = fp
            all_curves.append(s)
        #print(sensor_names)
    return all_curves

def compare_curves(array_curves):
    fn_order = fp_order = np.zeros((len(array_curves),len(array_curves)))

    for id_s, s in enumerate(array_curves):
        for id_t, t in enumerate(array_curves):
            order_fn = (s.fn <= t.fn)
            order_fp = (s.fp <= t.fp)
            if np.all(order_fn):
                fn_order[id_s][id_t] = 1.0
            if np.all(order_fp):
                fp_order[id_s][id_t] = 1.0
    return fn_order, fp_order

def produce_poset(fn_order, fp_order,array_curves):
    for i in len(fn_order):
        print(i)
        for j in len(fn_order):
            if (fn_order[i][j]):
                print(array_curves[i].sen, "<=", array_curves[j].sen)
    for i in range(fn_order):
        for j in range(fn_order):
            if (fp_order[i][j]):
                print(array_curves[i].sen, "<=", array_curves[j].sen)




curves_here = get_curves('curves.yaml')
fn, fp = compare_curves(curves_here)
produce_poset(fn, fp, curves_here)

