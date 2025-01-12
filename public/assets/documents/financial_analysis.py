"""
Joseph Muslu
DS2001
12/12/2024
FINAL PROJECT
"""

import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict

# file name constants
DATA_1 = "constituents.csv"
DATA_2 = "constituents-financials.csv"

def file_into_list_of_lists(filename):
    """
    Does: converts file from csv to list of lists, with each row a different list
    :param filename:
    :return: list of lists
    """
    data = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def column_into_ls(ls_of_ls, column_num):
    """
    converts a list of lists that is the dataset into a list that is just for a specific column with a number column input
    :param ls_of_ls: a list of lists that represents the dataset that will be converted into a list
    :param column_num: the number of the column that will be converted
    :return: a list that is just a single metric/column from the original dataset
    """
    data_ls = []
    for ls in ls_of_ls:
        data_ls.append(ls[column_num])

    return data_ls

def float_column_into_ls(ls_of_ls, float_column_num):
    """
       converts a list of lists that is the dataset into a list that is just for a specific column with a number column input
       :param ls_of_ls: a list of lists that represents the dataset that will be converted into a list
       :param float_column_num: the number of the column that will be converted that has float values
       :return: a list that is just a single metric/column from the original dataset that is a float
       """
    data_ls = []
    for ls in ls_of_ls:

        data_ls.append(ls[float_column_num])

    float_data_ls = []
    for item in data_ls:
        if item == '':
            float_data_ls.append("NULL")
        else:
            float_data_ls.append(float(item))
    return float_data_ls


def headquarters_into_location(ls):
    """
    converts a list of locations with more specific information such as city or multiple locations
    to just the outer country or state
    :param ls: the list of locations with all information
    :return: simplified list of locations
    """
    headquarters_ls_of_ls= []
    for location in ls:

        parts = location.split(',')

        headquarters_ls_of_ls.append(parts)

    location_list = []
    for ls in headquarters_ls_of_ls:
        location_list.append(ls[-1].strip())
    return location_list

def modify_null_lists_separate(company_name_ls, industry_ls, location_ls, pe_ratios_ls):
    """
    takes all of the data, and when encountering a null value, removes the corresponding value from each list
    :param company_name_ls: list of the companies that corresponds
    :param industry_ls: corresponding industry list
    :param location_ls: corresponding location list
    :param pe_ratios_ls: corresponding P/E ratio list, has null values
    :return: a list of lists with 4 lists back to back of the company names, industries, locations, and pe ratios
    """
    cleaned_companies = []
    cleaned_industries = []
    cleaned_locations = []
    cleaned_pe_ratios = []
    for i in range(len(pe_ratios_ls)):

        if pe_ratios_ls[i] == "NULL":
            continue
        elif pe_ratios_ls[i] >= 800:
            continue
        else:
            cleaned_companies.append(company_name_ls[i])
            cleaned_industries.append(industry_ls[i])
            cleaned_locations.append(location_ls[i])
            cleaned_pe_ratios.append(pe_ratios_ls[i])

    return cleaned_companies,cleaned_industries,cleaned_locations,cleaned_pe_ratios

def clean_overlap(ls_industries, ls_locations, ls_pe_ratios):
    """
    creates new lists of industries and locations based on when a location and industry match up, and has a list of the
    corresponding pe ratios that are averaged on overlap
    :param ls_pe_ratios: list of PE ratios
    :param ls_industries: list of industries
    :param ls_locations: list of locations
    :return: a list of lists with 3 lists back to back of the industry and location and corresponding pe ratios
    """
    grouped_data = defaultdict(list)
    for location, industry, pe in zip(ls_locations,ls_industries,ls_pe_ratios):
        grouped_data[(location,industry)].append(pe)

    unique_locations = []
    unique_industries = []
    average_pe_ratios = []

    for (location,industry),ratios in grouped_data.items():
        unique_locations.append(location)
        unique_industries.append(industry)
        average_pe_ratio = (sum(ratios)) / (len(ratios))
        average_pe_ratios.append(average_pe_ratio)

    return unique_industries,unique_locations,average_pe_ratios


def create_pe_ratio_heatmap(ls_industries, ls_locations, ls_pe_ratios):
    """
    creates a dataframe and pivot table from lists of industries, locations, and pe ratios to plot a heatmap with
    :param ls_industries: list of industries
    :param ls_locations: list of locations
    :param ls_pe_ratios: list of p/e ratios,
    :return:
    """
    df = pd.DataFrame({
        "Industry": ls_industries,
        "Location": ls_locations,
        "PE_Ratio": ls_pe_ratios
    })

    pivot_table = df.pivot_table(
        index="Location",
        columns="Industry",
        values="PE_Ratio",
    )

    plt.figure(figsize=(18, 10))  # Large figure to accommodate many locations

    sns.heatmap(pivot_table,
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                cbar=True,
                center=pivot_table.mean().mean(),
                cbar_kws={"label": "Average P/E Ratio"},
                linewidths=0.25)

    plt.title("Average P/E Ratio by Industry and Location", fontsize=16)
    plt.tight_layout()
    plt.savefig("Financial Heatmap")
    plt.show()

def main():

    # turns the data from the first constituent file into a list of lists, with each row being a separate list
    file_1_data = file_into_list_of_lists(DATA_1)

    # creates a list of the companies from the list of lists
    company_list = column_into_ls(file_1_data,1)

    # creates a list of the industries from the list of lists
    industry_list = column_into_ls(file_1_data,2)

    # creates a list of headquarters based on the list of lists
    headquarters_list = column_into_ls(file_1_data,4)

    # converts headquarters that has city and potentially multiple values into just a state/country
    location_list = headquarters_into_location(headquarters_list)

    # turns the data from the second file into a list of lists
    file_2_data = file_into_list_of_lists(DATA_2)

    # creates a list of p/e ratios for the companies from the list of lists in the second file
    pe_ratio_list = float_column_into_ls(file_2_data,4)

    # iterates through all the lists and removes all corresponding values for companies with outlier or unusable P/E ratios
    # and outputs as a list of 4 lists
    corrected_ls_of_ls = modify_null_lists_separate(company_list,industry_list,location_list,pe_ratio_list)

    # creates lists for the list of 4 lists generated from the previous function
    corrected_companies = corrected_ls_of_ls[0]
    corrected_industries = corrected_ls_of_ls[1]
    corrected_locations = corrected_ls_of_ls [2]
    corrected_pe_ratios = corrected_ls_of_ls [3]

    # takes the information for the industries and locations and p/e ratios and groups them together such that
    # companies in the same industry and location have their p/e ratios averaged and outputs them as a list of 3 lists
    mapped_points = clean_overlap(corrected_industries,corrected_locations,corrected_pe_ratios)

    # creates lists for the list of 3 lists generated from the previous function
    industries_mapped = mapped_points[0]
    locations_mapped = mapped_points[1]
    pe_ratios_mapped = mapped_points[2]

    # uses all the mapped industries and locations and pe ratios to create a heatmap
    create_pe_ratio_heatmap(industries_mapped,locations_mapped, pe_ratios_mapped)

main()






