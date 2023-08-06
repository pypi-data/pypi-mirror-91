import copy
import logging
import types
import typing

from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

LOG = logging.getLogger("mdocument")


class DocumentException(Exception):
    def __init__(self, message):
        self.message = message


class DocumentDoesntExist(DocumentException):
    def __init__(self):
        super().__init__("Document not found")


class DuplicateError(BaseException):
    pass


class NotFoundError(BaseException):
    pass


class UnknownModelField(BaseException):
    pass


class RequiredFieldMissing(BaseException):
    pass


class WrongValueType(BaseException):
    pass


class RelationNotSet(BaseException):
    pass


class ModelField:
    def __init__(
        self, type, default=None, optional=False, sensitive=False, relation=None
    ):
        self.type = type
        self.default = default
        self.optional = optional
        self.sensitive = sensitive
        self.relation = relation
        self.model = None
        self.name = None

        if isinstance(type, ModelField):
            if not relation:
                raise RelationNotSet()

    @property
    def is_related(self):
        return isinstance(self.type, ModelField)

    def to_dict(self):
        return {
            "type": self.type,
            "default": self.default,
            "optional": self.optional,
            "sensitive": self.sensitive,
            "relation": self.relation,
        }

    def __repr__(self):
        return f"ModelField({self.to_dict()}) "


class Index:
    def __init__(self, keys: typing.List[typing.Tuple[str, int]], **kwargs):
        self.keys = keys
        self.kwargs = kwargs


class Model:
    _id = ModelField(type=ObjectId)
    _primary_key_ = "_id"
    __relations__ = {}
    __indexes__ = []
    __document_cls__ = None

    Index = Index
    Field = ModelField

    def __init_subclass__(cls, **kwargs):
        for protected_field, value in cls._get_protected_from_parents().items():
            setattr(cls, protected_field, copy.deepcopy(value))
        for field_name, field in cls.__dict__.items():
            if not isinstance(field, (types.MethodType, classmethod)):
                if not field_name.startswith("_"):
                    if not isinstance(field, ModelField):
                        raise Exception(
                            f"Model field {field_name} should be ModelField type."
                        )
                if isinstance(field, ModelField):
                    field.model = cls
                    field.name = field_name
                    if field.is_related:
                        field.relation.register(field.type, field)

    @classmethod
    def _get_protected_from_parents(cls):
        protected_fields = {}
        for parent in cls.__bases__:
            if issubclass(parent, Model):
                protected_fields.update(parent._get_protected_from_parents())
                for field, field_type in parent.__dict__.items():
                    if field.startswith("_") and isinstance(field_type, ModelField):
                        protected_fields[field] = field_type
        return protected_fields

    @classmethod
    def fields(cls) -> typing.Dict[str, "ModelField"]:
        fields = {}
        for field, field_type in cls.__dict__.items():
            if isinstance(field_type, ModelField):
                fields[field] = field_type
        return fields

    @classmethod
    def fields_dict(cls):
        result = {}
        for field, model_field in cls.fields().items():
            result[field] = model_field.to_dict()
        return result

    @classmethod
    def validate(cls, document: "MDocument"):
        """Placeholder for custom model validation. Can be implemented in subclass."""

    @classmethod
    def _validate(cls, document: "MDocument"):
        """Validates that fields are present and have correct types."""

        if set(document.__document__).difference(cls.fields()):
            raise UnknownModelField(set(cls.fields()).difference(document.__document__))
        for field_name, field in cls.fields().items():
            if document.__document__.get(field_name) is None and not field.optional:
                raise RequiredFieldMissing(field_name)
            elif document.__document__.get(field_name) is None and field.optional:
                continue
            elif document.__document__.get(field_name):
                if isinstance(field.type, ModelField):
                    if not isinstance(
                        document.__document__.get(field_name), field.type.type
                    ):
                        raise WrongValueType(field_name)
                elif not isinstance(document.__document__.get(field_name), field.type):
                    raise WrongValueType(field_name)
        cls.validate(document)

    def __repr__(self):
        return f"{self.__document_cls__.__name__}Model({self.fields_dict()})"


class MetaDocument(type):
    __client__: AsyncIOMotorClient
    __collection__: str
    __database__: str

    Model = Model

    @property
    def collection(cls) -> AsyncIOMotorCollection:
        return cls.database[cls.__collection__]

    @property
    def client(cls) -> AsyncIOMotorClient:
        return cls.__client__

    @property
    def database(cls) -> AsyncIOMotorDatabase:
        return cls.client[cls.__database__]


class MDocument(metaclass=MetaDocument):
    __document__: dict
    __original_document__: dict

    NotFoundError = NotFoundError
    DuplicateError = DuplicateError

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.__class__.collection

    @property
    def client(self) -> AsyncIOMotorClient:
        return self.__class__.client

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self.__class__.database

    def __init__(self, doc):
        self.__document__ = doc
        self.__original_document__ = copy.deepcopy(doc)
        for key, value in doc.items():
            setattr(self, key, value)

    def __getitem__(self, item):
        return self.__document__[item]

    def __setitem__(self, key, value):
        self.__document__[key] = value

    def __getattr__(self, item):
        try:
            return self.__document__[item]
        except KeyError:
            raise AttributeError(item) from None

    def __setattr__(self, key, value):
        if key.startswith("_"):
            return super().__setattr__(key, value)
        if key in self.__class__.Model.fields():
            if not isinstance(value, getattr(self.__class__.Model, key).type):
                raise WrongValueType(key)
        else:
            raise UnknownModelField(key)

    @classmethod
    def __annotations__(cls):
        return cls.Model.__annotations__

    def __eq__(self, other):
        if isinstance(other, MDocument):
            return self.__document__ == other.__document__
        elif isinstance(other, dict):
            return self.__document__ == other
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__document__})"

    def __init_subclass__(cls, **kwargs):
        cls.Model.__document_cls__ = cls
        if getattr(cls, "__client__", None):
            if cls.collection and cls.database:
                for index in cls.Model.__indexes__:
                    cls.client.delegate[cls.__database__][
                        cls.__collection__
                    ].create_index(index.keys, **index.kwargs)

    @classmethod
    async def create(cls, doc: dict, **kwargs):
        """Creates new document."""

        result = cls.collection.insert_one(doc, **kwargs)
        return cls(result)

    @classmethod
    async def find_one(cls, query: dict, required: bool = True):
        """Finds one document."""

        result = await cls.collection.find_one(query)
        if result is None and required:
            raise cls.NotFoundError()
        return cls(result)

    @classmethod
    async def find_many(cls, query: dict, required: bool = True):
        """Finds multiple documents."""

        documents = []
        async for doc in cls.collection.find(query):
            documents.append(cls(doc))
        if not documents and required:
            raise
        return documents

    async def _update_related(self, client=None):
        """Updates related documents."""

        for relation in Model.__relations__.get(self.Model, []):
            await relation.update(client or self.__class__.__client__, self)

    async def _delete_related(self, client=None):
        """Deletes related documents."""

        for relation in Model.__relations__.get(self.Model, []):
            await relation.delete(client or self.__class__.__client__, self)

    async def save(self):
        """Saves current document to database."""

        self.collection.update_one(
            {
                self.Model._primary_key_: self.__original_document__[
                    self.Model._primary_key_
                ]
            }
        )
