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


class Arancio(BankAccountConfig):
    """ Ing Direct - Conto Corrente Arancio """

    def __init__(self):
        BankAccountConfig.__init__(self)

        self.delimiter = ','
        self.quotechar = '"'
        self.decimal_separator = ','
        self.thousands_separator ='.'
        self.dropped_lines = 1
        self.default_source_account = 'Attività:Attività correnti:Conto corrente'
        self.default_target_account = 'Sbilancio-EUR'
        self.default_memo = ''

    def get_date(self, line):
        s = line[1].split('/')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        ttype = line[2]
        txt = line[3]
        description = "<COMPLETARE>"
        
        if (ttype == "PAGAMENTO CARTA"):
            d = re.compile('^Operazione VPAY.*presso (.*)$')
            g = d.match(txt)
            if g.group(1): description = g.group(1)
            
        elif (ttype == "VS.DISPOSIZIONE"):
            d = re.compile('^BONIFICO DA VOI DISPOSTO .* A FAVORE DI (.*) C\. BENEF.*$')
            g = d.match(txt)
            if g.group(1): description = g.group(1)
            
        elif (ttype == "ACCREDITO BONIFICO"):
            d = re.compile('^Bonifico.* Anagrafica Ordinante (.*) Note.*$')
            g = d.match(txt)
            if g.group(1): description = g.group(1)
            
        elif (ttype == "PRELIEVO CARTA"):
            description = "Prelievo"
            
        elif (ttype == "ADD. RICARICA TELEFONICA"):
            description = "H3G"
            
        return ' '.join(description.split())
        
    def get_memo(self, line):
        memo = line[3]
        return ' '.join(memo.split())

    def get_debit(self, line):
        amount = line[4]
        amount = amount.replace('€', '')
        a = self.get_amount(amount)
        return abs(a) if (a < 0) else 0

    def get_credit(self, line):
        amount = line[4]
        amount = amount.replace('€', '')
        a = self.get_amount(amount)
        return a if (a > 0) else 0
        
    def get_target_account(self, line):
        target = self.default_target_account
        ttype = line[2]
        
        if (ttype == "PRELIEVO CARTA"):
            target = "Attività:Attività correnti:Liquidità"
            
        elif (ttype == "ADD. RICARICA TELEFONICA"):
            target = "Uscite:Servizi Internet"
            
        return target
