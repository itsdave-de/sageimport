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
    def do_import(self):
        #Excel Datei als Pandas Dataframe laden
        excel_file = frappe.utils.file_manager.get_file_path(self.datei)
        #frappe.publish_progress(0, 'Lese Excel Tabelle, das kann etwas dauern...')
        df = pd.read_excel(excel_file)
        for index, row in df.iterrows():
            cust = "CUST-" + row["Kd.-Nr."]
            print("Processing " + cust)
            cust_list = frappe.get_all("Customer", filters={"name": cust})
            if not cust_list:
                cust_doc = frappe.get_doc({
                    "doctype": "Customer",
                    "title": row["Name"],
                    "customer_name": row["Name"],
                    "sage_notizen": row["Memo"].replace("  ","<br>")
                })
                cust_doc.insert()
                frappe.rename_doc("Customer", cust_doc.name, cust)
                cust_doc = frappe.get_doc("Customer", cust)
                address_doc = frappe.get_doc({
                    "doctype": "Address",
                    "address_title": row["Name"] + "-haupt",
                    "pincode": row["PLZ"],
                    "address_line1": row["Straße"],
                    "city": row["Ort"],
                    "is_primary_address": 1,
                    "is_shipping_address": 1,
                    "email_id": row["Email"],
                    "phone": row["Telefon"]
                    }
                )
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
                
                
                

                
                


