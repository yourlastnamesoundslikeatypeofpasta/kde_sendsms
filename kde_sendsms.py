"""Send an sms with 'kdeconnect-cli --send-sms' """
import argparse
import re
import subprocess
import sys


def print_device_id():
    """
    User chooses a device ID
    return: the device ID
    """
    print('Searching for device ids...')
    device_out, stderr = subprocess.Popen(['kdeconnect-cli', '-l'],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT).communicate()

    device_id = list(re.findall(r'(?::\s)([\w]+)', str(device_out)))
    print('Device IDs On System:')
    for _id in device_id:
        print(f'\t{_id}')


def sendsms(phone_num, sms, d_id=None, bomb=False):
    """
    Send an sms via the kdeconnect-cli --send-sms <sms> --destination <phone_number> --device <device_id> command
    ;param phone_num: The phone number to send the sms to
    ;param sms: The sms to be sent
    ;param bomb: A boolean that indicates whether or not to send one letter at a time
    return: Print statement stating whether or not the sms was sent
    """

    # get the device id
    if not d_id:
        device_out, _ = subprocess.Popen(['kdeconnect-cli', '-l'],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT).communicate()

        # check if device id is correct
        error = str(device_out).startswith('b"error: No such object path')
        if error:
            return False

        d_id = list(re.findall(r'(?::\s)([\w]+)', str(device_out)))[0]
        if not d_id:
            return False

    # send sms
    if bomb:
        sms = list(sms)
        for letter in sms:
            output, _ = subprocess.Popen(['kdeconnect-cli',
                                          '--send-sms', letter,
                                          '--destination', phone_num,
                                          '--device', d_id],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT).communicate()
            error = str(output).startswith('b"error: No such object path')
            if error:
                return False
    else:
        output, _ = subprocess.Popen(['kdeconnect-cli',
                                      '--send-sms', sms,
                                      '--destination', phone_num,
                                      '--device', d_id],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT).communicate()
        error = str(output).startswith('b"error: No such object path')
        if error:
            return False

    print(f'Message sent to {phone_num}')
    return True


def main():
    """
    Parse arguments and sendsms
    :return: None
    """
    parser = argparse.ArgumentParser(description='Send an SMS via KDE "kdeconnect-cli --send-sms"')
    parser.add_argument('phonenumber', metavar='p', type=str,
                        help='The phone number you would like to send an sms to.')
    parser.add_argument('message', metavar='m', type=str, nargs='+',
                        help='The message you would like to send.')
    parser.add_argument('-d', '--device_id',
                        help='Override the default device id, and provide your own.')
    parser.add_argument('-b', '--bomb', type=bool, default=False, const=True, nargs='?',
                        help='Send one letter at a time')

    args = parser.parse_args()
    args.message = ' '.join(args.message)

    if args.device_id:
        # if the user provides a device id
        print(f'Using Device ID: {args.device_id}')
        result = sendsms(args.phonenumber, args.message, args.device_id)
        if not result:
            print('Error: Please verify your Device ID', file=sys.stderr)
            print_device_id()
    else:
        sendsms(args.phonenumber, args.message, bomb=args.bomb)


if __name__ == '__main__':
    main()
