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


class Fineco(BankAccountConfig):
    """ Fineco Bank """

    def __init__(self):
        BankAccountConfig.__init__(self)

        self.delimiter = ','
        self.quotechar = '"'
        self.dropped_lines = 7
        self.default_source_account = 'Attività:Attività correnti:Conto corrente:Fineco C/C'
        self.default_target_account = 'Sbilancio-EUR'
        self.default_memo = ''

    def get_date(self, line):
        s = line[1].split('/')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        ttype = line[4]
        description = "<COMPLETARE>"
        
        if (ttype == "Pagobancomat POS"):
            d = re.compile('^Pag.*presso\: (.*) Carta.*$')
            g = d.match(line[5])
            if (g is not None) and (g.group(1)): description = g.group(1)
            
        elif (ttype == "Pagamenti Visa Debit"):
            d = re.compile('^(.*) Carta.*$')
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
            description = "Bancomat"
            
        elif (ttype == "Prelievi Bancomat extra Gruppo"):
            description = "Bancomat"
            
        elif (ttype == "Ricarica telefonica"):
            description = "Vodafone"
            
        elif (ttype == "Stipendio"):
            description = "Vimar"
            
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
            target = "Uscite:Mobilità:Auto:Autostrada"
            
        elif (ttype == "Imposta di bollo deposito titoli"):
            target = "Uscite:Uscite Bancarie:Tasse"
            
        elif (ttype == "Imposta di Bollo su c/c"):
            target = "Uscite:Uscite Bancarie:Tasse"
            
        elif (ttype == "MaxiPrelievo Banche del Gruppo"):
            target = "Attività:Attività correnti:Liquidità:Portafoglio"
            
        elif (ttype == "Prelievi Bancomat extra Gruppo"):
            target = "Attività:Attività correnti:Liquidità:Portafoglio"
            
        elif (ttype == "Ricarica telefonica"):
            target = "Uscite:Cellulare"
            
        elif (ttype == "Stipendio"):
            target = "Entrate:Entrate Lavorative:Stipendio"
            
        return target
