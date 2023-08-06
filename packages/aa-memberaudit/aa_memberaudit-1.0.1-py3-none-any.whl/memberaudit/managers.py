from copy import deepcopy
import datetime as dt
from math import floor
from typing import Dict, Iterable, Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    Avg,
    Case,
    Count,
    F,
    ExpressionWrapper,
    Max,
    Min,
    Value,
    When,
)
from django.utils.timezone import now

from bravado.exception import HTTPUnauthorized, HTTPForbidden
from esi.models import Token

from eveuniverse.models import EveEntity, EveSolarSystem, EveType

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.services.hooks import get_extension_logger

from . import __title__
from .constants import (
    EVE_TYPE_ID_SOLAR_SYSTEM,
    EVE_CATEGORY_ID_SKILL,
    EVE_CATEGORY_ID_SHIP,
)
from .app_settings import MEMBERAUDIT_LOCATION_STALE_HOURS
from .helpers import fetch_esi_status
from .providers import esi
from .utils import LoggerAddTag, ObjectCacheMixin


logger = LoggerAddTag(get_extension_logger(__name__), __title__)

BULK_METHODS_BATCH_SIZE = 500


class EveShipTypeManger(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("eve_group")
            .filter(published=True)
            .filter(eve_group__eve_category_id=EVE_CATEGORY_ID_SHIP)
        )


class EveSkillTypeManger(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("eve_group")
            .filter(published=True)
            .filter(eve_group__eve_category_id=EVE_CATEGORY_ID_SKILL)
        )


class LocationManager(models.Manager):
    """Manager for Location model

    We recommend preferring the "async" variants, because it includes protection
    against exceeding the ESI error limit due to characters no longer having access
    to structures within their assets, contracts, etc.

    The async methods will first create an empty location and then try to
    update that empty location asynchronously from ESI.
    Updates might be delayed if the error limit is reached.

    The async method can also be used safely in mass updates, where the same
    unauthorized update might be requested multiple times.
    Additional requests for the same location will be ignored within a grace period.
    """

    _UPDATE_EMPTY_GRACE_MINUTES = 5

    def get_or_create_esi(self, id: int, token: Token) -> Tuple[models.Model, bool]:
        """gets or creates location object with data fetched from ESI

        Stale locations will always be updated.
        Empty locations will always be updated after grace period as passed
        """
        return self._get_or_create_esi(id=id, token=token, update_async=False)

    def get_or_create_esi_async(
        self, id: int, token: Token
    ) -> Tuple[models.Model, bool]:
        """gets or creates location object with data fetched from ESI asynchronous"""
        return self._get_or_create_esi(id=id, token=token, update_async=True)

    def _get_or_create_esi(
        self, id: int, token: Token, update_async: bool = True
    ) -> Tuple[models.Model, bool]:
        id = int(id)
        empty_threshold = now() - dt.timedelta(minutes=self._UPDATE_EMPTY_GRACE_MINUTES)
        stale_threshold = now() - dt.timedelta(hours=MEMBERAUDIT_LOCATION_STALE_HOURS)
        try:
            location = (
                self.exclude(
                    eve_type__isnull=True,
                    eve_solar_system__isnull=True,
                    updated_at__lt=empty_threshold,
                )
                .exclude(updated_at__lt=stale_threshold)
                .get(id=id)
            )
            created = False
        except self.model.DoesNotExist:
            if update_async:
                location, created = self.update_or_create_esi_async(id=id, token=token)
            else:
                location, created = self.update_or_create_esi(id=id, token=token)

        return location, created

    def update_or_create_esi_async(
        self, id: int, token: Token
    ) -> Tuple[models.Model, bool]:
        """updates or creates location object with data fetched from ESI asynchronous"""
        return self._update_or_create_esi(id=id, token=token, update_async=True)

    def update_or_create_esi(self, id: int, token: Token) -> Tuple[models.Model, bool]:
        """updates or creates location object with data fetched from ESI synchronous

        The preferred method to use is: `update_or_create_esi_async()`,
        since it protects against exceeding the ESI error limit and which can happen
        a lot due to users not having authorization to access a structure.
        """
        return self._update_or_create_esi(id=id, token=token, update_async=False)

    def _update_or_create_esi(
        self, id: int, token: Token, update_async: bool = True
    ) -> Tuple[models.Model, bool]:
        id = int(id)
        if self.model.is_solar_system_id(id):
            eve_solar_system, _ = EveSolarSystem.objects.get_or_create_esi(id=id)
            eve_type, _ = EveType.objects.get_or_create_esi(id=EVE_TYPE_ID_SOLAR_SYSTEM)
            location, created = self.update_or_create(
                id=id,
                defaults={
                    "name": eve_solar_system.name,
                    "eve_solar_system": eve_solar_system,
                    "eve_type": eve_type,
                },
            )
        elif self.model.is_station_id(id):
            logger.info("%s: Fetching station from ESI", id)
            station = esi.client.Universe.get_universe_stations_station_id(
                station_id=id
            ).results()
            location, created = self._station_update_or_create_dict(
                id=id, station=station
            )

        elif self.model.is_structure_id(id):
            if update_async:
                location, created = self._structure_update_or_create_esi_async(
                    id=id, token=token
                )
            else:
                location, created = self.structure_update_or_create_esi(
                    id=id, token=token
                )
        else:
            logger.warning(
                "%s: Creating empty location for ID not matching any known pattern:", id
            )
            location, created = self.get_or_create(id=id)

        return location, created

    def _station_update_or_create_dict(
        self, id: int, station: dict
    ) -> Tuple[models.Model, bool]:
        if station.get("system_id"):
            eve_solar_system, _ = EveSolarSystem.objects.get_or_create_esi(
                id=station.get("system_id")
            )
        else:
            eve_solar_system = None

        if station.get("type_id"):
            eve_type, _ = EveType.objects.get_or_create_esi(id=station.get("type_id"))
        else:
            eve_type = None

        if station.get("owner"):
            owner, _ = EveEntity.objects.get_or_create_esi(id=station.get("owner"))
        else:
            owner = None

        return self.update_or_create(
            id=id,
            defaults={
                "name": station.get("name", ""),
                "eve_solar_system": eve_solar_system,
                "eve_type": eve_type,
                "owner": owner,
            },
        )

    def _structure_update_or_create_esi_async(self, id: int, token: Token):
        from .tasks import (
            update_structure_esi as task_update_structure_esi,
            DEFAULT_TASK_PRIORITY,
        )

        id = int(id)
        location, created = self.get_or_create(id=id)
        task_update_structure_esi.apply_async(
            kwargs={"id": id, "token_pk": token.pk},
            priority=DEFAULT_TASK_PRIORITY,
        )
        return location, created

    def structure_update_or_create_esi(self, id: int, token: Token):
        """Update or creates structure from ESI"""
        fetch_esi_status().raise_for_status()
        try:
            structure = esi.client.Universe.get_universe_structures_structure_id(
                structure_id=id, token=token.valid_access_token()
            ).results()
        except (HTTPUnauthorized, HTTPForbidden) as http_error:
            logger.warn(
                "%s: No access to structure #%s: %s",
                token.character_name,
                id,
                http_error,
            )
            location, created = self.get_or_create(id=id)
        else:
            location, created = self._structure_update_or_create_dict(
                id=id, structure=structure
            )
        return location, created

    def _structure_update_or_create_dict(
        self, id: int, structure: dict
    ) -> Tuple[models.Model, bool]:
        """creates a new Location object from a structure dict"""
        if structure.get("solar_system_id"):
            eve_solar_system, _ = EveSolarSystem.objects.get_or_create_esi(
                id=structure.get("solar_system_id")
            )
        else:
            eve_solar_system = None

        if structure.get("type_id"):
            eve_type, _ = EveType.objects.get_or_create_esi(id=structure.get("type_id"))
        else:
            eve_type = None

        if structure.get("owner_id"):
            owner, _ = EveEntity.objects.get_or_create_esi(id=structure.get("owner_id"))
        else:
            owner = None

        return self.update_or_create(
            id=id,
            defaults={
                "name": structure.get("name", ""),
                "eve_solar_system": eve_solar_system,
                "eve_type": eve_type,
                "owner": owner,
            },
        )


class MailEntityManager(models.Manager):
    def get_or_create_esi(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        return self._get_or_create_esi(id=id, category=category, update_async=False)

    def get_or_create_esi_async(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        return self._get_or_create_esi(id=id, category=category, update_async=True)

    def _get_or_create_esi(
        self, id: int, category: str, update_async: bool
    ) -> Tuple[models.Model, bool]:
        id = int(id)
        try:
            return self.get(id=id), False
        except self.model.DoesNotExist:
            if update_async:
                return self.update_or_create_esi_async(id=id, category=category)
            else:
                return self.update_or_create_esi(id=id, category=category)

    def update_or_create_esi(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        """will try to update or create a new object from ESI

        Mailing lists can not be resolved from ESI
        and will therefore be created without name

        Trying to resolve a mailing list from ESI will result in an ESI error,
        which is masked by this method.

        Exceptions:
        - EsiOffline: ESI offline
        - EsiErrorLimitExceeded: ESI error limit exceeded
        - HTTP errors
        """
        id = int(id)
        try:
            obj = self.get(id=id)
            category = obj.category
        except self.model.DoesNotExist:
            pass

        if not category or category == self.model.Category.UNKNOWN:
            fetch_esi_status().raise_for_status()
            eve_entity, _ = EveEntity.objects.get_or_create_esi(id=id)
            if eve_entity:
                return self.update_or_create_from_eve_entity(eve_entity)
            else:
                return self.update_or_create(
                    id=id,
                    defaults={"category": self.model.Category.MAILING_LIST},
                )
        else:
            if category == self.model.Category.MAILING_LIST:
                return self.update_or_create(
                    id=id,
                    defaults={"category": self.model.Category.MAILING_LIST},
                )
            else:
                return self.update_or_create_from_eve_entity_id(id=id)

    def update_or_create_esi_async(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        """Same as update_or_create_esi, but will create and return an empty object and delegate the ID resolution to a task (if needed),
        which will automatically retry on many common error conditions
        """
        id = int(id)
        try:
            obj = self.get(id=id)
            if obj.category == self.model.Category.MAILING_LIST:
                return obj, False
            else:
                category = obj.category

        except self.model.DoesNotExist:
            pass

        if category and category in self.model.Category.eve_entity_compatible():
            return self.update_or_create_esi(id=id, category=category)
        else:
            return self._update_or_create_esi_async(id=id)

    def _update_or_create_esi_async(self, id: int) -> Tuple[models.Model, bool]:
        from .tasks import (
            update_mail_entity_esi as task_update_mail_entity_esi,
            DEFAULT_TASK_PRIORITY,
        )

        id = int(id)
        obj, created = self.get_or_create(
            id=id, defaults={"category": self.model.Category.UNKNOWN}
        )
        task_update_mail_entity_esi.apply_async(
            kwargs={"id": id}, priority=DEFAULT_TASK_PRIORITY
        )
        return obj, created

    def update_or_create_from_eve_entity(
        self, eve_entity: EveEntity
    ) -> Tuple[models.Model, bool]:
        category_map = {
            EveEntity.CATEGORY_ALLIANCE: self.model.Category.ALLIANCE,
            EveEntity.CATEGORY_CHARACTER: self.model.Category.CHARACTER,
            EveEntity.CATEGORY_CORPORATION: self.model.Category.CORPORATION,
        }
        return self.update_or_create(
            id=eve_entity.id,
            defaults={
                "category": category_map[eve_entity.category],
                "name": eve_entity.name,
            },
        )

    def update_or_create_from_eve_entity_id(self, id: int) -> Tuple[models.Model, bool]:
        eve_entity, _ = EveEntity.objects.get_or_create_esi(id=int(id))
        return self.update_or_create_from_eve_entity(eve_entity)

    def bulk_update_names(
        self, objs: Iterable[models.Model], keep_names: bool = False
    ) -> None:
        """Update names for given objects with categories
        that can be resolved by EveEntity (e.g. Character)

        Args:
        - obj: Existing objects to be updated
        - keep_names: When True objects that already have a name will not be updated

        """
        valid_categories = self.model.Category.eve_entity_compatible()
        valid_objs = {
            obj.id: obj
            for obj in objs
            if obj.category in valid_categories and (not keep_names or not obj.name)
        }
        if valid_objs:
            resolver = EveEntity.objects.bulk_resolve_names(valid_objs.keys())
            for obj in valid_objs.values():
                obj.name = resolver.to_name(obj.id)

            self.bulk_update(
                valid_objs.values(), ["name"], batch_size=BULK_METHODS_BATCH_SIZE
            )

    # def all_with_name_plus(self) -> models.QuerySet:
    #     """return all mailing lists annotated with name_plus_2 attribute"""
    #     return self.filter(category=self.model.Category.MAILING_LIST).annotate(
    #         name_plus_2=Case(
    #             When(name="", then=Concat(Value("Mailing List #"), "id")),
    #             default=F("name"),
    #             output_field=models.CharField(),
    #         )
    #     )


class CharacterManager(ObjectCacheMixin, models.Manager):
    def unregistered_characters_of_user_count(self, user: User) -> int:
        return CharacterOwnership.objects.filter(
            user=user, memberaudit_character__isnull=True
        ).count()

    def user_has_access(self, user: User) -> models.QuerySet:
        """Returns list of characters the given user has permission
        to access via character viewer
        """
        if user.has_perm("memberaudit.view_everything") and user.has_perm(
            "memberaudit.characters_access"
        ):
            qs = self.all()
        else:
            qs = self.select_related(
                "character_ownership__user",
            ).filter(character_ownership__user=user)
            if (
                user.has_perm("memberaudit.characters_access")
                and user.has_perm("memberaudit.view_same_alliance")
                and user.profile.main_character.alliance_id
            ):
                qs = qs | self.select_related(
                    "character_ownership__user__profile__main_character"
                ).filter(
                    character_ownership__user__profile__main_character__alliance_id=user.profile.main_character.alliance_id
                )
            elif user.has_perm("memberaudit.characters_access") and user.has_perm(
                "memberaudit.view_same_corporation"
            ):
                qs = qs | self.select_related(
                    "character_ownership__user__profile__main_character"
                ).filter(
                    character_ownership__user__profile__main_character__corporation_id=user.profile.main_character.corporation_id
                )

            if user.has_perm("memberaudit.view_shared_characters"):
                qs = qs | self.filter(is_shared=True)

        return qs


class CharacterAssetManager(models.Manager):
    def annotate_pricing(self) -> models.QuerySet:
        """Returns qs with annotated price and total columns"""
        return (
            self.select_related("eve_type__market_price")
            .annotate(
                price=Case(
                    When(
                        is_blueprint_copy=True,
                        then=Value(None),
                    ),
                    default=F("eve_type__market_price__average_price"),
                )
            )
            .annotate(
                total=Case(
                    When(
                        is_blueprint_copy=True,
                        then=Value(None),
                    ),
                    default=ExpressionWrapper(
                        F("eve_type__market_price__average_price") * F("quantity"),
                        output_field=models.FloatField(),
                    ),
                )
            )
        )


class CharacterContractItemManager(models.Manager):
    def annotate_pricing(self) -> models.QuerySet:
        """Returns qs with annotated price and total columns"""
        return (
            self.select_related("eve_type__market_price")
            .annotate(
                price=Case(
                    When(
                        raw_quantity=-2,
                        then=Value(None),
                    ),
                    default=F("eve_type__market_price__average_price"),
                )
            )
            .annotate(
                total=Case(
                    When(
                        raw_quantity=-2,
                        then=Value(None),
                    ),
                    default=ExpressionWrapper(
                        F("eve_type__market_price__average_price") * F("quantity"),
                        output_field=models.FloatField(),
                    ),
                )
            )
        )


class CharacterMailLabelManager(models.Manager):
    def get_all_labels(self) -> Dict[int, models.Model]:
        """Returns all label objects as dict by label_id"""
        label_pks = self.values_list("pk", flat=True)
        return {label.label_id: label for label in self.in_bulk(label_pks).values()}


class CharacterUpdateStatusManager(models.Manager):
    def statistics(self) -> dict:
        """returns detailed statistics about the last update run and the app"""
        from .models import (
            Character,
            CharacterAsset,
            CharacterMail,
            CharacterContract,
            CharacterContact,
            SkillSet,
            SkillSetGroup,
        )
        from . import app_settings
        from django.conf import settings as auth_settings

        def root_task_id_or_none(obj):
            try:
                return obj.root_task_id
            except AttributeError:
                return None

        all_characters_count = Character.objects.count()

        settings = {
            name: value
            for name, value in vars(app_settings).items()
            if name.startswith("MEMBERAUDIT_")
        }
        schedule = deepcopy(auth_settings.CELERYBEAT_SCHEDULE)
        for name, details in schedule.items():
            for k, v in details.items():
                if k == "schedule":
                    schedule[name][k] = str(v)

        settings["CELERYBEAT_SCHEDULE"] = schedule

        qs_base = self.filter(
            is_success=True,
            started_at__isnull=False,
            finished_at__isnull=False,
        ).exclude(root_task_id="", parent_task_id="")
        root_task_ids = {
            ring: root_task_id_or_none(
                qs_base.filter(section__in=Character.sections_in_ring(ring))
                .order_by("-finished_at")
                .first()
            )
            for ring in range(1, 4)
        }
        duration_expression = ExpressionWrapper(
            F("finished_at") - F("started_at"),
            output_field=models.fields.DurationField(),
        )
        qs_base = qs_base.filter(root_task_id__in=root_task_ids.values()).annotate(
            duration=duration_expression
        )
        update_stats = dict()
        if self.count() > 0:
            # per ring
            for ring in range(1, 4):
                sections = Character.sections_in_ring(ring)

                # calc totals
                qs = qs_base.filter(section__in=sections)
                try:
                    first = qs.order_by("started_at").first()
                    last = qs.order_by("finished_at").last()
                    started_at = first.started_at
                    finshed_at = last.finished_at
                    duration = round((finshed_at - started_at).total_seconds(), 1)
                except (KeyError, AttributeError):
                    first = None
                    last = None
                    duration = None
                    started_at = None
                    finshed_at = None

                available_time = (
                    settings[f"MEMBERAUDIT_UPDATE_STALE_RING_{ring}"]
                    - settings["MEMBERAUDIT_UPDATE_STALE_OFFSET"]
                ) * 60
                throughput = (
                    floor(all_characters_count / duration * 3600) if duration else None
                )
                within_boundaries = duration < available_time if duration else None
                update_stats[f"ring_{ring}"] = {
                    "total": {
                        "duration": duration,
                        "started_at": started_at,
                        "finshed_at": finshed_at,
                        "root_task_id": root_task_ids.get(ring),
                        "throughput_est": throughput,
                        "available_time": available_time,
                        "within_available_time": within_boundaries,
                    },
                    "max": {},
                    "sections": {},
                }

                # add longest running section w/ character
                obj = qs.order_by("-duration").first()
                update_stats[f"ring_{ring}"]["max"] = self._info_from_obj(obj)

                # add first and last section
                update_stats[f"ring_{ring}"]["first"] = self._info_from_obj(first)
                update_stats[f"ring_{ring}"]["last"] = self._info_from_obj(last)

                # calc section stats
                for section in sections:
                    try:
                        section_max = round(
                            qs_base.filter(section=section)
                            .aggregate(Max("duration"))["duration__max"]
                            .total_seconds(),
                            1,
                        )
                        section_avg = round(
                            qs_base.filter(section=section)
                            .aggregate(Avg("duration"))["duration__avg"]
                            .total_seconds(),
                            1,
                        )
                        section_min = round(
                            qs_base.filter(section=section)
                            .aggregate(Min("duration"))["duration__min"]
                            .total_seconds(),
                            1,
                        )
                    except (KeyError, AttributeError):
                        section_max = (None,)
                        section_avg = None
                        section_min = None

                    update_stats[f"ring_{ring}"]["sections"].update(
                        {
                            str(section): {
                                "max": section_max,
                                "avg": section_avg,
                                "min": section_min,
                            }
                        }
                    )

                ring_characters_count = (
                    Character.objects.filter(update_status_set__in=qs)
                    .annotate(num_sections=Count("update_status_set__section"))
                    .filter(num_sections=len(sections))
                    .count()
                )
                update_stats[f"ring_{ring}"]["total"][
                    "characters_count"
                ] = ring_characters_count
                update_stats[f"ring_{ring}"]["total"]["completed"] = (
                    ring_characters_count == all_characters_count
                )

        return {
            "app_totals": {
                "users_count": User.objects.filter(
                    character_ownerships__memberaudit_character__isnull=False
                )
                .distinct()
                .count(),
                "all_characters_count": all_characters_count,
                "skill_set_groups_count": SkillSetGroup.objects.count(),
                "skill_sets_count": SkillSet.objects.count(),
                "assets_count": CharacterAsset.objects.count(),
                "mails_count": CharacterMail.objects.count(),
                "contacts_count": CharacterContact.objects.count(),
                "contracts_count": CharacterContract.objects.count(),
            },
            "settings": settings,
            "update_statistics": update_stats,
        }

    @staticmethod
    def _info_from_obj(obj) -> dict:
        try:
            section_name = str(obj.section)
            character_name = str(obj.character)
            duration = round(obj.duration.total_seconds(), 1)
        except (KeyError, AttributeError):
            section_name = None
            character_name = None
            duration = None

        return {
            "section": section_name,
            "character": character_name,
            "duration": duration,
        }
