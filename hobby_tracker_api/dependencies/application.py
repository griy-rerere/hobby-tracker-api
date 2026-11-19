from hobby_tracker.application import CommandBus, QueryBus, commands, queries
from hobby_tracker_infrastructure.persistence.sqlalchemy import (
    SqlalchemyActivityRepository,
    SqlalchemyHobbyRepository,
    SqlalchemyUOW,
)
from hobby_tracker_infrastructure.persistence.sqlalchemy import (
    queries as sqla_queries,
)

from .auth_dependencies import CurrentUserID
from .sqla import SQLASession


def get_command_bus(
    sqla_session: SQLASession,
    user_id: CurrentUserID,
) -> CommandBus:
    hobby_repo = SqlalchemyHobbyRepository(session=sqla_session, user_id=user_id)
    activity_repo = SqlalchemyActivityRepository(session=sqla_session, user_id=user_id)
    uow = SqlalchemyUOW(sqla_session, hobby_repo, activity_repo)

    bus = CommandBus()
    bus.register(
        commands.AddActivityCommand,
        commands.AddActivityHandler(
            uow=uow, hobby_repo=hobby_repo, activity_repo=activity_repo
        ),
    )
    bus.register(
        commands.AddHobbyCommand,
        commands.AddHobbyHandler(uow=uow, hobby_repo=hobby_repo),
    )
    bus.register(
        commands.ChangeActivityDurationCommand,
        commands.ChangeActivityDurationHandler(uow=uow, activity_repo=activity_repo),
    )
    bus.register(
        commands.ChangeActivityStartCommand,
        commands.ChangeActivityStartHandler(uow=uow, activity_repo=activity_repo),
    )
    bus.register(
        commands.DeleteActivityCommand,
        commands.DeleteActivityHandler(uow=uow, activity_repo=activity_repo),
    )
    bus.register(
        commands.DeleteHobbyCommand,
        commands.DeleteHobbyHandler(uow=uow, hobby_repo=hobby_repo),
    )
    bus.register(
        commands.RenameHobbyCommand,
        commands.RenameHobbyHandler(uow=uow, hobby_repo=hobby_repo),
    )
    bus.register(
        commands.SetActivityNoteCommand,
        commands.SetActivityNoteHandler(uow=uow, activity_repo=activity_repo),
    )

    return bus


def get_query_bus(sqla_session: SQLASession, user_id: CurrentUserID) -> QueryBus:
    bus = QueryBus()

    bus.register(
        queries.HobbiesStatsQuery,
        sqla_queries.SqlalchemyHobbiesStatsHandler(
            session=sqla_session, user_id=user_id
        ),
    )
    bus.register(
        queries.HobbyStatsQuery,
        sqla_queries.SqlalchemyHobbyStatsHandler(session=sqla_session, user_id=user_id),
    )

    return bus
