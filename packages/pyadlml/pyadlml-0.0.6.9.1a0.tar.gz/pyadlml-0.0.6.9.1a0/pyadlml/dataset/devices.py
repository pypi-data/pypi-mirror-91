import numpy as np
import pandas as pd
import dask
from pyadlml.dataset import START_TIME, END_TIME, TIME, VAL, DEVICE

"""
    df_devices:
        also referred to as rep1
        a lot of data is found in this format.
        Exc: 
           | time      | device    | state
        ------------------------------------
         0  | timestamp | dev_name  |   1

    rep2:
        is used to calculate statistics for devices more easily
        and has lowest footprint in storage. Most of the computation 
        is done using this format
           | start_time | end_time   | device    
        ----------------------------------------
         0 | timestamp   | timestamp | dev_name  
 
 """


def _create_devices(dev_list, index=None):
    """
    creates an empty device dataframe
    """
    if index is not None:
        return pd.DataFrame(columns=dev_list, index=index)
    else:
        return pd.DataFrame(columns=dev_list)


def _check_devices_sequ_order(df):
    """
    iterate pairwise through each select device an check if the 
    sequential order in time is inconsistent

    Parameters
    ----------
    df : pd.DataFrame
        device representation 1  with columns [start_time, end_time, devices]
    """
    dev_list = df['device'].unique()
    no_errors = True
    for dev in dev_list:
        df_d = df[df['device'] == dev]
        for i in range(1, len(df_d)):
            st_j = df_d.iloc[i-1].start_time
            et_j = df_d.iloc[i-1].end_time
            st_i = df_d.iloc[i].start_time
            # et_i = df_d.iloc[i].end_time
            # if the sequential order is violated return false
            if not (st_j < et_j) or not (et_j < st_i):
                print('~'*50)
                if st_j >= et_j:
                    #raise ValueError('{}; st: {} >= et: {} |\n {} '.format(i-1, st_j, et_j, df_d.iloc[i-1]))
                    print('{}; st: {} >= et: {} |\n {} '.format(i-1, st_j, et_j, df_d.iloc[i-1]))
                if et_j >= st_i:
                    #raise ValueError('{},{}; et: {} >= st: {} |\n{}\n\n{}'.format(i-1,i, et_j, st_i, df_d.iloc[i-1], df_d.iloc[i]))
                    print('{},{}; et: {} >= st: {} |\n{}\n\n{}'.format(i-1,i, et_j, st_i, df_d.iloc[i-1], df_d.iloc[i]))
                no_errors = False
    return no_errors



def _is_dev_rep2(df):
    """
    """
    if not START_TIME in df.columns or not END_TIME in df.columns \
    or not DEVICE in df.columns or len(df.columns) != 3:
        return False
    return True

def _is_dev_rep1(df):
    """
    """
    if DEVICE in df.columns and VAL in df.columns \
    and TIME in df.columns and len(df.columns) == 3:
        return True
    return False

def device_rep1_2_rep2(df_rep1, drop=False):
    """ transforms a device representation 1 into 2
    Parameters
    ----------
    df_rep1 : pd.DataFrame
        rep1: col (time, device, val)
        example row: [2008-02-25 00:20:14, Freezer, False]
    drop : Boolean
        Indicates whether rows that have no starting/end timestamp should be dropped or the
        missing counterpart should be added with the first/last timestamp
    Returns
    -------
    df : pd.DataFrame
        rep: columns are (start time, end_time, device)
        example row: [2008-02-25 00:20:14, 2008-02-25 00:22:14, Freezer]         
    or 
    df, lst
    """
    df = df_rep1.copy().reset_index(drop=True)
    df = df.sort_values(TIME)
    df.loc[:,'ones'] = 1
    
    rows_changed = 0
    syn_acts = []
    if drop:
        to_delete_idx = []
        for dev in df['device'].unique():
            df_dev = df[df['device'] == dev]
            first_row = df_dev.iloc[0].copy()
            last_row = df_dev.iloc[len(df_dev)-1].copy()
            if not first_row['val']:
                to_delete_idx.append(first_row.name)
            if last_row['val']:
                to_delete_idx.append(last_row.name)
        df = df.drop(to_delete_idx)
        rows_changed = -len(to_delete_idx)
    else:
        # add values to things that are false
        first_timestamp = df['time'].iloc[0]
        last_timestamp = df['time'].iloc[len(df)-1]
        eps = pd.Timedelta('1ns')
        for dev in df['device'].unique():
            df_dev = df[df['device'] == dev]
            first_row = df_dev.iloc[0].copy()
            last_row = df_dev.iloc[len(df_dev)-1].copy()
            if not first_row['val']:
                first_row['val'] = True
                first_row['time'] = first_timestamp + eps
                syn_acts.append(first_row)
                df = df.append(first_row, ignore_index=True)
            if last_row['val']:
                last_row['val'] = False
                last_row['time'] = last_timestamp - eps
                syn_acts.append(last_row)
                df = df.append(last_row, ignore_index=True)
            eps += pd.Timedelta('1ns')
        rows_changed = len(syn_acts)
            
    df = df.reset_index(drop=True).sort_values(TIME)
    
    # seperate the 0to1 and 1to0 device changes
    df.loc[:,VAL] = df[VAL].astype(bool)
    df_start = df[df[VAL]] 
    df_end = df[~df[VAL]]    
    df_end = df_end.rename(columns={TIME: END_TIME})
    df_start = df_start.rename(columns={TIME: START_TIME})

    # ordered in time to index them and make a correspondence
    df_end.loc[:,'pairs'] = df_end.groupby([DEVICE])['ones'].apply(lambda x: x.cumsum())
    df_start.loc[:,'pairs'] = df_start.groupby([DEVICE])['ones'].apply(lambda x: x.cumsum())        
        
    
    df = pd.merge(df_start, df_end, on=['pairs', DEVICE])
    df = df.sort_values(START_TIME)
    
    # sanity checks        
    diff = int((len(df_rep1)+rows_changed)/2) - len(df)
    assert diff == 0, 'input {} - {} == {} result. Somewhere two following events of the \
        #        same device had the same starting point and end point'.format(int(len(df_rep1)/2), len(df), diff)
    
    if drop:
        return df[[START_TIME, END_TIME, DEVICE]]
    else:
        return df[[START_TIME, END_TIME, DEVICE]], syn_acts

def device_rep2_2_rep1(df_rep2):
    """
    Parameters
    ----------
    df_rep2 : pd.DataFrame
        rep2: columns (start time, end_time, device)

    Returns
    -------
    df : (pd.DataFrame)
        rep1: columns are (time, value, device)
        example row: [2008-02-25 00:20:14, Freezer, False]
    """
    # copy devices to new dfs 
    # one with all values but start time and other way around
    df_start = df_rep2.copy().loc[:, df_rep2.columns != END_TIME]
    df_end = df_rep2.copy().loc[:, df_rep2.columns != START_TIME]

    # set values at the end time to zero because this is the time a device turns off
    df_start[VAL] = True
    df_end[VAL] = False

    # rename column 'End Time' and 'Start Time' to 'Time'
    df_start.rename(columns={START_TIME: TIME}, inplace=True)
    df_end.rename(columns={END_TIME: TIME}, inplace=True)

    df = pd.concat([df_end, df_start]).sort_values(TIME)
    df = df.reset_index(drop=True)
    return df

def correct_device_rep1_ts_duplicates(df):
    """
    remove devices that went on and off at the same time. And add a microsecond
    to devices that trigger on the same time
    Parameters
    ----------
    df : pd.DataFrame
        Devices in representation 1; columns [time, device, value]
    """
    eps = pd.Timedelta('10ms')
    
    try:
        df[TIME]
    except KeyError:
        df = df.reset_index()
        
    # remove device if it went on and off at the same time    
    dup_mask = df.duplicated(subset=[TIME, DEVICE], keep=False)    
    df = df[~dup_mask]
    
    df = df.reset_index(drop=True)
    
    
    dup_mask = df.duplicated(subset=[TIME], keep=False)
    duplicates = df[dup_mask]    
    uniques = df[~dup_mask]
    
    # for every pair of duplicates add a millisecond on the second one
    duplicates = duplicates.reset_index(drop=True)
    sp = duplicates['time'] + eps   
    mask_p = (duplicates.index % 2 == 0) 
    
    duplicates['time'] = duplicates['time'].where(mask_p, sp)
    
    # concatenate and sort the dataframe 
    uniques = uniques.set_index(TIME)
    duplicates = duplicates.set_index(TIME)
    df = pd.concat([duplicates, uniques], sort=True)
    
    # set the time as index again
    df = df.sort_values(TIME).reset_index(drop=False)
    
    return df
    
def _has_timestamp_duplicates(df):
    """ check whether there are duplicates in timestamp present
    Parameters
    ----------
    df : pd.DataFrame
        data frame representation 1: [time, device, val]
    """
    df = df.copy()
    try:
        dup_mask = df.duplicated(subset=[TIME], keep=False)
    except KeyError:
        df = df.reset_index()
        dup_mask = df.duplicated(subset=[TIME], keep=False)
    return dup_mask.sum() > 0


def split_devices_binary(df):
    """ separate binary devices and non-binary devices
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe in device representation 1
    Returns
    -------
    df_binary, df_non_binary : pd.DataFrames
        Dataframe with binary devices and dataframe without binary devices
    """
    mask_binary = df[VAL].apply(lambda x: isinstance(x, bool))
    return df[mask_binary], df[~mask_binary]


def contains_non_binary(df) -> bool:
    """ determines whether the the dataframes values contain non-boolean values
    These can be continuous values of categorical.
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe in device representation 1
    Returns
    -------
    boolean
    """
    return not df[VAL].apply(lambda x: isinstance(x, bool)).all()


def correct_devices(df):
    """
    Parameters
    ----------
    df : pd.DataFrame
        either in device representation 1 or 2
    Returns
    -------
    cor_rep1 : pd.DataFrame
    """
    df = df.copy()
    df = df.drop_duplicates()        

    if df.empty:
        return df
    
    # bring in correct representation
    if _is_dev_rep2(df):
        df = device_rep2_2_rep1(df)
    elif not _is_dev_rep1(df):
        raise ValueError('Devices representation is not known')

    df = df.sort_values(by=TIME).reset_index(drop=True)

    # correct timestamp duplicates
    while _has_timestamp_duplicates(df):
        df = correct_device_rep1_ts_duplicates(df)
    assert not _has_timestamp_duplicates(df)

    if contains_non_binary(df):
        df_binary, df_non_binary = split_devices_binary(df)
        non_binary_exist = True
    else:
        df_binary = df
        non_binary_exist = False

    # correct on/off inconsistency
    if not is_on_off_consistent(df_binary):
        df_binary = correct_on_off_inconsistency(df_binary)
    assert is_on_off_consistent(df_binary)

    # join dataframes
    if non_binary_exist:
        df = df_binary.append(df_non_binary).reset_index(drop=True)
    else:
        df = df_binary

    return df


def on_off_consistent_func(df, dev):
    """ compute for each device if it is on/off consistent
    Parameters
    ----------
    df : pd.DataFrame
        the whole activity dataframe
    dev : str
        a device that occurs in the dataframe
    Returns
    -------
    tupel [arg1, arg2]
        first argument is a boolean whether this device is consistent
        second is
    """
    df_dev = df[df[DEVICE] == dev].sort_values(by=TIME).reset_index(drop=True)
    first_val = df_dev[VAL].iloc[0]
    if first_val:
        mask = np.zeros((len(df_dev)), dtype=bool)
        mask[::2] = True
    else:
        mask = np.ones((len(df_dev)), dtype=bool)
        mask[::2] = False
    return [not (df_dev[VAL] ^ mask).sum() > 0, df_dev[[TIME, DEVICE, VAL]]]

def is_on_off_consistent(df):
    """ devices can only go on after they are off and vice versa. check if this is true
        for every device.
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe in representation 1.
        The dataframe must not include timestamp duplicates! When it does they can be arbitrarily reordered
        when sorting for time thus destroying the consistency.
    """
    lazy_results = []
    for dev in df[DEVICE].unique():
        res = dask.delayed(on_off_consistent_func)(df.copy(), dev)
        lazy_results.append(res)

    results = np.array(list(dask.compute(*lazy_results)))
    return results[:,0].all()



from dask import delayed
def correct_on_off_inconsistency(df):
    """ 
    has multiple strategies for solving the patterns:
    e.g if the preceeding value is on and the same value is occuring now delete now
    Parameters
    ----------
    df : pd.DataFrame
        device representation 3
        
    Returns
    -------
    df : pd.DataFrame
        device representation 3
    """
    
    def correct_part(df_dev):
        """ get index of rows where the previous on/off value was the same and delete row
        Parameters
        ----------
        df_dev : pd.DataFrame
            subset of the big dataframe consisting only of events for a fixed device
        """
        df_dev['same_prec'] = ~(df_dev[VAL].shift(1) ^ df_dev[VAL])
        df_dev.loc[0, 'same_prec'] = False # correct shift artefact
        indices = list(df_dev[df_dev['same_prec']].index)
        df_dev = df_dev.drop(indices, axis=0)
        return df_dev[[TIME, DEVICE, VAL]]
                    
    df = df.copy()
    # create list of tuples e.g [(True, df_dev1), (False, df_dev2), ...]
    dev_list = df[DEVICE].unique()
    dev_df_list = []
    for devs in dev_list:
        dev_df_list.append(delayed(on_off_consistent_func)(df, devs))
    results = np.array(list(dask.compute(*dev_df_list)))

    # filter inconsistent devices
    incons = results[np.where(np.logical_not(results[:, 0]))[0], :][:, 1]

    corrected = []
    for part in incons:
        corrected.append(delayed(correct_part)(part))
    corr_dfs = delayed(lambda x: x)(corrected).compute()
    corr_devs = [df[DEVICE].iloc[0] for df in corr_dfs]
    tmp = [df[~df[DEVICE].isin(corr_devs)], *corr_dfs]

    return pd.concat(tmp, ignore_index=True)\
            .sort_values(by=TIME).reset_index(drop=True)
