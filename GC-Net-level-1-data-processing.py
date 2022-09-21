# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:00:14 2020

tip list:
    for plots in spyder command prompte
    %matplotlib inline
    for plots in a new window
    %matplotlib qt
@author: bav
"""
import os, sys
import PROMICE_toolbox as ptb
import matplotlib.pyplot as plt
import pandas as pd
import nead
import os.path
import numpy as np
import jaws_tools
import tocgen

from os import path

try:
    os.mkdir("figures")
    os.mkdir("figures/L1_data_treatment")
    os.mkdir("out")
except:
    print("figures and output folders already exist")

# uncomment for the overwriting report file
f = open("out/Report.md", "w")


def Msg(txt):
    f = open("out/Report.md", "a")
    print(txt)
    f.write(txt + "\n")


path_to_L0N = "L0M/"
site_list = pd.read_csv("metadata/GC-Net_location.csv", header=0, skipinitialspace=True)[1:2]
# print(site_list)

# uncomment for use at specific sites
# All station names: 'Swiss Camp 10m', 'Swiss Camp', 'Crawford Point 1', 'NASA-U',
# 'GITS', 'Humboldt', 'Summit', 'Tunu-N', 'DYE2', 'JAR1', 'Saddle',
# 'South Dome', 'NASA-E', 'CP2', 'NGRIP', 'NASA-SE', 'KAR', 'JAR 2',
# 'KULU', 'Petermann ELA', 'NEEM', 'E-GRIP'
# site_list = site_list.loc[site_list.Name.values == 'Swiss Camp',:]

for site, ID in zip(site_list.Name, site_list.ID):
    plt.close("all")
    Msg("# " + str(ID) + " " + site)
    filename = path_to_L0N + str(ID).zfill(2) + "-" + site + ".csv"
    if not path.exists(filename):
        Msg("Warning: No file for station " + str(ID) + " " + site)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df = df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp, utc=True)
    df = df.set_index("timestamp")

    # uncomment for use on reduce time window to save computational time
    # df = df.loc['2000':'2005',:]

    if site == "Swiss Camp 10m":
        df["TA2"] = np.nan
        df["TA4"] = np.nan
    if "HW1" not in df.columns:
        df["HW1"] = 2 + df["HS1"].max() - df["HS1"]
    if "HW2" not in df.columns:
        df["HW2"] = 3.4 + df["HS2"].max() - df["HS2"]
    df = df.resample("H").mean()

    Msg("## Manual flagging of data at " + site)
    df_out = ptb.flag_data(df, site)

    # flagging frozen values
    df_out = ptb.filter_zero_gradient(df_out)

    # gap-filling the temperature TA1 and TA2 with the secondary sensors on the same levels
    # df_out.loc[df.TA1.isnull(), 'TA1'] = df_out.loc[df_out.TA1.isnull(), 'TA3']
    # df_out.loc[df.TA2.isnull(), 'TA2'] = df_out.loc[df_out.TA2.isnull(), 'TA4']

    Msg("## Adjusting data at " + site)
    # we start by adjusting and filtering all variables except surface height
    df_v4 = ptb.adjust_data(df_out, site, skip_var=["HS1", "HS2"])

    # Applying standard filters again
    df_v4 = df_v4.resample("H").asfreq()
    df_v5 = ptb.filter_data(df_v4, site)
    ptb.plot_flagged_data(df_v5, site)
    df_v5 = ptb.remove_flagged_data(df_v5)

    # interpolating short gaps and calculating added variables
    df_v6 = ptb.augment_data(
        df_v5,
        site_list.loc[site_list.Name == site, "Northing"].values[0],
        site_list.loc[site_list.Name == site, "Easting"].values[0],
        site_list.loc[site_list.Name == site, "Elevationm"].values[0],
        site,
    )
    # removing empty rows:
    useful_var_list = [
        "ISWR",
        "OSWR",
        "NR",
        "TA1",
        "TA2",
        "TA3",
        "TA4",
        "RH1",
        "RH2",
        "P",
    ] + ["TS" + str(i) for i in range(1, 11)]
    ind_first = df_v6[
        [v for v in useful_var_list if v in df_v6.columns]
    ].first_valid_index()
    df_v6 = df_v6.loc[ind_first:, :]

    if len(df_v6) > 0:
        # get info related to the new fields
        (
            units,
            display_description,
            database_fields,
            database_fields_data_types,
        ) = ptb.field_info(df_v6.reset_index().columns)

        # write ini file
        nead.write_header(
            "L1_ini/" + str(ID).zfill(2) + "-" + site.replace(" ", "") + "_header.ini",
            df_v6.reset_index(),
            metadata=ds.attrs,
            units=units,
            display_description=display_description,
            database_fields=database_fields,
            database_fields_data_types=database_fields_data_types,
        )

        # saving to file
        nead.write(
            df_v6.reset_index(),
            "L1_ini/" + str(ID).zfill(2) + "-" + site.replace(" ", "") + "_header.ini",
            "L1/" + str(ID).zfill(2) + "-" + site.replace(" ", "") + ".csv",
        )
tocgen.processFile("out/Report.md", "out/report_with_toc.md")
f.close()
