'''
    Inspired by https://gist.github.com/baali/2633554
    Make sure you have IMAP enabled in your gmail settings.
    Also make sure you change the access for settings for less secure apps to enabled:
    https://www.google.com/settings/security/lesssecureapps
'''

import email, argparse
import getpass, imaplib
import os, sys
import base64, re

#in case of attachments with non-ascii names
def format_string(string):
  encodedStrComponents = re.split('\?',string)

  if(encodedStrComponents[0] == string):
    return string

  base64Str = encodedStr[3]

  uft8Str = base64.b64decode(base64Str).decode('UTF-8')
  return uft8Str

def main():
  script_dir = '.'
  parser = argparse.ArgumentParser(description="""This program fetches email attachments from a specified gmail accounts starred folder.
                                                  Emails to fetch can be filtered with some of the flags shown below.
                                                  If no optional flags are used, then all emails from the starred folder are fetched.
                                                  """)
  parser.add_argument('-o','--outdir', help='output directory of fetched data.', required=True)
  parser.add_argument('-s','--since', help='only fetch attachments newer or equal than give date. ex: 9-Aug-2014', required=False)
  parser.add_argument('-u','--unseen', action='store_true', help='only fetch attachments of messages flaged as unseen.', required=False)
  parser._optionals.title = "flag arguments"
  args = vars(parser.parse_args())

  if(args['outdir'].endswith('/')) : #strip away trailing backslash.
    args['outdir'] = args['outdir'][:-1]

  if args['outdir'] not in os.listdir(script_dir):
      print '\nDirectory: '+args['outdir']+' not found.'
      #os.mkdir(args['outdir'])
      #print 'Creating ./'+args['outdir']+'/'
      print 'Aborting.'
      return


  #userName = raw_input('Enter your Gmail username:')
  #passwd = getpass.getpass('Enter your password: ')
  userName = 'gmail user'
  passwd = 'gmail pass'


  imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
  typ, accountDetails = imapSession.login(userName, passwd)
  print 'OK'
  if typ != 'OK':
      print 'Not able to sign in!'
      raise

  imapSession.select('[Gmail]/Starred')

  if(args["since"] and args["unseen"] == True):
    typ, data = imapSession.search(None, "SINCE", args['since'], "UNSEEN" )
  elif(args["since"]):
    typ, data = imapSession.search(None, "SINCE", args['since'])
  elif(args["unseen"] == True):
    typ, data = imapSession.search(None, "UNSEEN")
  else:
    typ, data = imapSession.search(None, "ALL")

  if typ != 'OK':
      print 'Error searching Inbox.'
      raise

  uniqueID = 0 # this is to prevent attachment overwriting if two attachments have the same name.
  # Iterating over all emails

  for msgId in data[0].split():
      typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
      if typ != 'OK':
          print 'Error fetching mail.'
          raise

      emailBody = messageParts[0][1]
      mail = email.message_from_string(emailBody)
      for part in mail.walk():
          if part.get_content_maintype() == 'multipart':
              # print part.as_string()
              continue
          if part.get('Content-Disposition') is None:
              # print part.as_string()
              continue

          fileName = part.get_filename()
          fileName = format_string(fileName)
          #fileName = str(uniqueID) +'__'+ fileName
          uniqueID = uniqueID + 1

          if bool(fileName):
              filePath = os.path.join(script_dir, args['outdir'], fileName)
              if not os.path.isfile(filePath) :
                  print '[+] '+fileName
                  fp = open(filePath, 'wb')
                  fp.write(part.get_payload(decode=True))
                  fp.close()

  imapSession.close()
  imapSession.logout()
  print 'Done.'

  # run unzip.sh with the given argument in args['outdir'].
  import subprocess

  subprocess.call("./unzip.sh "+args['outdir'] , shell=True)


if __name__ == '__main__':
  main()
