import os

# input
#
# 0 Handelsdatum;
# 1 Valutadatum;
# 2 Transaktion;
# 3 Instrumentenart;
# 4 WP-Identifikationsart;
# 5 WP-Identifikation;
# 6 WP-Name;
# 7 Nominale / Stück;
# 8 Kurs / Limit;
# 9 Handelswährung;
# 10 Zahlungswährung;
# 11 Kurswert in Zahlungswährung;
# 12 Summe der eigenen Spesen in Zahlungswährung;
# 13 Summe der fremden Spesen in Zahlungswährung;
# 14 aufgelaufene Stückzinsen in Zahlungswährung;
# 15 bezahlte / erhaltene KESt in Zahlungswährung;
# 16 Endbetrag in Zahlungwährung;
# 17 Währungskurs;
# 18 Börse;
# 19 Status;
# 20 Orderart;
# 21 Gültigkeit;
# 22 Lagerland;
#
# 0          1          2    3     4    5            6                 7      8          9   10  11      12   13   14   15   16      17       18   19                         20    21                    22    
# 31.05.2021;02.06.2021;Kauf;Aktie;Isin;DE0005810055;DEUTSCHE BÖRSE AG;8,0000;133,900000;EUR;EUR;1071,20;2,50;0,75;0,00;0,00;1074,45;1,000000;TGAT;ausgeführt und abgerechnet;Limit;Ultimo laufende Woche;Deutschland;
# ...
# Depotumsätze;Depot: 65415959807;von: 01.01.2021;bis: 17.07.2021;Erzeugt: 17.07.2021 14:16:52;

# output
#
# 0 Date,
# 1 Type,
# 2 Value,
# 3 Transaction Currency,
# 4 Gross Amount,
# 5 Currency Gross Amount,
# 6 Exchange Rate,
# 7 Fees,
# 8 Taxes,
# 9 Shares,
# 10 ISIN,
# 11 WKN,
# 12 Ticker Symbol,
# 13 Security Name,
# 14 Note
#
# 0                1   2          3   4 5 6 7     8    9 10           11     12     13         14
# 2018-01-02T00:00,Buy,"1,047.16",EUR, , , ,10.00,0.00,9,DE0007236101,723610,SIE.DE,Siemens AG,
# ...

class Converter(object):
    def __init__(self, language, separator):
        self.language = language
        self.separator = separator

    def Header(self):
        if self.language == 'de':
            return self.separator.join(['Datum','Typ','Wert','Buchungswährung','Bruttobetrag','Währung Bruttobetrag','Wechselkurs','Gebühren','Steuern','Stück','ISIN','WKN','Ticker-Symbol','Wertpapiername','Notiz','\n'])
        else:
            return self.separator.join(['Date','Type','Value','Transaction Currency','Gross Amount','Currency Gross Amount','Exchange Rate','Fees','Taxes','Shares','ISIN','WKN','Ticker Symbol','Security Name','Note','\n'])

    def Line(self, line):
        cols = line.split(';')
        date = cols[1]
        if 'Kauf' in cols[2]:
            if self.language == 'de':
                type_ = 'Kauf'
            else:
                type_ = 'Buy'
        value = cols[16]
        if self.separator == ',':
            value = value.replace(',','.')                    
        transactionCurrency = cols[10]
        fees = str(float(cols[12].replace(',','.')) + float(cols[13].replace(',','.')))
        if self.separator == ';':
            fees = fees.replace('.',',')              
        taxes = ''
        shares = cols[7]
        if self.separator == ',':
            shares = shares.replace(',','.')
        isin = cols[5]
        wkn = '' #self.ISIN[2:11]
        tickerSymbol = ''
        securityName = cols[6]
        note = cols[22]
        return self.separator.join([date, type_, value, transactionCurrency, '', '', '', fees, taxes, shares, isin, wkn, tickerSymbol, securityName, note, '\n'])


def Hello2Portfolio(inputFilePath, outputFilePath, converter):    
    with open(inputFilePath, encoding='utf-8', errors='ignore') as inputFile:
        with open(outputFilePath, 'w', encoding='utf-8', errors='ignore') as outputFile:   
            for line in inputFile:    
                if 'Handelsdatum;Valutadatum;' in line:
                    outputFile.write(converter.Header())
                elif 'Ausschttung' in line: # 'ue' removed
                    continue
                elif 'Depotumstze;Depot:' in line: # 'ae' removed
                    continue
                elif line == '\n':
                    continue
                else:
                    outputFile.write(converter.Line(line))


def main():
    Hello2Portfolio(os.path.abspath('./Hello/Datenexport.csv'), os.path.abspath('./Portfolio/Datenexport.csv'), Converter('en', ','))
    Hello2Portfolio(os.path.abspath('./Hello/Datenexport.csv'), os.path.abspath('./Portfolio/Datenexport_de.csv'), Converter('de', ';'))

if __name__ == "__main__":
    main()
