"""
Integration Sandbox — creates the full data graph for testing.

create_integration_sandbox(session) → dict with all entities
sandbox_cleanup(session, sandbox) → deletes all created rows

Usage:
    sandbox = create_integration_sandbox(session)
    # ... run your tests ...
    sandbox_cleanup(session, sandbox)
"""
import uuid
from datetime import date, time, datetime, timedelta
from decimal import Decimal
from typing import Optional

from tests.factories.condo_factory import CondoFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.unit_factory import UnitFactory
from tests.factories.user_factory import UserFactory
from tests.factories.resident_factory import ResidentFactory
from tests.factories.charge_type_factory import ChargeTypeFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.ar_factory import AccountsReceivableFactory
from tests.factories.payment_factory import PaymentFactory
from tests.factories.receipt_factory import ReceiptFactory
from tests.factories.ledger_factory import LedgerFactory
from tests.factories.incident_factory import IncidentFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.document_factory import DocumentFactory
from tests.factories.vote_factory import VoteFactory
from tests.factories.meeting_factory import MeetingFactory
from tests.factories.announcement_factory import AnnouncementFactory
from tests.factories.notification_factory import NotificationFactory
from tests.factories.package_factory import PackageFactory
from tests.factories.amenity_factory import AmenityFactory


# ── Sandbox creation ────────────────────────────────────────────────────────

def create_integration_sandbox(
    session,
    condo_name: str = "Sandbox Condominium",
    buildings_count: int = 2,
    units_per_building: int = 3,
) -> dict:
    """
    Creates a full integration sandbox with entities across ALL modules.

    Graph:
        1 Condo
        ├── 2 Buildings (residential, commercial)
        │   ├── 3 Units each (6 total)
        │   │   ├── Users + Residents (6 each)
        │   │   └── AR entries per unit
        ├── 3 ChargeTypes
        ├── 5 Charges (unit/building/condo scope)
        ├── 3 Payments + Receipts
        ├── 3 LedgerEntries
        ├── 2 Incidents
        ├── 2 Visitors
        ├── 2 Documents
        ├── 1 Vote
        ├── 1 Meeting
        ├── 2 Announcements
        ├── 3 Notifications
        ├── 2 Packages
        └── 2 Amenities

    Returns: dict with all created entity lists keyed by module name.
    """
    sandbox = {}

    # ── 1. Condominium ──────────────────────────────────────────────────
    condo = CondoFactory.create(session, name=condo_name)
    sandbox["condo"] = condo

    # ── 2. Buildings ────────────────────────────────────────────────────
    buildings = []
    for i in range(buildings_count):
        btype = "RESIDENTIAL" if i == 0 else "COMMERCIAL"
        building = BuildingFactory.create(
            session,
            condominium_id=condo.id,
            code=f"BLD-{chr(65+i)}",
            name=f"Torre {chr(65+i)}",
            short_name=f"Torre {chr(65+i)}",
            floors_count=10,
            units_planned=units_per_building,
        )
        buildings.append(building)
    sandbox["buildings"] = buildings

    # ── 3. Units ────────────────────────────────────────────────────────
    units = []
    for bldg in buildings:
        for u in range(units_per_building):
            unit = UnitFactory.create(
                session,
                building_id=bldg.id,
                unit_number=f"{(u+1):03d}",
                code=f"UNIT-{bldg.code}-{u+1:02d}",
                name=f"Unidad {u+1}",
                floor_number=(u % 10) + 1,
                occupancy_status="occupied" if u < 2 else "vacant",
            )
            units.append(unit)
    sandbox["units"] = units

    # ── 4. Users + Residents ────────────────────────────────────────────
    users = []
    residents = []
    for i, unit in enumerate(units):
        user = UserFactory.create(
            session,
            email=f"sandbox-user-{i+1}@test.local",
        )
        resident = ResidentFactory.create(
            session,
            user_id=user.id,
            condominium_id=condo.id,
        )
        users.append(user)
        residents.append(resident)
    sandbox["users"] = users
    sandbox["residents"] = residents

    # ── 5. ChargeTypes ──────────────────────────────────────────────────
    charge_types = []
    for ct_data in [
        ("MANTENIMIENTO", "Cuota de mantenimiento"),
        ("AGUA", "Consumo de agua"),
        ("ESTACIONAMIENTO", "Alquiler de estacionamiento"),
    ]:
        ct = ChargeTypeFactory.create(
            session,
            code=f"{ct_data[0]}-{uuid.uuid4().hex[:6].upper()}",
            name=ct_data[1],
            is_global=1,
        )
        charge_types.append(ct)
    sandbox["charge_types"] = charge_types

    # ── 6. Charges ──────────────────────────────────────────────────────
    charges = []
    maintenance_ct = charge_types[0]
    water_ct = charge_types[1]
    parking_ct = charge_types[2]

    # Unit-level charge (first unit always exists)
    charges.append(ChargeFactory.create(
        session,
        condominium_id=condo.id,
        charge_type_id=maintenance_ct.id,
        scope="unit",
        unit_id=units[0].id,
        amount=Decimal("200.00"),
        description="Mantenimiento mensual",
        is_recurrent=1,
        period_pattern=date.today().strftime("%Y-%m"),
    ))
    # Building-level charge (first building always exists)
    charges.append(ChargeFactory.create(
        session,
        condominium_id=condo.id,
        charge_type_id=water_ct.id,
        scope="building",
        building_id=buildings[0].id,
        amount=Decimal("500.00"),
        description="Agua Torre A",
        distribution_mode="proportional_area",
    ))
    # Condo-level charge
    charges.append(ChargeFactory.create(
        session,
        condominium_id=condo.id,
        charge_type_id=parking_ct.id,
        scope="condominium",
        amount=Decimal("1000.00"),
        description="Mantenimiento estacionamientos",
        distribution_mode="proportional_coefficient",
    ))
    # More unit charges (only if enough units exist)
    if len(units) > 1:
        charges.append(ChargeFactory.create(
            session,
            condominium_id=condo.id,
            charge_type_id=maintenance_ct.id,
            scope="unit",
            unit_id=units[1].id,
            amount=Decimal("200.00"),
            description="Mantenimiento mensual U2",
            is_recurrent=1,
        ))
    if len(units) > 2:
        charges.append(ChargeFactory.create(
            session,
            condominium_id=condo.id,
            charge_type_id=water_ct.id,
            scope="unit",
            unit_id=units[2].id,
            amount=Decimal("80.00"),
            description="Agua U3",
        ))
    sandbox["charges"] = charges

    # ── 7. Accounts Receivable ──────────────────────────────────────────
    ar_entries = []
    num_ar = min(3, len(charges))
    for i in range(num_ar):
        charge = charges[i]
        unit_idx = i % len(units)
        user_idx = i % len(users)
        ar = AccountsReceivableFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[unit_idx].id,
            debtor_user_id=users[user_idx].id,
            amount=charge.amount,
            charge_id=charge.id,
            due_date=date.today() + timedelta(days=30),
            status="pending" if i > 0 else "paid",
            paid_amount=charge.amount if i == 0 else Decimal("0.00"),
        )
        ar_entries.append(ar)
    sandbox["ar_entries"] = ar_entries

    # ── 8. Receipts + Payments ──────────────────────────────────────────
    receipts = []
    payments = []
    if ar_entries:
        ar_paid = ar_entries[0]  # already paid
        receipt = ReceiptFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[0].id,
            ar_id=ar_paid.id,
            payer_user_id=users[0].id,
            amount_paid=ar_paid.amount,
            payment_method="transfer",
            receipt_number=f"REC-{uuid.uuid4().hex[:8].upper()}",
        )
        receipts.append(receipt)

        payment = PaymentFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[0].id,
            ar_id=ar_paid.id,
            payer_user_id=users[0].id,
            amount=ar_paid.amount,
            payment_method="transfer",
            receipt_id=receipt.id,
        )
        payments.append(payment)

        # Extra payment for AR #2 (partial) — only if >1 AR exists
        if len(ar_entries) > 1 and len(units) > 1 and len(users) > 1:
            ar_partial = ar_entries[1]
            payment2 = PaymentFactory.create(
                session,
                condominium_id=condo.id,
                unit_id=units[1].id,
                ar_id=ar_partial.id,
                payer_user_id=users[1].id,
                amount=Decimal("100.00"),
                payment_method="cash",
                receipt_id=None,
            )
            payments.append(payment2)

            receipt2 = ReceiptFactory.create(
                session,
                condominium_id=condo.id,
                unit_id=units[1].id,
                ar_id=ar_partial.id,
                payer_user_id=users[1].id,
                amount_paid=Decimal("100.00"),
                payment_method="cash",
            )
            receipts.append(receipt2)
    sandbox["receipts"] = receipts
    sandbox["payments"] = payments

    # ── 9. Ledger Entries ───────────────────────────────────────────────
    ledger_entries = []
    for i, ar in enumerate(ar_entries):
        unit_idx = i % len(units)
        charge_idx = i if i < len(charges) else None
        ledger = LedgerFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[unit_idx].id,
            entry_type="charge",
            description=f"Debito por {ar.description}",
            debit=ar.amount,
            credit=Decimal("0.00"),
            ar_id=ar.id,
            charge_id=charges[charge_idx].id if charge_idx is not None else None,
        )
        ledger_entries.append(ledger)
    # Payment ledger entry (if any payments exist)
    if payments:
        ledger_entries.append(LedgerFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[0].id,
            entry_type="payment",
            description="Pago recibido",
            debit=Decimal("0.00"),
            credit=payments[0].amount,
            ar_id=ar_entries[0].id,
            payment_id=payments[0].id,
        ))
    sandbox["ledger_entries"] = ledger_entries

    # ── 10. Incidents ───────────────────────────────────────────────────
    incidents = []
    incidents.append(IncidentFactory.create(
        session,
        condominium_id=condo.id,
        unit_id=units[0].id,
        reported_by_user_id=users[0].id,
        title="Fuga de agua en baño",
        category="plumbing",
        priority="high",
        status="pending",
        building_id=buildings[0].id,
        assigned_to_user_id=users[1].id if len(users) > 1 else users[0].id,
    ))
    if len(units) > 1 and len(users) > 1:
        incidents.append(IncidentFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[1].id,
            reported_by_user_id=users[1].id,
            title="Bombilla fundida en pasillo",
            category="electrical",
            priority="low",
            status="in_progress",
        ))
    sandbox["incidents"] = incidents

    # ── 11. Visitors ────────────────────────────────────────────────────
    visitors = []
    visitors.append(VisitorFactory.create(
        session,
        condominium_id=condo.id,
        unit_id=units[0].id,
        host_user_id=users[0].id,
        visitor_name="Juan Pérez",
        status="pending",
        visit_purpose="visit",
    ))
    if len(units) > 2 and len(users) > 2:
        visitors.append(VisitorFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[2].id,
            host_user_id=users[2].id,
            visitor_name="María Delivery",
            status="checked_in",
            visit_purpose="delivery",
            access_code="V9999",
        ))
    sandbox["visitors"] = visitors

    # ── 12. Documents ───────────────────────────────────────────────────
    documents = []
    documents.append(DocumentFactory.create(
        session,
        condominium_id=condo.id,
        uploader_user_id=users[0].id,
        title="Reglamento Interno 2026",
        category="regulation",
    ))
    if len(users) > 1:
        documents.append(DocumentFactory.create(
            session,
            condominium_id=condo.id,
            uploader_user_id=users[1].id,
            title="Acta de Asamblea",
            category="minutes",
        ))
    sandbox["documents"] = documents

    # ── 13. Meeting ─────────────────────────────────────────────────────
    meeting = MeetingFactory.create(
        session,
        condominium_id=condo.id,
        created_by_user_id=users[0].id,
        title="Asamblea General Anual",
        meeting_type="assembly",
        status="scheduled",
        meeting_date=datetime.utcnow() + timedelta(days=30),
        location="Salón Comunal",
    )
    sandbox["meetings"] = [meeting]

    # ── 14. Vote ────────────────────────────────────────────────────────
    vote = VoteFactory.create(
        session,
        condominium_id=condo.id,
        created_by_user_id=users[0].id,
        title="Aprobación presupuesto 2026",
        vote_type="open",
        status="active",
        meeting_id=meeting.id,
        voting_starts_at=datetime.utcnow(),
        voting_ends_at=datetime.utcnow() + timedelta(days=7),
    )
    sandbox["votes"] = [vote]

    # ── 15. Announcements ───────────────────────────────────────────────
    announcements = []
    announcements.append(AnnouncementFactory.create(
        session,
        condominium_id=condo.id,
        author_user_id=users[0].id,
        title="Mantenimiento programado de ascensores",
        content="El próximo sábado se realizará mantenimiento...",
        category="maintenance",
        is_pinned=True,
    ))
    if len(users) > 1:
        announcements.append(AnnouncementFactory.create(
            session,
            condominium_id=condo.id,
            author_user_id=users[1].id,
            title="Recordatorio: pago de cuotas",
            content="Se recuerda a todos los propietarios...",
            category="info",
        ))
    sandbox["announcements"] = announcements

    # ── 16. Notifications ───────────────────────────────────────────────
    notifications = []
    num_notif_users = min(3, len(users))
    for i in range(num_notif_users):
        user = users[i]
        notifications.append(NotificationFactory.create(
            session,
            user_id=user.id,
            type="info",
            resource_type="announcement",
            resource_id=announcements[0].id if announcements else 1,
            title=f"Notificación para usuario {i+1}",
            body="Tienes un nuevo anuncio en el condominio.",
        ))
    sandbox["notifications"] = notifications

    # ── 17. Packages ────────────────────────────────────────────────────
    packages = []
    packages.append(PackageFactory.create(
        session,
        condominium_id=condo.id,
        unit_id=units[0].id,
        recipient_user_id=users[0].id,
        carrier="DHL",
        tracking_number="DHL-123456",
        description="Paquete de Amazon",
        status="pending",
    ))
    if len(units) > 2 and len(users) > 2:
        packages.append(PackageFactory.create(
            session,
            condominium_id=condo.id,
            unit_id=units[2].id,
            recipient_user_id=users[2].id,
            carrier="FedEx",
            tracking_number="FDX-789012",
            description="Documentos legales",
            status="delivered",
        ))
    sandbox["packages"] = packages

    # ── 18. Amenities ───────────────────────────────────────────────────
    amenities = []
    amenities.append(AmenityFactory.create(
        session,
        condominium_id=condo.id,
        name="Piscina",
        scope="CONDOMINIUM",
        location="Terraza",
        max_capacity=30,
        booking_duration_min=120,
        requires_approval=False,
        status="active",
    ))
    amenities.append(AmenityFactory.create(
        session,
        condominium_id=condo.id,
        name="Gimnasio",
        scope="BUILDING",
        building_id=buildings[0].id,
        location="Piso 1",
        max_capacity=15,
        booking_duration_min=60,
        requires_approval=True,
        status="active",
    ))
    sandbox["amenities"] = amenities

    return sandbox


# ── Cleanup ─────────────────────────────────────────────────────────────────

def sandbox_cleanup(session, sandbox: dict) -> None:
    """
    Delete all entities created by create_integration_sandbox().

    Deletion order respects FK constraints (most-dependent → parent).
    Key rule: referencing tables deleted BEFORE referenced tables.
    """
    deletion_order = [
        # Leaf tables (most dependent, have FKs to everything else)
        ("ledger_entries", lambda e: e),
        ("notifications", lambda e: e),
        ("packages", lambda e: e),
        ("payments", lambda e: e),       # has FK → receipts, AR, units, users
        ("visitors", lambda e: e),
        ("incidents", lambda e: e),
        ("announcements", lambda e: e),
        ("documents", lambda e: e),
        ("votes", lambda e: e),
        ("meetings", lambda e: e),
        ("amenities", lambda e: e),
        ("receipts", lambda e: e),       # referenced by payments (already deleted)
        ("ar_entries", lambda e: e),     # referenced by ledger, payments, receipts
        ("charges", lambda e: e),
        ("charge_types", lambda e: e),
        # Parent tables
        ("residents", lambda e: e),
        ("units", lambda e: e),
        ("buildings", lambda e: e),
        ("users", lambda e: e),
        ("condo", lambda e: e),
    ]

    for key, _ in deletion_order:
        items = sandbox.pop(key, None)
        if items is None:
            continue
        if not isinstance(items, list):
            items = [items]
        for item in items:
            if item is not None:
                session.delete(item)
        session.flush()  # flush per-table to respect FK order
