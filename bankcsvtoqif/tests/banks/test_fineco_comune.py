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

from bankcsvtoqif.banks.fineco_comune import FinecoComune

target_account = 'Sbilancio-EUR'

class TestFinecoFastpay(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10,1";FastPay;Addebito FASTPAY Pedaggi da 01/08/16 al 31/08/16 Numero di pagamenti effettuati: 1"""

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = 'Autostrada'
        memo = 'FastPay - Addebito FASTPAY Pedaggi da 01/08/16 al 31/08/16 Numero di pagamenti effettuati: 1'
        debit = 10.1
        credit = 0
        target_account = 'Uscite:Trasporti'
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
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 5, 27)
        description = 'Prelievo'
        memo = 'Prelievi Bancomat extra Gruppo - Prelevamento Carta N ***** Data operazione 27/5/2016 Ora 13:41'
        debit = 250
        credit = 0
        target_account = 'Attività:Attività correnti:Liquidità'
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
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 1)
        description = 'GIULIA XXX - Saldo cene'
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
        self.csv = """10/06/2016;10/06/2016;"39,3";;Bonifico SEPA Italia;Ord: Ascell Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016"""

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 10)
        description = 'Ascell - RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016'
        memo = 'Bonifico SEPA Italia - Ord: Ascell Ben: XXX GIUSEPPE Dt-Reg: 1 0/06/2016 Banca Ord: ROMAITRRXXX Info: N OTPROVIDED Info-Cli: RIMBORSO - VS. RIF. RICHIESTA E DEL 21 04 2016'
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
        self.csv = """22/06/2016;18/06/2016;;"13,53";Pagamento Visa Debit;REPSOL DISTRIBUTORE    VIGONZA       ITCarta N. *****513Data operazione 18/06/2016"""

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 6, 18)
        description = 'REPSOL DISTRIBUTORE VIGONZA IT'
        memo = 'Pagamento Visa Debit - REPSOL DISTRIBUTORE VIGONZA ITCarta N. *****513Data operazione 18/06/2016'
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
        self.csv = """07/09/2016;07/08/2016;;"10,1";PagoBancomat POS;Pag. del 15/06/17 ora 17:44 presso: SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Car ta N° *****551 Nessuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA"
        memo = "PagoBancomat POS - Pag. del 15/06/17 ora 17:44 presso: SCANAGATT VIA DELL'INDUSTRIA KM. 23 PIANEZZE SAN 36060 ITA Car ta N° *****551 Nessuna Commissione"
        debit = 10.1
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoPOS(unittest.TestCase):

    def setUp(self):
        self.csv = """ "24/06/2017";"23/06/2017";"";"32,5";"PagoBancomat POS";"Pag. del 23/06/17 ora 21:06 presso: ERME S SNC DI RUZZA LUCA & C.   VIA DANTE ALI GHIERI,   VIGONOVO   30030     VE IT Car ta N° *****313 Nessuna Commissione" """


    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 23)
        description = "ERME S SNC DI RUZZA LUCA & C. VIA DANTE ALI GHIERI, VIGONOVO 30030 VE IT"
        memo = "PagoBancomat POS - Pag. del 23/06/17 ora 21:06 presso: ERME S SNC DI RUZZA LUCA & C. VIA DANTE ALI GHIERI, VIGONOVO 30030 VE IT Car ta N° *****313 Nessuna Commissione"
        debit = 32.5
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoRicarica(unittest.TestCase):

    def setUp(self):
        self.csv = """16/06/2017;16/06/2017;;"20";Ricarica telefonica;Ricarica telefonica: XXX Data: 16 /06/17 Ora: 18:08"""
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 16)
        description = "Ricarica telefonica"
        memo = "Ricarica telefonica - Ricarica telefonica: XXX Data: 16 /06/17 Ora: 18:08"
        debit = 20
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoAutostradaVisa(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10,1";Pagamento Visa Debit;AUTOST GRISIGNANO/PADO OVEST         ITCarta N. ***** 513Data operazione 08/06/17"""
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "AUTOST GRISIGNANO/PADO OVEST IT"
        memo = "Pagamento Visa Debit - AUTOST GRISIGNANO/PADO OVEST ITCarta N. ***** 513Data operazione 08/06/17"
        debit = 10.1
        credit = 0
        target_account = 'Uscite:Trasporti'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoAutostradaPos(unittest.TestCase):

    def setUp(self):
        self.csv = """07/09/2016;07/08/2016;;"10,1";PagoBancomat POS;Pag. del 08/06/17 ora 09:29 presso: AUT OST GRISIGNANO/PADO OVEST IT Carta N° *****551 Ne ssuna Commissione"""
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 8, 7)
        description = "AUT OST GRISIGNANO/PADO OVEST IT"
        memo = "PagoBancomat POS - Pag. del 08/06/17 ora 09:29 presso: AUT OST GRISIGNANO/PADO OVEST IT Carta N° *****551 Ne ssuna Commissione"
        debit = 10.1
        credit = 0
        target_account = 'Uscite:Trasporti'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoAliVisa(unittest.TestCase):

    def setUp(self):
        self.csv = """ "16/06/2017";"14/06/2017";"";"5,71";"Pagamento Visa Debit";"ALI'                   NOVENTA PADOV ITCarta N. ***** 134Data operazione 14/06/17" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 14)
        description = "ALI' NOVENTA PADOV IT"
        memo = "Pagamento Visa Debit - ALI' NOVENTA PADOV ITCarta N. ***** 134Data operazione 14/06/17"
        debit = 5.71
        credit = 0
        target_account = 'Uscite:Alimentari'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoAliPos(unittest.TestCase):

    def setUp(self):
        self.csv = """ "06/05/2017";"05/05/2017";"";"5,87";"PagoBancomat POS";"Pag. del 05/05/17 ora 12:48 presso: ALI' -NOVENTA PADOVANA   VIA G.MARCONI 9   NO VENTA PADOV   35027     NF ITA Carta N° *****313 Nessuna Commissione" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 5, 5)
        description = "ALI' -NOVENTA PADOVANA VIA G.MARCONI 9 NO VENTA PADOV 35027 NF ITA"
        memo = "PagoBancomat POS - Pag. del 05/05/17 ora 12:48 presso: ALI' -NOVENTA PADOVANA VIA G.MARCONI 9 NO VENTA PADOV 35027 NF ITA Carta N° *****313 Nessuna Commissione"
        debit = 5.87
        credit = 0
        target_account = 'Uscite:Alimentari'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoIpercoop(unittest.TestCase):

    def setUp(self):
        self.csv = """ "03/05/2017";"02/05/2017";"";"67,13";"PagoBancomat POS";"Pag. del 02/05/17 ora 20:00 presso: IPER COOP VIGONZA 344   V REGIA 86-BUSA   VIG ONZA   35010        ITA Carta N° *****31 3 Nessuna Commissione" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 5, 2)
        description = "IPER COOP VIGONZA 344 V REGIA 86-BUSA VIG ONZA 35010 ITA"
        memo = "PagoBancomat POS - Pag. del 02/05/17 ora 20:00 presso: IPER COOP VIGONZA 344 V REGIA 86-BUSA VIG ONZA 35010 ITA Carta N\xc2\xb0 *****31 3 Nessuna Commissione"
        debit = 67.13
        credit = 0
        target_account = 'Uscite:Alimentari'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoIpercoop2(unittest.TestCase):

    def setUp(self):
        self.csv = """ "03/05/2017";"02/05/2017";"";"67,13";"PagoBancomat POS";"Pag. del 05/07/17 ora 19:32 presso: NEG 0344 IPER VIGONZA   VIA REGIA 86   VIGON ZA   35010        ITA Carta N° *****313 Nessuna Commissione" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 5, 2)
        description = "IPERCOOP VIGONZA"
        memo = "PagoBancomat POS - Pag. del 05/07/17 ora 19:32 presso: NEG 0344 IPER VIGONZA VIA REGIA 86 VIGON ZA 35010 ITA Carta N\xc2\xb0 *****313 Nessuna Commissione"
        debit = 67.13
        credit = 0
        target_account = 'Uscite:Alimentari'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)
        
class TestFinecoBrico(unittest.TestCase):

    def setUp(self):
        self.csv = """ "27/02/2017";"26/02/2017";"";"18,2";"PagoBancomat POS";"Pag. del 26/02/17 ora 15:06 presso: BRICOCENTER PADOVA B1200   VIA VENEZIA 5 3/A   PADOVA   35128        ITA Carta N° *****313 Nessuna commissione" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 2, 26)
        description = "BRICOCENTER PADOVA B1200 VIA VENEZIA 5 3/A PADOVA 35128 ITA"
        memo = "PagoBancomat POS - Pag. del 26/02/17 ora 15:06 presso: BRICOCENTER PADOVA B1200 VIA VENEZIA 5 3/A PADOVA 35128 ITA Carta N\xc2\xb0 *****313 Nessuna commissione"
        debit = 18.2
        credit = 0
        target_account = 'Uscite:Ferramenta'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoLeroy(unittest.TestCase):

    def setUp(self):
        self.csv = """ "06/03/2017";"05/03/2017";"";"6,05";"PagoBancomat POS";"Pag. del 05/03/17 ora 17:29 presso: LEROY MERLIN ITALIA VICE   CC LE PIRAMID I VIA   TORRI DI QUARTESOL   36040 ITA Carta N° *****313 Nessuna commissione" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 3, 5)
        description = "LEROY MERLIN ITALIA VICE CC LE PIRAMID I VIA TORRI DI QUARTESOL 36040 ITA"
        memo = "PagoBancomat POS - Pag. del 05/03/17 ora 17:29 presso: LEROY MERLIN ITALIA VICE CC LE PIRAMID I VIA TORRI DI QUARTESOL 36040 ITA Carta N\xc2\xb0 *****313 Nessuna commissione"
        debit = 6.05
        credit = 0
        target_account = 'Uscite:Ferramenta'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoTigota(unittest.TestCase):

    def setUp(self):
        self.csv = """ "21/02/2017";"20/02/2017";"";"25,9";"PagoBancomat POS";"Pag. del 20/02/17 ora 13:31 presso: TIGOTA   VIA VENEZIA 124   PADOVA   3512 9        ITA Carta N° *****314 Nessuna commissione" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 2, 20)
        description = "TIGOTA VIA VENEZIA 124 PADOVA 3512 9 ITA"
        memo = "PagoBancomat POS - Pag. del 20/02/17 ora 13:31 presso: TIGOTA VIA VENEZIA 124 PADOVA 3512 9 ITA Carta N\xc2\xb0 *****314 Nessuna commissione"
        debit = 25.9
        credit = 0
        target_account = 'Uscite:Casalinghi'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoGiulia(unittest.TestCase):

    def setUp(self):
        self.csv = """ "03/01/2017";"03/01/2017";"5";"";"Bonifico SEPA Italia";"Ord: FAVARETTO GIULIA Ben: GIUSEP PE, GIULIA Dt-Reg: 03/01/2017 Banca Ord: XXX Info: NOTPROVIDED Info-Cli: giroconto su conto comune" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 1, 3)
        description = "FAVARETTO GIULIA - giroconto su conto comune"
        memo = "Bonifico SEPA Italia - Ord: FAVARETTO GIULIA Ben: GIUSEP PE, GIULIA Dt-Reg: 03/01/2017 Banca Ord: XXX Info: NOTPROVIDED Info-Cli: giroconto su conto comune"
        debit = 0
        credit = 5
        target_account = 'Entrate:Giulia'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoGiuseppe(unittest.TestCase):

    def setUp(self):
        self.csv = """ "18/12/2016";"18/12/2016";"5";"";"Giroconto";"Giroconto dal cc n. 1234990 / 01TRASFERIMENTO" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 12, 18)
        description = "Giuseppe - TRASFERIMENTO"
        memo = "Giroconto - Giroconto dal cc n. 1234990 / 01TRASFERIMENTO"
        debit = 0
        credit = 5
        target_account = 'Entrate:Giuseppe'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoGiuseppeErr(unittest.TestCase):

    def setUp(self):
        self.csv = """ "18/12/2016";"18/12/2016";"5";"";"Giroconto";"Giroconto dal cc n. 991234991 / 01PIZZE" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2016, 12, 18)
        description = "PIZZE"
        memo = "Giroconto - Giroconto dal cc n. 991234991 / 01PIZZE"
        debit = 0
        credit = 5
        target_account = 'Sbilancio-EUR'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoInternet(unittest.TestCase):

    def setUp(self):
        self.csv = """ "19/05/2017";"19/05/2017";"";"4,9";"SEPA Direct Debit";"Wind-Tre Addebito SDD fattura a Vs caric o da xxx Mand xxx xxx Per xxx xxx xxx xxx xxx xxx" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 5, 19)
        description = "Wind-Tre"
        memo = "SEPA Direct Debit - Wind-Tre Addebito SDD fattura a Vs caric o da xxx Mand xxx xxx Per xxx xxx xxx xxx xxx xxx"
        debit = 4.9
        credit = 0
        target_account = 'Uscite:Servizi:Internet'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)

class TestFinecoLuce(unittest.TestCase):

    def setUp(self):
        self.csv = """ "28/03/2017";"28/03/2017";"";"2";"SEPA Direct Debit";"SERVIZIO ELETTRICO NAZIONALE Addebito SD D fattura a Vs carico da xxx" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 3, 28)
        description = "SERVIZIO ELETTRICO NAZIONALE"
        memo = "SEPA Direct Debit - SERVIZIO ELETTRICO NAZIONALE Addebito SD D fattura a Vs carico da xxx"
        debit = 2
        credit = 0
        target_account = 'Uscite:Servizi:Elettricità'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)


class TestFinecoGSE(unittest.TestCase):

    def setUp(self):
        self.csv = """ "22/06/2017";"22/06/2017";"1";"";"Bonifico SEPA Italia";"Ord: GSE S.P.A. Ben: FAVARETTO GIULIA Dt -ord: 22/06/2017 Banca Ord: xxx Info-Cli: FT: 2018087" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 22)
        description = "GSE S.P.A. - FT: 2018087"
        memo = "Bonifico SEPA Italia - Ord: GSE S.P.A. Ben: FAVARETTO GIULIA Dt -ord: 22/06/2017 Banca Ord: xxx Info-Cli: FT: 2018087"
        debit = 0
        credit = 1
        target_account = 'Uscite:Servizi:Elettricità'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)


class TestFinecoETRA(unittest.TestCase):

    def setUp(self):
        self.csv = """ "22/06/2017";"22/06/2017";"1";"";"SEPA Direct Debit";"ENERGIA TERRITORIO RISOR Addebito SDD fa ttura a Vs carico da xxx Mand xxx xxx Per XX" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 22)
        description = "ETRA"
        memo = "SEPA Direct Debit - ENERGIA TERRITORIO RISOR Addebito SDD fa ttura a Vs carico da xxx Mand xxx xxx Per XX"
        debit = 0
        credit = 1
        target_account = 'Uscite:Servizi:Acqua'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)


class TestFinecoPizzalonga(unittest.TestCase):

    def setUp(self):
        self.csv = """ "22/06/2017";"22/06/2017";"1";"";"Pagamento Visa Debit";"ROLAND FATA D.I. NOVENTA PADOV IT Carta N. ***** 142 Data operazione 06/10/19" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 22)
        description = "Pizzalonga"
        memo = "Pagamento Visa Debit - ROLAND FATA D.I. NOVENTA PADOV IT Carta N. ***** 142 Data operazione 06/10/19"
        debit = 0
        credit = 1
        target_account = 'Uscite:Ristorazione'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)


class TestFinecoNai(unittest.TestCase):

    def setUp(self):
        self.csv = """ "22/06/2017";"22/06/2017";"1";"";"PagoBancomat POS";"Pag. del 19/10/19 ora 11:44 presso: NAI SRL VIA G. DE MENABUOI PADOVA 35100 ITA Carta N° *****313 Nessuna Commissione" """
        

    def test_can_instantiate(self):
        account_config = FinecoComune()
        self.assertEqual(type(account_config), FinecoComune)

    def test_getters(self):
        account_config = FinecoComune()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2017, 6, 22)
        description = "NAI SRL VIA G. DE MENABUOI PADOVA 35100 ITA"
        memo = "PagoBancomat POS - Pag. del 19/10/19 ora 11:44 presso: NAI SRL VIA G. DE MENABUOI PADOVA 35100 ITA Carta N° *****313 Nessuna Commissione"
        debit = 0
        credit = 1
        target_account = 'Uscite:Alimentari'
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_memo(line), memo)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
        self.assertEqual(account_config.get_target_account(line), target_account)
