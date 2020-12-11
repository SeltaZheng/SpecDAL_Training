import glob, os
import pandas as pd
import numpy as np
from specdal import Collection, Spectrum, filters, readers




# Directories:
dir_in = r'Z:\townsenduser-rw\projects\ABoVE\ground_data\2019\dry_data\dry_spec'
spec_out = r'Z:\townsenduser-rw\projects\ABoVE\ground_data\2019\spec_process' + '/Above_dry_spec_2019.csv'



# DATA Type

type = 'asd'

# Dry spectra or not
dry = True
fresh = not dry
# Interpolation tag:
interp = False

# collection name
fn = 'test'

# meta list
meta = []

# create a collection
c = Collection(name=fn)
spec_ls = glob.glob(dir_in + '/**/*.' + type, recursive=True)
spec_ls.sort()

for f in spec_ls:
    spec = Spectrum(filepath=f)
    c.append(spec)
    meta.append(os.path.basename(os.path.dirname(f)))


# perform jump correction for the collection
if type =='asd':
    c.jump_correct(splices=[1000, 1800], reference=0)

if interp:
    c.interpolate(spacing=1)

if dry:
    c, name_new = filters.filter_white(c)
# plot the collection
c.plot(legend = False, ylim = (0,1))

spec_data = c.data
spec_data = spec_data.T
spec_data.insert(loc=0, column='ExtraMeta', value=meta)
if fresh:
    # Filter the white panel data/ dark current data

    temp = spec_data.iloc[:, 1:].values
    temp = np.sum(temp, axis=1)
    index = (temp >= 100) & (temp < 900)
    spec_data = spec_data.iloc[index, ]



spec_data.to_csv(spec_out)











