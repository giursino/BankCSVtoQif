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
        self.csv = """07/09/2016;07/08/2016;;"10,1";FastPay;Addebito FASTPAY Pedaggi da 01/08/16 al 31/08/16 Numero di pagamenti effettuati: 1"""

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
        self.csv = """30/05/2016;27/05/2016;;250;Prelievi Bancomat extra Gruppo;Prelevamento Carta N ***** Data operazione 27/5/2016 Ora 13:41"""

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
        self.csv = """01/08/2016;01/08/2016;;38;Bonifico SEPA Italia;Ben: GIULIA XXX Ins: 30/07/2016 11 :42 Da: INTERNET Iban 444444 1111 TransID: 33333 1111 Cau: Saldo cene"""

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
        self.csv = """10/06/2016;10/06/2016;"15.039,3";;Bonifico SEPA Italia;Ord: Ascell Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 10)
        description = 'Ascell'
        memo = 'Bonifico SEPA Italia - Ord: Ascell Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016'
        debit = 0
        credit = 15039.3
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoVisa(unittest.TestCase):

    def setUp(self):
        self.csv = """22/06/2016;18/06/2016;;"13,53";Pagamento Visa Debit;REPSOL DISTRIBUTORE    VIGONZA       IT Carta N. *****513 Data operazione 18/06/2016"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 18)
        description = 'REPSOL DISTRIBUTORE VIGONZA IT'
        memo = 'Pagamento Visa Debit - REPSOL DISTRIBUTORE VIGONZA IT Carta N. *****513 Data operazione 18/06/2016'
        debit = 13.53
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoPOSError(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";PagoBancomat POS;Pag. del 15/06/17 ora 17:44 presso: SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Car ta N° *****551 Nessuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA"
        memo = "PagoBancomat POS - Pag. del 15/06/17 ora 17:44 presso: SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Car ta N° *****551 Nessuna Commissione"
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoPOS(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";PagoBancomat POS;Pag. del 15/06/17 ora 17:44 presso: SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Carta N° *****551 Nessuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA"
        memo = "PagoBancomat POS - Pag. del 15/06/17 ora 17:44 presso: SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Carta N° *****551 Nessuna Commissione"
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoRicarica(unittest.TestCase):

    def setUp(self):
        self.csv = """16/06/2017;16/06/2017;;"20";Ricarica telefonica;Ricarica telefonica: 3488727259 Data: 16 /06/17 Ora: 18:08"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 16)
        description = "Ricarica telefonica"
        memo = "Ricarica telefonica - Ricarica telefonica: 3488727259 Data: 16 /06/17 Ora: 18:08"
        debit = 20
        credit = 0
        target_account = 'Uscite:Cellulare'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)


class TestFinecoFasi1(unittest.TestCase):

    def setUp(self):
        self.csv = """10/06/2016;10/06/2016;"39,3";;Bonifico SEPA Italia;Ord: FASI Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 10)
        description = 'FASIOPEN (Rimborso del 21.04.2016)'
        memo = 'Bonifico SEPA Italia - Ord: FASI Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016'
        debit = 0
        credit = 39.3
        # Rimosso perchè con più persone può andare in passività o in attività
        #target_account = 'Attività:Attività correnti:Denaro Prestato:Anticipo:Fondo di Assistenza Sanitaria'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoFasi2(unittest.TestCase):

    def setUp(self):
        self.csv = """10/06/2016;10/06/2016;"39,3";;Bonifico SEPA Italia;Ord: FASI Ben: XXX GIUSEPPE Dt-ord: 10/12/2019 Banca Ord: BANCA DI CREDITO COOPERAT Info-Cli: RIMBORSO FASIOPEN - VS. RIF. RICHIESTA/E DEL 15/10/2019"""

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 10)
        description = 'FASIOPEN (Rimborso del 15.10.2019)'
        memo = 'Bonifico SEPA Italia - Ord: FASI Ben: XXX GIUSEPPE Dt-ord: 10/12/2019 Banca Ord: BANCA DI CREDITO COOPERAT Info-Cli: RIMBORSO FASIOPEN - VS. RIF. RICHIESTA/E DEL 15/10/2019'
        debit = 0
        credit = 39.3
        # Rimosso perchè con più persone può andare in passività o in attività
        #target_account = 'Attività:Attività correnti:Denaro Prestato:Anticipo:Fondo di Assistenza Sanitaria'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoCarburante1(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";PagoBancomat POS;Pag. del 15/06/17 ora 17:44 presso: STAZIONE_SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Carta N° *****551 Nessuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "STAZIONE SCANAGATTA"
        memo = "PagoBancomat POS - Pag. del 15/06/17 ora 17:44 presso: STAZIONE_SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Carta N° *****551 Nessuna Commissione"
        debit = 10
        credit = 0
        target_account = 'Uscite:Mobilità:Auto:Carburante'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoCarburante2(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";PagoBancomat POS;Pag. del 27/11/19 ora 18:24 presso: STAZIONE SCANAGATT VIA DELL'INDUSTRIA PIANEZZE 36060 ITA Carta N° *****551 Nessuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "STAZIONE SCANAGATTA"
        memo = "PagoBancomat POS - Pag. del 27/11/19 ora 18:24 presso: STAZIONE SCANAGATT VIA DELL'INDUSTRIA PIANEZZE 36060 ITA Carta N° *****551 Nessuna Commissione"
        debit = 10
        credit = 0
        target_account = 'Uscite:Mobilità:Auto:Carburante'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoCarburanteError(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";PagoBancomat POS;Pag. del 15/06/17 ora 17:44 presso: STAZ IONE_SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Carta N° *****551 Nessuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "STAZIONE SCANAGATTA"
        memo = "PagoBancomat POS - Pag. del 15/06/17 ora 17:44 presso: STAZ IONE_SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Carta N° *****551 Nessuna Commissione"
        debit = 10
        credit = 0
        target_account = 'Uscite:Mobilità:Auto:Carburante'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoAutostradaVisa(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";Pagamento Visa Debit;AUTOST GRISIGNANO/PADO OVEST         IT Carta N. ***** 513 Data operazione 08/06/17"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "AUTOST GRISIGNANO/PADO OVEST IT"
        memo = "Pagamento Visa Debit - AUTOST GRISIGNANO/PADO OVEST IT Carta N. ***** 513 Data operazione 08/06/17"
        debit = 10
        credit = 0
        target_account = 'Uscite:Mobilità:Auto:Autostrada'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoAutostradaPos(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";PagoBancomat POS;Pag. del 08/06/17 ora 09:29 presso: AUT OST GRISIGNANO/PADO OVEST IT Carta N° *****551 Ne ssuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "AUT OST GRISIGNANO/PADO OVEST IT"
        memo = "PagoBancomat POS - Pag. del 08/06/17 ora 09:29 presso: AUT OST GRISIGNANO/PADO OVEST IT Carta N° *****551 Ne ssuna Commissione"
        debit = 10
        credit = 0
        target_account = 'Uscite:Mobilità:Auto:Autostrada'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoFarmaciaVisa(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";Pagamento Visa Debit;FARMACIA ALL ANGELO    PADOVA        IT Carta N. ***** 513 Data operazione 04/05/17"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "FARMACIA ALL ANGELO PADOVA IT"
        memo = "Pagamento Visa Debit - FARMACIA ALL ANGELO PADOVA IT Carta N. ***** 513 Data operazione 04/05/17"
        debit = 10
        credit = 0
        target_account = 'Uscite:Sanità:Farmaci'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoFarmaciaPos(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";PagoBancomat POS;Pag. del 04/03/17 ora 10:58 presso: FARMACIA AI DUE GIGLI VIA DANTE 27 P ADOVA 35100 NFTITA Carta N° *****551 Nessuna commissione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "FARMACIA AI DUE GIGLI VIA DANTE 27 P ADOVA 35100 NFTITA"
        memo = "PagoBancomat POS - Pag. del 04/03/17 ora 10:58 presso: FARMACIA AI DUE GIGLI VIA DANTE 27 P ADOVA 35100 NFTITA Carta N° *****551 Nessuna commissione"
        debit = 10
        credit = 0
        target_account = 'Uscite:Sanità:Farmaci'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)
        

class TestFinecoMaxiprelievo(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";Maxiprelievo;Prelevamento carta N° *****        551 Data operazione"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "Bancomat"
        memo = "Maxiprelievo - Prelevamento carta N° ***** 551 Data operazione"
        debit = 10
        credit = 0
        target_account = 'Attività:Attività correnti:Liquidità:Portafoglio'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)


class TestFinecoImpostaBollo(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";Imposta bollo conto corrente;Imposta di bollo di conto corrente del 31.12.2017"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "Fineco"
        memo = "Imposta bollo conto corrente - Imposta di bollo di conto corrente del 31.12.2017"
        debit = 10
        credit = 0
        target_account = 'Uscite:Uscite Bancarie:Tasse'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)


class TestFinecoImpostaBolloTitoli(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";Imposta bollo dossier titoli;Addebito imposta di bollo Dossier"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "Fineco"
        memo = "Imposta bollo dossier titoli - Addebito imposta di bollo Dossier"
        debit = 10
        credit = 0
        target_account = 'Uscite:Uscite Bancarie:Tasse'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)
        

class TestFinecoSEPADirectDebitPaypal(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";SEPA Direct Debit;PayPal (Europe) S.a.r.l. et Cie. S.C.A. Addebito SDD fattura a Vs carico da *** Mand *** Per ***"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "PayPal (Europe) S.a.r.l. et Cie. S.C.A."
        memo = "SEPA Direct Debit - PayPal (Europe) S.a.r.l. et Cie. S.C.A. Addebito SDD fattura a Vs carico da *** Mand *** Per ***"
        target_account = 'Attività:Attività correnti:Conto corrente:Paypal'
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoSEPADirectDebitNormal(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";SEPA Direct Debit;NEXI PAYMENTS SPA Addebito SDD fattura a Vs carico da *** Mand ***"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "NEXI PAYMENTS SPA"
        memo = "SEPA Direct Debit - NEXI PAYMENTS SPA Addebito SDD fattura a Vs carico da *** Mand ***"
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        

class TestFinecoStipendio(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10";Stipendio;Ord: VIMAR SPA Ben: *** Dt-o rd: *** Banca Ord: *** Info-Cli: STIPENDIO ***"""
        

    def test_can_instantiate(self):
        account_config = Fineco()
        self.assertEqual(type(account_config), Fineco)

    def test_getters(self):
        account_config = Fineco()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "Vimar"
        memo = "Stipendio - Ord: VIMAR SPA Ben: *** Dt-o rd: *** Banca Ord: *** Info-Cli: STIPENDIO ***"
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
