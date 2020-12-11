import os, glob

dir_in = r'Z:\townsenduser-rw\projects\ABoVE\ground_data\2019\fresh_data\BARR\spectra\BARR_20190718'
sub_ls = glob.glob(dir_in + '/*/')

for sub in sub_ls:
    tag = os.path.basename(os.path.split(sub)[0])
    fn = glob.glob(sub + '*')
    for f in fn:
        f_out = f.replace('_000', '_'+tag+'_000')
        os.rename(f, f_out)