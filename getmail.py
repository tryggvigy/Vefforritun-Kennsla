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
import csv
import prettyprint

def abort():
    print(prettyprint.colorize_fail('[!]') + ' Aborting...')
    sys.exit()

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
  parser = argparse.ArgumentParser(
    description="""
      This program fetches email attachments from a specified gmail accounts STARRED folder.
      Emails to fetch can be filtered with some of the flags shown below.
      If no optional flags are used, then all emails from the starred folder are fetched."""
  )
  parser.add_argument('-o','--outdir',
    help='output directory of fetched data.', required=True)
  parser.add_argument('-s','--since',
    help='only fetch attachments newer or equal than give date. ex: 9-Aug-2014', required=False)
  parser.add_argument('-u','--unseen', action='store_true',
    help='only fetch attachments of messages flaged as unseen.', required=False)
  parser._optionals.title = "flag arguments"
  args = vars(parser.parse_args())

  if(args['outdir'].endswith('/')) : #strip away trailing backslash.
    args['outdir'] = args['outdir'][:-1]

  if args['outdir'] not in os.listdir(script_dir):
      print '\nDirectory: '+args['outdir']+' not found.'
      print 'Aborting.'
      return


  # Read gmail credentials from csv file.
  with open('auth.csv', 'rb') as f:
      reader = csv.reader(f)
      auth = list(reader)[0]

  userName = auth[0]
  passwd = auth[1]


  imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
  typ, accountDetails = imapSession.login(userName, passwd)

  # if typ != 'OK':
  #     print 'Not able to sign in!'
  #     raise

  print(prettyprint.colorize_info('[*] ') + accountDetails[0])

  imapSession.select('[Gmail]/Starred')

  if(args["since"] and args["unseen"] == True):
    typ, data = imapSession.search(None, "SINCE", args['since'], "UNSEEN" )
  elif(args["since"]):
    typ, data = imapSession.search(None, "SINCE", args['since'])
  elif(args["unseen"] == True):
    typ, data = imapSession.search(None, "UNSEEN")
  else:
    typ, data = imapSession.search(None, "ALL")

  if(len(data) == 1 and data[0] == ''):
    print(prettyprint.colorize_warning('[!] ') + 'No emails found')
  else:
    print(prettyprint.colorize_info('[*] ') + 'Emails found')


  # if typ != 'OK':
  #     print 'Error searching Inbox.'
  #     raise

  uniqueID = 0 # prevent attachment overwriting if two attachments have the same name.
  should_run_postscript = True
  # Iterating over all emails
  for msgId in data[0].split():
      typ, messageParts = imapSession.fetch(msgId, '(RFC822)')

    #   if typ != 'OK':
    #       print 'Error fetching mail.'
    #       raise

      emailBody = messageParts[0][1]
      mail = email.message_from_string(emailBody)
      for part in mail.walk():
          if part.get_content_maintype() == 'multipart':
              continue
          if part.get('Content-Disposition') is None:
              continue

          fileName = part.get_filename()
          fileName = format_string(fileName)
          fileName = str(uniqueID) +'__'+ fileName
          uniqueID = uniqueID + 1

          if bool(fileName):
              filePath = os.path.join(script_dir, args['outdir'], fileName)
              if not os.path.isfile(filePath) :
                  print(prettyprint.colorize_success('[+] ') + fileName)
                  fp = open(filePath, 'wb')
                  fp.write(part.get_payload(decode=True))
                  fp.close()
              else:
                  print(prettyprint.colorize_fail('[!]') +
                    ' File: ' + fileName + ' already exists in output directory')
                  abort()

  imapSession.close()
  imapSession.logout()
  print(prettyprint.colorize_info('[*]') + ' Done')

if __name__ == '__main__':
  main()
