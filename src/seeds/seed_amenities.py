"""
Seed amenities — mixed CONDOMINIUM + BUILDING scope examples.

Run with: python -m seeds.seed_amenities
"""
import uuid as uuid_lib

from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity
from library.dddpy.shared.mysql.session_manager import session_scope


SEEDS = [
    # --- CONDOMINIUM scope (shared by all buildings) ---
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "CONDOMINIUM",
        "building_id": None,
        "name": "Piscina General",
        "description": "Piscina pública del condominio, disponible para todos los residentes",
        "location": "Zona central",
        "max_capacity": 50,
        "booking_duration_min": 120,
        "requires_approval": False,
        "booking_price": 0.00,
        "security_deposit_amount": 0.00,
        "is_reservable": False,
        "status": "active",
    },
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "CONDOMINIUM",
        "building_id": None,
        "name": "Cancha de Fútbol",
        "description": "Cancha sintética de fútbol 7",
        "location": "Área deportiva",
        "max_capacity": 14,
        "booking_duration_min": 90,
        "requires_approval": True,
        "booking_price": 50.00,
        "security_deposit_amount": 100.00,
        "is_reservable": True,
        "status": "active",
    },
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "CONDOMINIUM",
        "building_id": None,
        "name": "Lavandería Común",
        "description": "Lavandería con lavadoras y secadoras industriales",
        "location": "Sótano 1",
        "max_capacity": 10,
        "booking_duration_min": 60,
        "requires_approval": False,
        "booking_price": 10.00,
        "security_deposit_amount": 0.00,
        "is_reservable": True,
        "status": "active",
    },
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "CONDOMINIUM",
        "building_id": None,
        "name": "Parrillas Comunes",
        "description": "Zona de parrillas al aire libre para eventos",
        "location": "Jardín norte",
        "max_capacity": 30,
        "booking_duration_min": 180,
        "requires_approval": True,
        "booking_price": 80.00,
        "security_deposit_amount": 200.00,
        "is_reservable": True,
        "status": "active",
    },

    # --- BUILDING scope (exclusive to a specific building) ---
    # Building 1 (Torre A) exclusive amenities
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "BUILDING",
        "building_id": 1,
        "name": "Gimnasio Torre A",
        "description": "Gimnasio exclusivo para residentes de Torre A",
        "location": "Piso 1, Torre A",
        "max_capacity": 15,
        "booking_duration_min": 60,
        "requires_approval": False,
        "booking_price": 0.00,
        "security_deposit_amount": 0.00,
        "is_reservable": False,
        "status": "active",
    },
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "BUILDING",
        "building_id": 1,
        "name": "SUM Torre A",
        "description": "Salón de usos múltiples — reuniones, eventos",
        "location": "Piso 2, Torre A",
        "max_capacity": 25,
        "booking_duration_min": 120,
        "requires_approval": True,
        "booking_price": 150.00,
        "security_deposit_amount": 500.00,
        "is_reservable": True,
        "status": "active",
    },
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "BUILDING",
        "building_id": 1,
        "name": "Cine Torre A",
        "description": "Sala de cine privada con proyector 4K",
        "location": "Sótano, Torre A",
        "max_capacity": 20,
        "booking_duration_min": 150,
        "requires_approval": True,
        "booking_price": 30.00,
        "security_deposit_amount": 150.00,
        "is_reservable": True,
        "status": "active",
    },

    # Building 2 (Torre B) exclusive amenities
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "BUILDING",
        "building_id": 2,
        "name": "Parrilla Torre B",
        "description": "Parrilla privada en terraza de Torre B",
        "location": "Terraza, Torre B",
        "max_capacity": 12,
        "booking_duration_min": 120,
        "requires_approval": True,
        "booking_price": 40.00,
        "security_deposit_amount": 100.00,
        "is_reservable": True,
        "status": "active",
    },
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "BUILDING",
        "building_id": 2,
        "name": "Karaoke Torre B",
        "description": "Sala de karaoke con equipo de sonido profesional",
        "location": "Piso 3, Torre B",
        "max_capacity": 10,
        "booking_duration_min": 120,
        "requires_approval": True,
        "booking_price": 60.00,
        "security_deposit_amount": 200.00,
        "is_reservable": True,
        "status": "active",
    },
    {
        "uuid": str(uuid_lib.uuid4()),
        "condominium_id": 1,
        "scope": "BUILDING",
        "building_id": 2,
        "name": "Cafetería Torre B",
        "description": "Cafetería exclusiva con máquina espresso y lounge",
        "location": "Lobby, Torre B",
        "max_capacity": 15,
        "booking_duration_min": 60,
        "requires_approval": False,
        "booking_price": 0.00,
        "security_deposit_amount": 0.00,
        "is_reservable": False,
        "status": "active",
    },
]


def seed():
    """Insert seed amenities if not already present (idempotent by uuid)."""
    print("🌱 Seeding amenities (CONDOMINIUM + BUILDING)...")
    with session_scope() as session:
        existing_uuids = {
            row.uuid
            for row in session.query(DBAmenity.uuid).filter(
                DBAmenity.uuid.in_([s["uuid"] for s in SEEDS])
            ).all()
        }

        inserted = 0
        for data in SEEDS:
            if data["uuid"] in existing_uuids:
                continue
            session.add(DBAmenity(**data))
            inserted += 1

        if inserted:
            session.flush()
            print(f"   ✅ {inserted} new amenities inserted")
        else:
            print("   ⏭️  All seed amenities already exist (skipped)")

    # Quick summary
    print()
    print("📊 Summary by scope:")
    condo_count = sum(1 for s in SEEDS if s["scope"] == "CONDOMINIUM")
    building_count = sum(1 for s in SEEDS if s["scope"] == "BUILDING")
    print(f"   CONDOMINIUM: {condo_count}")
    print(f"   BUILDING:    {building_count}")


if __name__ == "__main__":
    seed()
