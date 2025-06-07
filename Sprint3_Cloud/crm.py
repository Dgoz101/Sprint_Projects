"""
Summary: Provides CRUD operations for customer records and their interactions.
"""
from datetime import datetime
from init import db

def create_customer(customer_id: str, name: str, email: str):
    """Create (or overwrite) a customer document."""
    db.collection("customers").document(customer_id).set({
        "name": name,
        "email": email,
        "created_at": datetime.utcnow()
    })

def get_customer_interactions(customer_id: str):
    """Read all interactions for a customer."""
    return db.collection("customers") \
             .document(customer_id) \
             .collection("interactions") \
             .order_by("timestamp") \
             .stream()

def add_interaction(customer_id: str, interaction_type: str, details: str):
    """Create (add) a new interaction under a customer."""
    db.collection("customers") \
      .document(customer_id) \
      .collection("interactions") \
      .add({
          "type": interaction_type,
          "details": details,
          "timestamp": datetime.utcnow()
      })

def update_customer_email(customer_id: str, new_email: str):
    """Modify a customer’s email field (document ID won’t change)."""
    db.collection("customers").document(customer_id).update({
        "email": new_email
    })

def delete_interaction(customer_id: str, interaction_id: str):
    """Delete one interaction document."""
    db.collection("customers") \
      .document(customer_id) \
      .collection("interactions") \
      .document(interaction_id) \
      .delete()

def delete_customer(customer_id: str):
    """Delete a customer document."""
    db.collection("customers").document(customer_id).delete()
