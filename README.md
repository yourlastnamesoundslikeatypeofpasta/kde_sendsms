# kde_sendsms
A quick and hacky CL script to send sms through KDE Connect.

usage: kde_send_sms.py [-h] [-d DEVICE_ID] p m [m ...]

Send an SMS via KDE "kdeconnect-cli --send-sms"

positional arguments:
  p                     The phone number you would like to send an sms to.
  m                     The message you would like to send.

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE_ID, --device_id DEVICE_ID
                        Overide the default device id, and provide your own.
