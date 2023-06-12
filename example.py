# load libraries
import matplotlib.pyplot as plt

import ionmix4_modifier as im4

plt.style.use("bmh")

file_in = "initial.cn4"
file_out = "finial.cn4"
minimum_temp_eV = 0.05

# ---BELOW DOESN'T NEED MODIFIED---#

ionmix = im4.parse_ionmix4(file_in)
ionmix.parse_metadata()
ionmix.parse_tables()

# you can plot some info here
fig, axes = plt.subplots(3, 2, tight_layout=True, dpi=150, sharex=True)
axes = axes.flatten()
for idx, key in enumerate(["zbar", "pion", "pele", "eint_ele", "eint_ion"]):
    idx += 1
    im = axes[idx].plot(ionmix.temp, ionmix.tables[key].min(axis=0), label="origional")
    axes[idx].set(ylabel=key)
    axes[idx].set_xscale("symlog")
    axes[idx].set_yscale("log")

ionmix.set_minimum_temperature(minimum_temp_eV)
ionmix.output_to_file(file_out)

for idx, key in enumerate(["zbar", "pion", "pele", "eint_ele", "eint_ion"]):
    idx += 1
    im = axes[idx].plot(ionmix.temp, ionmix.tables[key].min(axis=0), label="trimmed")
    axes[idx].set(ylabel=key)
    axes[idx].set_xscale("symlog")
    axes[idx].set_yscale("log")
axes[0].set(yticks=[])
axes[0].grid(False)
fig.supxlabel("Temperature [eV]")
fig.legend(["origional", "modified"], loc="upper left")
fig.suptitle("Minimum table value with temperature")
plt.show()
