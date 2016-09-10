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

from bankcsvtoqif.banks.arancio import Arancio

target_account = 'Sbilancio-EUR'

class TestArancioPagCarta(unittest.TestCase):

    def setUp(self):
        self.csv = '"11/05/2016","08/05/2016","PAGAMENTO CARTA","Operazione VPAY del 08/05/2016 alle ore 17:48 con Carta xxxxxxxxxxxx5555 Div=EUR Importo in divisa=29.3 / Importo in Euro=29.3 presso AVANZI AGRICOLA","€ -29,30"'

    def test_can_instantiate(self):
        account_config = Arancio()
        self.assertEqual(type(account_config), Arancio)

    def test_getters(self):
        account_config = Arancio()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 5, 8)
        description = 'AVANZI AGRICOLA'
        memo = 'Operazione VPAY del 08/05/2016 alle ore 17:48 con Carta xxxxxxxxxxxx5555 Div=EUR Importo in divisa=29.3 / Importo in Euro=29.3 presso AVANZI AGRICOLA'
        debit = 29.30
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestArancioBonificoOut(unittest.TestCase):

    def setUp(self):
        self.csv = '"26/08/2016","26/08/2016","VS.DISPOSIZIONE","BONIFICO DA VOI DISPOSTO NOP 02272737401 A FAVORE DI e distribuzione C. BENEF. IT69K0306902117100000009741 NOTE: Corrispettivo pratica n. ***","€ -122,00"'

    def test_can_instantiate(self):
        account_config = Arancio()
        self.assertEqual(type(account_config), Arancio)

    def test_getters(self):
        account_config = Arancio()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 26)
        description = 'e distribuzione'
        memo = 'BONIFICO DA VOI DISPOSTO NOP 02272737401 A FAVORE DI e distribuzione C. BENEF. IT69K0306902117100000009741 NOTE: Corrispettivo pratica n. ***'
        debit = 122
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestArancioBonificoIn(unittest.TestCase):

    def setUp(self):
        self.csv = '"20/07/2016","20/07/2016","ACCREDITO BONIFICO","Bonifico N. *** BIC Ordinante IBSPIT2PXXX Data Ordine Codifica Ordinante IT*** Anagrafica Ordinante XXX GIULIA Note: GIROCONTO","€ 1.500,00"'

    def test_can_instantiate(self):
        account_config = Arancio()
        self.assertEqual(type(account_config), Arancio)

    def test_getters(self):
        account_config = Arancio()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 7, 20)
        description = 'XXX GIULIA'
        memo = 'Bonifico N. *** BIC Ordinante IBSPIT2PXXX Data Ordine Codifica Ordinante IT*** Anagrafica Ordinante XXX GIULIA Note: GIROCONTO'
        debit = 0
        credit = 1500
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestArancioPrelievo(unittest.TestCase):

    def setUp(self):
        self.csv = '"29/07/2016","22/07/2016","PRELIEVO CARTA","Prelievo carta del 22/07/2016 alle ore 00:27 con Carta xxxxxxxxxxxx1111 di Abi Div=EUR Importo in divisa=150 / Importo in Euro=150 presso BCO POPOLARE","€ -150,00"'

    def test_can_instantiate(self):
        account_config = Arancio()
        self.assertEqual(type(account_config), Arancio)

    def test_getters(self):
        account_config = Arancio()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 7, 22)
        description = 'Prelievo'
        memo = 'Prelievo carta del 22/07/2016 alle ore 00:27 con Carta xxxxxxxxxxxx1111 di Abi Div=EUR Importo in divisa=150 / Importo in Euro=150 presso BCO POPOLARE'
        debit = 150
        credit = 0
        target_account = "Attività:Attività correnti:Liquidità"
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestArancioRicarica(unittest.TestCase):

    def setUp(self):
        self.csv = '"30/06/2016","30/06/2016","ADD. RICARICA TELEFONICA","Operazione di ricarica telefonica H3G del numero *** eseguita il 30/06/2016 alle ore 07:02 con Id-transazione ***","€ -20,00"'

    def test_can_instantiate(self):
        account_config = Arancio()
        self.assertEqual(type(account_config), Arancio)

    def test_getters(self):
        account_config = Arancio()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 30)
        description = 'H3G'
        memo = 'Operazione di ricarica telefonica H3G del numero *** eseguita il 30/06/2016 alle ore 07:02 con Id-transazione ***'
        debit = 20
        credit = 0
        target_account = "Uscite:Servizi Internet"
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

