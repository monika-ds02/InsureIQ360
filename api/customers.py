from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import duckdb

from api.main import get_current_user

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

DB_PATH = "dbt_insureiq360/dev.duckdb"


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class Customer(CustomerCreate):
    id: int
    customer_code: str


def get_connection():
    return duckdb.connect(DB_PATH)


# =========================
# CREATE CUSTOMER
# =========================
@router.post("/", response_model=Customer)
async def create_customer(
    customer: CustomerCreate,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        # Generate next numeric ID
        next_id = con.execute("""
            SELECT COALESCE(MAX(id), 0) + 1
            FROM customers
        """).fetchone()[0]

        # Generate next customer code
        next_code_number = con.execute("""
            SELECT COALESCE(
                MAX(
                    TRY_CAST(
                        SUBSTRING(customer_code, 4)
                        AS INTEGER
                    )
                ),
                0
            ) + 1
            FROM customers
        """).fetchone()[0]

        customer_code = f"CUS{next_code_number:03d}"

        result = con.execute("""
            INSERT INTO customers (
                id,
                customer_code,
                name,
                email,
                phone,
                address
            )
            VALUES (?, ?, ?, ?, ?, ?)
            RETURNING
                id,
                customer_code,
                name,
                email,
                phone,
                address
        """, [
            next_id,
            customer_code,
            customer.name,
            customer.email,
            customer.phone,
            customer.address
        ]).fetchone()

        return Customer(
            id=result[0],
            customer_code=result[1],
            name=result[2],
            email=result[3],
            phone=result[4],
            address=result[5]
        )

    finally:
        con.close()


# =========================
# GET ALL CUSTOMERS
# =========================
@router.get("/", response_model=List[Customer])
async def get_customers(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                id,
                customer_code,
                name,
                email,
                phone,
                address
            FROM customers
            ORDER BY id
        """).fetchall()

        return [
            Customer(
                id=row[0],
                customer_code=row[1],
                name=row[2],
                email=row[3],
                phone=row[4],
                address=row[5]
            )
            for row in rows
        ]

    finally:
        con.close()


# =========================
# GET CUSTOMER BY ID
# =========================
@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        row = con.execute("""
            SELECT
                id,
                customer_code,
                name,
                email,
                phone,
                address
            FROM customers
            WHERE id = ?
        """, [customer_id]).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return Customer(
            id=row[0],
            customer_code=row[1],
            name=row[2],
            email=row[3],
            phone=row[4],
            address=row[5]
        )

    finally:
        con.close()


# =========================
# EDIT / UPDATE CUSTOMER
# =========================
@router.put("/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT
                id,
                customer_code
            FROM customers
            WHERE id = ?
        """, [customer_id]).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        result = con.execute("""
            UPDATE customers
            SET
                name = ?,
                email = ?,
                phone = ?,
                address = ?
            WHERE id = ?
            RETURNING
                id,
                customer_code,
                name,
                email,
                phone,
                address
        """, [
            customer.name,
            customer.email,
            customer.phone,
            customer.address,
            customer_id
        ]).fetchone()

        return Customer(
            id=result[0],
            customer_code=result[1],
            name=result[2],
            email=result[3],
            phone=result[4],
            address=result[5]
        )

    finally:
        con.close()


# =========================
# DELETE CUSTOMER
# =========================
@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT id
            FROM customers
            WHERE id = ?
        """, [customer_id]).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        con.execute("""
            DELETE FROM customers
            WHERE id = ?
        """, [customer_id])

        return {
            "message": "Customer deleted successfully",
            "customer_id": customer_id
        }

    finally:
        con.close()


# =========================
# CUSTOMER DETAILS
# =========================
@router.get("/{customer_id}/details")
async def get_customer_details(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        # Get customer
        customer = con.execute("""
            SELECT
                id,
                customer_code,
                name,
                email,
                phone,
                address
            FROM customers
            WHERE id = ?
        """, [customer_id]).fetchone()

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        customer_code = customer[1]

        # Get policies using customer_code
        policies = con.execute("""
            SELECT
                policy_id,
                customer_id,
                policy_type,
                premium,
                status
            FROM policies
            WHERE customer_id = ?
            ORDER BY policy_id
        """, [customer_code]).fetchall()

        # Get claims using customer_code
        claims = con.execute("""
            SELECT
                claim_id,
                customer_id,
                policy_id,
                claim_amount,
                status
            FROM fact_claims
            WHERE customer_id = ?
            ORDER BY claim_id
        """, [customer_code]).fetchall()

        return {
            "customer": {
                "id": customer[0],
                "customer_code": customer[1],
                "name": customer[2],
                "email": customer[3],
                "phone": customer[4],
                "address": customer[5]
            },
            "policies": [
                {
                    "policy_id": row[0],
                    "customer_id": row[1],
                    "policy_type": row[2],
                    "premium": row[3],
                    "status": row[4]
                }
                for row in policies
            ],
            "claims": [
                {
                    "claim_id": row[0],
                    "customer_id": row[1],
                    "policy_id": row[2],
                    "claim_amount": row[3],
                    "status": row[4]
                }
                for row in claims
            ]
        }

    finally:
        con.close()