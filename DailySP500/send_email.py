import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import sys
import os.path

from_addr = "doug.axtell@gmail.com"
preamble = "Today's S&P 500 score"
epilogue = ""
##server_name = "ASPMX.L.GOOGLE.com"
server_name = "smtp.gmail.com"
#server_port = "465"
server_port = "587"

## See http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html for the inspiration on sending to a gmail account using another gmail account to authorize...

class EmailReportManager:
    '''
    This should be used to send test results to concerned testers.
    This classs should be a Singleton. See http://www.python.org/workshops/1997-10/proceedings/savikko.html if you want to enforce this.
    '''

    def __init__( self ):
        self.msg = MIMEMultipart()
        self.msg['From'] = from_addr
        self.msg.preamble = preamble
        self.msg.epilogue = epilogue
        self.to_addrs = []

    # Pass 't' to add a text file, and 'b' to add a binary file.
    def AttachFile( self, file_path, file_type ):
        if file_type == "t":
            attach_handle = open( file_path, "r" )
            attachment = MIMEText( attach_handle.read() )
        elif file_type == "b":
            attachment = MIMEBase( "application", "octet_stream" )
            attach_handle = open( file_path, "rb" )
            attachment.set_payload( attach_handle.read() )
            attachment.add_header( "Content-Disposition", "attachment", filename=os.path.basename( file_path ) )
        else:
            raise TypeError("Invalid type parameter \"" + file_type + "\" was received.")
        attach_handle.close()
        self.msg.attach( attachment )

    def SetSubject( self, subject ):
        self.msg["Subject"] = subject

    # Always set the body before adding any attachements.
    def SetBody( self, body_string ):
        body = MIMEText( body_string )
        self.msg.attach( body )

    # Append additional recipients to the recipients list.
    def AddRecipients( self, recip_list ):
        self.to_addrs = self.to_addrs + recip_list

    def SendMessage( self ):
        try:
            self.msg['To'] = ", ".join( self.to_addrs )
            server = smtplib.SMTP( server_name, server_port )
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('doug.axtell@gmail.com','7-SenyaR-7')
            server.sendmail( from_addr, self.to_addrs, self.msg.as_string() )
            server.quit()
##        except smtplib.SMTPRecipientsRefused, recipients:
##            print "\r\n**** Here are the recipients that were refused: ****"
##            recips = recipients.items()
##            print recips
##            raise RuntimeError, str( recips )
##        except AttributeError, msg:
##            raise RuntimeError, msg
        except:
            raise RuntimeError(str(sys.exc_info()[0]))
