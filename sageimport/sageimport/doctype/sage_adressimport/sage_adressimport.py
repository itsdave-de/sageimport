# -*- coding: utf-8 -*-
# Copyright (c) 2021, itsdave GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import file_manager
import pandas as pd
import numpy as np

class SageAdressimport(Document):
    @frappe.whitelist()
    def do_import(self):
        #Excel Datei als Pandas Dataframe laden
        excel_file = frappe.utils.file_manager.get_file_path(self.datei)
        #frappe.publish_progress(0, 'Lese Excel Tabelle, das kann etwas dauern...')
        df = pd.read_excel(excel_file)
        df = df.replace(np.nan, '', regex=True)
        output = ""

        for index, row in df.iterrows():
            try:
                cust = "CUST-" + row["Kd.-Nr."]
                output += "verarbeite " + cust + "\n"
                cust_list = frappe.get_all("Customer", filters={"name": cust})
                if not cust_list:
                    cust_doc = frappe.get_doc({
                        "doctype": "Customer",
                        "title": row["Name"],
                        "customer_name": row["Name"],
                        "sage_notizen": row["Memo"].replace("  ","<br>"),
                        "sage_adresse": row["Adresse"]
                    })
                    cust_doc.insert()
                    frappe.rename_doc("Customer", cust_doc.name, cust)
                    cust_doc = frappe.get_doc("Customer", cust)
                    address_doc = frappe.get_doc({
                        "doctype": "Address",
                        "address_title": row["Name"] + "-haupt",
                        "is_primary_address": 1,
                        "is_shipping_address": 1,
                        }
                    )
                    #Pflichtfelder Prüfen
                    if row["Email"] != "":
                        address_doc.email_id = row["Email"]
                    else:
                        address_doc.email_id = "gibts@gar.nicht"

                    if row["Straße"] != "":
                        address_doc.address_line1 = row["Straße"]
                    else:
                        address_doc.address_line1 = "STRASSE FEHLT!"
                    
                    if  row["Telefon"] != "":
                        address_doc.phone = row["Telefon"]
                    else:
                        address_doc.phone = "TELEFON FEHLT"
                        
                    if row["PLZ"] != "":
                        address_doc.pincode = row["PLZ"]
                    else:
                        address_doc.pincode = "PLZ FEHLT"
                    
                    if row["Ort"] != "":
                        address_doc.city = row["Ort"]
                    else:
                        address_doc.city = "ORT FEHLT"
                    
                    #land auflösen
                    country = frappe.get_all("Country", filters={"code": row["Land"].lower() })
                    if len(country) >= 1:
                        address_doc.country = country[0]["name"]
                    else:
                        address_doc.country = "Germany"

                    
                    address_doc.insert()
                    #Dynamic Link einfügen
                    link_doc = frappe.get_doc(
                        {
                            'doctype': 'Dynamic Link',
                            'link_doctype': 'Customer',
                            'link_name': cust_doc.name,
                        }
                    )
                    address_doc.append("links", link_doc)
                    address_doc.save()
                    cust_doc.customer_primary_address = address_doc.name
                    cust_doc.save()
            except Exeption as e:
                output += e.message
        self.output = output
        self.save()


                
                
                

                
                


