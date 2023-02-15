from __future__ import annotations

from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Extra, EmailStr, Field, conint, constr

from app.models.rwmodel import RWModel
from app.models.dbmodel import DateTimeModelMixin, DBModelMixin, PyObjectId


class Meta(BaseModel):
    class Config:
        extra = Extra.allow
        allow_population_by_field_name = True

    name: str = Field(
        ...,
        description='Name of the data controller.',
        examples=['Green Company'],
        title='Name',
    )
    version: conint(ge=1) = Field(
        ...,
        description='This number serves to version documents of a controller specific process.',
        examples=[1],
        title='Version',
    )
    hash: constr(min_length=64, max_length=64) = Field(
        ...,
        alias='_hash',
        description='The hash is based on one SHA256 calculation of the document.',
        examples=['be81d309088dde861ab5fc4d62d4bbfe0aeef3e3baf2f5362c1086f451f0a1e7'],
        title='_hash',
    )


class Manual(BaseModel):
    available: bool
    address: Optional[str] = Field(
        None,
        description='Address for the postal DSAR, typically the address of a Data Protection Officer.',
        examples=['Straße des 17. Juni, 10587 Berlin'],
        title='Address',
    )
    email: Optional[EmailStr] = Field(
        None,
        description='Email address for an electronic submission of a manual access request',
        examples=['rta@mycompany.com'],
        title='Email',
    )
    phone: Optional[
        constr(
            strip_whitespace=True,
            regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$",
        )
    ] = Field(None, examples=['+49 151 1234 5678'])
    authentication: Optional[str] = Field(
        None,
        description='Type of identification evidence that should be stated in the email to achieve faster processing of request',
        examples=['ID', 'Account name', 'Full name and birthdate', 'None'],
    )


class WorkflowContainer(BaseModel):
    automationEngine: str = Field(
        ...,
        description='Automation engine that is used to describe the specific workflow',
    )
    workflow: List[Dict[str, Any]] = Field(
        ...,
        description='Automation engine specific workflow to execute the access request with a specific set of request parameters',
    )
    version: Optional[int] = None
    verified: Optional[bool] = True


class Webinterface(BaseModel):
    available: bool
    startUrl: Optional[str] = Field(
        None,
        description='URL to startelement of request process',
        examples=['https://takeout.google.com/'],
        title='Url',
    )
    authentication: Optional[constr(regex=r'^(password|cookie|email|2FA|ID)$')] = Field(
        None,
        description='Kind of authentication actions required during or before the request process is started',
        examples=['password', 'cookie', 'email', '2FA', 'ID'],
    )
    workflowContainer: Optional[WorkflowContainer] = Field(
        None,
        description='The workflow for the data request process encoded in an automation engine specific format',
    )


class Authentication(BaseModel):
    authDescription: constr(regex=r'^(password|token|2FA)$') = Field(
        ...,
        description='Kind of authentication actions required during or before the request process is started',
        examples=['password', '2FA', 'token'],
    )
    authProcessStage: constr(regex=r'^(preprocessing|requestParameter)$') = Field(
        ...,
        description='Process stage, where the authentication is required',
        examples=['preprocessing', 'requestParameter'],
    )


class ApiParameter(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None


class Api(BaseModel):
    available: bool
    endpoint: Optional[str] = None
    authentication: Optional[Authentication] = None
    apiParameters: Optional[List[ApiParameter]] = None


class RequestInterfaceItem(BaseModel):
    manual: Optional[Manual] = Field(
        description='Describes the manual request process'
    )
    webinterface: Optional[Webinterface] = Field(
        description='Describes the semi-automatic request process using a webinterface',
    )
    api: Optional[Api] = Field(
        description='Describes the fully automated request process using an API'
    )


class CustomRange(BaseModel):
    available: bool = Field(
        ..., description='Describes if a custom time range is available'
    )
    range: Optional[List[Any]] = Field(
        None, description='There might be multiple available time ranges.'
    )


class TimeRange(BaseModel):
    allTime: bool
    customRange: Optional[CustomRange] = Field(
        None,
        description='Describes options for a specific time range that shall be included in the DSAR',
    )


class RequestParameter(BaseModel):
    timeRange: TimeRange = Field(
        ..., description='The time range that shall be included in the DSAR'
    )
    mediaQuality: Optional[List[constr(regex=r'^(small|medium|high)$')]] = None
    dataFormat: List[constr(regex=r'^(JSON|CSV|PDF|HTML|Text)$')]
    categories: Optional[List[str]] = None


class ItemBase(RWModel):
    class Config:
        extra = Extra.allow

    meta: Meta = Field(
        ...,
        description='Meta information for the identification and verification of the document.',
        examples=[
            {
                'name': 'Google',
                'version': 1,
                'status': 'active',
                '_hash': 'd732a793562a3e5dc57645a8',
            }
        ],
        title='Meta',
    )
    requestInterface: List[RequestInterfaceItem]
    requestParameter: Optional[RequestParameter] = Field(
        None,
        description='The parameters describe options to refine the general access request',
    )


class Item(DateTimeModelMixin, ItemBase):
    # Add optional created and updated timestamps
    pass


class ItemInDB(DBModelMixin, Item):
    # Add optional id information
    id: PyObjectId = Field(
        default_factory=PyObjectId,
        description='The id of a controller instance. The id is necessary to distinguish several processing tasks of the same data item (locally unique ID that can be based on the database implementation).',
        examples=['f1424f86-ca0f-4f0c-9438-43cc00509931'],
        title='_id',
        alias='_id'
    )