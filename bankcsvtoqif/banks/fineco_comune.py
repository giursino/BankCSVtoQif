# -*- coding: utf-8 -*-


# BankCSVtoQif - Smart conversion of csv files from a bank to qif
# Copyright (C) 2015-2016  Nikolai Nowaczyk
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from bankcsvtoqif.banks import BankAccountConfig
from datetime import datetime
import re


class FinecoComune(BankAccountConfig):
    """ Fineco Bank - Conto Comune """

    def __init__(self):
        BankAccountConfig.__init__(self)

        self.delimiter = ';'
        self.quotechar = '"'
        self.decimal_separator = ','
        self.thousands_separator ='.'
        self.dropped_lines = 7
        self.default_source_account = 'Attività:Attività correnti:Conto corrente'
        self.default_target_account = 'Sbilancio-EUR'
        self.default_memo = ''

    def get_date(self, line):
        s = line[0].split('/')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        ttype = line[3]
        description = "<COMPLETARE>"
        
        if (ttype == "PagoBancomat POS"):
            d = re.compile('^Pag.*presso\: (.*) C[ ]*a[ ]*r[ ]*t[ ]*a.*$')
            g = d.match(line[4])
            if (g is not None) and (g.group(1)): description = g.group(1)
            
            # Rinomino in modo comprensibile: IperCoop
            d = re.compile('^.* 0344 .*$')
            g = d.match(description)
            if (g is not None): description = "IPERCOOP VIGONZA"
            
            
        elif (ttype == "Pagamento Visa Debit"):
            d = re.compile('^(.*)C[ ]*a[ ]*r[ ]*t[ ]*a.*$')
            g = d.match(line[4])
            if (g is not None) and g.group(1): description = g.group(1)

            # Rinomino in modo comprensibile: Pizzalonga
            d = re.compile('^ROLAND FATA.*$')
            g = d.match(description)
            if (g is not None): description = "PIZZALONGA"
            
            
        elif (ttype == "Bonifico SEPA Italia"):
            d = re.compile('^Ben\: (.*) Ins\:.* Cau\: (.*)$|^Ord\: (.*) Ben\:.* Info-Cli\: (.*)$')
            g = d.match(line[4])
            if (g is not None) and g.group(1) and g.group(2): description = g.group(1) + " - " + g.group(2)
            if (g is not None) and g.group(3) and g.group(4): description = g.group(3) + " - " + g.group(4)
            
            
        elif (ttype == "FastPay"):
            description = "Autostrada"
            
        elif (ttype == "Imposta bollo dossier titoli"):
            description = "Fineco"
            
        elif (ttype == "Imposta bollo conto corrente"):
            description = "Fineco"
            
        elif (ttype == "Canone Mensile Conto"):
            description = "Fineco"

        elif (ttype == "Rimborso Canone 2020"):
            description = "Fineco"
            
        elif (ttype == "MaxiPrelievo Banche del Gruppo"):
            description = "Prelievo"
            
        elif (ttype == "Maxiprelievo"):
            description = "Prelievo"
                        
        elif (ttype == "Prelievi Bancomat extra Gruppo"):
            description = "Prelievo"
            
        elif (ttype == "Ricarica telefonica"):
            description = "Ricarica telefonica"
            
        elif (ttype == "SEPA Direct Debit"):
            d = re.compile('^(.*) A[ ]*d[ ]*d[ ]*e[ ]*b[ ]*i[ ]*t[ ]*o[ ]* S[ ]*D[ ]*D[ ]*.*$')
            g = d.match(line[4])
            if (g is not None) and g.group(1): description = g.group(1)
            
            # Rinomino in modo comprensibile: ETRA
            if (description == "ENERGIA TERRITORIO RISOR"): description = "ETRA"
        
        
        elif (ttype == "Giroconto"):
            d = re.compile('^Giroconto (dal|sul) cc n. [0-9]*([0-9]{3}).*01[ -]*(.*)$')
            g = d.match(line[4])
            if (g is not None) and g.group(2) and g.group(3):
                if g.group(2) == "990": description = "Giuseppe" + " - " + g.group(3)
                elif g.group(2) == "660": description = "Giulia" + " - " + g.group(3)
                else: description = g.group(3)
                        
        return ' '.join(description.split())
        
    def get_memo(self, line):
        memo = line[3] + ' - ' + line[4]
        return ' '.join(memo.split())

    def get_debit(self, line):
        return self.get_absolute_amount(line[2])

    def get_credit(self, line):
        return self.get_absolute_amount(line[1])
        
    def get_target_account(self, line):
        target = self.default_target_account
        ttype = line[3]
        
        if (ttype == "FastPay"):
            target = "Uscite:Trasporti"
            
        elif (ttype == "Imposta bollo dossier titoli"):
            target = "Uscite:Servizi:Banca"
            
        elif (ttype == "Imposta bollo conto corrente"):
            target = "Uscite:Servizi:Banca"
            
        elif (ttype == "Canone Mensile Conto"):
            target = "Uscite:Servizi:Banca"

        elif (ttype == "Rimborso Canone 2020"):
            target = "Uscite:Servizi:Banca"
            
        elif (ttype == "MaxiPrelievo Banche del Gruppo"):
            target = "Attività:Attività correnti:Liquidità"
            
        elif (ttype == "Maxiprelievo"):
            target = "Attività:Attività correnti:Liquidità"
                        
        elif (ttype == "Prelievi Bancomat extra Gruppo"):
            target = "Attività:Attività correnti:Liquidità"
            
        elif (ttype == "PagoBancomat POS") or (ttype == "Pagamento Visa Debit"):
            description = self.get_description(line)
            if (description != "<COMPLETARE>"):
                
                # ALI'
                d = re.compile('^A[ ]*L[ ]*I[ ]*\'.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"
            
                # IPERCOOP
                d= re.compile('^I[ ]*P[ ]*E[ ]*R[ ]*C[ ]*O[ ]*O[ ]*P.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"
            
                # IPERCOOP
                d= re.compile('.*344 .*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # COOP
                d= re.compile('.*478 .*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # BRICO
                d = re.compile('B[ ]*R[ ]*I[ ]*C[ ]*O.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ferramenta"
            
                # LEROY
                d = re.compile('L[ ]*E[ ]*R[ ]*O[ ]*Y.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ferramenta"

                # FERRAMENTA
                d = re.compile('FERRAMENTA');
                g = d.match(description);
                if (g is not None): return "Uscite:Ferramenta"
            
                # TIGOTA
                d = re.compile('T[ ]*I[ ]*G[ ]*O[ ]*T[ ]*A.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Casalinghi"
                
                # AUTOST
                d = re.compile('^A[ ]*U[ ]*T[ ]*O[ ]*S[ ]*T.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Trasporti"
                
                # SUPERSTRADA
                d = re.compile('SUPERSTRADA.*$')
                g = d.match(description);
                if (g is not None): return "Uscite:Trasporti"

                # PIZZA
                d = re.compile('(?i)^.*PIZZA.*$')
                g = d.match(description);
                if (g is not None): return "Uscite:Ristorazione"

                # PIZZALONGA
                d= re.compile('^PIZZALONGA.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ristorazione"

                # PIZZALONGA
                d= re.compile('^PADOVA FOOD.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ristorazione"

                # PIZZALONGA
                d= re.compile('^PADOVA HFB.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ristorazione"

                # NAI
                d= re.compile('^NAI SRL.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # MACELLERIA
                d= re.compile('.* MACELLERI[A ].*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # SUPERMERCATO
                d= re.compile('.*SUPERMERCATO.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # PAN BIANCO
                d= re.compile('^PAN BIANCO.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # PANIFICIO
                d= re.compile('^.*PANIFICIO.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # ORTOFRUTTA ROSSO CILIEGIA
                d= re.compile('^BALDON ANGELA.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # MERCATO
                d= re.compile('^FINACOM.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # MERCATO
                d= re.compile('^PIZZOLATO ANTONIO.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # PESCE
                d= re.compile('^GIANNI E MIRCA.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Alimentari"

                # GELATO - SumUp  *LA BOTTEGA D
                d= re.compile('^SumUp.*LA BOTTEGA.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ristorazione"

                # GELATO ANGELA
                d= re.compile('^THE ICELAB.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ristorazione"

                # BIMBOSTORE
                d= re.compile('^PRENATAL.*VIA FRACCALANZA.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Prole:Materiale di consumo"

                # PRENATAL
                d= re.compile('^PRENATAL.*VIA VENEZIA.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Prole:Materiale di consumo"

                # OVIESSE
                d= re.compile('^OVIESSE.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Prole:Abbigliamento"

                # FARMACIA
                d= re.compile('^FARMACIA.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Prole:Salute"

                # FARMACIA LLOYDS
                d= re.compile('.*LLOYDS.*');
                g = d.match(description);
                if (g is not None): return "Uscite:Prole:Salute"

                # NUOTO
                d= re.compile('.*NUOTO.*');
                g = d.match(description);
                if (g is not None): return "Uscite:Prole:Sport"


        elif (ttype == "Bonifico SEPA Italia"):
            
            # Giulia
            d = re.compile('Ord\: FAVARETTO GIULIA Ben\:')
            g = d.match(line[4])
            if (g is not None): return "Entrate:Giulia"
            
            # GSE
            d = re.compile('Ord\: GSE S.P.A. Ben\:')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Elettricità"

            # GSE
            d = re.compile('Ord\: GESTORE DEI SERVIZI ENERGETICI.* Ben\:')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Elettricità"

            # INPS
            d = re.compile('Ord\: INPS')
            g = d.match(line[4])
            if (g is not None): return "Entrate:Contributi Statali"


        elif (ttype == "Giroconto"):
            
            d = re.compile('^Giroconto (dal|sul) cc n. [0-9]*([0-9]{3}).*01[ -]*(.*)$')
            g = d.match(line[4])
            # Giuseppe
            if (g is not None) and g.group(2) and g.group(3) and g.group(2) == "990":
                if  "TRASFERIMENTO" in g.group(3): return "Entrate:Giuseppe"
            # Giulia
            if (g is not None) and g.group(2) and g.group(3) and g.group(2) == "660":
                if  "SPESE COMUNI" in g.group(3): return "Entrate:Giulia"
            
        elif (ttype == "SEPA Direct Debit"):
            
            # Internet
            #d = re.compile('W[ ]*i[ ]*n[ ]*d[ ]*-[ ]*T[ ]*r[ ]*e[ ]*')
            d = re.compile('(?i)WIND[- ]TRE')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Internet"
            
            # Enel
            d = re.compile('^.*E[ ]*L[ ]*E[ ]*T[ ]*T[ ]*R[ ]*I[ ]*C[ ]*O.*$')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Elettricità"

            # Elettricità Sorgenia
            d = re.compile('^.*Sorgenia.*$')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Elettricità"
            
            # Elettricità A2A
            d = re.compile('^.*A2A.*$')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Elettricità"
            
            # Acqua
            d = re.compile('^.*E[ ]*N[ ]*E[ ]*R[ ]*G[ ]*I[ ]*A[ ]*T[ ]*E[ ]*R[ ]*R[ ]*I[ ]*T[ ]*O[ ]*R[ ]*I[ ]*O.*$')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Acqua"
            
            # Acqua
            d = re.compile('.*ETRA.*')
            g = d.match(line[4])
            if (g is not None): return "Uscite:Servizi:Acqua"
            
        return target
