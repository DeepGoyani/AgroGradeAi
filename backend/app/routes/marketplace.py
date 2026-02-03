"""
AgroGrade AI - Marketplace API Routes
Product listing, cart management, and marketplace functionality
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import uuid

from .auth import get_current_user

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

# Database setup
DB_PATH = Path(__file__).parent.parent.parent / "agrograde_marketplace.db"

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_marketplace_db():
    """Initialize marketplace database tables"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quality TEXT NOT NULL,
                grade INTEGER NOT NULL,
                price REAL NOT NULL,
                unit TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                location TEXT NOT NULL,
                farmer_id TEXT NOT NULL,
                farmer_name TEXT NOT NULL,
                rating REAL DEFAULT 0,
                reviews INTEGER DEFAULT 0,
                description TEXT,
                harvest_date TEXT,
                available BOOLEAN DEFAULT 1,
                certified BOOLEAN DEFAULT 0,
                favorites INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL,
                items TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()

# Pydantic models
class Product(BaseModel):
    id: str
    name: str
    category: str
    quality: str
    grade: int
    price: float
    unit: str
    quantity: int
    location: str
    farmer_id: str
    farmer_name: str
    rating: float
    reviews: int
    description: str
    harvest_date: str
    available: bool
    certified: bool
    favorites: int

class CartItem(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=1)

@router.get("/products")
async def get_products(
    category: Optional[str] = None,
    quality: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
    certified_only: bool = False,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get marketplace products with filters"""
    try:
        init_marketplace_db()
        
        with get_db() as conn:
            query = "SELECT * FROM products WHERE available = 1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if quality:
                query += " AND quality = ?"
                params.append(quality)
            
            if min_price:
                query += " AND price >= ?"
                params.append(min_price)
            
            if max_price:
                query += " AND price <= ?"
                params.append(max_price)
            
            if location:
                query += " AND location LIKE ?"
                params.append(f"%{location}%")
            
            if certified_only:
                query += " AND certified = 1"
            
            query += " ORDER BY created_at DESC"
            
            cursor = conn.execute(query, params)
            products = [dict(row) for row in cursor.fetchall()]
        
        return {"products": products, "total": len(products)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")

@router.get("/products/{product_id}")
async def get_product(
    product_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get single product details"""
    try:
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM products WHERE id = ? AND available = 1",
                (product_id,)
            )
            product = cursor.fetchone()
            
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            return dict(product)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product: {str(e)}")

@router.post("/cart/add")
async def add_to_cart(
    cart_item: CartItem,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add product to cart"""
    try:
        with get_db() as conn:
            # Check if product exists and is available
            cursor = conn.execute(
                "SELECT * FROM products WHERE id = ? AND available = 1",
                (cart_item.product_id,)
            )
            product = cursor.fetchone()
            
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            # Check if already in cart
            cursor = conn.execute(
                "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
                (current_user["id"], cart_item.product_id)
            )
            existing_item = cursor.fetchone()
            
            if existing_item:
                # Update quantity
                conn.execute(
                    "UPDATE cart SET quantity = quantity + ? WHERE id = ?",
                    (cart_item.quantity, existing_item["id"])
                )
            else:
                # Add new item
                cart_id = str(uuid.uuid4())
                conn.execute(
                    "INSERT INTO cart (id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                    (cart_id, current_user["id"], cart_item.product_id, cart_item.quantity)
                )
            
            conn.commit()
        
        return {"message": "Product added to cart successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add to cart: {str(e)}")

@router.get("/cart")
async def get_cart(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's cart"""
    try:
        with get_db() as conn:
            cursor = conn.execute("""
                SELECT c.*, p.name, p.price, p.unit, p.image
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = ?
                ORDER BY c.added_at DESC
            """, (current_user["id"],))
            
            cart_items = []
            total = 0
            
            for row in cursor.fetchall():
                item = dict(row)
                item["subtotal"] = item["price"] * item["quantity"]
                total += item["subtotal"]
                cart_items.append(item)
        
        return {"items": cart_items, "total": total, "count": len(cart_items)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cart: {str(e)}")

@router.delete("/cart/{item_id}")
async def remove_from_cart(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Remove item from cart"""
    try:
        with get_db() as conn:
            cursor = conn.execute(
                "DELETE FROM cart WHERE id = ? AND user_id = ?",
                (item_id, current_user["id"])
            )
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Cart item not found")
            
            conn.commit()
        
        return {"message": "Item removed from cart"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove from cart: {str(e)}")

@router.post("/favorite/{product_id}")
async def toggle_favorite(
    product_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Toggle product favorite status"""
    try:
        with get_db() as conn:
            # Check if product exists
            cursor = conn.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            )
            product = cursor.fetchone()
            
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            # Toggle favorite count
            conn.execute(
                "UPDATE products SET favorites = favorites + 1 WHERE id = ?",
                (product_id,)
            )
            
            conn.commit()
        
        return {"message": "Favorite toggled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle favorite: {str(e)}")

@router.get("/categories")
async def get_categories():
    """Get available product categories"""
    try:
        categories = [
            {"id": "vegetables", "name": "Vegetables", "count": 45},
            {"id": "grains", "name": "Grains", "count": 32},
            {"id": "fibers", "name": "Fibers", "count": 28},
            {"id": "fruits", "name": "Fruits", "count": 18}
        ]
        
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")

@router.get("/locations")
async def get_locations():
    """Get available product locations"""
    try:
        locations = [
            {"id": "gujarat", "name": "Gujarat", "count": 28},
            {"id": "punjab", "name": "Punjab", "count": 35},
            {"id": "tamil_nadu", "name": "Tamil Nadu", "count": 22},
            {"id": "maharashtra", "name": "Maharashtra", "count": 18},
            {"id": "uttar_pradesh", "name": "Uttar Pradesh", "count": 15},
            {"id": "andhra_pradesh", "name": "Andhra Pradesh", "count": 12}
        ]
        
        return {"locations": locations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch locations: {str(e)}")

# Initialize database on import
init_marketplace_db()
