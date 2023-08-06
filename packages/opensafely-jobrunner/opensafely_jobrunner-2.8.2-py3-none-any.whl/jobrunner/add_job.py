"""
Development utility for creating and submitting a JobRequest without having a
job-server
"""
import argparse
import dataclasses
import pprint
from pathlib import Path
from urllib.parse import urlparse
import textwrap

from .log_utils import configure_logging
from .sync import job_request_from_remote_format
from .database import find_where
from .models import Job
from .create_or_update_jobs import create_or_update_jobs


def main(
    repo_url, actions, commit, branch, workspace, database, force_run_dependencies
):
    # Make paths to local repos absolute
    parsed = urlparse(repo_url)
    if not parsed.scheme and not parsed.netloc:
        path = Path(parsed.path).resolve()
        # In case we're on Windows
        repo_url = str(path).replace("\\", "/")
    job_request = job_request_from_remote_format(
        dict(
            identifier=Job.new_id(),
            sha=commit,
            workspace=dict(name=workspace, repo=repo_url, branch=branch, db=database),
            requested_actions=actions,
            force_run_dependencies=force_run_dependencies,
        )
    )
    print("Submitting JobRequest:\n")
    display_obj(job_request)
    create_or_update_jobs(job_request)
    jobs = find_where(Job, job_request_id=job_request.id)
    print(f"Created {len(jobs)} new jobs:\n")
    for job in jobs:
        display_obj(job)


def display_obj(obj):
    if hasattr(obj, "asdict"):
        data = obj.asdict()
    else:
        data = dataclasses.asdict(obj)
    output = pprint.pformat(data)
    print(textwrap.indent(output, "  "))
    print()


if __name__ == "__main__":
    configure_logging()
    parser = argparse.ArgumentParser(description=__doc__.partition("\n\n")[0])
    parser.add_argument("repo_url", help="URL (or local path) of git repository")
    parser.add_argument("actions", nargs="+", help="Name of project action to run")
    parser.add_argument(
        "--commit",
        help=(
            "Git commit to use (if repo_url is a local checkout, use current "
            "checked out commit by default)"
        ),
    )
    parser.add_argument(
        "--branch",
        help="Git branch or ref to use if no commit supplied (default HEAD)",
        default="HEAD",
    )
    parser.add_argument(
        "--workspace", help="Workspace ID (default 'test')", default="test"
    )
    parser.add_argument(
        "--database", help="Database name (default 'dummy')", default="dummy"
    )
    parser.add_argument("-f", "--force-run-dependencies", action="store_true")

    args = parser.parse_args()
    main(**vars(args))
