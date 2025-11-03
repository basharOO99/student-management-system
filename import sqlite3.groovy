import sqlite3
from typing import Optional, List, Dict, Any

from datetime import datetime

class DatabaseHandler:
    DB_NAME = 'car_parts_management.db'

    @staticmethod
    def _connect():
        conn = sqlite3.connect(DatabaseHandler.DB_NAME)
        conn.row_factory = sqlite3.Row  # لتمكين الوصول بالحقول بالاسم
        return conn

    @staticmethod
    def create_table():
        with DatabaseHandler._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    origin TEXT,                     -- e.g. "Korean" or "Japanese"
                    is_original INTEGER NOT NULL,    -- 1 = original, 0 = replica
                    description TEXT,
                    cost_price REAL NOT NULL,        -- تكلفة الشراء علينا
                    sale_price REAL NOT NULL,        -- سعر البيع
                    quantity INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_parts_name ON parts(name)')
            conn.commit()

    @staticmethod
    def add_part(name: str,
                 origin: Optional[str],
                 is_original: int,
                 cost_price: float,
                 sale_price: float,
                 quantity: int,
                 description: Optional[str] = None) -> int:
        with DatabaseHandler._connect() as conn:
            cur = conn.execute('''
                INSERT INTO parts (name, origin, is_original, description, cost_price, sale_price, quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, origin, is_original, description, cost_price, sale_price, quantity))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def update_part(part_id: int, **fields) -> None:
        """
        تحديث حقول منقولة كـ keyword args، مثال:
        update_part(1, sale_price=120.0, quantity=5)
        """
        if not fields:
            return
        cols = ', '.join([f"{k}=?" for k in fields.keys()])
        vals = list(fields.values())
        vals.append(part_id)
        with DatabaseHandler._connect() as conn:
            conn.execute(f'UPDATE parts SET {cols} WHERE id=?', vals)
            conn.commit()

    @staticmethod
    def update_quantity(part_id: int, delta: int) -> None:
        """زيادة/نقص الكمية (delta يمكن أن يكون سالباً)"""
        with DatabaseHandler._connect() as conn:
            conn.execute('UPDATE parts SET quantity = quantity + ? WHERE id=?', (delta, part_id))
            conn.commit()

    @staticmethod
    def delete_part(part_id: int) -> None:
        with DatabaseHandler._connect() as conn:
            conn.execute('DELETE FROM parts WHERE id=?', (part_id,))
            conn.commit()

    @staticmethod
    def get_part(part_id: int) -> Optional[Dict[str, Any]]:
        """يعيد السطر مع حقل profit محسوب"""
        with DatabaseHandler._connect() as conn:
            cur = conn.execute('''
                SELECT *, (sale_price - cost_price) AS profit
                FROM parts
                WHERE id=?
            ''', (part_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def list_parts(origin: Optional[str] = None,
                   is_original: Optional[int] = None,
                   low_stock_threshold: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        يعيد قائمة بالقطع مع حقل profit.
        يمكن التصفية حسب origin و is_original، أو حسب threshold للكمية القليلة.
        """
        query = 'SELECT *, (sale_price - cost_price) AS profit FROM parts WHERE 1=1'
        params: List[Any] = []
        if origin is not None:
            query += ' AND origin = ?'
            params.append(origin)
        if is_original is not None:
            query += ' AND is_original = ?'
            params.append(is_original)
        if low_stock_threshold is not None:
            query += ' AND quantity <= ?'
            params.append(low_stock_threshold)
        query += ' ORDER BY name COLLATE NOCASE'
        with DatabaseHandler._connect() as conn:
            cur = conn.execute(query, params)
            return [dict(r) for r in cur.fetchall()]

    @staticmethod
    def compute_total_inventory_value() -> Dict[str, float]:
        """
        يحسب القيم الإجمالية:
          - total_cost: مجموع (cost_price * quantity)
          - total_sale_value: مجموع (sale_price * quantity)
          - total_potential_profit: مجموع ((sale_price - cost_price) * quantity)
        """
        with DatabaseHandler._connect() as conn:
            cur = conn.execute('''
                SELECT
                    SUM(cost_price * quantity) AS total_cost,
                    SUM(sale_price * quantity) AS total_sale_value,
                    SUM((sale_price - cost_price) * quantity) AS total_potential_profit
                FROM parts
            ''')
            row = cur.fetchone()
            return {
                'total_cost': row['total_cost'] or 0.0,
                'total_sale_value': row['total_sale_value'] or 0.0,
                'total_potential_profit': row['total_potential_profit'] or 0.0
            }

    @staticmethod
    def export_to_csv(csv_path: str) -> None:
        rows = DatabaseHandler.list_parts()
        if not rows:
            return
        # ترتيب الحقول
        fieldnames = ['id','name','origin','is_original','description','cost_price','sale_price','quantity','profit','created_at']
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                # تأكد من وجود كل الحقول
                out = {k: r.get(k) for k in fieldnames}
                writer.writerow(out)

# مثال على استخدام سريع
if __name__ == '__main__':
    DatabaseHandler.create_table()

    # إضافة مثال
    pid = DatabaseHandler.add_part(
        name="Brake Pad - Front",
        origin="Korean",
        is_original=1,
        cost_price=25.0,
        sale_price=45.0,
        quantity=100,
        description="Front brake pads, OEM"
    )
    print("Inserted part id:", pid)

    # جلب وعرض الربح
    p = DatabaseHandler.get_part(pid)
    print("Part with profit:", p)

    # حساب القيمة الإجمالية للمخزون
    totals = DatabaseHandler.compute_total_inventory_value()
    print("Inventory totals:", totals)
