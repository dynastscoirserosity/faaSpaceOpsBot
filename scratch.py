import os
import requests
from bs4 import BeautifulSoup

import new_twitter

# download the target page
faa_site = requests.get('https://www.fly.faa.gov/adv/adv_spt.jsp')

# parse the HTML content of the page
soup = BeautifulSoup(faa_site.content, 'html.parser')
find_text = soup.find('pre').get_text()

no_space_ops = 0
if find_text.find('SPACE OPERATION(S)') != -1:
    space_operation = find_text.find('SPACE OPERATION(S)') + 20
elif find_text.find('SPACE OPERATION') != -1:
    space_operation = find_text.find('SPACE OPERATION') + 17
elif find_text.find('LAUNCH/RECOVERY') != -1:
    space_operation = find_text.find('LAUNCH/RECOVERY') + 17
elif find_text.find('LAUNCH/REENTRY') != -1:
    space_operation = find_text.find('LAUNCH/REENTRY') + 16
else:
    no_space_ops = 1

if no_space_ops == 1:
    print('Someone left out space operations!')
    with open('scratchiest.txt', 'w') as new_file:
        new_file.write('')
else:
    if find_text.find('FLIGHT CHECK(S):') == -1:
        flight_check = find_text.find('FLIGHT CHECK:') - 5
    else:
        flight_check = find_text.find('FLIGHT CHECK(S):') - 3

    with open('scratch.txt', 'w') as file:
        x = space_operation
        while space_operation <= x <= flight_check:
            file.write(find_text[x])
            x += 1

    with open('scratch.txt', 'r+') as file:
        with open('scratchier.txt', 'w') as new_file:
            for line in file.readlines():
                if line.strip() == '':
                    new_file.write('\n')
                else:
                    new_file.write(line.lstrip())

    with open('scratchier.txt', 'r+') as file:
        with open('scratchiest.txt', 'w') as new_file:
            for l_no, line in enumerate(file):
                if line.startswith('PRIMARY'):
                    line = line.replace('PRIMARY', '== PRIMARY ==\n')
                    line = line.lstrip()
                    line = line.replace('\t', '', 1)
                    line = line.replace(':', '').replace('\t', ' / ')
                    new_file.write(line)
                elif line.startswith('BACKUP'):
                    line = line.replace('DATES', '')
                    if line.startswith('BACKUPS'):
                        line = line.replace('BACKUPS', '== BACKUP(S) ==\n')
                    elif line.startswith('BACKUP'):
                        line = line.replace('BACKUP', '== BACKUP(S) ==\n')
                    line = line.lstrip()
                    line = line.replace('\t', '', 2)
                    line = line.replace(':', '').replace('\t', ' / ')
                    new_file.write(line)
                elif line.startswith('SPLASHDOWN'):
                    line = line.replace('SPLASHDOWN', '== SPLASHDOWN ==\n')
                    line = line.replace(':', '').replace('\t', ' / ')
                    new_file.write(line)
                elif line.strip() == '':
                    new_file.write('\n')
                else:
                    if l_no == 0:
                        if line == '':
                            print('First line is empty!')
                        else:
                            new_file.write(line.replace('\t', ' / '))
                    else:
                        new_file.write(line.replace('\t', ' / '))
    os.remove('scratch.txt')

    os.remove('scratchier.txt')

new_twitter.run()

os.remove('scratchiest.txt')

