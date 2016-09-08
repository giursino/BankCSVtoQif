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

import unittest
from datetime import datetime
from bankcsvtoqif.tests.banks import csvline_to_line

from bankcsvtoqif.banks.fineco import Fineco

target_account = 'Sbilancio-EUR'

class TestFinecoFastpay(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016,07/08/2016,,"10.1",FastPay,Addebito FASTPAY Pedaggi da 01/08/16 al 31/08/16 Numero di pagamenti effettuati: 1"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = 'Autostrada'
        memo = 'FastPay - Addebito FASTPAY Pedaggi da 01/08/16 al 31/08/16 Numero di pagamenti effettuati: 1'
        debit = 10.1
        credit = 0
        target_account = 'Uscite:Mobilità:Auto:Autostrada'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoPrelievo(unittest.TestCase):

    def setUp(self):
        self.csv = """30/05/2016,27/05/2016,,250,Prelievi Bancomat extra Gruppo,Prelevamento Carta N ***** Data operazione 27/5/2016 Ora 13:41"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 5, 27)
        description = 'Bancomat'
        memo = 'Prelievi Bancomat extra Gruppo - Prelevamento Carta N ***** Data operazione 27/5/2016 Ora 13:41'
        debit = 250
        credit = 0
        target_account = 'Attività:Attività correnti:Liquidità:Portafoglio'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoBonificoOut(unittest.TestCase):

    def setUp(self):
        self.csv = """01/08/2016,01/08/2016,,38,Bonifico SEPA Italia,Ben: GIULIA XXX Ins: 30/07/2016 11 :42 Da: INTERNET Iban 444444 1111 TransID: 33333 1111 Cau: Saldo cene"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 1)
        description = 'GIULIA XXX'
        memo = 'Bonifico SEPA Italia - Ben: GIULIA XXX Ins: 30/07/2016 11 :42 Da: INTERNET Iban 444444 1111 TransID: 33333 1111 Cau: Saldo cene'
        debit = 38
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoBonificoIn(unittest.TestCase):

    def setUp(self):
        self.csv = """10/06/2016,10/06/2016,"39.3",,Bonifico SEPA Italia,Ord: FASI Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 10)
        description = 'FASI'
        memo = 'Bonifico SEPA Italia - Ord: FASI Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016'
        debit = 0
        credit = 39.3
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoVisa(unittest.TestCase):

    def setUp(self):
        self.csv = """22/06/2016,18/06/2016,,"13.53",Pagamenti Visa Debit,REPSOL DISTRIBUTORE    VIGONZA       IT Carta N. *****513 Data operazione 18/06/2016"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 18)
        description = 'REPSOL DISTRIBUTORE VIGONZA IT'
        memo = 'Pagamenti Visa Debit - REPSOL DISTRIBUTORE VIGONZA IT Carta N. *****513 Data operazione 18/06/2016'
        debit = 13.53
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)
