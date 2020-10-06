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
    fn_order = np.zeros((len(array_curves), len(array_curves)))
    fp_order = np.zeros((len(array_curves), len(array_curves)))

    for id_s, s in enumerate(array_curves):
        for id_t, t in enumerate(array_curves):
            order_fn = (s.fn <= t.fn)
            order_fp = (s.fp <= t.fp)
            if np.all(order_fn):
                fn_order[id_s][id_t] = 1
            if np.all(order_fp):
                fp_order[id_s][id_t] = 1
    return fn_order, fp_order

def produce_poset_fn(fn_order, array_curves):
    poset_fn = open("poset_fn.mcdp_poset", 'w')
    poset_fn.write("poset {\n")
    for a in array_curves:
        poset_fn.write(a.sen + ' ')
    poset_fn.write("\n")
    for i in range(len(fn_order)):
        for j in range(len(fn_order)):
            if (i!=j):
                if (fn_order[i][j]):
                    poset_fn.write(array_curves[i].sen + " <= " + array_curves[j].sen + "\n")
    poset_fn.write("}")

def produce_poset_fp(fp_order, array_curves):
    poset_fp = open("poset_fp.mcdp_poset", 'w')
    poset_fp.write("poset {\n")
    for a in array_curves:
        poset_fp.write(a.sen + ' ')
    poset_fp.write("\n")
    for i in range(len(fp_order)):
        for j in range(len(fp_order)):
            if (i != j):
                if (fp_order[i][j]):
                    poset_fp.write(array_curves[i].sen + " <= " + array_curves[j].sen + "\n")
    poset_fp.write("}")



curves_here = get_curves('curves.yaml')
fn, fp = compare_curves(curves_here)
produce_poset_fn(fn, curves_here)
produce_poset_fp(fp, curves_here)

