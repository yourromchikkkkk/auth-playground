from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, model_serializer, model_validator

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    """Generic response schema to unify API responses"""

    status: int
    message: str
    docs: Optional[List[T]] = None
    error: Optional[str] = None

    @model_validator(mode="after")
    def validate_mutually_exclusive_fields(self):
        """Ensure docs and error are mutually exclusive"""
        has_docs = self.docs is not None
        has_error = self.error is not None

        # TODO: add a way to handle the warnings
        # if has_docs and has_error:

        return self

    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        """Serialize model, excluding docs if error is present and vice versa"""
        data = {"status": self.status, "message": self.message}

        has_error = self.error is not None

        if has_error:
            data["error"] = self.error
        else:
            data["docs"] = self.docs

        return data

    class Config:
        from_attributes = True
