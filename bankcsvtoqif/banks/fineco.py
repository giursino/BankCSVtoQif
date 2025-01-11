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

        self.delimiter = ';'
        self.quotechar = '"'
        self.decimal_separator = ','
        self.thousands_separator ='.'
        self.dropped_lines = 7
        self.default_source_account = 'Attività:Attività correnti:Conto corrente:Fineco C/C'
        self.default_target_account = 'Sbilancio-EUR'
        self.default_memo = ''

    def get_date(self, line):
        s = line[0].split('/')
        #                 yyyy       mm        dd
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        ttype = line[3]
        description = "<COMPLETARE>"
        
        if (ttype == "PagoBancomat POS"):
            d = re.compile(r'^Pag.*presso: (.*) C[ ]*a[ ]*r[ ]*t[ ]*a.*$')
            g = d.match(line[4])
            if (g is not None) and (g.group(1)): 
              description = g.group(1)

              # STAZIONE SCANAGATTA
              d = re.compile(r'^S[ ]*T[ ]*A[ ]*Z[ ]*I[ ]*O[ ]*N[ ]*E[ ]*[_ ]*S[ ]*C[ ]*A[ ]*N[ ]*A[ ]*G[ ]*A[ ]*T[ ]*T.*$');
              g = d.match(description);
              if (g is not None): description = "STAZIONE SCANAGATTA"
            
        elif (ttype == "Pagamento Visa Debit"):
            d = re.compile(r'^(.*) C[ ]*a[ ]*r[ ]*t[ ]*a.*$')
            g = d.match(line[4])
            if (g is not None) and g.group(1): description = g.group(1)
            
        elif (ttype == "SEPA Direct Debit"):
            d = re.compile(r'^(.*) A[ ]*d[ ]*d[ ]*e[ ]*b[ ]*i[ ]*t[ ]*o[ ]* [ ]*S[ ]*D[ ]*D[ ]*.*$')
            #d = re.compile(r'^(.*)Addebito SDD.*$')
            #d = re.compile(r'^(.*)$')
            g = d.match(line[4])
            if (g is not None) and g.group(1): description = g.group(1)
            
        elif (ttype == "Bonifico SEPA Italia"):
            d = re.compile(r'^Ben: (.*) Ins:.*$|^Ord\: (.*) Ben\:.*$')
            g = d.match(line[4])
            if (g is not None):
        
              # Bonifico in uscita
              if (g.group(1)): 
                description = g.group(1)
                
              # Bonifico in entrata
              elif (g.group(2)): 
                
                # FASIOPEN
                if (g.group(2) == "FASI"):
                  fasi_descr = re.compile(r'.* Info-Cli: .* ([0-9]{2})[/ ]{1}([0-9]{2})[/ ]{1}([0-9]{4})$');
                  fasi_date = fasi_descr.match(line[4]);
                  if (fasi_date is not None): description = "FASIOPEN (Rimborso del " + fasi_date.group(1) + "." + fasi_date.group(2) + "." + fasi_date.group(3) + ")"
                  
                else:
                  description = g.group(2)
            
        elif (ttype == "FastPay"):
            description = "Autostrada"
            
        elif (ttype == "Canone Mensile Conto"):
            description = "Fineco"
            
        elif (ttype == "Sconto Canone Mensile"):
            description = "Fineco"
            
        elif (ttype == "Imposta bollo dossier titoli"):
            description = "Fineco"
            
        elif (ttype == "Imposta bollo conto corrente"):
            description = "Fineco"
            
        elif (ttype == "MaxiPrelievo Banche del Gruppo"):
            description = "Bancomat"
            
        elif (ttype == "Maxiprelievo"):
            description = "Bancomat"
            
        elif (ttype == "Prelievi Bancomat extra Gruppo"):
            description = "Bancomat"
            
        elif (ttype == "Ricarica telefonica"):
            description = "Ricarica telefonica"
            
        elif (ttype == "Stipendio"):
            description = "Vimar"
            
        elif (ttype == "Giroconto"):
            description = "CONTO CORRENTE COMUNE"
            
        elif ((ttype == "Stacco Cedole Italia") or
              (ttype == "Ritenuta su Cedole") or
              (ttype == "Stacco Cedole Estero")):
            d = re.compile(r'^(Rit.)*[C|c]ed.su [0-9,.]+ (.*)$')
            g = d.match(line[4])
            if (g is not None) and (g.group(2)): 
              description = g.group(2)

        elif (ttype == "Compravendita Titoli"):
            d = re.compile(r'^Compravendita Titoli (.*) Qta.*$')
            g = d.match(line[4])
            if (g is not None) and (g.group(1)): 
              description = g.group(1)

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
            target = "Uscite:Mobilità:Auto:Autostrada"
            
        elif ((ttype == "Canone Mensile Conto") or
             (ttype == "Sconto Canone Mensile")):
            target = "Uscite:Uscite Bancarie:Costi"

        elif ((ttype == "Imposta bollo dossier titoli") or
             (ttype == "Imposta bollo conto corrente")):
            target = "Uscite:Uscite Bancarie:Tasse"
            
        elif ((ttype == "MaxiPrelievo Banche del Gruppo") or 
             (ttype == "Maxiprelievo") or 
             (ttype == "Prelievi Bancomat extra Gruppo")):
            target = "Attività:Attività correnti:Liquidità:Portafoglio"
            
        elif (ttype == "Ricarica telefonica"):
            target = "Uscite:Cellulare"
            
        elif (ttype == "Stipendio"):
            target = "Entrate:Entrate Lavorative:Stipendio"
            
        elif ((ttype == "PagoBancomat POS") or 
             (ttype == "Pagamento Visa Debit") or 
             (ttype == "SEPA Direct Debit")):
            description = self.get_description(line)
            if (description != "<COMPLETARE>"):
                
                # STAZIONE_SCANAGATT
                d = re.compile(r'^S[ ]*T[ ]*A[ ]*Z[ ]*I[ ]*O[ ]*N[ ]*E[ ]*[_ ]*S[ ]*C[ ]*A[ ]*N[ ]*A[ ]*G[ ]*A[ ]*T[ ]*T.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Mobilità:Auto:Carburante"
            
                # ENI
                d = re.compile(r'^ENI .*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Mobilità:Auto:Carburante"
            
                # ESSO
                d = re.compile(r'.* ESSO .*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Mobilità:Auto:Carburante"

                # AUTOST
                d = re.compile(r'^A[ ]*U[ ]*T[ ]*O[ ]*S[ ]*T.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Mobilità:Auto:Autostrada"
             
                # FARMACIA
                d = re.compile(r'.*F[ ]*A[ ]*R[ ]*M[ ]*A[ ]*C[ ]*I[ ]*A.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Sanità:Farmaci"
             
                # PAYPAL
                d = re.compile(r'.*P[ ]*a[ ]*y[ ]*P[ ]*a[ ]*l.*$');
                g = d.match(description);
                if (g is not None): return "Attività:Attività correnti:Conto corrente:Paypal"

                # MYCICERO
                d = re.compile(r'.*WWW.MYCICERO.IT.*$');
                g = d.match(description);
                if (g is not None): return "Uscite:Mobilità:Auto:Parcheggio"

            
        elif (ttype == "Bonifico SEPA Italia"):
          description = self.get_description(line)
                  
          # FASIOPEN
          # Rimosso perchè con più persone può andare in passività o in attività
          #d = re.compile(r'Ord\: FASI Ben\:')
          #g = d.match(line[5])
          #if (g is not None): return "Attività:Attività correnti:Denaro Prestato:Anticipo:Fondo di Assistenza Sanitaria"

        elif ((ttype == "Stacco Cedole Italia") or
             (ttype == "Ritenuta su Cedole") or
             (ttype == "Stacco Cedole Estero")):
          target = "Entrate:Interessi"

        elif (ttype == "Compravendita Titoli"):
          target = "Attività:Investimenti:Obbligazioni:Fineco - Dossier Titoli"

        return target
