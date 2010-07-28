# Import needed modules from the Python Standar Module set
import csv
import re

# The RunOneSimulation() function simulates a multi-year investment in fund that "tracks" the Dow Jones Industrial Average.
# Using daily Dow Jones scores starting in October of 1928 and ending in January of 2010
#   (downloaded from http://finance.yahoo.com/q/hp?s=%5EDJI [see link "Download to Spreadsheet" near the bottom),
#   this routine simulates the investment as described in comments below.
# Lines beginning with ## offer explanatory remarks.
def RunOneSimulation(term_start, term_end, init_balance, monthly_pay, output, include_monthly_contrib=True):
    term_start_str = '01/../' + str(term_start)
    if term_end >= 100:
        term_end = term_end - 100
    term_end_str = '01/../' + format(term_end,'02')
    regex_obj_start = re.compile(term_start_str)
    regex_obj_end = re.compile(term_end_str)
    ## Open the spreadsheet
    index_reader = csv.reader(open('dj_hist_sorted.csv'))
    within_term = False
    balance = float(init_balance)
    trading_days = 0
    new_months = 0
    output_line = []
    ## Evaluate each row in the spreadsheet
    for row in index_reader:
        ## Check the current row's date to see if it begins the investment's first year
        if not within_term:
            if regex_obj_start.match(row[0]) != None:
                within_term = True
                #print('term start: ' + row[0])
                output_line.append(row[0])
                date_chunks = row[0].split('/')
                current_month = date_chunks[0]
        ## Check the current row's date to see if it ends the investment's final year
        if regex_obj_end.match(row[0]) != None:
            if within_term:
                #print('term end: ' + row[0]) #print this date just once
                output_line.append(row[0])
            within_term = False
        ## If the investment period has started, but not yet ended, then
        ##  calculate the growth/decline of the Dow Jones since the previous day, and then
        ##  apply that growth/shrinking to the balance of the investment
        if within_term:
            #apply today's score to balance
            #print('yesterday\'s score: ' + yesterdays_score)
            #print('today\'s score: ' + row[4])
            diff = float(row[4]) - float(yesterdays_score)
            #print('diff: ' + str(diff))
            percent_delta = diff / float(yesterdays_score)
            #print('delta: ' + str(percent_delta))
            if include_monthly_contrib:
                date_chunks = row[0].split('/')
                if current_month != date_chunks[0]:
                    current_month = date_chunks[0]
                    balance = balance + monthly_pay
                    new_months += 1
            balance = balance + (balance * percent_delta)
            trading_days += 1
        yesterdays_score = row[4]
    if include_monthly_contrib:
        output_line.append(str(monthly_pay))
        pay_in = float(init_balance + (monthly_pay * new_months))
    else:
        output_line.append('')
        pay_in = float(init_balance)
    output_line.append(str(trading_days))
    output_line.append('$' + format(pay_in,',.2f'))
    output_line.append('$' + format(init_balance,',.2f'))
    output_line.append('$' + format(balance,',.2f'))
    output_line.append(format(balance / pay_in,',.2f'))
    output.writerow(output_line)
    return balance

## Here are the simulations to be run
##simulations = [
##    ['01/../30','01/../60']
##    , ['01/../35','01/../65']
##    , ['01/../40','01/../70']
##    , ['01/../50','01/../80']
##    , ['01/../55','01/../85']
##    , ['01/../60','01/../90']
##    , ['01/../70','01/../00']
##    , ['01/../71','01/../01']
##    , ['01/../72','01/../02']
##    , ['01/../73','01/../03']
##    , ['01/../74','01/../04']
##    , ['01/../75','01/../05']
##    , ['01/../76','01/../06']
##    , ['01/../77','01/../07']
##    , ['01/../78','01/../08']
##    , ['01/../79','01/../09']
##    , ['01/../80','01/../10']
##]

## Here is the initial balance, and here is the monthly payment for each simulation
init_balance = 0
monthly_pay = 150
invest_length = 30

## Create the output file, and write the column headers in as the first row
output = csv.writer(open('model_monthly-pay.csv', 'w', newline='\n'))
output.writerow(['start', 'end', 'monthly pay', 'trading days', 'total contrib', 'begin balance', 'end balance', 'growth factor'])

under_perform_count = 0
#for term in simulations:
for term in range(29, 81):
    final_balance = RunOneSimulation(term, term+invest_length, init_balance, monthly_pay, output)
    if final_balance < 196000.00:
        under_perform_count += 1
print('there were ' + str(under_perform_count) + ' under-performing periods')
