from pathlib import Path
from typing import Union

from Bio.Blast import NCBIWWW
from thoipapy.utils import get_free_space, HardDriveSpaceException
import os
import tarfile
import platform
import time
from time import strftime
from thoipapy.utils import delete_BLAST_xml, make_sure_path_exists


def download_homologues_from_ncbi_mult_prot(s, df_set, logging):
    """Runs download_homologues_from_ncbi for a set of proteins

    Parameters
    ----------
    s : dict
        Settings dictionary
    df_set : pd.DataFrame
        Dataframe containing the list of proteins to process, including their TMD sequences and full-length sequences
        index : range(0, ..)
        columns : ['acc', 'seqlen', 'TMD_start', 'TMD_end', 'tm_surr_left', 'tm_surr_right', 'database',  ....]
    logging : logging.Logger
        Python object with settings for logging to console and file.
    """
    expect_value = s["expect_value"]
    hit_list_size = int(s["hit_list_size"])

    OS_description = platform.system()

    # try to detect if there's not enough HD space for the download.
    # currently not working for
    if "Linux" in OS_description or "Windows" in OS_description:
        try:
            byteformat = "GB"
            data_dir = s["data_dir"]

            size = get_free_space(data_dir, byteformat)
            # logging.info('Hard disk remaining space = {}'.format(size))

            if size[0] < 5:
                raise HardDriveSpaceException(
                    "Hard drive space limit reached, there is only %s %s space left." % (size[0], size[1]))

        # log the exception, so you actually can see what goes on in the logfile
        except HardDriveSpaceException as e:
            logging.critical(e)
            # now stop all processes and raise an error
            raise HardDriveSpaceException("process stopped")
    else:
        logging.warning("Your system does not seem to be Linux or Windows. Harddrive space check not conducted.")

    ##############################################################################################
    #                                                                                            #
    #      download homologues from protein lists file                                           #
    #                                                                                            #
    ##############################################################################################

    for i in df_set.index:
        acc = df_set.loc[i, "acc"]
        TMD_seq_pl_surr = df_set.loc[i, "TMD_seq_pl_surr"]
        # TMD_seq_pl_surr = df_set.loc[i, "full_seq"]
        database = df_set.loc[i, "database"]

        # run online server NCBI blastp with biopython module
        blast_xml_file = os.path.join(s["data_dir"], "homologues", "xml", database, "{}.surr{}.BLAST.xml".format(acc, s["num_of_sur_residues"]))
        xml_tar_gz = blast_xml_file[:-4] + ".xml.tar.gz"
        xml_txt = blast_xml_file[:-4] + "_details.txt"

        if not os.path.isfile(xml_tar_gz):
            run_download = True
        else:
            if s["rerun_existing_blast_results"]:
                run_download = True
                logging.info('{} starting download_homologues_from_ncbi_mult_prot (EXISTING xml.tar.gz FILE WILL BE OVERWRITTEN)'.format(acc))
            elif s["rerun_existing_blast_results"] in [False, 0]:
                run_download = False
                logging.info('{} download_homologues_from_ncbi_mult_prot skipped (EXISTING xml.tar.gz FILE)'.format(acc))
                # skip protein
                continue
            else:
                raise ValueError('s["rerun_existing_blast_results"] does not seem to be True or False')

        if run_download:
            download_homologues_from_ncbi(acc, TMD_seq_pl_surr, blast_xml_file, xml_txt, xml_tar_gz, expect_value, hit_list_size, logging)

    logging.info('homologues download was finished')


def download_homologues_from_ncbi(acc: str, TMD_seq_pl_surr: str, blast_xml_file: Union[Path, str], xml_txt: Union[Path, str], xml_tar_gz: Union[Path, str], expect_value: float, hit_list_size: int, logging, db: str = "nr"):
    """Downloads homologue xml file using NCBI BLAST via the biopython qBLAST wrapper.

    Parameters
    ----------
    acc : str
        Protein accession number. (e.g. UniProt acc, PDB_acc + chain letter)
    TMD_seq_pl_surr : str
        TMD sequence plus surrouding residues (usually 20) for BLAST
    blast_xml_file : str
        Path to xml file with BLAST results from NCBI.
    xml_txt : str
        Path to a text file that saves the download date, etc.
    xml_tar_gz : str
        Path to compressed tar file containing blast_xml_file, with BLAST results from NCBI.
    expect_value : float or int
        BLAST parameter "expect", which gives the expected number of random matches after BLAST with these parameters.
        Typically 10.
    hit_list_size : int
        Maximum number of BLAST hits.
    logging : logging.Logger
        Python object with settings for logging to console and file.
    db : database
        NCBI database to search.
        Default is "nr"
    """
    logging.info('{} starting download_homologues_from_ncbi'.format(acc))

    # create an empty text file with the download date
    date = strftime("%Y%m%d")
    with open(xml_txt, "w") as f:
        f.write("acc\t{}\ndownload_date\t{}\ndatabase\tncbi_nr\nexpect_value\t{}\n".format(acc, date, expect_value))

    query_fasta_string = ">{} TMD add surround 20 residues\n{}".format(acc, TMD_seq_pl_surr)
    make_sure_path_exists(blast_xml_file, isfile=True)

    start = time.time()

    try:
        tmp_protein_homologues_xml_handle = NCBIWWW.qblast("blastp", db, query_fasta_string,
                                                           expect=expect_value,
                                                           hitlist_size=hit_list_size)
        with open(blast_xml_file, "w") as save_tmp_xml_file:
            save_tmp_xml_file.write(tmp_protein_homologues_xml_handle.read())

        tmp_protein_homologues_xml_handle.close()

    except:
        logging.warning(f"{acc} query string not found in the CGI context in qblast")

    duration = time.time() - start

    if os.path.isfile(blast_xml_file):
        with tarfile.open(xml_tar_gz, mode='w:gz') as tar:
            # add the files to the compressed tarfile
            tar.add(blast_xml_file, arcname=os.path.basename(blast_xml_file))
            tar.add(xml_txt, arcname=os.path.basename(xml_txt))

        delete_BLAST_xml(blast_xml_file)

    logging.info("Output file: {}. (time taken = {:0.3f} min)".format(xml_tar_gz, duration / 60))


def download_10_homologues_from_ncbi(s, df_set, logging):
    """Runs download_homologues_from_ncbi for a set of proteins

    Parameters
    ----------
    s : dict
        Settings dictionary
    df_set : pd.DataFrame
        Dataframe containing the list of proteins to process, including their TMD sequences and full-length sequences
        index : range(0, ..)
        columns : ['acc', 'seqlen', 'TMD_start', 'TMD_end', 'tm_surr_left', 'tm_surr_right', 'database',  ....]
    logging : logging.Logger
        Python object with settings for logging to console and file.
    """
    expect_value = 1
    hit_list_size = 10

    ##############################################################################################
    #                                                                                            #
    #      download homologues from protein lists file                                           #
    #                                                                                            #
    ##############################################################################################

    for i in df_set.index:
        acc = df_set.loc[i, "acc"]
        full_seq = df_set.loc[i, "full_seq"]
        database = df_set.loc[i, "database"]

        # run online server NCBI blastp with biopython module
        blast_xml_file = os.path.join(s["data_dir"], "homologues", "xml", "10_hits", database, "{}.surr{}.BLAST.xml".format(acc, s["num_of_sur_residues"]))
        xml_tar_gz = blast_xml_file[:-4] + ".xml.tar.gz"
        xml_txt = blast_xml_file[:-4] + "_details.txt"

        if not os.path.isfile(xml_tar_gz):
            run_download = True
        else:
            if s["rerun_existing_blast_results"]:
                run_download = True
                logging.info('{} starting download_homologues_from_ncbi_mult_prot (EXISTING xml.tar.gz FILE WILL BE OVERWRITTEN)'.format(acc))
            elif s["rerun_existing_blast_results"] in [False, 0]:
                run_download = False
                logging.info('{} download_homologues_from_ncbi_mult_prot skipped (EXISTING xml.tar.gz FILE)'.format(acc))
                # skip protein
                continue
            else:
                raise ValueError('s["rerun_existing_blast_results"] does not seem to be True or False')

        if run_download:
            download_homologues_from_ncbi(acc, full_seq, blast_xml_file, xml_txt, xml_tar_gz, expect_value, hit_list_size, logging)

    logging.info('homologues download was finished')
