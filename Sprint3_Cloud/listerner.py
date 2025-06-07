"""
Summary: Sets up a real-time Firestore listener for customer interaction changes.
"""
import threading
from init import db

def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        print(change.type.name, change.document.id, change.document.to_dict())

def watch_customer(customer_id: str):
    interactions_ref = (
        db.collection("customers")
          .document(customer_id)
          .collection("interactions")
    )
    interactions_ref.on_snapshot(on_snapshot)
    threading.Event().wait()

if __name__ == "__main__":
    watch_customer("alice@example.com")
