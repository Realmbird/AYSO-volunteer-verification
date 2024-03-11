import pandas as pd
import numpy as np
import glob

def update_summary_report(summary_report, update_report):
    summary_data = pd.read_excel(summary_report)
    update_data = pd.read_excel(update_report, header=4)
    combined_data = pd.concat([summary_data, update_data], axis=0)
    combined_data['Surname'] =\
        combined_data['Surname'].str.capitalize()
    combined_data['Firstname'] =\
        combined_data['Firstname'].str.capitalize()
    combined_data['Username'] =\
        combined_data['Username'].str.upper()
    combined_data.sort_values(by=['Username', 'Surname', 'Firstname'],
                              inplace=True, ignore_index=True)
    combined_data.drop_duplicates(subset='Username', keep='first',
                                  inplace=True)
    combined_data.sort_values(by=['Surname', 'Firstname', 'Username'],
                              inplace=True, ignore_index=True)
    combined_data.drop_duplicates(subset=['Surname', 'Firstname'],
                                  keep = 'first', inplace=True)
    combined_data.reset_index(drop=True, inplace=True)
    undpos0 = summary_report.rfind('_')
    undpos1 = update_report.rfind('_')
    outfil = summary_report[:undpos0] + update_report[undpos1:]
    combined_data.to_excel(outfil, index=False)

def select_most_recent_version_of_report(reports):
    #sort by six-character datestring after last _ in name
    datestrings = []
    for report in reports:
        undpos = report.rfind('_')
        datestrings.append(report[undpos+1:undpos+7])
    ind_max = np.argmax(datestrings)
    return ind_max
    
def recalculate_coaches_missing_inperson(training_report_dir, init_datestring,
                                         updated_cert_level):
    if updated_cert_level == '10U':
        srchstr =\
            training_report_dir + '/*10Uonline' + '*' + init_datestring + '*'
        summary_online_reports = glob.glob(srchstr)
        if len(summary_online_reports) == 1:
            summary_online_report = summary_online_reports[0]
        else:
            ind_report = select_most_recent_version_of_report(summary_online_reports)
            summary_online_report = summary_online_reports[ind_report]
        online_completed_data = pd.read_excel(summary_online_report)
        online_completed_data['Username'] =\
            online_completed_data['Username'].str.upper()
        srchstr =\
            training_report_dir + '/*10Uinperson' +\
                '*' + init_datestring + '*'
        inperson_reports = glob.glob(srchstr)
        if len(inperson_reports) == 1:
            inperson_report = inperson_reports[0]
        else:
            ind_report = select_most_recent_version_of_report(inperson_reports)
            inperson_report = inperson_reports[ind_report]
        inperson_data = pd.read_excel(inperson_report)
        inperson_data['Username'] =\
            inperson_data['Username'].str.upper()
        #drop anyone in online_completed_data set who also completed an in-person class
        online_completed_data =\
            online_completed_data[~online_completed_data['Username'].isin(inperson_data['Username'])]
    else:
        srchstr =\
            training_report_dir + '/*' + updated_cert_level + 'online' +\
            '*' + init_datestring + '*'
        summary_online_reports = glob.glob(srchstr)
        if len(summary_online_reports) == 1:
            summary_online_report = summary_online_reports[0]
        else:
            ind_report = select_most_recent_version_of_report(summary_online_reports)
            summary_online_report = summary_online_reports[ind_report]
        online_completed_data = pd.read_excel(summary_online_report)
        online_completed_data['Username'] =\
            online_completed_data['Username'].str.upper()
        srchstr =\
            training_report_dir + '/*' + updated_cert_level + 'inperson_' +\
            '*' + init_datestring + '*'
        inperson_reports = glob.glob(srchstr)
        if len(inperson_reports) == 1:
            inperson_report = inperson_reports[0]
        else:
            ind_report = select_most_recent_version_of_report(inperson_reports)
            inperson_report = inperson_reports[ind_report]
        inperson_data = pd.read_excel(inperson_report)
        inperson_data['Username'] =\
            inperson_data['Username'].str.upper()
        #drop anyone in online_completed_data set who also completed an in-person class
        online_completed_data =\
            online_completed_data[~online_completed_data['Username'].isin(inperson_data['Username'])]
    undpos = summary_online_report.rfind('_')
    current_datestring = summary_online_report[undpos+1:undpos+7]
    outfil = training_report_dir + '/Coaches_missing_' + updated_cert_level +\
        '_InPersonClass_' + current_datestring + '.xlsx'
    online_completed_data.sort_values(by=['Surname', 'Firstname', 'Username'],
                                      inplace=True, ignore_index=True)
    online_completed_data.drop_duplicates(subset=['Surname', 'Firstname'],
                                          keep='first', inplace=True)
    online_completed_data.reset_index(drop=True, inplace=True)
    online_completed_data.to_excel(outfil, index=False)
    outfil2 = training_report_dir + '/Coaches_missing_' + updated_cert_level +\
        '_InPersonClass.xlsx'
    online_completed_data.to_excel(outfil2, index=False)
    return

def create_coaches_missing_cert_report(training_report_dir, init_datestring,
                                       current_datestring):
    certs = ['10U', '12U', 'Int', 'Adv']
    U10_fields = ['Online', 'Both', 'Field', 'Full']
    U1246_fields = ['Pre', 'InPerson']
    U10_summary_fields = ['online', 'inperson', 'inperson', 'inperson']
    U1246_summary_fields = ['online', 'inperson']
    #U10_fields should differ from U1246 fields
    fields = U10_fields + U1246_fields
    summary_fields = U10_summary_fields + U1246_summary_fields
    #check for any training update reports
    srchstr = training_report_dir + '/*' + current_datestring + '*'
    update_reports = glob.glob(srchstr)
    srchstr = training_report_dir + '/*' + init_datestring + '*'
    summary_reports = glob.glob(srchstr)
    updated_cert_levels = []
    if len(update_reports) > 0:
        for update_report in update_reports:
            for cert in certs:
                if update_report.find(cert) > -1:
                    for ifield in range(len(fields)):
                        field = fields[ifield]
                        summary_field = summary_fields[ifield]
                        summary_reports_matching = []
                        if update_report.find(field) > -1:
                            for summary_report in summary_reports:
                                if (summary_report.find(cert) > -1 and
                                    summary_report.find(summary_field) > -1):
                                    summary_reports_matching.append(summary_report)
                                    updated_cert_levels.append(cert)
                        if len(summary_reports_matching) > 0:
                            ind_summary_report =\
                                select_most_recent_version_of_report(summary_reports_matching)
                            summary_report_use = summary_reports_matching[ind_summary_report]
                            update_summary_report(summary_report_use,
                                                  update_report)
                            if cert == '10U' and ifield > 0:
                                summary_reports = glob.glob(srchstr)
                            updated_cert_levels.append(cert)
                    break
    updated_cert_levels = list(set(updated_cert_levels))
    for updated_cert_level in updated_cert_levels:
        recalculate_coaches_missing_inperson(training_report_dir,
                                             init_datestring,
                                             updated_cert_level)
        
    return

def parse_AdminGrade_data(admingrade_data):
    admingrade_data.sort_values(by=['Admin_ID', 'Last_Name', 'First_Name'],
                                inplace=True, ignore_index=True)
    current_ID = 'init'
    current_last = 'init'
    current_first = 'init'
    current_email = 'init'
    U6Coach = []
    U8Coach = []
    U10Coach = []
    U12Coach = []
    IntCoach = []
    AdvCoach = []
    U8Official = []
    RegRef = []
    IntRef = []
    AdvRef = []
    NatRef = []
    ID = []
    FirstName = []
    LastName = []
    Email = []
    u6c = ''
    u8c = ''
    u10c = ''
    u12c = ''
    intc = ''
    advc = ''
    u8r = ''
    regr = ''
    intr = ''
    advr = ''
    natr = ''
    for irow in range(admingrade_data.shape[0]):
        if (admingrade_data['Admin_ID'][irow] != current_ID or
            admingrade_data['Last_Name'][irow].capitalize() != current_last or
            admingrade_data['First_Name'][irow].capitalize() != current_first):
            if irow > 0:
                U6Coach.append(u6c)
                U8Coach.append(u8c)
                U10Coach.append(u10c)
                U12Coach.append(u12c)
                IntCoach.append(intc)
                AdvCoach.append(advc)
                U8Official.append(u8r)
                RegRef.append(regr)
                IntRef.append(intr)
                AdvRef.append(advr)
                NatRef.append(natr)
                ID.append(current_ID)
                FirstName.append(current_first)
                LastName.append(current_last)
                Email.append(current_email)
            current_ID = admingrade_data['Admin_ID'][irow]
            current_last = admingrade_data['Last_Name'][irow].capitalize()
            current_first = admingrade_data['First_Name'][irow].capitalize()
            current_email = admingrade_data['Email'][irow].lower()
            u6c = ''
            u8c = ''
            u10c = ''
            u12c = ''
            intc = ''
            advc = ''
            u8r = ''
            regr = ''
            intr = ''
            advr = ''
            natr = ''
        if (admingrade_data['Admin_ID'][irow] == current_ID and
            admingrade_data['Last_Name'][irow].capitalize() == current_last and
            admingrade_data['First_Name'][irow].capitalize() == current_first):
            if admingrade_data['Coaching_License/Referee_Grade'][irow].find('10U Coach') > -1:
                u10c = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('12U Coach') > -1:
                u12c = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('6U Coach') > -1:
                u6c = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('8U Coach') > -1:
                u8c = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('8U Official') > -1:
                u8r = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('Advanced (19U) Coach') > -1:
                advc = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('Advanced Referee') > -1:
                advr = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('Intermediate (14U) Coach') > -1:
                intc = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('Intermediate Referee') > -1:
                intr = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('National Referee') > -1:
                natr = 'x'
            elif admingrade_data['Coaching_License/Referee_Grade'][irow].find('Regional Referee') > -1:
                regr = 'x'
    U6Coach.append(u6c)
    U8Coach.append(u8c)
    U10Coach.append(u10c)
    U12Coach.append(u12c)
    IntCoach.append(intc)
    AdvCoach.append(advc)
    U8Official.append(u8r)
    RegRef.append(regr)
    IntRef.append(intr)
    AdvRef.append(advr)
    NatRef.append(natr)
    ID.append(current_ID)
    FirstName.append(current_first)
    LastName.append(current_last)
    Email.append(current_email)
    admingrade_certs = {
        'ID': ID,
        'FirstName': FirstName,
        'LastName': LastName,
        'U6Coach': U6Coach,
        'U8Coach': U8Coach,
        'U10Coach': U10Coach,
        'U12Coach': U12Coach,
        'IntCoach': IntCoach,
        'AdvCoach': AdvCoach,
        'U8Official': U8Official,
        'RegRef': RegRef,
        'IntRef': IntRef,
        'AdvRef': AdvRef,
        'NatRef': NatRef,
        'Email': Email
        }
    admingrade_df = pd.DataFrame(admingrade_certs)
    # outfil = r'C:/Work/misc/ayso/report_inputs/ParsedAdminGrade.xlsx'
    # admingrade_df.to_excel(outfil, index=False)
    return admingrade_df

def combine_AdminGrade_PreviousData_MissingInPerson(admingrade_data,
                                                    previous_data,
                                                    missinginperson_dir,
                                                    init_datestring):
    #previous_data should contain not-in-database info, possibly with other certs
    admingrade_data.sort_values(by=['Admin_ID', 'Last_Name', 'First_Name'],
                                inplace=True, ignore_index=True)
    parsed_admingrade_data = parse_AdminGrade_data(admingrade_data)
    parsed_admingrade_data.sort_values(by=['ID', 'LastName', 'FirstName'],
                                       inplace=True, ignore_index=True)
    previous_data.drop_duplicates(subset = ['ID', 'LastName', 'FirstName'],
                                  keep='first', inplace=True)
    previous_data.reset_index(drop=True, inplace=True)
    previous_data.sort_values(by=['ID', 'LastName', 'FirstName'],
                              inplace=True, ignore_index=True)
    LastNameCap = previous_data['LastName'].str.capitalize()
    FirstNameCap = previous_data['FirstName'].str.capitalize()
    previous_data.drop(['LastName', 'FirstName'], axis=1, inplace=True)
    previous_data['LastName'] = LastNameCap
    previous_data['FirstName'] = FirstNameCap
    
    prev_cat = previous_data['ID'] + '_' + previous_data['LastName'] + '_' +\
        previous_data['FirstName']
    parsed_cat = parsed_admingrade_data['ID'] + '_' +\
        parsed_admingrade_data['LastName'] + '_' +\
        parsed_admingrade_data['FirstName']
    comp3 = prev_cat.isin(parsed_cat)
    prev_in_parsed = previous_data[comp3].copy(deep=True)
    prev_not_in_parsed = previous_data[~comp3].copy(deep=True)
    comp3 = parsed_cat.isin(prev_cat)
    parsed_in_prev = parsed_admingrade_data[comp3].copy(deep=True)
    parsed_not_in_prev = parsed_admingrade_data[~comp3].copy(deep=True)
    prev_in_parsed.reset_index(drop=True, inplace=True)
    prev_not_in_parsed.reset_index(drop=True, inplace=True)
    parsed_in_prev.reset_index(drop=True, inplace=True)
    parsed_not_in_prev.reset_index(drop=True, inplace=True)
    
    #update previous_data values, for rows with matching ID and name in parsed_admingrade_data
    prev_in_parsed.sort_values(by=['ID', 'LastName', 'FirstName'],
                              inplace=True, ignore_index=True)
    parsed_in_prev.sort_values(by=['ID', 'LastName', 'FirstName'],
                              inplace=True, ignore_index=True)
    # outfil = r'C:/Work/misc/ayso/report_inputs/ParsedInPrev.xlsx'
    # parsed_in_prev.to_excel(outfil, index=False)
    # outfil = r'C:/Work/misc/ayso/report_inputs/PrevInParsed.xlsx'
    # prev_in_parsed.to_excel(outfil, index=False)
    for irow in range(prev_in_parsed.shape[0]):
        if parsed_in_prev['U6Coach'][irow] == 'x':
            prev_in_parsed['U6Coach'][irow] = 'x'
        if parsed_in_prev['U8Coach'][irow] == 'x':
            prev_in_parsed['U8Coach'][irow] = 'x'
        if parsed_in_prev['U10Coach'][irow] == 'x':
            if prev_in_parsed['U10Full'][irow] == 'x':
                pass
            elif (prev_in_parsed['U10Online'][irow] == 'x' and
                  prev_in_parsed['U10Field'][irow] == 'x'):
                pass
            elif prev_in_parsed['U10Online'][irow] == 'x':
                prev_in_parsed['U10Field'][irow] = 'x'
            elif prev_in_parsed['U10Field'][irow] == 'x':
                prev_in_parsed['U10Online'][irow] = 'x'
            else:
                prev_in_parsed['U10Full'][irow] = 'x'
        if parsed_in_prev['U12Coach'][irow] == 'x':
            prev_in_parsed['U12Coach'][irow] = 'x'
        if parsed_in_prev['IntCoach'][irow] == 'x':
            prev_in_parsed['IntCoach'][irow] = 'x'
        if parsed_in_prev['IntCoach'][irow] == 'x':
            prev_in_parsed['IntCoach'][irow] = 'x'
        if parsed_in_prev['U8Official'][irow] == 'x':
            prev_in_parsed['U8Official'][irow] = 'x'
        if parsed_in_prev['RegRef'][irow] == 'x':
            prev_in_parsed['RegRef'][irow] = 'x'
        if parsed_in_prev['IntRef'][irow] == 'x':
            prev_in_parsed['IntRef'][irow] = 'x'
        if parsed_in_prev['AdvRef'][irow] == 'x':
            prev_in_parsed['AdvRef'][irow] = 'x'
        if parsed_in_prev['NatRef'][irow] == 'x':
            prev_in_parsed['NatRef'][irow] = 'x'
        prev_in_parsed['Email'][irow] = parsed_in_prev['Email'][irow]
    #combine subset of previous data not needing updating, with subset of previous data that was updated
    prev_data_updated = pd.concat([prev_in_parsed, prev_not_in_parsed], axis=0)
    
    #create blank list to be added as columns to parsed_not_in_prev
    blanklist = []
    for irow in range(parsed_not_in_prev.shape[0]):
        blanklist.append('')
    parsed_not_in_prev['SafeSport'] = blanklist
    parsed_not_in_prev['LiveScan'] = blanklist
    parsed_not_in_prev['SafeHaven'] = blanklist
    parsed_not_in_prev['Concussion'] = blanklist
    parsed_not_in_prev['Cardiac'] = blanklist
    parsed_not_in_prev['U12Pre'] = blanklist
    parsed_not_in_prev['IntPre'] = blanklist
    parsed_not_in_prev['AdvPre'] = blanklist
    #add new volunteers from parsed admingrade data
    prev_data_updated = pd.concat([prev_data_updated, parsed_not_in_prev], axis=0)
    prev_data_updated.sort_values(by=['ID', 'LastName', 'FirstName'],
                                  inplace=True, ignore_index=True)
    prev_data_updated.reset_index(drop=True, inplace=True)
    admingrade_plus_notindb_data = prev_data_updated.copy(deep=True)
    admingrade_plus_notindb_data.sort_values(by=['LastName', 'FirstName', 'ID'],
                                             inplace=True, ignore_index=True)

    #remove in-person certs not showing in etrainu
    certs = ['10U', '12U', 'Int', 'Adv']
    for cert in certs:
        missinginperson_fil = missinginperson_dir + '/Coaches_missing_' +\
            cert + '_InPersonClass.xlsx'
        missinginperson_data = pd.read_excel(missinginperson_fil)
        ID_number = missinginperson_data['Username'].str[5:-8]
        #Have to adjust ID for AYSO.xxxx.learner
        prev_cat = prev_data_updated['ID'] + '_' +\
            prev_data_updated['LastName'] + '_' +\
            prev_data_updated['FirstName']
        missing_cat = ID_number + '_' +\
            missinginperson_data['Surname'] + '_' +\
            missinginperson_data['Firstname']
        comp3 = prev_cat.isin(missing_cat)
        prev_in_missing = prev_data_updated[comp3].copy(deep=True)
        prev_not_in_missing = prev_data_updated[~comp3].copy(deep=True)
        prev_in_missing.reset_index(drop=True, inplace=True)
        prev_not_in_missing.reset_index(drop=True, inplace=True)
        blanklist = []
        for irow in range(prev_in_missing.shape[0]):
            blanklist.append('')
        if cert == '10U':
            prev_in_missing['U10Field'] = blanklist
            prev_in_missing['U10Full'] = blanklist
        elif cert == '12U':
            prev_in_missing['U12Coach'] = blanklist
        elif cert == 'Int':
            prev_in_missing['IntCoach'] = blanklist
        elif cert== 'Adv':
            prev_in_missing['AdvCoach'] = blanklist
        prev_data_updated = pd.concat([prev_in_missing, prev_not_in_missing], axis=0)
        prev_data_updated.reset_index(drop=True, inplace=True)
    
        #add 10U online, 12/Int/Adv Pre from etrainu
        srchstr = missinginperson_dir + '/TrainingStatusReport_' +\
            cert + 'online_' + init_datestring + '*.xlsx'
        summary_online_reports = glob.glob(srchstr)
        if len(summary_online_reports) == 1:
            summary_online_report = summary_online_reports[0]
        else:
            ind_report = select_most_recent_version_of_report(summary_online_reports)
            summary_online_report = summary_online_reports[ind_report]
        online_data = pd.read_excel(summary_online_report)
        ID_number = online_data['Username'].str[5:-8]
        #Have to adjust ID for AYSO.xxxx.learner
        prev_cat = prev_data_updated['ID'] + '_' +\
            prev_data_updated['LastName'] + '_' +\
            prev_data_updated['FirstName']
        online_cat = ID_number + '_' +\
            online_data['Surname'] + '_' +\
            online_data['Firstname']
        comp3 = prev_cat.isin(online_cat)
        prev_in_online = prev_data_updated[comp3].copy(deep=True)
        prev_not_in_online = prev_data_updated[~comp3].copy(deep=True)
        prev_in_online.reset_index(drop=True, inplace=True)
        prev_not_in_online.reset_index(drop=True, inplace=True)
        xlist = []
        for irow in range(prev_in_online.shape[0]):
            xlist.append('x')
        if cert == '10U':
            prev_in_online['U10Online'] = xlist
        elif cert == '12U':
            prev_in_online['U12Pre'] = xlist
        elif cert == 'Int':
            prev_in_online['IntPre'] = xlist
        elif cert == 'Adv':
            prev_in_online['AdvPre'] = xlist
        prev_data_updated = pd.concat([prev_in_online, prev_not_in_online], axis=0)
        prev_data_updated.reset_index(drop=True, inplace=True)
    
        #add inperson from etrainu
        srchstr = missinginperson_dir + '/TrainingStatusReport_' +\
            cert + 'inperson_' + init_datestring + '*.xlsx'
        summary_inperson_reports = glob.glob(srchstr)
        if len(summary_inperson_reports) == 1:
            summary_inperson_report = summary_inperson_reports[0]
        else:
            ind_report = select_most_recent_version_of_report(summary_inperson_reports)
            summary_inperson_report = summary_inperson_reports[ind_report]
        inperson_data = pd.read_excel(summary_inperson_report)
        ID_number = inperson_data['Username'].str[5:-8]
        #Have to adjust ID for AYSO.xxxx.learner
        prev_cat = prev_data_updated['ID'] + '_' +\
            prev_data_updated['LastName'] + '_' +\
            prev_data_updated['FirstName']
        inperson_cat = ID_number + '_' +\
            inperson_data['Surname'] + '_' +\
            inperson_data['Firstname']
        comp3 = prev_cat.isin(inperson_cat)
        prev_in_inperson = prev_data_updated[comp3].copy(deep=True)
        prev_not_in_inperson = prev_data_updated[~comp3].copy(deep=True)
        prev_in_inperson.reset_index(drop=True, inplace=True)
        prev_not_in_inperson.reset_index(drop=True, inplace=True)
        prev_in_inperson.sort_values(by=['ID','LastName','FirstName'],
                                      inplace=True, ignore_index=True)
        comp3 = inperson_cat.isin(prev_cat)
        inperson_in_prev = inperson_data[comp3].copy(deep=True)
        inperson_in_prev.sort_values(by=['Username','Surname','Firstname'],
                                      inplace=True, ignore_index=True)
        xlist = []
        xlist_field = []
        xlist_full = []
        for irow in range(prev_in_inperson.shape[0]):
            xlist.append('x')
            if inperson_in_prev['Course'][irow].lower().find('field') > -1:
                xlist_field.append('x')
                xlist_full.append('')
            else:
                xlist_field.append('')
                xlist_full.append('x')
        if cert == '10U':
            prev_in_inperson['U10Full'] = xlist_full
            prev_in_inperson['U10Field'] = xlist_field
        elif cert == '12U':
            prev_in_inperson['U12Coach'] = xlist
        elif cert == 'Int':
            prev_in_inperson['IntCoach'] = xlist
        elif cert == 'Adv':
            prev_in_inperson['AdvCoach'] = xlist
        prev_data_updated = pd.concat([prev_in_inperson, prev_not_in_inperson], axis=0)
        prev_data_updated.reset_index(drop=True, inplace=True)
    
    modadmingrade_data = prev_data_updated.copy(deep=True)
    modadmingrade_data.sort_values(by=['ID', 'LastName', 'FirstName'],
                                   inplace=True, ignore_index=True)
    return admingrade_plus_notindb_data, modadmingrade_data

def combine_admincred_and_modadmingrade_certs(admincred_data,
                                              modadmingrade_data):
    admincred_data.sort_values(by=['Admin_ID', 'Last_Name', 'First_Name'],
                                inplace=True, ignore_index=True)
    admincred_data['Last_Name'] = admincred_data['Last_Name'].str.capitalize()
    admincred_data['First_Name'] = admincred_data['First_Name'].str.capitalize()
    modadmingrade_data.sort_values(by=['ID', 'LastName', 'FirstName'],
                                    inplace=True, ignore_index=True)
    
    #split volunteers in admincred data into two groups: those in modadmingrade data and those not
    cred_cat = admincred_data['Admin_ID'] + '_' +\
        admincred_data['Last_Name'] + '_' +\
        admincred_data['First_Name']
    modg_cat = modadmingrade_data['ID'] + '_' +\
        modadmingrade_data['LastName'] + '_' +\
        modadmingrade_data['FirstName']
    comp3 = cred_cat.isin(modg_cat)
    cred_in_modg = admincred_data[comp3].copy(deep=True)
    cred_not_in_modg = admincred_data[~comp3].copy(deep=True)
    cred_in_modg.reset_index(drop=True, inplace=True)
    cred_not_in_modg.reset_index(drop=True, inplace=True)
    #split volunteers in modadmingrade data into two groups: those in admincred data and those not
    comp3 = modg_cat.isin(cred_cat)
    modg_in_cred = modadmingrade_data[comp3].copy(deep=True)
    modg_not_in_cred = modadmingrade_data[~comp3].copy(deep=True)
    modg_in_cred.reset_index(drop=True, inplace=True)
    modg_not_in_cred.reset_index(drop=True, inplace=True)
    #sort the volunteers in both groups in the same order in cred_in_modg and modg_in_cred
    cred_in_modg.sort_values(by=['Admin_ID', 'Last_Name', 'First_Name'],
                             inplace=True, ignore_index=True)
    modg_in_cred.sort_values(by=['ID', 'LastName', 'FirstName'],
                             inplace=True, ignore_index=True)
    #some fields appear in both cred and modg, some only in modg, and some only in cred
    #have to combine entries for some fields in cred_in_modg and modg_in_cred
    blanklist = []
    for irow in range(modg_in_cred.shape[0]):
        blanklist.append('')
    ID = cred_in_modg['Admin_ID']
    LastName = cred_in_modg['Last_Name']
    FirstName = cred_in_modg['First_Name']
    Email = cred_in_modg['Email']
    RiskStatus = cred_in_modg['Risk_Status']
    SafeSportC = (cred_in_modg['SafeSport_Verified'] == 'Y')
    LiveScanC = (cred_in_modg['CA_Mandated_Fingerprinting_Verified'] == 'Y')
    SafeHavenC = (cred_in_modg['AYSOs_Safe_Haven_Verified'] =='Y')
    ConcussionC = (cred_in_modg['Concussion_Awareness_Verified'] == 'Y')
    CardiacC = (cred_in_modg['Sudden_Cardiac_Arrest_Verified'] == 'Y')
    SafeSportM = (modg_in_cred['SafeSport'] == 'x')
    LiveScanM = (modg_in_cred['LiveScan'] == 'x')
    SafeHavenM = (modg_in_cred['SafeHaven'] == 'x')
    ConcussionM = (modg_in_cred['Concussion'] == 'x')
    CardiacM = (modg_in_cred['Cardiac'] == 'x')
    SafeSportW = np.where(np.any([SafeSportC, SafeSportM], axis=0))
    LiveScanW = np.where(np.any([LiveScanC, LiveScanM], axis=0))
    SafeHavenW = np.where(np.any([SafeHavenC, SafeHavenM], axis=0))
    ConcussionW = np.where(np.any([ConcussionC, ConcussionM], axis=0))
    CardiacW = np.where(np.any([CardiacC, CardiacM], axis=0))
    SafeSport = np.asarray(blanklist.copy())
    SafeSport[SafeSportW[0]] = 'x'
    SafeSport.tolist()
    LiveScan =np.asarray(blanklist.copy())
    LiveScan[LiveScanW[0]] = 'x'
    SafeHaven = np.asarray(blanklist.copy())
    SafeHaven[SafeHavenW[0]] = 'x'
    SafeHaven.tolist()
    Concussion = np.asarray(blanklist.copy())
    Concussion[ConcussionW[0]] = 'x'
    Concussion.tolist()
    Cardiac = np.asarray(blanklist.copy())
    Cardiac[CardiacW[0]] = 'x'
    Cardiac.tolist()
#    print(SafeHavenB[:20])
    U6Coach = modg_in_cred['U6Coach']
    U8Coach = modg_in_cred['U8Coach']
    U10Online = modg_in_cred['U10Online']
    U10Field = modg_in_cred['U10Field']
    U10Full = modg_in_cred['U10Full']
    U12Coach = modg_in_cred['U12Coach']
    U12Pre = modg_in_cred['U12Pre']
    IntCoach = modg_in_cred['IntCoach']
    IntPre = modg_in_cred['IntPre']
    AdvCoach = modg_in_cred['AdvCoach']
    AdvPre = modg_in_cred['AdvPre']
    U8Official = modg_in_cred['U8Official']
    RegRef = modg_in_cred['RegRef']
    IntRef = modg_in_cred['IntRef']
    AdvRef = modg_in_cred['AdvRef']
    NatRef = modg_in_cred['NatRef']
    CoachLicense = cred_in_modg['Coaching_License_Level']
    RefGrade = cred_in_modg['Referee_Grade']
    
    #add values for cred_not_in_modg
    print('cred_not_in_modg.shape[0] ', cred_not_in_modg.shape[0])
    if cred_not_in_modg.shape[0] > 0:
        blanklist = []
        for irow in range(cred_not_in_modg.shape[0]):
            blanklist.append('')
        ID = np.hstack((ID, cred_not_in_modg['Admin_ID']))
        LastName = np.hstack((LastName, cred_not_in_modg['Last_Name']))
        FirstName = np.hstack((FirstName, cred_not_in_modg['First_Name']))
        Email = np.hstack((Email, cred_not_in_modg['Email']))
        RiskStatus = np.hstack((RiskStatus, cred_not_in_modg['Risk_Status']))
        tmp = np.asarray(blanklist.copy())
        tmp2 = np.where(cred_not_in_modg['SafeSport_Verified'] == 'Y')
        tmp[tmp2[0]] = 'x'
        SafeSport = np.hstack((SafeSport, tmp.tolist()))
        tmp = np.asarray(blanklist.copy())
        tmp2 = np.where(cred_not_in_modg['CA_Mandated_Fingerprinting_Verified'] == 'Y')
        tmp[tmp2[0]] = 'x'
        LiveScan = np.hstack((LiveScan, tmp.tolist()))
        tmp = np.asarray(blanklist.copy())
        tmp2 = np.where(cred_not_in_modg['AYSOs_Safe_Haven_Verified'] == 'Y')
        tmp[tmp2[0]] = 'x'
        SafeHaven = np.hstack((SafeHaven, tmp.tolist()))
        tmp = np.asarray(blanklist.copy())
        tmp2 = np.where(cred_not_in_modg['Concussion_Awareness_Verified'] == 'Y')
        tmp[tmp2[0]] = 'x'
        Concussion = np.hstack((Concussion, tmp.tolist()))
        tmp = np.asarray(blanklist.copy())
        tmp2 = np.where(cred_not_in_modg['Sudden_Cardiac_Arrest_Verified'] == 'Y')
        tmp[tmp2[0]] = 'x'
        Cardiac = np.hstack((Cardiac, tmp.tolist()))
        U6Coach = np.hstack((U6Coach, blanklist))
        U8Coach = np.hstack((U8Coach, blanklist))
        U10Online = np.hstack((U10Online, blanklist))
        U10Field = np.hstack((U10Field, blanklist))
        U10Full = np.hstack((U10Full, blanklist))
        U12Coach = np.hstack((U12Coach, blanklist))
        U12Pre = np.hstack((U12Pre, blanklist))
        IntCoach = np.hstack((IntCoach, blanklist))
        IntPre = np.hstack((IntPre, blanklist))
        AdvCoach = np.hstack((AdvCoach, blanklist))
        AdvPre = np.hstack((AdvPre, blanklist))
        U8Official = np.hstack((U8Official, blanklist))
        RegRef = np.hstack((RegRef, blanklist))
        IntRef = np.hstack((IntRef, blanklist))
        AdvRef = np.hstack((AdvRef, blanklist))
        NatRef = np.hstack((NatRef, blanklist))
        CoachLicense = np.hstack((CoachLicense, cred_not_in_modg['Coaching_License_Level']))
        RefGrade = np.hstack((RefGrade, cred_not_in_modg['Referee_Grade']))
    
    #add values for modg_not_in_cred
    print('modg_not_in_cred.shape[0] ', modg_not_in_cred.shape[0])
    if modg_not_in_cred.shape[0] > 0:
        blanklist = []
        for irow in range(modg_not_in_cred.shape[0]):
            blanklist.append('')
        ID = np.hstack((ID, modg_not_in_cred['ID']))
        LastName = np.hstack((LastName, modg_not_in_cred['LastName']))
        FirstName = np.hstack((FirstName, modg_not_in_cred['FirstName']))
        Email = np.hstack((Email, modg_not_in_cred['Email']))
        RiskStatus = np.hstack((RiskStatus, blanklist))
        SafeSport = np.hstack((SafeSport, modg_not_in_cred['SafeSport']))
        LiveScan = np.hstack((LiveScan, modg_not_in_cred['LiveScan']))
        SafeHaven = np.hstack((SafeHaven, modg_not_in_cred['SafeHaven']))
        Concussion = np.hstack((Concussion, modg_not_in_cred['Concussion']))
        Cardiac = np.hstack((Cardiac, modg_not_in_cred['Cardiac']))
        U6Coach = np.hstack((U6Coach, modg_not_in_cred['U6Coach']))
        U8Coach = np.hstack((U8Coach, modg_not_in_cred['U8Coach']))
        U10Online = np.hstack((U10Online, modg_not_in_cred['U10Online']))
        U10Field = np.hstack((U10Field, modg_not_in_cred['U10Field']))
        U10Full = np.hstack((U10Full, modg_not_in_cred['U10Full']))
        U12Coach = np.hstack((U12Coach, modg_not_in_cred['U12Coach']))
        U12Pre = np.hstack((U12Pre, modg_not_in_cred['U12Pre']))
        IntCoach = np.hstack((IntCoach, modg_not_in_cred['IntCoach']))
        IntPre = np.hstack((IntPre, modg_not_in_cred['IntPre']))
        AdvCoach = np.hstack((AdvCoach, modg_not_in_cred['AdvCoach']))
        AdvPre = np.hstack((AdvPre, modg_not_in_cred['AdvPre']))
        U8Official = np.hstack((U8Official, modg_not_in_cred['U8Official']))
        RegRef = np.hstack((RegRef, modg_not_in_cred['RegRef']))
        IntRef = np.hstack((IntRef, modg_not_in_cred['IntRef']))
        AdvRef = np.hstack((AdvRef, modg_not_in_cred['AdvRef']))
        NatRef = np.hstack((NatRef, modg_not_in_cred['NatRef']))
        CoachLicense = np.hstack((CoachLicense, blanklist))
        RefGrade = np.hstack((RefGrade, blanklist))
    
    combined_certs = {
        'ID': ID,
        'LastName': LastName,
        'FirstName': FirstName,
        'RiskStatus': RiskStatus,
        'SafeSport': SafeSport,
        'LiveScan': LiveScan,
        'SafeHaven': SafeHaven,
        'Concussion': Concussion,
        'Cardiac': Cardiac,
        'U6Coach': U6Coach,
        'U8Coach': U8Coach,
        'U10Online': U10Online,
        'U10Field': U10Field,
        'U10Full': U10Full,
        'U12Coach': U12Coach,
        'U12Pre': U12Pre,
        'IntCoach': IntCoach,
        'IntPre': IntPre,
        'AdvCoach': AdvCoach,
        'AdvPre': AdvPre,
        'U8Official': U8Official,
        'RegRef': RegRef,
        'IntRef': IntRef,
        'AdvRef': AdvRef,
        'NatRef': NatRef,
        'CoachLicense': CoachLicense,
        'RefGrade': RefGrade,
        'Email': Email
        }
    combined_certs_df = pd.DataFrame(combined_certs)
    return combined_certs_df

def parse_data_by_division(cert_df, vol_df, add_df, drop_df, division):
    #concatenate column entries in cert_df for eventual comparison to vol_df
    cert_cat =\
        cert_df['ID'] + '_' + cert_df['LastName'] + '_' + cert_df['FirstName']
    #select columns from vol_df2 that are also in coach add and drop dfs
    vol_df2 =\
        vol_df[['Association_Volunteer_ID', 'Volunteer_Last_Name',
                'Volunteer_First_Name', 'Division_Name']].copy(deep=True)
    #remove birth years from division names in vol_df
    div_tmp = vol_df2['Division_Name'].copy(deep=True)
    for irow in range(len(div_tmp)):
        div_tmp[irow] = div_tmp[irow].split(' ')[0]
    vol_df2['Division_Name'] = div_tmp
    #rename columns in add_df to match vol_df
    add_df2 = add_df.rename(columns={'ID': 'Association_Volunteer_ID',
                                     'LastName': 'Volunteer_Last_Name',
                                     'FirstName': 'Volunteer_First_Name',
                                     'Division': 'Division_Name'})
    #combine vol_df and add_df
    vol_df3 = pd.concat([vol_df2, add_df2])
    #drop duplicates
    vol_df3.drop_duplicates(keep = 'first', inplace=True)
    vol_df3.reset_index(drop=True, inplace=True)
    if division == 'Vol':
        vol_df3.drop_duplicates(subset=['Association_Volunteer_ID',
                                        'Volunteer_Last_Name',
                                        'Volunteer_First_Name'],
                                keep='first', inplace=True)
        vol_df3.reset_index(drop=True, inplace=True)
    #concatenate vol_df3 column entries to compare to drop_df
    vol_cat = vol_df3['Association_Volunteer_ID'] + '_' +\
        vol_df3['Volunteer_Last_Name'] + '_' +\
        vol_df3['Volunteer_First_Name'] + '_' +\
        vol_df3['Division_Name']
    #concatenate drop_df4 column entries
    drop_cat = drop_df['ID'] + '_' + drop_df['LastName'] + '_' +\
        drop_df['FirstName'] + '_' + drop_df['Division']
    #find and remove rows in vol_df3 also in drop_df
    comp4 = vol_cat.isin(drop_cat)
    vol_df4 = vol_df3[~comp4]
    vol_df4.reset_index(drop=True, inplace=True)
    #concatenate entries in vol_df4 for comparison to cert_df
    vol_cat = vol_df4['Association_Volunteer_ID'] + '_' +\
        vol_df4['Volunteer_Last_Name'] + '_' +\
        vol_df4['Volunteer_First_Name']
    comp3 = cert_cat.isin(vol_cat)
    cert_in_vol_df = cert_df[comp3].copy(deep=True)
    cert_in_vol_df.reset_index(drop=True, inplace=True)
    comp3 = vol_cat.isin(cert_cat)
    vol_in_cert_df = vol_df4[comp3].copy(deep=True)
    vol_in_cert_df.reset_index(drop=True, inplace=True)
    vol_not_in_cert_df = vol_df4[~comp3].copy(deep=True)
    vol_not_in_cert_df.reset_index(drop=True, inplace=True)
    cert_in_vol_df.sort_values(by=['ID', 'LastName', 'FirstName'],
                               inplace=True, ignore_index=True)
    vol_in_cert_df.sort_values(by=['Association_Volunteer_ID', 'Volunteer_Last_Name',
                                   'Volunteer_First_Name'],
                               inplace=True, ignore_index=True)

    division_match = []
    if division == 'Vol':
        for irow in range(vol_in_cert_df.shape[0]):
            division_match.append(True)
    elif division == '6UB' or division == '6UG':
        for irow in range(vol_in_cert_df.shape[0]):
            if (vol_in_cert_df['Division_Name'][irow].find(division) > -1 and
                vol_in_cert_df['Division_Name'][irow].find('16U') == -1):
                division_match.append(True)
            else:
                division_match.append(False)
    else:
        for irow in range(vol_in_cert_df.shape[0]):
            if vol_in_cert_df['Division_Name'][irow].find(division) > -1:
                division_match.append(True)
            else:
                division_match.append(False)
    vol_in_cert_and_div = vol_in_cert_df[division_match]
    
    division_match = []
    if division == 'Vol':
        for irow in range(vol_not_in_cert_df.shape[0]):
            division_match.append(True)
    elif division == '6UB' or division == '6UG':
        for irow in range(vol_not_in_cert_df.shape[0]):
            if (vol_not_in_cert_df['Division_Name'][irow].find(division) > -1 and
                vol_not_in_cert_df['Division_Name'][irow].find('16') == -1):
                division_match.append(True)
            else:
                division_match.append(False)
    else:
        for irow in range(vol_not_in_cert_df.shape[0]):
            if vol_not_in_cert_df['Division_Name'][irow].find(division) > -1:
                division_match.append(True)
            else:
                division_match.append(False)
    vol_not_in_cert_and_in_div = vol_not_in_cert_df[division_match]
    
    #select certifications for volunteers in division
    cert_cat = cert_in_vol_df['ID'] + '_' + cert_in_vol_df['LastName'] + '_' +\
        cert_in_vol_df['FirstName']
    vol_cat = vol_in_cert_and_div['Association_Volunteer_ID'] + '_' +\
        vol_in_cert_and_div['Volunteer_Last_Name'] + '_' +\
        vol_in_cert_and_div['Volunteer_First_Name']
    comp3 = cert_cat.isin(vol_cat)
    vol_cert_df = cert_in_vol_df[comp3].copy(deep=True)
    vol_cert_df.reset_index(drop=True, inplace=True)
    
    #add volunteers without certification
    if len(vol_not_in_cert_and_in_div) > 0:
        vol_add =\
            vol_not_in_cert_and_in_div[['Volunteer_Last_Name',
                                        'Volunteer_First_Name']].copy(deep=True)
        vol_add.rename(columns={'Volunteer_Last_Name': 'Last',
                                'Volunteer_First_Name': 'First'},
                       inplace=True)
    
    if division == 'Vol':
        reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                       'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                       'LiveScan', 'RefGrade', 'CoachLicense']].copy()
    elif (division.find('16U') > -1 or division.find('19U') > -1):
        reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                       'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                       'LiveScan', 'AdvCoach', 'AdvPre', 'CoachLicense',
                                       'Email']].copy()
    elif division.find('14U') > -1:
        reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                       'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                       'LiveScan', 'IntCoach', 'IntPre', 'CoachLicense',
                                       'Email']].copy()
    elif division.find('12U') > -1:
        reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                       'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                       'LiveScan', 'U12Coach', 'U12Pre', 'CoachLicense',
                                       'Email']].copy()
    elif division.find('10U') > -1:
        reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                       'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                       'LiveScan', 'U10Online', 'U10Field', 'U10Full', 
                                       'CoachLicense','Email']].copy()
    elif (division.find('7U') > -1 or division.find('8U') > -1):
        reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                       'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                       'LiveScan', 'U8Coach', 'CoachLicense',
                                       'RefGrade','Email']].copy()
    else:
        reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                       'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                       'LiveScan', 'U6Coach', 'CoachLicense',
                                       'Email']].copy()
    reduced_cert_df['SafeHaven'][reduced_cert_df['SafeHaven']=='Y'] = 'x'
    reduced_cert_df['Concussion'][reduced_cert_df['Concussion']=='Y'] = 'x'
    reduced_cert_df['Cardiac'][reduced_cert_df['Cardiac']=='Y'] = 'x'
    reduced_cert_df['SafeSport'][reduced_cert_df['SafeSport']=='Y'] = 'x'
    reduced_cert_df['LiveScan'][reduced_cert_df['LiveScan']=='Y'] = 'x'
    if division != 'Vol':
        VolStatus = []
        for irow in range(reduced_cert_df.shape[0]):
            if (reduced_cert_df['RiskStatus'][irow].lower() == 'green' or
                reduced_cert_df['RiskStatus'][irow].lower() == 'blue'):
                VolStatus.append('x')
            else:
                VolStatus.append('')
        reduced_cert_df.drop('RiskStatus', axis=1, inplace=True)
        reduced_cert_df['VolStatus'] = VolStatus
        temp_cols = reduced_cert_df.columns.tolist()
        new_cols = temp_cols[:2] + temp_cols[-1:] + temp_cols[2:-1]
        reduced_cert_df = reduced_cert_df[new_cols]
    reduced_cert_df.rename(columns={'FirstName': 'First', 'LastName': 'Last'},
                           inplace=True)
    if division != 'Vol':
        reduced_cert_df.rename(columns={'CoachLicense': 'MaxLicense'}, inplace=True)
    if 'vol_add' in locals():
        print('adding ', vol_add.shape[0], ' vols not in certs for ', division)
        # reduced_cert_df = \
        #     reduced_cert_df.append(vol_add, ignore_index=True)
        reduced_cert_df =\
            pd.concat([reduced_cert_df, vol_add], ignore_index=True)
        reduced_cert_df.fillna(' ', inplace=True)
    reduced_cert_df.sort_values(by=['Last', 'First'], 
                                inplace=True, ignore_index=True)
    return reduced_cert_df

def add_vol_data_to_cert_data(cert_df, vol_df):
    #concatenate column entries in cert_df for eventual comparison to vol_df
    cert_df.sort_values(by=['LastName', 'FirstName'], 
                        inplace=True, ignore_index=True)
    vol_df.sort_values(by=['Volunteer_Last_Name', 'Volunteer_First_Name'], 
                       inplace=True, ignore_index=True)
    cert_cat =\
        cert_df['ID'] + '_' + cert_df['LastName'] + '_' + cert_df['FirstName']
    #select columns from vol_df2 that are also in coach add and drop dfs
    vol_df2 =\
        vol_df[['Association_Volunteer_ID', 'Volunteer_Last_Name',
                'Volunteer_First_Name', 'Division_Name',
                'Volunteer_Role']].copy(deep=True)
    #remove birth years from division names in vol_df
    div_tmp = vol_df2['Division_Name'].copy(deep=True)
    for irow in range(len(div_tmp)):
        div_tmp[irow] = div_tmp[irow].split(' ')[0]
    #remove / from division names in vol_df
    for irow in range(len(div_tmp)):
        if div_tmp[irow].find('/') > -1:
            div_tmp[irow] = div_tmp[irow].split('/')[-1]
    vol_df2['Division_Name'] = div_tmp

    current_ID = 'init'
    current_last = 'init'
    current_first = 'init'
    CoachVolDivMax = []
    RefVolDivMax = []
    Youth = []
    FirstName = []
    LastName = []
    ID = []
    current_coachdivmax = 0
    current_refdivmax = 0
    current_youth = False
    for irow in range(vol_df2.shape[0]):
        if (vol_df2['Association_Volunteer_ID'][irow] != current_ID or
            vol_df2['Volunteer_Last_Name'][irow].capitalize() != current_last or
            vol_df2['Volunteer_First_Name'][irow].capitalize() != current_first):
            if irow > 0:
                FirstName.append(current_first)
                LastName.append(current_last)
                ID.append(current_ID)
                CoachVolDivMax.append(current_coachdivmax)
                RefVolDivMax.append(current_refdivmax)
                if current_youth:
                    Youth.append('Y')
                else:
                    Youth.append('')
            current_first = vol_df2['Volunteer_First_Name'][irow].capitalize()
            current_last = vol_df2['Volunteer_Last_Name'][irow].capitalize()
            current_ID = vol_df2['Association_Volunteer_ID'][irow]
            current_div = int(vol_df2['Division_Name'][irow][:-2])
            if vol_df2['Volunteer_Role'][irow].lower().find('coach') > -1:
                current_coachdivmax = current_div
                current_refdivmax = 0
            elif vol_df2['Volunteer_Role'][irow].lower().find('referee') > -1:
                current_coachdivmax = 0
                current_refdivmax = current_div
            else:
                current_coachdivmax = 0
                current_refdivmax = 0
            if vol_df2['Volunteer_Role'][irow].lower().find('youth') > -1:
                current_youth = True
            else:
                current_youth = False
        else:
            if vol_df2['Volunteer_Role'][irow].lower().find('youth') > -1:
                current_youth = True
            if vol_df2['Division_Name'][irow].find('U') > -1:
                current_div = int(vol_df2['Division_Name'][irow][:-2])
                if vol_df2['Volunteer_Role'][irow].lower().find('coach') > -1:
                    current_coachdivmax = max(current_coachdivmax,
                                              current_div)
                elif vol_df2['Volunteer_Role'][irow].lower().find('referee') > -1:
                    current_refdivmax = max(current_refdivmax,
                                            current_div)
    FirstName.append(current_first)
    LastName.append(current_last)
    ID.append(current_ID)
    # if current_coachdivmax == 0:
    #     CoachVolDivMax.append('')
    # else:
    #     CoachVolDivMax.append(str(current_coachdivmax))
    CoachVolDivMax.append(current_coachdivmax)
    # if current_refdivmax == 0:
    #     RefVolDivMax.append('')
    # else:
    #     RefVolDivMax.append(str(current_refdivmax))
    RefVolDivMax.append(current_refdivmax)
    if current_youth:
        Youth.append('Y')
    else:
        Youth.append('')

    vol_certs3 = {
        'FirstName': FirstName,
        'LastName': LastName,
        'ID': ID,
        'CoachVolMax': CoachVolDivMax,
        'RefVolMax': RefVolDivMax,
        'Youth': Youth
        }
    vol_df3 = pd.DataFrame(vol_certs3)

    #concatenate vol_df3 column entries to compare to cert_df
    vol_cat = vol_df3['ID'] + '_' +\
        vol_df3['LastName'] + '_' +\
        vol_df3['FirstName']

    comp3 = cert_cat.isin(vol_cat)
    cert_in_vol_df = cert_df[comp3].copy(deep=True)
    cert_in_vol_df.reset_index(drop=True, inplace=True)
    comp3 = vol_cat.isin(cert_cat)
    vol_in_cert_df = vol_df3[comp3].copy(deep=True)
    vol_in_cert_df.reset_index(drop=True, inplace=True)
    vol_not_in_cert_df = vol_df3[~comp3].copy(deep=True)
    vol_not_in_cert_df.reset_index(drop=True, inplace=True)
    cert_in_vol_df.sort_values(by=['LastName', 'FirstName', 'ID'],
                               inplace=True, ignore_index=True)
    vol_in_cert_df.sort_values(by=['LastName','FirstName', 'ID'],
                               inplace=True, ignore_index=True)
    #add vol info to cert info for volunteers in both
    cert_in_vol_df['CoachVolMax'] = vol_in_cert_df['CoachVolMax']
    cert_in_vol_df['RefVolMax'] = vol_in_cert_df['RefVolMax']
    cert_in_vol_df['Youth'] = vol_in_cert_df['Youth']
    
    vol_cert_df = cert_in_vol_df.copy(deep=True)
    vol_cert_df.reset_index(drop=True, inplace=True)
    
    #add volunteers without certification
    if len(vol_not_in_cert_df) > 0:
        vol_add =\
            vol_not_in_cert_df[['LastName', 'FirstName', 'ID',
                                'CoachVolMax', 'RefVolMax', 'Youth']].copy(deep=True)
    
    reduced_cert_df = vol_cert_df[['FirstName', 'LastName', 'RiskStatus',
                                   'SafeHaven', 'Concussion', 'Cardiac', 'SafeSport', 
                                   'LiveScan', 'RefGrade', 'CoachLicense',
                                   'CoachVolMax', 'RefVolMax', 'Youth',
                                   'Email']].copy(deep=True)
    
    reduced_cert_df['SafeHaven'][reduced_cert_df['SafeHaven']=='Y'] = 'x'
    reduced_cert_df['Concussion'][reduced_cert_df['Concussion']=='Y'] = 'x'
    reduced_cert_df['Cardiac'][reduced_cert_df['Cardiac']=='Y'] = 'x'
    reduced_cert_df['SafeSport'][reduced_cert_df['SafeSport']=='Y'] = 'x'
    reduced_cert_df['LiveScan'][reduced_cert_df['LiveScan']=='Y'] = 'x'

    reduced_cert_df.rename(columns={'FirstName': 'First', 'LastName': 'Last'},
                           inplace=True)
    
    if 'vol_add' in locals():
        print('adding ', vol_add.shape[0], ' vols not in certs for VolPlus')
        # reduced_cert_df = \
        #     reduced_cert_df.append(vol_add, ignore_index=True)
        vol_add.rename(columns={'FirstName': 'First', 'LastName': 'Last'},
                       inplace=True)
        reduced_cert_df =\
            pd.concat([reduced_cert_df, vol_add], ignore_index=True)
        reduced_cert_df.fillna(' ', inplace=True)
    reduced_cert_df.sort_values(by=['Last', 'First'], 
                                inplace=True, ignore_index=True)
    return reduced_cert_df

def add_MBPostal_data_to_cert_data(cert_data, MBPostal_data):
    comp = cert_data['ID'].isin(MBPostal_data['ID'])
    cert2_data = cert_data.copy(deep=True)
    cert2_data['LiveScan'][comp] = 'x'
    return cert2_data

def find_fullcert_6U(x):
    volstat_y = (x['VolStatus'] == 'x')
    safehaven_y = (x['SafeHaven'] == 'x')
    concuss_y = (x['Concussion'] == 'x')
    cardiac_y = (x['Cardiac'] == 'x')
    U6Coach_y = (x['6UCoach'] == 'x')
    comp5 = np.vstack((volstat_y, safehaven_y, concuss_y, cardiac_y, U6Coach_y)).T
    comp5_all = np.all(comp5, axis=1)
    return comp5_all

def find_fullcert_8U(x):
    volstat_y = (x['VolStatus'] == 'x')
    safehaven_y = (x['SafeHaven'] == 'x')
    concuss_y = (x['Concussion'] == 'x')
    cardiac_y = (x['Cardiac'] == 'x')
    U8Coach_y = (x['8UCoach'] == 'x')
    comp5 = np.vstack((volstat_y, safehaven_y, concuss_y, cardiac_y, U8Coach_y)).T
    comp5_all = np.all(comp5, axis=1)
    return comp5_all
    
def find_fullcert_10U(x):
    volstat_y = (x['VolStatus'] == 'x')
    safehaven_y = (x['SafeHaven'] == 'x')
    concuss_y = (x['Concussion'] == 'x')
    cardiac_y = (x['Cardiac'] == 'x')
    safesport_y = (x['SafeSport'] == 'x')
    livescan_y = (x['LiveScan'] == 'x')
    U10Online_y = (x['10UOnline'] == 'x')
    U10Field_y = (x['10UField'] == 'x')
    U10Full_y = (x['10UFull'] == 'x')
    comp2 = np.vstack((U10Online_y, U10Field_y)).T
    comp2_both = np.all(comp2, axis=1)
    comp2 = np.vstack((comp2_both, U10Full_y)).T
    comp3_all = np.any(comp2, axis=1)
    comp7 = np.vstack((volstat_y, safehaven_y, concuss_y, cardiac_y,
                       safesport_y, livescan_y, comp3_all)).T
    comp7_all = np.all(comp7, axis=1)
    return comp7_all

def find_fullcert_12U(x):
    volstat_y = (x['VolStatus'] == 'x')
    safehaven_y = (x['SafeHaven'] == 'x')
    concuss_y = (x['Concussion'] == 'x')
    cardiac_y = (x['Cardiac'] == 'x')
    U12Coach_y = (x['12UCoach'] == 'x')
    safesport_y = (x['SafeSport'] == 'x')
    livescan_y = (x['LiveScan'] == 'x')
    comp7 = np.vstack((volstat_y, safehaven_y, concuss_y, cardiac_y,
                       U12Coach_y, safesport_y, livescan_y)).T
    comp7_all = np.all(comp7, axis=1)
    return comp7_all

def find_fullcert_14U(x):
    volstat_y = (x['VolStatus'] == 'x')
    safehaven_y = (x['SafeHaven'] == 'x')
    concuss_y = (x['Concussion'] == 'x')
    cardiac_y = (x['Cardiac'] == 'x')
    IntCoach_y = (x['IntCoach'] == 'x')
    safesport_y = (x['SafeSport'] == 'x')
    livescan_y = (x['LiveScan'] == 'x')
    comp7 = np.vstack((volstat_y, safehaven_y, concuss_y, cardiac_y,
                       IntCoach_y, safesport_y, livescan_y)).T
    comp7_all = np.all(comp7, axis=1)
    return comp7_all

def find_fullcert_19U(x):
    volstat_y = (x['VolStatus'] == 'x')
    safehaven_y = (x['SafeHaven'] == 'x')
    concuss_y = (x['Concussion'] == 'x')
    cardiac_y = (x['Cardiac'] == 'x')
    AdvCoach_y = (x['AdvCoach'] == 'x')
    safesport_y = (x['SafeSport'] == 'x')
    livescan_y = (x['LiveScan'] == 'x')
    comp7 = np.vstack((volstat_y, safehaven_y, concuss_y, cardiac_y,
                       AdvCoach_y, safesport_y, livescan_y)).T
    comp7_all = np.all(comp7, axis=1)
    return comp7_all

def highlight_df(x):
#    red = f'{"background-color:red"}'
    red = f'{"background-color:#fb2943"}'
#    green = f'{"background-color:#2ca02c"}'
    green = f'{"background-color:#00FF00"}'
    fullcert_y = (x['FullCerts'] == 'x')
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1.loc[fullcert_y,'First'] = green
    df1.loc[fullcert_y,'Last'] = green
    df1.loc[~fullcert_y,'First'] = red
    df1.loc[~fullcert_y,'Last'] = red
    return df1

def generate_coachcerts_report(combined_certs_data, coachdetails_data, coach_adds,
                               coach_drops, season, outputfile):
    U5B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '5UB')
    U5B_data.rename(columns={'U6Coach': '6UCoach'}, inplace=True)
    U5B_data['FullCerts'] = ''
    fullcert_U5B = find_fullcert_6U(U5B_data)
    U5B_data['FullCerts'][fullcert_U5B] = 'x'
    U5B_data = U5B_data.style.apply(highlight_df, axis=None)

    U5G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '5UG')
    U5G_data.rename(columns={'U6Coach': '6UCoach'}, inplace=True)
    U5G_data['FullCerts'] = ''
    fullcert_U5G = find_fullcert_6U(U5G_data)
    U5G_data['FullCerts'][fullcert_U5G] = 'x'
    U5G_data = U5G_data.style.apply(highlight_df, axis=None)
    
    U6B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '6UB')
    U6B_data.rename(columns={'U6Coach': '6UCoach'}, inplace=True)
    U6B_data['FullCerts'] = ''
    fullcert_U6B = find_fullcert_6U(U6B_data)
    U6B_data['FullCerts'][fullcert_U6B] = 'x'
    U6B_data = U6B_data.style.apply(highlight_df, axis=None)
    
    U6G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '6UG')
    U6G_data.rename(columns={'U6Coach': '6UCoach'}, inplace=True)
    U6G_data['FullCerts'] = ''
    fullcert_U6G = find_fullcert_6U(U6G_data)
    U6G_data['FullCerts'][fullcert_U6G] = 'x'
    U6G_data = U6G_data.style.apply(highlight_df, axis=None)
    U7B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '7UB')
    U7B_data.rename(columns={'U8Coach': '8UCoach'}, inplace=True)
    U7B_data['FullCerts'] = ''
    fullcert_U7B = find_fullcert_8U(U7B_data)
    U7B_data['FullCerts'][fullcert_U7B] = 'x'
    U7B_data = U7B_data.style.apply(highlight_df, axis=None)
    U7G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '7UG')
    U7G_data.rename(columns={'U8Coach': '8UCoach'}, inplace=True)
    U7G_data['FullCerts'] = ''
    fullcert_U7G = find_fullcert_8U(U7G_data)
    U7G_data['FullCerts'][fullcert_U7G] = 'x'
    U7G_data = U7G_data.style.apply(highlight_df, axis=None)
    
    U8B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '8UB')
    U8B_data.rename(columns={'U8Coach': '8UCoach'}, inplace=True)
    U8B_data['FullCerts'] = ''
    fullcert_U8B = find_fullcert_8U(U8B_data)
    U8B_data['FullCerts'][fullcert_U8B] = 'x'
    U8B_data = U8B_data.style.apply(highlight_df, axis=None)
    
    U8G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                      coach_adds, coach_drops, '8UG')
    U8G_data.rename(columns={'U8Coach': '8UCoach'}, inplace=True)
    U8G_data['FullCerts'] = ''
    fullcert_U8G = find_fullcert_8U(U8G_data)
    U8G_data['FullCerts'][fullcert_U8G] = 'x'
    U8G_data = U8G_data.style.apply(highlight_df, axis=None)
    
    U10B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                       coach_adds, coach_drops, '10UB')
    U10B_data.rename(columns={'U10Full': '10UFull', 
                              'U10Online': '10UOnline', 
                              'U10Field': '10UField'}, inplace=True)
    U10B_data['FullCerts'] = ''
    fullcert_U10B = find_fullcert_10U(U10B_data)
    U10B_data['FullCerts'][fullcert_U10B] = 'x'
    U10B_data = U10B_data.style.apply(highlight_df, axis=None)
    
    U10G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                       coach_adds, coach_drops, '10UG')
    U10G_data.rename(columns={'U10Full': '10UFull', 
                              'U10Online': '10UOnline', 
                              'U10Field': '10UField'}, inplace=True)
    U10G_data['FullCerts'] = ''
    fullcert_U10G = find_fullcert_10U(U10G_data)
    U10G_data['FullCerts'][fullcert_U10G] = 'x'
    U10G_data = U10G_data.style.apply(highlight_df, axis=None)
    
    U12B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                       coach_adds, coach_drops, '12UB')
    U12B_data.rename(columns={'U12Coach': '12UCoach', 
                              'U12Pre': '12UPre'}, inplace=True)
    U12B_data['FullCerts'] = ''
    fullcert_U12B = find_fullcert_12U(U12B_data)
    U12B_data['FullCerts'][fullcert_U12B] = 'x'
    U12B_data = U12B_data.style.apply(highlight_df, axis=None)
    
    U12G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                       coach_adds, coach_drops, '12UG')
    U12G_data.rename(columns={'U12Coach': '12UCoach', 
                              'U12Pre': '12UPre'}, inplace=True)
    U12G_data['FullCerts'] = ''
    fullcert_U12G = find_fullcert_12U(U12G_data)
    U12G_data['FullCerts'][fullcert_U12G] = 'x'
    U12G_data = U12G_data.style.apply(highlight_df, axis=None)
    
    U14B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                       coach_adds, coach_drops, '14UB')
    U14B_data['FullCerts'] = ''
    fullcert_U14B = find_fullcert_14U(U14B_data)
    U14B_data['FullCerts'][fullcert_U14B] = 'x'
    U14B_data = U14B_data.style.apply(highlight_df, axis=None)
    
    U14G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                       coach_adds, coach_drops, '14UG')
    U14G_data['FullCerts'] = ''
    fullcert_U14G = find_fullcert_14U(U14G_data)
    U14G_data['FullCerts'][fullcert_U14G] = 'x'
    U14G_data = U14G_data.style.apply(highlight_df, axis=None)
    
    if season == 'fall':
        U16B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                           coach_adds, coach_drops, '16UB')
        U16B_data['FullCerts'] = ''
        fullcert_U16B = find_fullcert_19U(U16B_data)
        U16B_data['FullCerts'][fullcert_U16B] = 'x'
        U16B_data = U16B_data.style.apply(highlight_df, axis=None)
        
        U16G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                           coach_adds, coach_drops, '16UG')
        U16G_data['FullCerts'] = ''
        fullcert_U16G = find_fullcert_19U(U16G_data)
        U16G_data['FullCerts'][fullcert_U16G] = 'x'
        U16G_data = U16G_data.style.apply(highlight_df, axis=None)
        
        U19B_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                           coach_adds, coach_drops, '19UB')
        U19B_data['FullCerts'] = ''
        fullcert_U19B = find_fullcert_19U(U19B_data)
        U19B_data['FullCerts'][fullcert_U19B] = 'x'
        U19B_data = U19B_data.style.apply(highlight_df, axis=None)
        
        U19G_data = parse_data_by_division(combined_certs_data, coachdetails_data,
                                           coach_adds, coach_drops, '19UG')
        U19G_data['FullCerts'] = ''
        fullcert_U19G = find_fullcert_19U(U19G_data)
        U19G_data['FullCerts'][fullcert_U19G] = 'x'
        U19G_data = U19G_data.style.apply(highlight_df, axis=None)
    
    with pd.ExcelWriter(outputfile) as writer:
        U5B_data.to_excel(writer, sheet_name='5UB', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','6UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'FullCerts','Email'])
        U5G_data.to_excel(writer, sheet_name='5UG', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','6UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'FullCerts','Email'])
        U6B_data.to_excel(writer, sheet_name='6UB', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','6UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'FullCerts','Email'])
        U6G_data.to_excel(writer, sheet_name='6UG', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','6UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'FullCerts','Email'])
        U7B_data.to_excel(writer, sheet_name='7UB', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','8UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'RefGrade','FullCerts','Email'])
        U7G_data.to_excel(writer, sheet_name='7UG', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','8UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'RefGrade','FullCerts','Email'])
        U8B_data.to_excel(writer, sheet_name='8UB', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','8UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'RefGrade','FullCerts','Email'])
        U8G_data.to_excel(writer, sheet_name='8UG', index=False,
                          columns=['First','Last','VolStatus','SafeHaven',
                                   'Concussion','Cardiac','8UCoach',
                                   'MaxLicense','SafeSport','LiveScan',
                                   'RefGrade','FullCerts','Email'])
        U10B_data.to_excel(writer, sheet_name='10UB', index=False,
                           columns=['First','Last','VolStatus','SafeHaven',
                                    'Concussion','Cardiac','10UFull',
                                    '10UOnline','10UField',
                                    'SafeSport','LiveScan','MaxLicense',
                                    'FullCerts','Email'])
        U10G_data.to_excel(writer, sheet_name='10UG', index=False,
                           columns=['First','Last','VolStatus','SafeHaven',
                                    'Concussion','Cardiac','10UFull',
                                    '10UOnline','10UField',
                                    'SafeSport','LiveScan','MaxLicense',
                                    'FullCerts','Email'])
        U12B_data.to_excel(writer, sheet_name='12UB', index=False,
                           columns=['First','Last','VolStatus','SafeHaven',
                                    'Concussion','Cardiac','12UCoach',
                                    '12UPre',
                                    'SafeSport','LiveScan','MaxLicense',
                                    'FullCerts','Email'])
        U12G_data.to_excel(writer, sheet_name='12UG', index=False,
                           columns=['First','Last','VolStatus','SafeHaven',
                                    'Concussion','Cardiac','12UCoach',
                                    '12UPre',
                                    'SafeSport','LiveScan','MaxLicense',
                                    'FullCerts','Email'])
        U14B_data.to_excel(writer, sheet_name='14UB', index=False,
                           columns=['First','Last','VolStatus','SafeHaven',
                                    'Concussion','Cardiac','IntCoach',
                                    'IntPre',
                                    'SafeSport','LiveScan','MaxLicense',
                                    'FullCerts','Email'])
        U14G_data.to_excel(writer, sheet_name='14UG', index=False,
                           columns=['First','Last','VolStatus','SafeHaven',
                                    'Concussion','Cardiac','IntCoach',
                                    'IntPre',
                                    'SafeSport','LiveScan','MaxLicense',
                                    'FullCerts','Email'])
        if season == 'fall':
            U16B_data.to_excel(writer, sheet_name='16UB', index=False,
                               columns=['First','Last','VolStatus','SafeHaven',
                                        'Concussion','Cardiac','AdvCoach',
                                        'AdvPre',
                                        'SafeSport','LiveScan','MaxLicense',
                                        'FullCerts','Email'])
            U16G_data.to_excel(writer, sheet_name='16UG', index=False,
                               columns=['First','Last','VolStatus','SafeHaven',
                                        'Concussion','Cardiac','AdvCoach',
                                        'AdvPre',
                                        'SafeSport','LiveScan','MaxLicense',
                                        'FullCerts','Email'])
            U19B_data.to_excel(writer, sheet_name='19UB', index=False,
                               columns=['First','Last','VolStatus','SafeHaven',
                                        'Concussion','Cardiac','AdvCoach',
                                        'AdvPre',
                                        'SafeSport','LiveScan','MaxLicense',
                                        'FullCerts','Email'])
            U19G_data.to_excel(writer, sheet_name='19UG', index=False,
                               columns=['First','Last','VolStatus','SafeHaven',
                                        'Concussion','Cardiac','AdvCoach',
                                        'AdvPre',
                                        'SafeSport','LiveScan','MaxLicense',
                                        'FullCerts','Email'])
    
    # writer._save()
    # writer.close()
    return