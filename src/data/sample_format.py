from datetime import datetime
from datetime import date
import re
from pandas import infer_freq


def age_bracket_encoder(age_bracket):
    age_bracket_to_int_dict = {
        '18-24': 1,
        '25-40': 2,
        '41-60': 3,
        '60+': 4,
    }
    if age_bracket in age_bracket_to_int_dict:
        return age_bracket_to_int_dict[age_bracket]
    else:
        return 2 # if null then default to 4

def job_encoder(job):
    job_to_int_dict = {'white-collar': 1, 'blue-collar': 2, 'technician': 3, 'other': 4, 'pink-collar': 5, 'self-employed': 6, 'entrepreneur': 7}
    if job in job_to_int_dict:
        return job_to_int_dict[job]
    else:
        return 4 # if null then default to 4

marital_type_dict = {'married': 1, 'single': 2, 'divorced': 3, 'unknown': 4}

education_to_int_dict = {
    'bachelors': 1,
    'secondary': 2,
    'senior_secondary': 3,
    'masters': 4,
    'unknown': 5,
    'illiterate': 6
}

loan_type_dict = {'yes': 1, 'no': 0, 'unknown': 2}
poutcome_type_dict = {'success': 1, 'failure': 0, 'nonexistent': 2}


def check_date_format(date_str):
    # check if date is in the format dd/mm/yy 
    date_str= str(date_str)
    # Enforce date format check
    # 
    fmt_type_a = '^[0-3][0-9]\/[0-1][0-9]\/[0-9]{2}$' # '%d/%m/%y'
    fmt_type_b = '^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$'# '%Y-%m-%d'
    fmt_type_c = '^[0-9]{4}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'# %Y-%m-%d %H:%M:%S'
    # print(date_str)
    if re.match(fmt_type_a, date_str) is not None:
        data_fmt = datetime.strptime(date_str, '%d/%m/%y')
        return data_fmt
    if re.match(fmt_type_b, date_str) is not None:
        data_fmt = datetime.strptime(date_str, '%Y-%m-%d')
        return data_fmt
    if re.match(fmt_type_c, date_str) is not None:
        data_fmt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return data_fmt
    # if date_str is not in the format, return Today to avoid error    
    return datetime.now().strftime('%Y-%m-%d')

def convert_sample(sample):
    new_sample = {}
    for key in sample.keys():
        if key == 'client_id':
            new_sample[key] = sample[key]
        if key == 'age_bracket':
            new_sample[key] = age_bracket_encoder(sample[key])
        if key == 'job':
            new_sample[key] = job_encoder(sample[key])
        if key == 'marital':
            new_sample[key] = marital_type_dict[sample[key]]
        if key == 'education':
            new_sample[key] = education_to_int_dict[sample[key]]
        if key == 'has_housing_loan':
            new_sample[key] = loan_type_dict[sample[key]]
        if key == 'has_personal_loan':
            new_sample[key] = loan_type_dict[sample[key]]
        if key == 'poutcome': # not used
            new_sample[key] = poutcome_type_dict[sample[key]]
        if key == 'prev_call_duration':
            value = int(sample[key])
            new_sample[key] = value if value < 100000 else 99999
        if key == 'days_since_last_call':
            new_sample[key] = int(sample[key])

        if key == 'num_contacts_prev':
            value = int(sample[key])
            new_sample[key] = value if value < 1000 else 1000

        if key == 'cpi':
            value = float(sample[key])
            new_sample[key] = value if value < 100 else 100

        if key == 'contact_date':
            contact_data_fmt =  check_date_format(sample[key])    
            new_sample['contact_weekday'] =  contact_data_fmt.isoweekday()
            # https://docs.python.org/3/library/datetime.html#datetime.date.isoweekday
    return new_sample
 