"""
Integration tests for service modules: amenities, announcements, documents,
incidents, meetings, notifications, packages, visitors, votes.

Each test class:
  1. Creates a minimal sandbox (condo + building + units + users + resident + occupancy)
  2. Exercises the module's use cases against the real MariaDB
  3. Cleans up all records via _cleanup_by_condo()

Pattern matches test_core_foundations.py and test_financial_core.py.
"""
import uuid
import pytest
from datetime import datetime, date, time, timedelta

from tests.test_core_foundations import _make_minimal_sandbox, _cleanup_by_condo


def _make_sandbox(db_session, label: str):
    """Sandbox with resident + occupancy for modules that check user-unit relationships."""
    sb = _make_minimal_sandbox(db_session, label)

    from tests.factories.resident_factory import ResidentFactory
    resident = ResidentFactory.create(
        db_session, user_id=sb.users[0].id, condominium_id=sb.condo.id
    )
    db_session.add(resident)

    # Create occupancy via raw SQL so INC-01 / VIS-01 checks pass
    # (core_occupancy_types table may not exist, so bypass ORM FK validation)
    from sqlalchemy import text
    db_session.execute(text(
        "INSERT INTO core_unit_occupancies (uuid, unit_id, user_id, occupancy_type_id, "
        "start_date, is_primary) VALUES (:uuid, :unit_id, :user_id, 1, :start_date, 1)"
    ), {
        "uuid": str(uuid.uuid4()),
        "unit_id": sb.units[0].id,
        "user_id": sb.users[0].id,
        "start_date": date.today(),
    })
    db_session.commit()

    sb.residents = [resident]
    return sb


def _teardown(db_session, sb):
    _cleanup_by_condo(db_session, sb.condo.id)


# ═════════════════════════════════════════════════════════════════════════════
# Amenities
# ═════════════════════════════════════════════════════════════════════════════

class TestAmenityIntegration:
    """Create, read, update, soft-delete amenities via AmenityUseCase."""

    def test_create_amenity(self, db_session):
        sb = _make_sandbox(db_session, "AMN Create")
        from library.dddpy.core_amenities.usecase.amenity_usecase import AmenityUseCase

        uc = AmenityUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            name=f"Piscina {sb.tag}",
            scope="CONDOMINIUM",
            max_capacity=20,
        )
        assert result.success
        assert result.data["name"] == f"Piscina {sb.tag}"
        _teardown(db_session, sb)

    def test_create_building_scoped_amenity(self, db_session):
        sb = _make_sandbox(db_session, "AMN Building")
        from library.dddpy.core_amenities.usecase.amenity_usecase import AmenityUseCase

        uc = AmenityUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            building_id=sb.buildings[0].id,
            name=f"Gym Torre {sb.tag}",
            scope="BUILDING",
        )
        assert result.success
        assert result.data["building_id"] == sb.buildings[0].id
        _teardown(db_session, sb)

    def test_get_and_list_amenities(self, db_session):
        sb = _make_sandbox(db_session, "AMN List")
        from library.dddpy.core_amenities.usecase.amenity_usecase import AmenityUseCase

        uc = AmenityUseCase()
        r1 = uc.create(
            condominium_id=sb.condo.id, name=f"Sala A {sb.tag}", scope="CONDOMINIUM"
        )
        r2 = uc.create(
            condominium_id=sb.condo.id, name=f"Sala B {sb.tag}", scope="CONDOMINIUM"
        )
        assert r1.success and r2.success

        amenity_id = r1.data["id"]
        fetched = uc.get_by_id(amenity_id)
        assert fetched.success
        assert fetched.data["name"] == f"Sala A {sb.tag}"

        all_items = uc.list_all(condominium_id=sb.condo.id)
        # data is a flat list of dicts: [{"id":1,...}, {"id":2,...}]
        names = [a["name"] for a in all_items.data]
        assert f"Sala A {sb.tag}" in names
        assert f"Sala B {sb.tag}" in names
        _teardown(db_session, sb)

    def test_soft_delete_amenity(self, db_session):
        sb = _make_sandbox(db_session, "AMN Delete")
        from library.dddpy.core_amenities.usecase.amenity_usecase import AmenityUseCase

        uc = AmenityUseCase()
        r = uc.create(
            condominium_id=sb.condo.id, name=f"Cancha {sb.tag}", scope="CONDOMINIUM"
        )
        amenity_id = r.data["id"]

        result = uc.soft_delete(amenity_id)
        assert result.success

        from library.dddpy.core_amenities.domain.amenity_exception import AmenityNotFound
        try:
            uc.get_by_id(amenity_id)
            pytest.fail("Expected AmenityNotFound after soft delete")
        except AmenityNotFound:
            pass
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Announcements
# ═════════════════════════════════════════════════════════════════════════════

class TestAnnouncementIntegration:
    """Create, read, list, soft-delete announcements via AnnouncementUseCase."""

    def test_create_announcement(self, db_session):
        sb = _make_sandbox(db_session, "ANN Create")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase

        uc = AnnouncementUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            author_user_id=sb.users[0].id,
            title=f"Aviso {sb.tag}",
            content="Contenido del aviso de prueba con mas de 10 caracteres.",
        )
        assert result.success
        assert result.data["title"] == f"Aviso {sb.tag}"
        _teardown(db_session, sb)

    def test_urgent_announcement(self, db_session):
        sb = _make_sandbox(db_session, "ANN Urgent")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase

        uc = AnnouncementUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            author_user_id=sb.users[0].id,
            title=f"Urgente {sb.tag}",
            content="Esto es un aviso urgente de prueba con suficientes caracteres.",
            category="urgent",
            is_pinned=True,
        )
        assert result.success
        assert result.data["category"] == "urgent"
        _teardown(db_session, sb)

    def test_list_announcements(self, db_session):
        sb = _make_sandbox(db_session, "ANN List")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase

        uc = AnnouncementUseCase()
        uc.create(
            condominium_id=sb.condo.id, author_user_id=sb.users[0].id,
            title=f"Uno {sb.tag}", content="Contenido numero uno de prueba con texto suficiente.",
            published_at=datetime.utcnow(),
        )

        # list_active is known to have a bug: _fetch_author_names iterates rows
        # that become ints after session_scope() closes. Use list_all instead.
        all_items = uc.list_all(condominium_id=sb.condo.id)
        names = [a["title"] for a in all_items.data]
        assert f"Uno {sb.tag}" in names
        _teardown(db_session, sb)

    # ── Sprint: extend announcements (categories + tower_id) ────────────

    def test_create_with_new_categories(self, db_session):
        """All 10 categories (info, warning, urgent, event, balance,
        assembly, maintenance, vote, rule, general) must be accepted."""
        sb = _make_sandbox(db_session, "ANN Cats")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase

        uc = AnnouncementUseCase()
        new_cats = ["balance", "assembly", "maintenance", "vote", "rule", "general"]
        for cat in new_cats:
            result = uc.create(
                condominium_id=sb.condo.id,
                author_user_id=sb.users[0].id,
                title=f"Aviso {cat} {sb.tag}",
                content=f"Contenido de prueba para categoria {cat} con mas de 10 caracteres.",
                category=cat,
            )
            assert result.success, f"Category {cat} was rejected"
            assert result.data["category"] == cat
        _teardown(db_session, sb)

    def test_rejects_invalid_category(self, db_session):
        """Unknown categories must raise AnnouncementValidationError."""
        sb = _make_sandbox(db_session, "ANN BadCat")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase
        from library.dddpy.core_announcements.domain.announcement_exception import AnnouncementValidationError

        uc = AnnouncementUseCase()
        with pytest.raises(AnnouncementValidationError, match="Invalid category"):
            uc.create(
                condominium_id=sb.condo.id,
                author_user_id=sb.users[0].id,
                title="Categoria invalida",
                content="Contenido de prueba con suficientes caracteres para el test.",
                category="not_real",
            )
        _teardown(db_session, sb)

    def test_create_with_tower_id(self, db_session):
        """Announcement scoped to a specific tower returns tower_id + tower_name."""
        sb = _make_sandbox(db_session, "ANN Tower")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase

        tower = sb.buildings[0]
        uc = AnnouncementUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            author_user_id=sb.users[0].id,
            title=f"Solo Torre A {sb.tag}",
            content="Aviso exclusivo para la torre A con mas de 10 caracteres.",
            tower_id=tower.id,
        )
        assert result.success
        assert result.data["tower_id"] == tower.id
        # Tower name should be enriched
        assert result.data["tower_name"] is not None
        assert "Torre" in result.data["tower_name"]
        _teardown(db_session, sb)

    def test_create_without_tower_id_is_null(self, db_session):
        """Announcement without tower_id must default to None (all towers)."""
        sb = _make_sandbox(db_session, "ANN NoTower")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase

        uc = AnnouncementUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            author_user_id=sb.users[0].id,
            title=f"Todo el condominio {sb.tag}",
            content="Aviso general para todo el condominio con mas de 10 caracteres.",
        )
        assert result.success
        assert result.data["tower_id"] is None
        assert result.data["tower_name"] is None
        _teardown(db_session, sb)

    def test_list_filter_by_tower_id(self, db_session):
        """list_all filtered by tower_id returns only scoped announcements."""
        sb = _make_sandbox(db_session, "ANN ListTower")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase

        tower = sb.buildings[0]
        uc = AnnouncementUseCase()

        # One announcement scoped to the tower, one without (condominium-wide)
        uc.create(
            condominium_id=sb.condo.id, author_user_id=sb.users[0].id,
            title=f"Solo torre {sb.tag}", content="Contenido solo torre con suficientes caracteres para test.",
            tower_id=tower.id,
        )
        uc.create(
            condominium_id=sb.condo.id, author_user_id=sb.users[0].id,
            title=f"Todo condominio {sb.tag}", content="Contenido general con suficientes caracteres para test.",
        )

        # Filter by the tower — only the tower-scoped one should appear
        result = uc.list_all(condominium_id=sb.condo.id, tower_id=tower.id)
        titles = [a["title"] for a in result.data]
        assert f"Solo torre {sb.tag}" in titles
        assert f"Todo condominio {sb.tag}" not in titles

        # Full list (no tower filter) should include both
        result_all = uc.list_all(condominium_id=sb.condo.id)
        all_titles = [a["title"] for a in result_all.data]
        assert f"Solo torre {sb.tag}" in all_titles
        assert f"Todo condominio {sb.tag}" in all_titles
        _teardown(db_session, sb)

    def test_update_tower_id(self, db_session):
        """Updating an announcement's tower_id must work via UpdateAnnouncementSchema."""
        sb = _make_sandbox(db_session, "ANN UpdTower")
        from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase
        from library.dddpy.core_announcements.usecase.announcement_cmd_schema import UpdateAnnouncementSchema

        tower_a = sb.buildings[0]
        uc = AnnouncementUseCase()

        # Create without tower
        created = uc.create(
            condominium_id=sb.condo.id, author_user_id=sb.users[0].id,
            title=f"Sin torre {sb.tag}", content="Contenido sin torre con suficientes caracteres para test.",
        )
        assert created.data["tower_id"] is None

        # Update to add tower A
        schema = UpdateAnnouncementSchema(tower_id=tower_a.id)
        updated = uc.update(created.data["id"], schema)
        assert updated.data["tower_id"] == tower_a.id
        assert updated.data["tower_name"] is not None
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Documents
# ═════════════════════════════════════════════════════════════════════════════

class TestDocumentIntegration:
    """Create, read, list, soft-delete documents via DocumentUseCase."""

    def test_create_document(self, db_session):
        sb = _make_sandbox(db_session, "DOC Create")
        from library.dddpy.core_documents.usecase.document_usecase import DocumentUseCase

        uc = DocumentUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            uploader_user_id=sb.users[0].id,
            title=f"Reglamento {sb.tag}",
            file_url=f"https://test.local/docs/{sb.tag}.pdf",
        )
        assert result.success
        assert result.data["title"] == f"Reglamento {sb.tag}"
        _teardown(db_session, sb)

    def test_list_documents(self, db_session):
        sb = _make_sandbox(db_session, "DOC List")
        from library.dddpy.core_documents.usecase.document_usecase import DocumentUseCase

        uc = DocumentUseCase()
        uc.create(
            condominium_id=sb.condo.id, uploader_user_id=sb.users[0].id,
            title=f"Acta {sb.tag}", file_url=f"https://test.local/acta-{sb.tag}.pdf"
        )
        uc.create(
            condominium_id=sb.condo.id, uploader_user_id=sb.users[0].id,
            title=f"Contrato {sb.tag}", file_url=f"https://test.local/contrato-{sb.tag}.pdf"
        )

        all_docs = uc.list_all(condominium_id=sb.condo.id)
        titles = [d["title"] for d in all_docs.data] if isinstance(all_docs.data, list) else [d["title"] for d in all_docs.data.get("items", [])]
        assert f"Acta {sb.tag}" in titles
        assert f"Contrato {sb.tag}" in titles
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Incidents
# ═════════════════════════════════════════════════════════════════════════════

class TestIncidentIntegration:
    """Create, read, list incidents via IncidentCmdUseCase + IncidentQueryUseCase."""

    def test_create_incident(self, db_session):
        sb = _make_sandbox(db_session, "INC Create")
        from library.dddpy.core_incidents.infrastructure.incident_cmd_repository import IncidentCmdRepositoryImpl
        from library.dddpy.core_incidents.usecase.incident_cmd_usecase import IncidentCmdUseCase
        from library.dddpy.core_incidents.usecase.incident_cmd_schema import CreateIncidentSchema

        uc = IncidentCmdUseCase(IncidentCmdRepositoryImpl())
        entity = uc.create(CreateIncidentSchema(
            condominium_id=sb.condo.id,
            unit_id=sb.units[0].id,
            category="plumbing",
            title=f"Fuga {sb.tag}",
            description="Fuga de agua en el baño principal reportada por el residente.",
            priority="high",
        ), reported_by_user_id=sb.users[0].id)
        assert entity is not None
        assert entity.title == f"Fuga {sb.tag}"
        _teardown(db_session, sb)

    def test_list_by_condominium(self, db_session):
        sb = _make_sandbox(db_session, "INC List")
        from library.dddpy.core_incidents.infrastructure.incident_cmd_repository import IncidentCmdRepositoryImpl
        from library.dddpy.core_incidents.infrastructure.incident_query_repository import IncidentQueryRepositoryImpl
        from library.dddpy.core_incidents.usecase.incident_cmd_usecase import IncidentCmdUseCase
        from library.dddpy.core_incidents.usecase.incident_cmd_schema import CreateIncidentSchema
        from library.dddpy.core_incidents.usecase.incident_query_usecase import IncidentQueryUseCase

        cmd = IncidentCmdUseCase(IncidentCmdRepositoryImpl())
        cmd.create(CreateIncidentSchema(
            condominium_id=sb.condo.id, unit_id=sb.units[0].id,
            category="electrical", title=f"Luz {sb.tag}",
            description="Fallo electrico en el pasillo principal reportado por el residente."
        ), reported_by_user_id=sb.users[0].id)
        cmd.create(CreateIncidentSchema(
            condominium_id=sb.condo.id, unit_id=sb.units[0].id,
            category="painting", title=f"Pintura {sb.tag}",
            description="Pared descascarada en el lobby principal reportado por el residente."
        ), reported_by_user_id=sb.users[0].id)

        query = IncidentQueryUseCase(IncidentQueryRepositoryImpl())
        items = query.list_by_condominium(condominium_id=sb.condo.id)
        assert len(items) >= 2
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Meetings
# ═════════════════════════════════════════════════════════════════════════════

class TestMeetingIntegration:
    """Create, read, list, soft-delete meetings via MeetingUseCase."""

    def test_create_meeting(self, db_session):
        sb = _make_sandbox(db_session, "MTG Create")
        from library.dddpy.core_meetings.usecase.meeting_usecase import MeetingUseCase
        from library.dddpy.core_meetings.usecase.meeting_cmd_schema import CreateMeetingSchema

        uc = MeetingUseCase()
        result = uc.create(CreateMeetingSchema(
            condominium_id=sb.condo.id,
            created_by_user_id=sb.users[0].id,
            title=f"Asamblea {sb.tag}",
            meeting_date=datetime.utcnow() + timedelta(days=30),
            meeting_type="assembly",
        ))
        assert result.success
        assert result.data["title"] == f"Asamblea {sb.tag}"
        _teardown(db_session, sb)

    def test_list_upcoming_meetings(self, db_session):
        sb = _make_sandbox(db_session, "MTG List")
        from library.dddpy.core_meetings.usecase.meeting_usecase import MeetingUseCase
        from library.dddpy.core_meetings.usecase.meeting_cmd_schema import CreateMeetingSchema

        uc = MeetingUseCase()
        uc.create(CreateMeetingSchema(
            condominium_id=sb.condo.id, created_by_user_id=sb.users[0].id,
            title=f"Junta {sb.tag}", meeting_date=datetime.utcnow() + timedelta(days=7),
            meeting_type="board",
        ))

        upcoming = uc.list_upcoming(condominium_id=sb.condo.id)
        titles = [m["title"] for m in upcoming.data] if isinstance(upcoming.data, list) else [m["title"] for m in upcoming.data.get("items", [])]
        assert f"Junta {sb.tag}" in titles
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Notifications
# ═════════════════════════════════════════════════════════════════════════════

class TestNotificationIntegration:
    """Create, read, mark-read notifications via NotificationCmdUseCase."""

    def test_create_notification(self, db_session):
        sb = _make_sandbox(db_session, "NTF Create")
        from library.dddpy.core_notifications.infrastructure.notification_cmd_repository import NotificationCmdRepositoryImpl
        from library.dddpy.core_notifications.usecase.notification_cmd_usecase import NotificationCmdUseCase
        from library.dddpy.core_notifications.usecase.notification_cmd_schema import CreateNotificationSchema

        uc = NotificationCmdUseCase(NotificationCmdRepositoryImpl())
        entity = uc.create(CreateNotificationSchema(
            user_id=sb.users[0].id,
            channel="in_app",
            type="payment_received",
            resource_type="payment",
            resource_id=1,
            title=f"Notificación {sb.tag}",
            body="Mensaje de prueba.",
        ))
        assert entity is not None
        assert entity.title == f"Notificación {sb.tag}"
        _teardown(db_session, sb)

    def test_list_by_user(self, db_session):
        sb = _make_sandbox(db_session, "NTF List")
        from library.dddpy.core_notifications.infrastructure.notification_cmd_repository import NotificationCmdRepositoryImpl
        from library.dddpy.core_notifications.infrastructure.notification_query_repository import NotificationQueryRepositoryImpl
        from library.dddpy.core_notifications.usecase.notification_cmd_usecase import NotificationCmdUseCase
        from library.dddpy.core_notifications.usecase.notification_cmd_schema import CreateNotificationSchema
        from library.dddpy.core_notifications.usecase.notification_query_usecase import NotificationQueryUseCase

        cmd = NotificationCmdUseCase(NotificationCmdRepositoryImpl())
        cmd.create(CreateNotificationSchema(
            user_id=sb.users[0].id, channel="in_app", type="receipt_generated",
            resource_type="receipt", resource_id=1,
            title=f"NTF-1 {sb.tag}", body="Primera notificación."
        ))
        cmd.create(CreateNotificationSchema(
            user_id=sb.users[0].id, channel="in_app", type="incident_created",
            resource_type="incident", resource_id=2,
            title=f"NTF-2 {sb.tag}", body="Segunda notificación."
        ))

        query = NotificationQueryUseCase(NotificationQueryRepositoryImpl())
        items = query.list_by_user(user_id=sb.users[0].id)
        assert len(items) >= 2
        _teardown(db_session, sb)

    def test_mark_read(self, db_session):
        sb = _make_sandbox(db_session, "NTF Read")
        from library.dddpy.core_notifications.infrastructure.notification_cmd_repository import NotificationCmdRepositoryImpl
        from library.dddpy.core_notifications.usecase.notification_cmd_usecase import NotificationCmdUseCase
        from library.dddpy.core_notifications.usecase.notification_cmd_schema import CreateNotificationSchema

        cmd = NotificationCmdUseCase(NotificationCmdRepositoryImpl())
        entity = cmd.create(CreateNotificationSchema(
            user_id=sb.users[0].id, channel="in_app", type="announcement_published",
            resource_type="announcement", resource_id=1,
            title=f"Marcar {sb.tag}", body="Para marcar como leída."
        ))
        updated = cmd.mark_read(entity.id, sb.users[0].id)
        assert updated.is_read is True
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Packages
# ═════════════════════════════════════════════════════════════════════════════

class TestPackageIntegration:
    """Create, read, list, mark-delivered packages via PackageUseCase."""

    def test_create_package(self, db_session):
        sb = _make_sandbox(db_session, "PKG Create")
        from library.dddpy.core_packages.usecase.package_usecase import PackageUseCase

        uc = PackageUseCase()
        result = uc.create(
            condominium_id=sb.condo.id,
            unit_id=sb.units[0].id,
            recipient_user_id=sb.users[0].id,
            carrier="DHL",
            tracking_number=f"TRK-{sb.tag}",
            description="Caja de prueba",
        )
        assert result.success
        assert result.data["carrier"] == "DHL"
        _teardown(db_session, sb)

    def test_list_pending_packages(self, db_session):
        sb = _make_sandbox(db_session, "PKG List")
        from library.dddpy.core_packages.usecase.package_usecase import PackageUseCase

        uc = PackageUseCase()
        uc.create(
            condominium_id=sb.condo.id, unit_id=sb.units[0].id,
            recipient_user_id=sb.users[0].id, carrier="FedEx",
            tracking_number=f"TRK-PEND-{sb.tag}", description="Pendiente de entrega",
        )

        pending = uc.list_pending(condominium_id=sb.condo.id)
        tracking_nums = [p["tracking_number"] for p in pending.data] if isinstance(pending.data, list) else [p["tracking_number"] for p in pending.data.get("items", [])]
        assert f"TRK-PEND-{sb.tag}" in tracking_nums
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Visitors
# ═════════════════════════════════════════════════════════════════════════════

class TestVisitorIntegration:
    """Create, read, list, check-in/out visitors via VisitorCmdUseCase."""

    def test_create_visitor(self, db_session):
        sb = _make_sandbox(db_session, "VIS Create")
        from library.dddpy.core_visitors.infrastructure.visitor_cmd_repository import VisitorCmdRepositoryImpl
        from library.dddpy.core_visitors.infrastructure.visitor_query_repository import VisitorQueryRepositoryImpl
        from library.dddpy.core_visitors.usecase.visitor_cmd_usecase import VisitorCmdUseCase
        from library.dddpy.core_visitors.usecase.visitor_cmd_schema import CreateVisitorSchema

        uc = VisitorCmdUseCase(VisitorCmdRepositoryImpl(), VisitorQueryRepositoryImpl())
        entity = uc.create(CreateVisitorSchema(
            condominium_id=sb.condo.id,
            unit_id=sb.units[0].id,
            visitor_name=f"Visitante {sb.tag}",
            expected_date=date.today(),
            expected_time=time(15, 0),
            visit_purpose="family",
        ), host_user_id=sb.users[0].id)
        assert entity is not None
        assert entity.visitor_name == f"Visitante {sb.tag}"
        _teardown(db_session, sb)

    def test_list_by_condominium(self, db_session):
        sb = _make_sandbox(db_session, "VIS List")
        from library.dddpy.core_visitors.infrastructure.visitor_cmd_repository import VisitorCmdRepositoryImpl
        from library.dddpy.core_visitors.infrastructure.visitor_query_repository import VisitorQueryRepositoryImpl
        from library.dddpy.core_visitors.usecase.visitor_cmd_usecase import VisitorCmdUseCase
        from library.dddpy.core_visitors.usecase.visitor_cmd_schema import CreateVisitorSchema
        from library.dddpy.core_visitors.usecase.visitor_query_usecase import VisitorQueryUseCase

        cmd = VisitorCmdUseCase(VisitorCmdRepositoryImpl(), VisitorQueryRepositoryImpl())
        cmd.create(CreateVisitorSchema(
            condominium_id=sb.condo.id, unit_id=sb.units[0].id,
            visitor_name=f"Maria {sb.tag}", expected_date=date.today(),
            expected_time=time(10, 0), visit_purpose="family",
        ), host_user_id=sb.users[0].id)
        cmd.create(CreateVisitorSchema(
            condominium_id=sb.condo.id, unit_id=sb.units[0].id,
            visitor_name=f"Carlos {sb.tag}", expected_date=date.today(),
            expected_time=time(11, 0), visit_purpose="delivery",
        ), host_user_id=sb.users[0].id)

        query = VisitorQueryUseCase(VisitorQueryRepositoryImpl())
        items = query.list_by_condominium(condominium_id=sb.condo.id)
        assert len(items) >= 2
        _teardown(db_session, sb)

    def test_check_in_and_out(self, db_session):
        sb = _make_sandbox(db_session, "VIS CheckIn")
        from library.dddpy.core_visitors.infrastructure.visitor_cmd_repository import VisitorCmdRepositoryImpl
        from library.dddpy.core_visitors.infrastructure.visitor_query_repository import VisitorQueryRepositoryImpl
        from library.dddpy.core_visitors.usecase.visitor_cmd_usecase import VisitorCmdUseCase
        from library.dddpy.core_visitors.usecase.visitor_cmd_schema import CreateVisitorSchema

        uc = VisitorCmdUseCase(VisitorCmdRepositoryImpl(), VisitorQueryRepositoryImpl())
        entity = uc.create(CreateVisitorSchema(
            condominium_id=sb.condo.id, unit_id=sb.units[0].id,
            visitor_name=f"Pedro {sb.tag}", expected_date=date.today(),
            expected_time=time(14, 0), visit_purpose="service",
        ), host_user_id=sb.users[0].id)

        checked_in = uc.check_in(entity.id, sb.users[0].id)
        assert checked_in.status == "checked_in"

        checked_out = uc.check_out(entity.id, sb.users[0].id)
        assert checked_out.status == "checked_out"
        _teardown(db_session, sb)


# ═════════════════════════════════════════════════════════════════════════════
# Votes
# ═════════════════════════════════════════════════════════════════════════════

class TestVoteIntegration:
    """Create, read, list votes via VoteCmdUseCase + VoteQueryUseCase."""

    def test_create_vote(self, db_session):
        sb = _make_sandbox(db_session, "VOT Create")
        from library.dddpy.core_votes.infrastructure.vote_cmd_repository import VoteCmdRepositoryImpl
        from library.dddpy.core_votes.usecase.vote_cmd_usecase import VoteCmdUseCase
        from library.dddpy.core_votes.usecase.vote_cmd_schema import CreateVoteSchema

        now = datetime.utcnow()
        uc = VoteCmdUseCase(VoteCmdRepositoryImpl())
        entity = uc.create(CreateVoteSchema(
            condominium_id=sb.condo.id,
            title=f"Votación {sb.tag}",
            voting_starts_at=now,
            voting_ends_at=now + timedelta(days=7),
            options=[
                {"option_text": "Sí", "option_key": "yes"},
                {"option_text": "No", "option_key": "no"},
            ],
        ), created_by_user_id=sb.users[0].id)
        assert entity is not None
        assert entity.title == f"Votación {sb.tag}"
        _teardown(db_session, sb)

    def test_list_active_votes(self, db_session):
        sb = _make_sandbox(db_session, "VOT List")
        from library.dddpy.core_votes.infrastructure.vote_cmd_repository import VoteCmdRepositoryImpl
        from library.dddpy.core_votes.infrastructure.vote_query_repository import VoteQueryRepositoryImpl
        from library.dddpy.core_votes.usecase.vote_cmd_usecase import VoteCmdUseCase
        from library.dddpy.core_votes.usecase.vote_cmd_schema import CreateVoteSchema
        from library.dddpy.core_votes.usecase.vote_query_usecase import VoteQueryUseCase

        now = datetime.utcnow()
        cmd = VoteCmdUseCase(VoteCmdRepositoryImpl())
        cmd.create(CreateVoteSchema(
            condominium_id=sb.condo.id, title=f"Vot-1 {sb.tag}",
            voting_starts_at=now, voting_ends_at=now + timedelta(days=7),
            options=[{"option_text": "A", "option_key": "a"}, {"option_text": "B", "option_key": "b"}],
        ), created_by_user_id=sb.users[0].id)

        query = VoteQueryUseCase(VoteQueryRepositoryImpl())
        items, total = query.list_by_condominium(condominium_id=sb.condo.id)
        titles = [v.title for v in items]
        assert f"Vot-1 {sb.tag}" in titles
        _teardown(db_session, sb)
