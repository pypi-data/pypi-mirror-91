import json
from uuid import uuid4

import numpy as np
from datetime import datetime
from typing import List, Dict


class AnnotationSession:
    @staticmethod
    def create(
        ids: List[str], users: List[str], target_number_of_annotation_per_user: int
    ):
        created_at = datetime.utcnow().strftime("%B %d %Y - %H:%M:%S")
        users = users
        number_of_ids = len(ids)
        number_of_users = len(users)
        target_number_of_annotation_per_user = target_number_of_annotation_per_user
        split_tasks = np.split(np.array(ids), number_of_users)

        # TODO if there is remaining target number of annotation
        # current_number_target_per_user = split_tasks[0].shape[0]
        # remaining_task_to_configure = self.target_number_of_annotation_per_user - current_number_target_per_user
        # Get it evenly and distributed
        tasks = {}
        for i, user in enumerate(users):
            tasks[user] = list(split_tasks[i])

        return AnnotationSession(
            str(uuid4()),
            created_at,
            number_of_ids,
            number_of_users,
            target_number_of_annotation_per_user,
            tasks,
        )

    def __init__(
        self,
        id: str,
        created_at: str,
        number_of_ids: int,
        number_of_users: int,
        target_number_of_annotation_per_user: int,
        tasks: Dict[str, List[str]],
    ):
        self.id = id
        self.created_at = created_at
        self.number_of_ids = number_of_ids
        self.number_of_users = number_of_users
        self.target_number_of_annotation_per_user = target_number_of_annotation_per_user
        self.tasks = tasks

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "number_of_ids": self.number_of_ids,
            "number_of_users": self.number_of_users,
            "target_number_of_annotation_per_user": self.target_number_of_annotation_per_user,
            "tasks": self.tasks,
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def save(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.to_dict(), outfile, indent=4)

    @staticmethod
    def from_filename(filename):
        with open(filename, "r") as infile:
            kdict = json.load(infile)
            return AnnotationSession(
                kdict.get("id"),
                kdict.get("created_at"),
                kdict.get("number_of_ids"),
                kdict.get("number_of_users"),
                kdict.get("target_number_of_annotation_per_user"),
                kdict.get("tasks"),
            )

    def get_tasks_by_user(self, username: str) -> List[str]:
        return self.tasks.get(username)
