import logging
from typing import List

from .models import Project

log = logging.getLogger(__name__)


def has_projects(*, user: str) -> bool:
    """Return true if the user has any projects in the database."""
    log.debug("Checking if %s has any projects", user)

    return Project.objects.filter(user=user).count() > 0


def projects_for_user(*, user: str, archived: bool = False) -> List[Project]:
    """Return a list of all projects for a given user.

    :param archived: If true, return a list of archived projects.
    """
    log.debug(
        "Fetching %s projects for user %s", "archived" if archived else "active", user
    )

    query_set = Project.objects.filter(user=user, archived=archived)
    return query_set.order_by("created").all()


def get_project(*, user: str, slug: str) -> Project:
    """Get a project for a user by slug."""
    log.debug("Retrieving project %s for user %s", slug, user)
    return Project.objects.get(user=user, slug=slug)
