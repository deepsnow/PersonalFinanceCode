import urllib.request
import csv
from datetime import datetime
import send_email

## initialize
url = 'http://finance.yahoo.com'
sp_anchor_prefix = '<span class="streaming-datum" id="'
score_anchor_suffix = 'yfs_l10_^gspc">'
delta_anchor_suffix = 'yfs_c10_^gspc">'
percent_anchor_suffix = 'yfs_pp0_^gspc">'
sp_str_esc = 'S&amp;P 500'

def Extract( line, sentinel ):
    score_begin_index = line.find(sentinel) 
    score_end_index = line.find('</span>',score_begin_index)
    return line[score_begin_index + len(sentinel):score_end_index]


## begin: get the S&P 500 score from the Internet
score = ''
delta = ''
percent_delta = ''
html_handle = urllib.request.urlopen(url)
for line in html_handle:
    str_line = str(line)
    str_index = str_line.find(sp_str_esc) # find the line containing today's S&P 500 outcome
    if str_index != -1:
        score = Extract( str_line, sp_anchor_prefix + score_anchor_suffix ) # find the S&P 500 closing score
        delta = Extract( str_line, sp_anchor_prefix + delta_anchor_suffix ) # find the S&P 500 change value
        percent_delta = Extract( str_line, sp_anchor_prefix + percent_anchor_suffix ) # find the S&P 500 percent change

## archive: record the S&P 500 score in a CSV file (a poor man's spreadsheet)
dt_stamp = datetime.now().strftime('%c')
#archiver = csv.writer(open('sp500_archive.csv', 'a'),dialect='excel')
archiver = csv.writer(open('sp500_archive.csv', 'a', newline='\n'))
archiver.writerow([dt_stamp,score,delta,percent_delta])

## notify: send Peter an e-mail the three values
email_mngr = send_email.EmailReportManager()
#email_mngr.SetSubject(dt_stamp + ' ' + score + ' ' + delta + ' ' + percent_delta)
email_mngr.SetSubject(dt_stamp + ' ' + percent_delta)
email_mngr.AddRecipients(['doug.axtell@gmail.com','petercontibrown@gmail.com'])
email_mngr.SendMessage()
