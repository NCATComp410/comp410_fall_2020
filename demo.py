# COMP410 Fall initial demo example
import asa_parser as ap
import git
import os
import pandas as pd


def run_demo():
    # Find path to the data directory in this repo
    data_path = os.path.join(git.Repo('.', search_parent_directories=True).working_tree_dir, 'data')

    # Create an asa sh tech object
    primary_asa = ap.AsaParser(os.path.join(data_path, 'showtech_primary.txt'))

    # show clock example
    print(primary_asa.clock())

    # show failover history example
    print(primary_asa.failover_history())

    # create a dataframe
    df = pd.read_json(primary_asa.failover_history())
    # top reasons found in the failover history
    print(df['Reason'].value_counts())
    print('Demo Message')

    #show process cpu-hog
    print(primary_asa.support_cpu_hog())


if __name__ == "__main__":
    run_demo()
