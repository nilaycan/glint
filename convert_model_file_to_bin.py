from numpy import array, delete, where, in1d
from pickle import dump

"""
This script is not for glint users but for the SW developers.
It does the preprocessing for prediction of methylation level by SNPs.

*** This is not the final version of the script ***
The final script was deleted by mistake... this is not the version that was used in the last (and first) version of the software.
But this script is close to the final one and by lokking at the output files you can rewrite it if needed.
The only reasons I can think of for you to need this script are:
- if you have different model file than the one we used for the last version.
- if you need to extract more data than we already extracted.

The output files of the deleted scripts are
    - "sites_ids_list" a list of cpgs (that can be explained by SNPs), which describes the cpgs IDs: the id of the cpg name at line number i is i.
    - "snps_ids_list"  a list of SNPs descibing their ids:  the id of the SNP at line number i is i.
    - "site_snps_list" which describe for each site the snps that "explain" it. the numbers in the i'th line are the ids of the snps descibe the site which is is i.
    - "sites_scores_list" the score at the i'th line is the predictions correlation of i'th site (site which id is i)
    - "sites_snps_coeff_list" the numbers at the i'th line are the coefficients of the snps which "explain" the i'th site. the j'th number is the coefficient of the j'th snp at the i'th i in the file "site_snps_list"

Note: I decided to save lists and not pickles after comparing the runtime of loading both of them. 
"loadtxt" is used for loading lists, and it makes the loading much faster than pickle.

This script parsers the "model"* file, i.e. the file with the coefficients for making methylation predictions from SNPs.
The file is "heavy" and it takes time to read and parse it. So this preprocessing-script does the "hard work",
extracts and saves the relevant information in a way that it will be efficient to get it on "real time".

This script should be executed once, in cases when:

* in this case the "model" file name was KORA_model_multiple_snps_W_50_M_10.
 The structure of the file, culumn by column: 
  cpg id, chromosome num, score (prediction correlation), lasso's lambda, number of predicting SNPs (an integer in the range 1-10),
  the position in basepairs of the predicting SNPs (the average across the predicting SNPs).
  The following columns are triplets, each describing one of the the predicting SNPs of the current cpg. 
  For each predicting SNP we have 3 values: "rs" id (the identifier of the SNP - note that it doesn't always start with "rs"),
  reference allele, coefficient.
"""

KORA_MODEL_FILE_PATH = "/Users/yedidimr/Downloads/KORA_model_multiple_snps_W_50_M_10.txt" # put here the path to this file
BAD_PROBES_FILE_PATH = "parsers/assets/polymorphic_cpgs.2013.txt" # put here the path to the artifacts file
SITE_ID_INDEX = 0
PREDICTION_CORRELATION_SCORE_INDEX = 2
NUMBER_OF_PREDICTIONG_SNPS_INDEX = 4
FIRST_SNP_INDEX = 6

data = file(KORA_MODEL_FILE_PATH, 'r').read()
print 1
artifacts = array(file(BAD_PROBES_FILE_PATH, 'r').read().splitlines())
print 2
sites = data.splitlines()
sites_names = array([site.split('\t')[0] for site in sites])
print 3
# remove artifacts
sites_indices_to_remove = where(in1d(sites_names , artifacts))[0]
print sites[sites_indices_to_remove[0]] in artifacts
# sites_indices_to_remove = [i for i in range(len(sites_names)) if sites_names[i] in artifacts]
sites = array(sites)
keep_sites = delete(sites, sites_indices_to_remove)
print 4
sites_ids = []
snps_ids = []
sites_scores = []
current_site_snps_list = []
sites_snps_list = []
current_site_coeffs_list = []
sites_coeffs_list = []
current_snp_index = 0
print "Parsing data... this gonna take some time..."
#extract the relevant information - non-artifacts cpgs, the coefficient, the alleles...
# snps_info = dict()
# sites_info = dict()
for site in keep_sites:
    site_info = site.split('\t')
    site_id = site_info[SITE_ID_INDEX]
    site_score = site_info[PREDICTION_CORRELATION_SCORE_INDEX]
    # number_of_predictors = int(site_info[NUMBER_OF_PREDICTIONG_SNPS_INDEX])
    # # site_snps_list = []
    # current_site_snps_list = []
    # current_site_coeffs_list = []
    # for i in range(number_of_predictors):
    #     snp_id = site_info[FIRST_SNP_INDEX + i*3]
    #     # allele = site_info[FIRST_SNP_INDEX + i*3 + 1]
    #     coeff = float(site_info[FIRST_SNP_INDEX + i*3 + 2])
        
    #     if snp_id not in snps_ids:
    #         snps_ids.append(snp_id)
    #         snp_index = current_snp_index
    #         current_snp_index += 1
    #     else:
    #         snp_index = snps_ids.index(snp_id)

    #     current_site_snps_list.append(str(snp_index))
    #     current_site_coeffs_list.append(str(coeff))
    #     # site_snps_list.append(snp_id)
    #     # if snp_id not in snps_info:
    #     #     snps_info[snp_id] = [(site_id, allele, coeff)]
    #     # else:
    #     #     snps_info[snp_id].append((site_id, allele, coeff))
        
        
    
    # # sites_info[site_id] = (site_score, number_of_predictors, site_snps_list) #TODO remove unneccecery site_snps_list
    # sites_ids.append(site_id)
    sites_scores.append(str(site_score))
    # sites_snps_list.append("\t".join(current_site_snps_list))
    # sites_coeffs_list.append("\t".join(current_site_coeffs_list))

# #
# with open("sites_snps_coeff_list", 'wb') as f1:
#     f1.write("\n".join(sites_coeffs_list))
# f1.close()

# with open("site_snps_list", 'wb') as f1:
#     f1.write("\n".join(sites_snps_list))
# f1.close()


with open("sites_scores_list", 'wb') as f1:
    f1.write("\n".join(sites_scores))
f1.close()

# with open("sites_ids_list", 'wb') as f1:
#     f1.write("\n".join(sites_ids))
# f1.close()

# with open("snps_ids_list", 'wb') as f1:
#     f1.write("\n".join(snps_ids))
# f1.close()