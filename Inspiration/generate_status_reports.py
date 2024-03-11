import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import glob
from report_utils import get_reports
from report_utils import extract_datestrings
from report_utils import read_admincred_report
from report_utils import read_admingrade_report
from report_utils import read_voldetails_report
from report_utils import extract_coachdetails
from report_utils import extract_allocateddetails
from report_utils import add_missing_voldetail_IDs
from report_utils import read_missingID_report
from report_utils import read_grade_plus_notindb_report
from report_utils import read_coach_add_report
from report_utils import read_coach_drop_report
from cert_processing_utils import create_coaches_missing_cert_report
from cert_processing_utils import update_summary_report
from cert_processing_utils import select_most_recent_version_of_report
from cert_processing_utils import recalculate_coaches_missing_inperson
from cert_processing_utils import combine_AdminGrade_PreviousData_MissingInPerson
from cert_processing_utils import combine_admincred_and_modadmingrade_certs
from cert_processing_utils import parse_data_by_division
from cert_processing_utils import generate_coachcerts_report
from cert_processing_utils import add_vol_data_to_cert_data
from cert_processing_utils import add_MBPostal_data_to_cert_data


# gets reports and finds certs

input_dir = r'C:/ayso/report_inputs'
# input_dir = r'C:/Work/misc/report_inputs'
input_datestrings_file = input_dir +'/datestrings.txt'
#1st line of file should be previous datestring, 2nd should be current
previous_datestring, current_datestring =\
    extract_datestrings(input_datestrings_file)
init_datestring = '190724'

current_reports = get_reports(input_dir, current_datestring)
previous_reports = get_reports(input_dir, previous_datestring)
print('got reports')

IDs_not_in_admin_report = input_dir +'/missing_admin_IDs.xlsx'
missingID_data = read_missingID_report(IDs_not_in_admin_report)
print('got missing admin IDs')

coach_add_report = input_dir + '/fall_2023_coach_adds.xlsx'
coach_drop_report = input_dir + '/fall_2023_coach_drops.xlsx'
coach_adds = read_coach_add_report(coach_add_report)
coach_drops = read_coach_drop_report(coach_drop_report)

allocated_add_report = input_dir + '/allocated_adds.xlsx'
allocated_drop_report = input_dir + '/allocated_drops.xlsx'
allocated_adds = read_coach_add_report(allocated_add_report)
allocated_drops = read_coach_drop_report(allocated_drop_report)

program_name = '2023 Fall Soccer'
for current_report in current_reports:
    if current_report.find('AdminCredentialsStatusDynamic') > -1:
        admincred_data = read_admincred_report(current_report)
        print('read admincred report')
        # print(admincred_data.columns)
    elif current_report.find('AdminLicenseGrade') > -1:
        admingrade_data = read_admingrade_report(current_report)
        print('read admingrade report')
    elif current_report.find('Volunteer_Details') > -1:
        voldetails_data = read_voldetails_report(current_report)
        print('read voldetails report')
        use_email = False
        voldetails_data =\
            add_missing_voldetail_IDs(voldetails_data, admincred_data, 
                                      missingID_data, use_email)
        print('added missing voldetails IDs')
        coachdetails_data = extract_coachdetails(voldetails_data, program_name)
        outfil = input_dir + '/CoachDetails' + current_datestring + '.xlsx'
        coachdetails_data.to_excel(outfil, index=False)
        print('extracted coach data')
        allocateddetails_data = extract_allocateddetails(coachdetails_data)
        outfil = input_dir + '/AllocatedCoachDetails' + current_datestring + '.xlsx'
        allocateddetails_data.to_excel(outfil, index=False)
        print('extracted allocated coach data')

for previous_report in previous_reports:
    if (previous_report.find('AdminGradePlusNotInDb') > -1 and
        previous_report.find('orig') == -1):
        previous_grade_plus_notindb_data =\
            read_grade_plus_notindb_report(previous_report)
        # print('read previous AdminGradePlusNotInDb report')
        # print(previous_grade_plus_notindb_data['LastName'][1106:1111])

training_report_dir = input_dir + '/Training_Status_Reports'
create_coaches_missing_cert_report(training_report_dir,
                                    init_datestring,
                                    current_datestring)
print('updated training status reports, created coaches missing cert reports')
        
admingrade_plus_notindb_data, modadmingrade_data = \
    combine_AdminGrade_PreviousData_MissingInPerson(admingrade_data,
                                                    previous_grade_plus_notindb_data,
                                                    training_report_dir,
                                                    init_datestring)
outfil = input_dir + '/AdminGradePlusNotInDb' + current_datestring + '.xlsx'
admingrade_plus_notindb_data.to_excel(outfil, index=False)
outfil = input_dir + '/ModAdminGrade' + current_datestring + '.xlsx'
modadmingrade_data.to_excel(outfil, index=False)
print('wrote admingrade_plus_notindb data, modadmingrade_data')

combined_certs_data =\
    combine_admincred_and_modadmingrade_certs(admincred_data, modadmingrade_data)
outfil = input_dir + '/CombinedCerts' + current_datestring + '.xlsx'
combined_certs_data.to_excel(outfil, index=False)
print('wrote combined certs data')

vol_certs_data = parse_data_by_division(combined_certs_data, voldetails_data,
                                        coach_adds, coach_drops, 'Vol')
outfil = input_dir + '/VolCerts' + current_datestring + '.xlsx'
vol_certs_data.to_excel(outfil, sheet_name = 'Vol', index=False,
                        columns=['First','Last','RiskStatus','SafeHaven',
                                 'Concussion','Cardiac','SafeSport','LiveScan',
                                 'RefGrade','CoachLicense'])
print('wrote VolCerts data')

volplus_certs_data = add_vol_data_to_cert_data(combined_certs_data, voldetails_data)
outfil = input_dir + '/VolPlus_Certs' + current_datestring + '.xlsx'
volplus_certs_data.to_excel(outfil, sheet_name = 'Vol', index=False,
                            columns=['First','Last','RiskStatus','SafeHaven',
                                     'Concussion','Cardiac','SafeSport','LiveScan',
                                     'RefGrade','CoachLicense', 'CoachVolMax',
                                     'RefVolMax', 'Youth', 'Email'])

add_MB_Postal_LS_data = True
if add_MB_Postal_LS_data:
    infil = input_dir + '/Manhattan_Postal_LiveScans.xlsx'
    MBPostal_data = pd.read_excel(infil)
    combined_certs_data2 = add_MBPostal_data_to_cert_data(combined_certs_data, MBPostal_data)
else:
    combined_certs_data2 = combined_certs_data.copy(deep=True)
    

outfil = input_dir + '/CoachCerts' + current_datestring + '.xlsx'
season = 'fall'
generate_coachcerts_report(combined_certs_data2, coachdetails_data, coach_adds,
                               coach_drops, season, outfil)
print('wrote CoachCerts data')

outfil = input_dir + '/AllocatedCoachCerts' + current_datestring + '.xlsx'
season = 'fall'
generate_coachcerts_report(combined_certs_data2, allocateddetails_data, allocated_adds,
                               allocated_drops, season, outfil)
print('wrote AllocatedCoachCerts data')