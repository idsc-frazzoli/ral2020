from mcdp_dp import (
    CatalogueDP
)

from mcdp_lang import parse_poset
from mcdp_posets import FiniteCollectionAsSpace, Nat, PosetProduct, Rcomp, RcompUnits

import csv

def CatalogueDPTable(fileName, nF):
    def get_unit(unit_list):
        if len(unit_list) == 1:
            return unit_list[0]

        unit_out = '(' + unit_list[0] + ')'
        for unit in unit_list[1:]:
            unit_out = unit_out + 'x' + '(' + unit + ')'
        return unit_out

    def get_tuple(x):
        if len(x) == 1:
            return x[0]
        else:
            return tuple(x)

    with open(fileName) as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

        # Extract data (first row units, else data)
        units = data[0]
        data = data[1:]

        # Units
        f_unit = get_unit(units[1:1+nF])
        print(f_unit)
        r_unit = get_unit(units[1 + nF:])

        entries = []
        # Entries
        for i in range(len(data)):
            entry = []
            f = []
            r = []
            for j in range(len(data[i])):
                if j == 0:
                    name = str(data[i][j])
                else:
                    value = data[i][j]
                    if units[j].lower() == "nat":
                        value = int(value)
                    elif units[j].lower() == "`timeday":
                        value = value
                    else:
                        value = float(value)
                    if j>=1 and j<1+nF:
                        f.append(value)
                    else:
                        r.append(value)
            entry = (name, get_tuple(f), get_tuple(r))
            entries.append(entry)

            # Implementations
            m = [entry[0] for a in entries]

    M = FiniteCollectionAsSpace(m, T=str)
    F = parse_poset(f_unit)
    R = parse_poset(r_unit)

    return CatalogueDP(F, R, M, entries)