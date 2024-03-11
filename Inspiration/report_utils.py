import pandas as pd
import numpy as np
import glob

# gets the reports
def get_reports(input_dir, datestring):
    srchstr = input_dir + '/*' + datestring + '*'
    input_fils = glob.glob(srchstr)
    input_fils.sort()
    return input_fils

def extract_datestrings(datestrings_filnam):
    datestrings_file = open(datestrings_filnam, 'r')
    linesi = datestrings_file.readlines()
    count = 0
    for linei in linesi:
        if count == 0:
            previous_datestring = linei
            eol_pos = previous_datestring.find('\n')
            if eol_pos > -1:
                previous_datestring = previous_datestring[:eol_pos]
            count = count + 1
        elif count == 1:
            current_datestring = linei
            eol_pos = current_datestring.find('\n')
            if eol_pos > -1:
                current_datestring = current_datestring[:eol_pos]
    return previous_datestring, current_datestring

def read_voldetails_report(voldetail_report):
    voldetails_data =\
        pd.read_excel(voldetail_report, keep_default_na=False)
    voldetails_data.columns = voldetails_data.columns.str.replace(' ','_')
    LastNameCap = voldetails_data['Volunteer_Last_Name'].str.capitalize()
    FirstNameCap = voldetails_data['Volunteer_First_Name'].str.capitalize()
    voldetails_data.drop(['Volunteer_Last_Name', 'Volunteer_First_Name'],
                         axis=1, inplace=True)
    voldetails_data['Volunteer_Last_Name'] = LastNameCap
    voldetails_data['Volunteer_First_Name'] = FirstNameCap
    voldetails_data.sort_values(by=['Association_Volunteer_ID', 
                                    'Volunteer_Last_Name', 
                                    'Volunteer_First_Name'],
                                inplace=True, ignore_index=True)
    return voldetails_data

def extract_coachdetails(voldetails_data, program_name):
    coachdetails_data =\
        voldetails_data[voldetails_data['Volunteer_Role'].str.lower().str.find('coach') > -1]
    coachdetails_data =\
        coachdetails_data[coachdetails_data['Program_Name'].str.find(program_name) > -1]
    coachdetails_data.reset_index(drop=True, inplace=True)
    return coachdetails_data

def extract_allocateddetails(coachdetails_data):
    allocateddetails_data =\
        coachdetails_data[coachdetails_data['Team_Name'].str.lower().str.find('unallocated') ==-1]
    allocateddetails_data.reset_index(drop=True, inplace=True)    
    return allocateddetails_data

def read_admingrade_report(adminlicensegrade_report):
    admingrade_data =\
        pd.read_excel(adminlicensegrade_report,
                      converters={'DOB': pd.to_datetime,
                                  'License/Grade Obtained': pd.to_datetime},
                      keep_default_na=False, header=1)
    admingrade_data.columns = admingrade_data.columns.str.replace(' ','_')
    admingrade_data.sort_values(by=['Admin_ID', 'Last_Name', 'First_Name'],
                                inplace=True, ignore_index=True)
    return admingrade_data

def read_admincred_report(admincredentials_report):
    admincred_data =\
        pd.read_excel(admincredentials_report, dtype=str,
                      keep_default_na=False, header=[2,3])
    # admincred_data.columns =\
    #     ['' if col.startswith('Unnamed') 
    #       else col for col in admincred_data.columns]
    admincred_data.columns = admincred_data.columns.map('_'.join)
    col_names = []
    for col_ind in range(len(admincred_data.columns)):
        tmp = admincred_data.columns[col_ind]
        cr_pos = tmp.find('\n')
        if cr_pos > -1:
            tmp = tmp[:cr_pos] + ' ' + tmp[cr_pos+1:]
        unnamed_pos = tmp.find('Unnamed')
        if unnamed_pos > -1:
            und_pos = tmp.rfind('_')
            tmp = tmp[und_pos+1:]
        col_names.append(tmp)
    admincred_data.columns = col_names
    admincred_data.columns = admincred_data.columns.str.replace(' ','_')
    admincred_data.sort_values(by=['Admin_ID', 'Last_Name', 'First_Name'],
                               inplace=True, ignore_index=True)
    return admincred_data

def add_missing_voldetail_IDs(voldetail_data, admincred_data, missingID_data, 
                              use_email=False):
    vol_ids = []
    for vind in range(len(voldetail_data)):
        vid = voldetail_data['Association_Volunteer_ID'][vind]
        if len(vid) == 0:
            firstname = voldetail_data['Volunteer_First_Name'][vind].lower()
            lastname = voldetail_data['Volunteer_Last_Name'][vind].lower()
            emailaddress = voldetail_data['Volunteer_Email_Address'][vind].lower()
            found = False
            if use_email:
                for aind in range(len(admincred_data)):
                    if (admincred_data['First_Name'][aind].lower() == firstname and
                        admincred_data['Last_Name'][aind].lower() == lastname and
                        admincred_data['Email'][aind].lower() == emailaddress):
                        vol_ids.append(admincred_data['Admin_ID'][aind])
            #            print('found id for '+ firstname + ' ' + lastname)
                        found = True
                        break
            else:
                for aind in range(len(admincred_data)):
                    if (admincred_data['First_Name'][aind].lower() == firstname and
                        admincred_data['Last_Name'][aind].lower() == lastname):
                        vol_ids.append(admincred_data['Admin_ID'][aind])
            #            print('found id for '+ firstname + ' ' + lastname)
                        found = True
                        break
            if not found:
                for aind in range(len(missingID_data)):
                    if (missingID_data['First_Name'][aind].lower() == firstname and
                        missingID_data['Last_Name'][aind].lower() == lastname):
                        vol_ids.append(missingID_data['ID'][aind])
                        found = True
                        break
                if not found:
                    vol_ids.append(vid)
                    print('Did not find id for ' + firstname + ' ' + lastname)
        else:
            vol_ids.append(vid)
    voldetail_data['Association_Volunteer_ID'] = vol_ids
    return voldetail_data

def read_missingID_report(missingID_report):
    missingID_data =\
        pd.read_excel(missingID_report, keep_default_na=False)
    return missingID_data

def read_grade_plus_notindb_report(admingrade_plus_notindb_report):
    grade_plus_notindb_data =\
        pd.read_excel(admingrade_plus_notindb_report, 
                      keep_default_na=False)
    grade_plus_notindb_data.columns = grade_plus_notindb_data.columns.str.replace(' ','_')
    grade_plus_notindb_data['LastName'] =\
        grade_plus_notindb_data['LastName'].str.capitalize()
    grade_plus_notindb_data['FirstName'] =\
        grade_plus_notindb_data['FirstName'].str.capitalize()
    grade_plus_notindb_data.sort_values(by=['ID', 'LastName', 'FirstName'],
                                        inplace=True, ignore_index=True)
    return grade_plus_notindb_data

def read_coach_add_report(coach_add_report):
    coach_add_data =\
        pd.read_excel(coach_add_report, keep_default_na=False)
    coach_add_data['FirstName'] =\
        coach_add_data['FirstName'].str.capitalize()
    coach_add_data['LastName'] =\
        coach_add_data['LastName'].str.capitalize()
    coach_add_data.sort_values(by=['ID', 'LastName', 'FirstName'],
                               inplace=True, ignore_index=True)
    return coach_add_data
    
def read_coach_drop_report(coach_drop_report):
    coach_drop_data =\
        pd.read_excel(coach_drop_report, keep_default_na=False)
    coach_drop_data['FirstName'] =\
        coach_drop_data['FirstName'].str.capitalize()
    coach_drop_data['LastName'] =\
        coach_drop_data['LastName'].str.capitalize()
    coach_drop_data.sort_values(by=['ID', 'LastName', 'FirstName'],
                                inplace=True, ignore_index=True)
    return coach_drop_data