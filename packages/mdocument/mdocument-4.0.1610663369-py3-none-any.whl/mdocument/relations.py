import typing
from abc import abstractmethod

from mdocument.document import Model, ModelField


class Relation:
    def __init__(self, parent_field: ModelField, child_field: ModelField):
        self.parent_field = parent_field
        self.child_field = child_field

    @classmethod
    def register(cls, parent_field: ModelField, child_field: ModelField):
        """Saves relation to Model relations map."""

        Model.__relations__.setdefault(parent_field.model, []).append(
            cls(parent_field, child_field)
        )
        Model.__relations__.setdefault(child_field.model, []).append(
            cls(parent_field, child_field)
        )

    @abstractmethod
    async def delete(self, client, document):
        """Deletes related documents."""

    @abstractmethod
    async def update(self, client, document):
        """Updates related documents."""

    @abstractmethod
    async def create_index(self):
        """Creates index for relation."""  # TODO

    @property
    def parent_document_cls(self):
        return self.parent_field.model.__document_cls__

    @property
    def child_document_cls(self):
        return self.child_field.model.__document_cls__

    def get_collections(
        self, client
    ) -> typing.Tuple["AsyncIOMotorCollection", "AsyncIOMotorCollection"]:
        """Gets parent and child connection."""

        parent_collection = client[self.parent_document_cls.__database__][
            self.parent_document_cls.__collection__
        ]
        child_collection = client[self.child_document_cls.__database__][
            self.child_document_cls.__collection__
        ]
        return parent_collection, child_collection


class RelationManyToOne(Relation):
    """Multiple parents one child.
    This means that child field type is a tuple.
    Updates child field when parent updates.
    Deletion happens when all parents are deleted.
    """

    async def delete(self, client: "AsyncIOMotorClient", document: "MDocument"):
        """Deletes child with only one parent. And removes parent from children. """

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                "$and": [
                    {
                        self.child_field.name: document.__original_document__[
                            self.parent_field.name
                        ]
                    },
                    {f"{self.child_field.name}.1": {"$exists": True}},
                ]
            }
            update_query = {
                "$pull": {self.child_field.name: document[self.parent_field.name]}
            }
            await child_collection.update_one(search_query, update_query)
            search_query = {
                "$and": [
                    {
                        self.child_field.name: document.__original_document__[
                            self.parent_field.name
                        ]
                    },
                    {f"{self.child_field.name}.1": {"$exists": False}},
                ]
            }
            await child_collection.delete_one(search_query)

    async def update(self, client, document):
        """Updates child fields from parent."""

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                self.child_field.name: document.__original_document__[
                    self.parent_field.name
                ]
            }
            update_query = {
                "$set": {f"{self.child_field.name}.$": document[self.parent_field.name]}
            }
            # TODO: Check that field is updated.
            await child_collection.update_many(search_query, update_query)


class RelationOneToOne(Relation):
    """One parent one child.
    Updates field when parent/child changes.
    Creates unique index for field.
    """

    async def delete(self, client, document):
        """Deletes child if parent is deleted."""

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                self.child_field.name: document.__original_document__[
                    self.parent_field.name
                ]
            }
            await child_collection.delete_one(search_query)

    async def update(self, client, document):
        """Updates children field value."""

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                self.child_field.name: document.__original_document__[
                    self.parent_field.name
                ]
            }
            update_query = {
                "$set": {self.child_field.name: document[self.parent_field.name]}
            }
            await child_collection.update_one(search_query, update_query)


class RelationOneToMany(Relation):
    """One parent multiple children.
    Updates field when parent/child changes.
    Deletes children when parent deleted.
    """

    async def delete(self, client, document):
        """Deletes all children if parent is deleted."""

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                self.child_field.name: document.__original_document__[
                    self.parent_field.name
                ]
            }
            await child_collection.delete_many(search_query)

    async def update(self, client, document):
        """Updates all children field value if parent is updated."""

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                self.child_field.name: document.__original_document__[
                    self.parent_field.name
                ]
            }
            update_query = {
                "$set": {self.child_field.name: document[self.parent_field.name]}
            }
            await child_collection.update_many(search_query, update_query)


class RelationManyToMany(Relation):
    """Multiple parents multiple children.
    Updates list when parent/child updates.
    Deletes all children when its all parents deleted.
    """

    async def delete(self, client: "AsyncIOMotorClient", document: "MDocument"):
        """Deletes children with only one parent. And removes parent from children. """

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                "$and": [
                    {
                        self.child_field.name: document.__original_document__[
                            self.parent_field.name
                        ]
                    },
                    {f"{self.child_field.name}.1": {"$exists": True}},
                ]
            }
            update_query = {
                "$pull": {self.child_field.name: document[self.parent_field.name]}
            }
            await child_collection.update_many(search_query, update_query)
            search_query = {
                "$and": [
                    {
                        self.child_field.name: document.__original_document__[
                            self.parent_field.name
                        ]
                    },
                    {f"{self.child_field.name}.1": {"$exists": False}},
                ]
            }
            await child_collection.delete_many(search_query)

    async def update(self, client, document):
        """Updates all childes fields from parent."""

        _, child_collection = self.get_collections(client)

        if isinstance(document, self.parent_document_cls):
            search_query = {
                self.child_field.name: document.__original_document__[
                    self.parent_field.name
                ]
            }
            update_query = {
                "$set": {f"{self.child_field.name}.$": document[self.parent_field.name]}
            }
            # TODO: Check that field is updated.
            await child_collection.update_many(search_query, update_query)
