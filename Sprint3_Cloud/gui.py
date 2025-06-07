"""
Summary: Provides a Tkinter GUI for performing CRUD operations on customers
and interactions, with real-time notifications only for new interactions.
"""
import tkinter as tk
from tkinter import messagebox, ttk
import uuid

from init import db
from crm import (
    create_customer,
    get_customer_interactions,
    add_interaction,
    update_customer_email,
    delete_interaction,
    delete_customer
)

class CRMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Firestore CRM GUI")
        self.geometry("1000x600")

        self._listener = None
        self._ignore_initial = False

        self.create_widgets()
        self.refresh_customers()

    def create_widgets(self):
        cust_frame = ttk.LabelFrame(self, text="Customers")
        cust_frame.pack(fill="x", padx=10, pady=5)

        self.cust_tree = ttk.Treeview(
            cust_frame,
            columns=("name", "email", "created_at"),
            show="headings"
        )
        for col, lbl in [("name","Name"),("email","Email"),("created_at","Created At")]:
            self.cust_tree.heading(col, text=lbl)
        self.cust_tree.bind("<<TreeviewSelect>>", self.on_customer_select)
        self.cust_tree.pack(side="left", fill="both", expand=True)

        cust_scroll = ttk.Scrollbar(
            cust_frame, orient="vertical", command=self.cust_tree.yview
        )
        self.cust_tree.configure(yscrollcommand=cust_scroll.set)
        cust_scroll.pack(side="left", fill="y")

        cust_ctrl = ttk.Frame(cust_frame)
        cust_ctrl.pack(side="left", padx=10, pady=5, fill="y")
        ttk.Label(cust_ctrl, text="Customer ID:").pack(anchor="w")
        self.cust_id_entry = ttk.Entry(cust_ctrl); self.cust_id_entry.pack(fill="x")
        ttk.Label(cust_ctrl, text="Name:").pack(anchor="w")
        self.cust_name_entry = ttk.Entry(cust_ctrl); self.cust_name_entry.pack(fill="x")
        ttk.Label(cust_ctrl, text="Email:").pack(anchor="w")
        self.cust_email_entry = ttk.Entry(cust_ctrl); self.cust_email_entry.pack(fill="x")

        ttk.Button(cust_ctrl, text="Create",      command=self.create_customer).pack(fill="x", pady=2)
        ttk.Button(cust_ctrl, text="Update Email", command=self.modify_customer).pack(fill="x", pady=2)
        ttk.Button(cust_ctrl, text="Delete",      command=self.remove_customer).pack(fill="x", pady=2)
        ttk.Button(cust_ctrl, text="Refresh",     command=self.refresh_customers).pack(fill="x", pady=2)

        int_frame = ttk.LabelFrame(self, text="Interactions")
        int_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.int_tree = ttk.Treeview(
            int_frame,
            columns=("type", "details", "timestamp"),
            show="headings"
        )
        for col, lbl in [("type","Type"),("details","Details"),("timestamp","Timestamp")]:
            self.int_tree.heading(col, text=lbl)
        self.int_tree.pack(side="left", fill="both", expand=True)

        int_scroll = ttk.Scrollbar(
            int_frame, orient="vertical", command=self.int_tree.yview
        )
        self.int_tree.configure(yscrollcommand=int_scroll.set)
        int_scroll.pack(side="left", fill="y")

        int_ctrl = ttk.Frame(int_frame)
        int_ctrl.pack(side="left", padx=10, pady=5, fill="y")
        ttk.Label(int_ctrl, text="Type:").pack(anchor="w")
        self.int_type_combo = ttk.Combobox(
            int_ctrl,
            values=["sale","return","complaint","suggestion"],
            state="readonly"
        )
        self.int_type_combo.pack(fill="x")
        ttk.Label(int_ctrl, text="Details:").pack(anchor="w")
        self.int_details_entry = ttk.Entry(int_ctrl)
        self.int_details_entry.pack(fill="x")

        ttk.Button(int_ctrl, text="Add",    command=self.create_interaction).pack(fill="x", pady=2)
        ttk.Button(int_ctrl, text="Delete", command=self.delete_interaction).pack(fill="x", pady=2)
        ttk.Button(int_ctrl, text="Refresh",command=self.refresh_interactions).pack(fill="x", pady=2)

    def create_customer(self):
        cid, name, email = (
            self.cust_id_entry.get().strip(),
            self.cust_name_entry.get().strip(),
            self.cust_email_entry.get().strip()
        )
        if not cid or not name or not email:
            messagebox.showwarning("Input error","Customer ID, Name, and Email are required.")
            return
        create_customer(cid, name, email)
        messagebox.showinfo("Success", f"Created customer: {cid}")
        self.refresh_customers()

    def modify_customer(self):
        sel = self.cust_tree.selection()
        if not sel:
            messagebox.showwarning("Select customer","Please select a customer first.")
            return
        cid = sel[0]
        new_email = self.cust_email_entry.get().strip()
        if not new_email:
            messagebox.showwarning("Input error","New email is required.")
            return
        update_customer_email(cid, new_email)
        messagebox.showinfo("Success",f"Updated email for {cid}")
        self.refresh_customers()

    def remove_customer(self):
        sel = self.cust_tree.selection()
        if not sel:
            messagebox.showwarning("Select customer","Please select a customer first.")
            return
        cid = sel[0]
        if messagebox.askyesno("Confirm delete", f"Delete customer {cid}?"):
            delete_customer(cid)
            messagebox.showinfo("Deleted",f"Deleted customer {cid}")
            self.refresh_customers()

    def refresh_customers(self):
        for i in self.cust_tree.get_children():
            self.cust_tree.delete(i)
        for doc in db.collection("customers").stream():
            data = doc.to_dict()
            self.cust_tree.insert(
                "", "end", iid=doc.id,
                values=(data.get("name"), data.get("email"), data.get("created_at"))
            )

    def on_customer_select(self, event):
        sel = self.cust_tree.selection()
        if not sel:
            return
        cid = sel[0]
        self.refresh_interactions()

        self._ignore_initial = True

        if self._listener:
            self._listener.unsubscribe()

        col_ref = db.collection("customers").document(cid).collection("interactions")
        self._listener = col_ref.on_snapshot(self._on_interaction_change)

    def create_interaction(self):
        sel = self.cust_tree.selection()
        if not sel:
            messagebox.showwarning("Select customer","Please select a customer first.")
            return
        cid = sel[0]
        itype = self.int_type_combo.get()
        details = self.int_details_entry.get().strip()
        if not itype or not details:
            messagebox.showwarning("Input error","Type and Details are required.")
            return
        add_interaction(cid, itype, details)
        messagebox.showinfo("Success",f"Added interaction to {cid}")
        self.refresh_interactions()

    def delete_interaction(self):
        sel = self.int_tree.selection()
        if not sel:
            messagebox.showwarning("Select interaction","Please select an interaction first.")
            return
        iid = sel[0]
        cid = self.cust_tree.selection()[0]
        if messagebox.askyesno("Confirm delete", f"Delete interaction {iid}?"):
            delete_interaction(cid, iid)
            messagebox.showinfo("Deleted",f"Deleted interaction {iid}")
            self.refresh_interactions()

    def refresh_interactions(self):
        for i in self.int_tree.get_children():
            self.int_tree.delete(i)
        sel = self.cust_tree.selection()
        if not sel:
            return
        cid = sel[0]
        for doc in get_customer_interactions(cid):
            data = doc.to_dict()
            self.int_tree.insert(
                "", "end", iid=doc.id,
                values=(data.get("type"), data.get("details"), data.get("timestamp"))
            )

    def _on_interaction_change(self, col_snapshot, changes, read_time):
        if self._ignore_initial:
            self._ignore_initial = False
            return

        for change in changes:
            if change.type.name == 'ADDED':
                data = change.document.to_dict()
                self.after(0, lambda d=data: messagebox.showinfo(
                    "New Interaction",
                    f"Type: {d['type']}\nDetails: {d['details']}"
                ))
        self.after(0, self.refresh_interactions)

if __name__ == "__main__":
    app = CRMApp()
    app.mainloop()
