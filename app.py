import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

st.title('Explore Imaris data file (xlxs)')

ready = False

# make a fileiput widget
uploaded_file = st.sidebar.file_uploader("Choose a xls file", 'xls')

if uploaded_file is not None:
    xlsfile = pd.ExcelFile(uploaded_file)
    sheetnames = xlsfile.sheet_names
    sheet = st.sidebar.selectbox('Which sheet to choose', sheetnames)
    ready = True


def loadsheet(file, selectedsheet):
    selected_sheet = pd.read_excel(file, selectedsheet, header=1)
    return selected_sheet


def makehistogram(histdata):
    plt.figure()
    plt.hist(histdata)
    st.pyplot()


def extractintensity(file,sheetnames):
    intensityindex = [re.search(r'intensity', sheet_a, re.IGNORECASE) for sheet_a in sheetnames]
    sheetlistintensity = [sheetname for sheetname, intindx in zip(sheetnames, intensityindex) if intindx]
    st.write(sheetlistintensity)
    listofchannels = []
    intensitydf = None
    for sheet_i in sheetlistintensity:
        name = 'ch ' + re.findall(r'.*ch=(\d+)', sheet_i, re.IGNORECASE)[0] + '  ' + re.findall(r'Intensity (\w+)', sheet_i, re.IGNORECASE)[0]
        tempdataframe = pd.read_excel(file, sheet_i, header=1)
        if intensitydf is None:
            intensitydf = tempdataframe[['ID', 'Surpass Object', 'Category']]

        intensitydf[name] = tempdataframe.iloc[:,0]
        listofchannels.append(name)
    #TODO find a way to sort the dataframe so all ch 1 is collected in one place
    #resultdf = [intensitydf.iloc[:,0:3], intensitydf.sort()]
    return listofchannels, resultdf


if ready:
    data = loadsheet(xlsfile, sheet)
    st.write(data)

    # Extract all information about channels.
    listofchannels, dataframeintensity = extractintensity(xlsfile, sheetnames)
    st.write(dataframeintensity)

    if re.search(r'intensity', sheet, re.IGNORECASE):
        columnnames = data.columns
        makehistogram(data[columnnames[0]])
        #st.write(currentfigure)


