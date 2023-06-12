"""
This code can be used to remove the low temperature region of EOS files written in the .cn4 format
"""

import re

import numpy as np

"""
file_in = "initial_file.cn4"
file_out = "modified_file.cn4"
minimum_temp_eV = 0.1

ionmix = parse_ionmix4(file_in)
ionmix.parse_metadata()
ionmix.parse_tables()
ionmix.set_minimum_temperature(minimum_temp_eV)
ionmix.output_to_file(file_out)

# you can plot some info here 
for key in ['zbar', 'pion', 'pele', 'eint_ele', 'eint_ion']:
    fig, ax = plt.subplots()
    im = ax.plot(ionmix.temp, ionmix.tables[key].min(axis=0))
    ax.set(xlabel='temp_eV', ylabel=key)
    ax.set_xscale('symlog', linthresh=ionmix.temp[1])
    ax.set_yscale('log')
"""


def chunkstring(string, length):
    return re.findall(".{%d}" % length, string)


class parse_ionmix4:
    def __init__(self, f):
        #
        with open(f, "r") as fp:
            self.filelines = fp.readlines()
        print(f)
        self.char_per_float = 12

        # note flash only reads
        # zbar, pion, pele, eint_ele, eint_ion
        self.table_types = [
            "zbar",
            "dz_dte",
            "pion",
            "pele",
            "dpion_dtion",
            "dpele_dtele",
            "eint_ion",
            "eint_ele",
            "dion_eint_dtion",
            "dele_eint_dtele",
            "dion_eint_dnion",
            "dele_eint_dnion",
        ]

    def parse_metadata(self):
        # parse meta data (i.e. 1st 4 lines of the file
        self.metadata = self.filelines[:4]
        self.ntemp = int(self.metadata[0][:10])
        self.ndens = int(self.metadata[0][10:20])

    def adjust_metadata(self):
        # replace the number of temperature and density entries
        line0 = f"{self.ntemp:>10}{self.ndens:>10}\n"
        self.metadata[0] = line0

    def parse_tables(self):
        self.flattened_tables_str = "".join(l.strip() for l in self.filelines[4:])

        nstart = 0

        # get temperature array
        temps = self.flattened_tables_str[
            nstart : nstart + self.char_per_float * self.ntemp
        ]
        temps = chunkstring(temps, 12)
        self.temp = np.array(temps, dtype="float")
        nstart += self.char_per_float * self.ntemp

        # get number densities
        dens = self.flattened_tables_str[
            nstart : nstart + self.char_per_float * self.ndens
        ]
        dens = chunkstring(dens, 12)
        self.dens = np.array(dens, dtype="float")
        nstart += self.char_per_float * self.ndens

        # get many grids
        self.tables = {}
        for tt in self.table_types:
            out = self.flattened_tables_str[
                nstart : nstart + self.char_per_float * self.ndens * self.ntemp
            ]
            out = chunkstring(out, 12)
            out = np.array(out, dtype="float")
            self.tables[tt] = out.reshape(self.ndens, self.ntemp).copy()
            nstart += self.char_per_float * self.ndens * self.ntemp

    def set_minimum_temperature(self, min_temp):
        # get index corresponding to the cutoff temperature
        min_idx = np.arange(self.ntemp)[self.temp >= min_temp][0]
        self.temp = self.temp[min_idx:]
        self.ntemp = self.temp.size

        # Slice the table to remove the low temperatures
        for tt in self.table_types:
            self.tables[tt] = self.tables[tt][:, min_idx:]
        # correct the details of the metadata
        self.adjust_metadata()

    def output_to_file(self: object, filename: str):
        # open the output file
        with open(filename, "w") as fp:
            fp.writelines(self.metadata)

            # now need to write the tables
            for tt in self.table_types:
                # some formatting to make it look like a cn4 file
                out = np.char.mod("%.6E", self.tables[tt].flatten())
                out = [
                    "".join(out[i * 4 : (i + 1) * 4]) + "\n"
                    for i in range(int(out.size / 4) + 1)
                ]
                if len(out[-1].strip()) == 0:
                    out.pop()
                fp.writelines(out)
