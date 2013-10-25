import os
import sys
import re

sourceFiles = [
    '5k 2012.csv',
    '2012 raffle.csv',
    '2013 gala.csv',
    '2013 raffle tickets.csv',
    'BRK11.csv',
    'Dine for CASA.csv',
    'fashion show.csv',
    'gala donation.csv',
    'general.csv',
    'go blue.csv',
    'note cards.csv',
    'potential donors deleted from Donor perfect.csv'
]


def procesFile(sourceFile):
    print 'Processing {0}'.format(sourceFile)

    expStart = re.compile('^Name/Address,.*')
    expStop = re.compile('^Total Count: ([0-9]*).*,')
    expNameA1 = re.compile('"(.*)\([0-9]*\).*",')
    expNameA2 = re.compile('(.*)\([0-9]*\).*,')
    expLineA1 = re.compile('"(.*)",')
    expLineA2 = re.compile('(?!,)(.*?),')
    expLocation1 = re.compile('(.*),.*([A-Z]{2}).*([0-9]{5}).*')
    expLocation2 = re.compile('(.*),.*([A-Z]{2}).*([0-9]{5}-[0-9]{4}).*')

    itemsExpected = 0
    addressRecords = [ ]
    addressRecord = [ ]

    with open(sourceFile) as f:
        collecting = False
        for line in f:
            if collecting:
                mo = expStop.match(line)
                if mo:
                    print 'Found stop line: {0}'.format(line)
                    itemsExpected = int(mo.group(1))
                    collecting = False
                    break

                mo = expNameA1.match(line) or expNameA2.match(line)
                if mo:
                    if len(addressRecord) > 0:
                        addressRecords.append(addressRecord)
                    name = mo.group(1)[:-1].strip()
                    print 'Found name: {0}'.format(name)
                    addressRecord = [ name ]
                    continue

                mo = expLineA1.match(line) or expLineA2.match(line)
                if mo:
                    address = mo.group(1).strip()
                    mo2 = expLocation1.match(address) or expLocation2.match(address)
                    if mo2:
                        print 'Found address line: {0}'.format(address)
                        addressRecord.append(mo2.group(1).strip())
                        addressRecord.append(mo2.group(2).strip())
                        addressRecord.append(mo2.group(3).strip())
                        addressRecords.append(addressRecord)

                        if len(addressRecord) > 7:
                            print 'WARNING:  Too many lines found in {0}, {1}'.format(sourceFile, addressRecord[0])
                        elif len(addressRecord) < 4:
                            print 'WARNING:  Too few lines found in {0}, {1}'.format(sourceFile, addressRecord[0])

                        addressRecord = [ ]
                        continue

                    else:
                        print 'Found middle line: {0}'.format(address)
                        addressRecord.append(address)
                        continue

                print 'Skipping line: {0}'.format(line)

            elif expStart.match(line):
                print 'Found start line: {0}'.format(line)
                collecting = True

    print 'Finished {0} with {1} items, expected {2} items'.format(sourceFile, len(addressRecords), itemsExpected)
    if len(addressRecords) != itemsExpected:
        print 'WARNING:  Number of records do not match in: {0}'.format(sourceFile)
        
    dataFile = open('processed-{0}'.format(sourceFile), 'wt')
    dataFile.write('"Name 1","Name 2","Name 3","Street Address","Town","State","Zip Code"\n')
    for rec in addressRecords:
        if len(rec) == 5:
            dataFile.write('"",')
            dataFile.write('"",')
        if len(rec) == 6:
            dataFile.write('"",')
        dataFile.write('"' + '","'.join(rec) + '"\n')
    dataFile.close()


def main(argv):
    for sourceFile in sourceFiles:
        procesFile(sourceFile)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
