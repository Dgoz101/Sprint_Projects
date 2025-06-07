"""
Summary: Demonstrates CRM functionality for multiple customers (five entries),
each with a UUID-based email suffix to avoid collisions.
"""
import uuid
from crm import create_customer, add_interaction, get_customer_interactions
from auth import signup, login

def demo():
    customers = [
        {
            "base": "alice",
            "name": "Alice Smith",
            "interactions": [
                ("sale", "Purchased item #1234"),
                ("complaint", "Item arrived damaged")
            ]
        },
        {
            "base": "bob",
            "name": "Bob Jones",
            "interactions": [
                ("suggestion", "Add a loyalty rewards feature"),
                ("return", "Returned item #5678")
            ]
        },
        {
            "base": "charlie",
            "name": "Charlie Brown",
            "interactions": [
                ("sale", "Bought 3 units of SKU #9012"),
                ("suggestion", "Offer volume discounts")
            ]
        },
        {
            "base": "dana",
            "name": "Dana White",
            "interactions": [
                ("complaint", "Late delivery"),
                ("return", "Returned defective item #3456")
            ]
        },
        {
            "base": "lebron",
            "name": "LeBron James",
            "interactions": [
                ("sale", "Purchased item #7890"),
                ("suggestion", "Improve website UI")
            ]
        }
    ]

    for cust in customers:
        suffix = uuid.uuid4().hex[:8]
        email = f"{cust['base']}+{suffix}@example.com"
        password = "SuperSecret123"

        user = signup(email, password)
        print(f"Signed up {cust['name']} → UID: {user['localId']}")

        create_customer(email, cust["name"], email)

        session = login(email, password)
        print(f"Logged in {cust['name']}, token expires in: {session['expiresIn']} seconds")

        for itype, details in cust["interactions"]:
            add_interaction(email, itype, details)

        print(f"\nInteractions for {cust['name']}:")
        get_customer_interactions(email)
        print("-" * 60, "\n")

if __name__ == "__main__":
    demo()
