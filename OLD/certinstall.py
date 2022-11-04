import certifi,requests

if __name__ == '__main__':
    
    try:
        test = requests.get('https://sock.infasys.co.uk')
    except requests.exceptions.SSLError as err:
        print('SSL Error. Adding custom certs to Certifi store...')
        cafile = certifi.where();
        print(f"{cafile}")
        with open('cacerticate.pem', 'rb') as infile:
            customca = infile.read()
        with open(cafile, 'ab') as outfile:
            outfile.write(customca)
        print('That might have worked.')
# with open(cafile, 'ab') as outfile:
#         outfile.write(customca)

