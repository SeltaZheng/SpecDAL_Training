import glob, os
import pandas as pd
import numpy as np
from specdal import Collection, Spectrum, filters, readers




# Directories:
dir_in = r'D:\GoogleDrive\OtherRequests\SpecDAL_Training\Sample_Data\fresh_spec'
spec_out = r'D:\GoogleDrive\OtherRequests\SpecDAL_Training\Sample_Data' + '/fresh_test.csv'



# DATA Type

type = 'sed'

# Dry spectra or not
dry = False
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

if fresh:
    # Filter the white panel data/ dark current data
    spec_data.insert(loc=0, column='ExtraMeta', value=meta)
    temp = spec_data.iloc[:, 1:].values
    temp = np.sum(temp, axis=1)
    index = (temp >= 100) & (temp < 900)
    spec_data = spec_data.iloc[index, ]



spec_data.to_csv(spec_out)











