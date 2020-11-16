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

        
    #show process cpu-hog in a dataframe
    df = pd.read_json(primary_asa.show_process_cpu_hog())
    print('Show Process Cpu Hog')
    print(df['Process'].unique())

    
    # startup-config errors in a dataframe
    df = pd.read_json(primary_asa.startup_config_errors())
    print('Startup config errors')
    # show unique values in StarInfo
    print(df['CriticalError'].unique())

    
    # tech support license
    print(primary_asa.show_tech_support_license())

    # cpu detailed
    print(primary_asa.show_cpu_detailed())

    # cpu usage
    print(primary_asa.show_cpu_usage())

    # memory region
    print(primary_asa.show_memory_region())

    # ipsec stats
    print(primary_asa.ipsec_stats())

    # context details
    print(primary_asa.show_context_details())

    # interface
    print(primary_asa.show_interface())

    # traffic
    print(primary_asa.show_traffic())

    #show memory
    print(primary_asa.show_memory())

    #show memory detail
    print(primary_asa.show_memory_detail())


    #show process
    print(primary_asa.show_process())


    #show logging buffered
    print(primary_asa.show_logging_buffered())

    #show kernel process
    print(primary_asa.show_kernel_process())
    

if __name__ == "__main__":
    run_demo()