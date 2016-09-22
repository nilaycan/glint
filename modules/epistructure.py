from module import Module
from utils import pca
from numpy import savetxt
import logging

class Epistructure(Module):
    EPISTRUCTURE_FILE_SUFFIX = ".epistructure.txt"

    def __init__(self, meth_data, informative_list):
        """
        informative_list - list of sites (cpgnames) to use 
        meth_data - MethylationData object with data of m sites X  n samples
        """
        self.informative_sites = informative_list
        self.meth_data = meth_data

    def capture_ancestry(self, num_of_pcs = 2, covars_to_regress = None, save_file = None):
        logging.info("Running epistructure...")
        logging.info("Removing non-informative sites...")
        self.meth_data.include(self.informative_sites)

        covars = fs_meth_data.get_covariates_subset(covars_to_regress)
        if covars is not None:
            logging.info("regressing out covariates...")
            fs_meth_data.regress_out(covars)
        else:
            logging.info("ignoring covariates")

        logging.info("running PCA...")
        pca_out = pca.PCA(self.meth_data.data.transpose()) # meth_data should be transposed before passing to pca

        if save_file:
            output_filename = save_file + self.EPISTRUCTURE_FILE_SUFFIX
            savetxt(output_filename, pca_out.P[:,range(num_of_pcs)]) # saves it as samples X PCs
            logging.info("first %s PCs are saved to %s" % (num_of_pcs, output_filename))
        

