"""Module to resolve the queries.

API
---

.. autofunction:: resolver_query_properties
.. autofunction:: resolver_query_job
.. autofunction:: resolver_query_jobs

"""
from typing import Any, Dict, List, Optional

from tartiflette import Resolver

from insilicodatabase import fetch_properties_from_collection

from .data import JOBS


@Resolver("Query.properties")
async def resolver_query_properties(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning Properties based on their `collection_name`.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    The list of all jobs with the given status.
    """
    data = fetch_properties_from_collection(ctx["mongodb"], args["collection_name"])
    data = list(data)
    for entry in data:
        entry["id"] = entry.pop("_id")
        entry["collection_name"] = args["collection_name"]
    return data


@Resolver("Query.jobs")
async def resolver_query_jobs(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning jobs based on their status.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    The list of all jobs with the given status.
    """
    return [x for x in JOBS if x["status"] == args["status"]]


@Resolver("Query.job")
async def resolver_query_job(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning a single job based on its status.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    A single job with the given status
    """
    return next(x for x in JOBS if x["status"] == args["status"])
