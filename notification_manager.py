# https://www.youtube.com/watch?v=g_j6ILT-X0k
from email.message import EmailMessage
import smtplib

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.sender = 'nspotts7@gmail.com'
        self.app_password = "qwqv iybb gdlm jdnz"
        
    def send_message(self, msg: str, trigger: str=False):
      # for backwards compatibility
      self.send_email(msg=msg)
      
    def send_email(self, msg:str, subject:str="Automated Email", recipient:str="nathan_spotts@hotmail.com", is_html:bool=False):
        em = EmailMessage()
        em['From'] = self.sender
        em['To'] = recipient
        em['Subject'] = subject
        # print(em.get_default_type())
        # print(em.get_content_subtype())
        subtype = 'plain'
        if is_html:
            subtype = 'html'
        em.set_content(msg, subtype=subtype)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(self.sender, self.app_password)
                smtp_server.sendmail(self.sender, recipient, em.as_string())
            print('Message Sent!')
        except Exception as e:
            print(e)
            
             
if __name__ == "__main__":
    nm = NotificationManager()
    
    # sample html email
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
          h1{font-size:56px}
          h2{font-size:28px;font-weight:900}
          p{font-weight:100}
          td{vertical-align:top}
          #email{margin:auto;width:600px;background-color:#fff}
        </style>
    </head>
    <body bgcolor="#F5F8FA" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
    <div id="email">
        <table role="presentation" width="100%">
            <tr>
                <td bgcolor="#00A4BD" align="center" style="color: white;">
                    <h1> Welcome!</h1>
                </td>
        </table>
        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
            <tr>
                <td>
                    <h2>Custom stylized email</h2>
                    <p>
                        You can add HTML/CSS code here to stylize your emails.
                    </p>
                </td>
            </tr>
        </table>
    </div>
    </body>
    </html>
    '''
    
    # sample plain text email
    text = "Test Text"
    
    nm.send_email(html, "Email Subject", "nathan_spotts@hotmail.com", is_html=True)