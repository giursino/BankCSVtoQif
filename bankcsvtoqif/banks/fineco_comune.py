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

        self.delimiter = ','
        self.quotechar = '"'
        self.dropped_lines = 7
        self.default_source_account = 'Attività:Attività correnti:Conto corrente'
        self.default_target_account = 'Sbilancio-EUR'
        self.default_memo = ''

    def get_date(self, line):
        s = line[1].split('/')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        ttype = line[4]
        description = "<COMPLETARE>"
        
        if (ttype == "Pagobancomat POS"):
            d = re.compile('^Pag.*presso\: (.*) C[ ]*a[ ]*r[ ]*t[ ]*a.*$')
            g = d.match(line[5])
            if (g is not None) and (g.group(1)): description = g.group(1)
            
        elif (ttype == "Pagamenti Visa Debit"):
            d = re.compile('^(.*) C[ ]*a[ ]*r[ ]*t[ ]*a.*$')
            g = d.match(line[5])
            if (g is not None) and g.group(1): description = g.group(1)
            
        elif (ttype == "Bonifico SEPA Italia"):
            d = re.compile('^Ben\: (.*) Ins\:.*$|^Ord\: (.*) Ben\:.*$')
            g = d.match(line[5])
            if (g is not None) and g.group(1): description = g.group(1)
            if (g is not None) and g.group(2): description = g.group(2)
            
        elif (ttype == "FastPay"):
            description = "Autostrada"
            
        elif (ttype == "Imposta di bollo deposito titoli"):
            description = "Fineco"
            
        elif (ttype == "Imposta di Bollo su c/c"):
            description = "Fineco"
            
        elif (ttype == "MaxiPrelievo Banche del Gruppo"):
            description = "Prelievo"
            
        elif (ttype == "Prelievi Bancomat extra Gruppo"):
            description = "Prelievo"
            
        elif (ttype == "Ricarica telefonica"):
            description = "Ricarica telefonica"
            
        elif (ttype == "Sepa Direct Debit"):
            d = re.compile('^(.*) A[ ]*d[ ]*d[ ]*e[ ]*b[ ]*i[ ]*t[ ]*o[ ]* S[ ]*D[ ]*D[ ]*.*$')
            g = d.match(line[5])
            if (g is not None) and g.group(1): description = g.group(1)
        
        elif (ttype == "Giroconto"):
            d = re.compile('^Giroconto (dal|sul) cc n. [0-9]{4}990.*01[ -]*.*$')
            g = d.match(line[5])
            if (g is not None): description = "Giuseppe"
                        
        return ' '.join(description.split())
        
    def get_memo(self, line):
        memo = line[4] + ' - ' + line[5]
        return ' '.join(memo.split())

    def get_debit(self, line):
        return float(line[3]) if line[3] else 0

    def get_credit(self, line):
        return float(line[2]) if line[2] else 0
        
    def get_target_account(self, line):
        target = self.default_target_account
        ttype = line[4]
        
        if (ttype == "FastPay"):
            target = "Uscite:Trasporti"
            
        elif (ttype == "Imposta di bollo deposito titoli"):
            target = "Uscite:Servizi:Banca"
            
        elif (ttype == "Imposta di Bollo su c/c"):
            target = "Uscite:Servizi:Banca"
            
        elif (ttype == "MaxiPrelievo Banche del Gruppo"):
            target = "Attività:Attività correnti:Liquidità"
            
        elif (ttype == "Prelievi Bancomat extra Gruppo"):
            target = "Attività:Attività correnti:Liquidità"
            
        elif (ttype == "Pagobancomat POS") or (ttype == "Pagamenti Visa Debit"):
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
            
                # BRICO
                d = re.compile('B[ ]*R[ ]*I[ ]*C[ ]*O.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Ferramenta"
            
                # LEROY
                d = re.compile('L[ ]*E[ ]*R[ ]*O[ ]*Y.*$');
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
            
        elif (ttype == "Bonifico SEPA Italia"):
            
            # Giulia
            d = re.compile('Ord\: FAVARETTO GIULIA Ben\:')
            g = d.match(line[5])
            if (g is not None): return "Entrate:Giulia"
            
            # GSE
            d = re.compile('Ord\: GSE S.P.A. Ben\:')
            g = d.match(line[5])
            if (g is not None): return "Uscite:Servizi:Elettricità"
                        
        elif (ttype == "Giroconto"):
            
            # Giuseppe
            d = re.compile('^Giroconto dal cc n. [0-9]{4}990.*01[ -]*.*$')
            g = d.match(line[5])
            if (g is not None): return "Entrate:Giuseppe"
            
        elif (ttype == "Sepa Direct Debit"):
            
            # Internet
            d = re.compile('W[ ]*i[ ]*n[ ]*d[ ]*-[ ]*T[ ]*r[ ]*e[ ]*')
            g = d.match(line[5])
            if (g is not None): return "Uscite:Servizi:Internet"
            
            # Enel
            d = re.compile('^.*E[ ]*L[ ]*E[ ]*T[ ]*T[ ]*R[ ]*I[ ]*C[ ]*O.*$')
            g = d.match(line[5])
            if (g is not None): return "Uscite:Servizi:Elettricità"
            
                
        return target
