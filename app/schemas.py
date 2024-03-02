from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, TypeVar


T = TypeVar('T')

class PostBase(BaseModel):
    id = int
    title: str
    content: str
    published: bool = True

class AddLeasee(BaseModel):
    name: str
    f_name: str
    address: str
    district: str
    upazilla: str
    remarks: str
    nid_number: str
    dob: str
    phone_number: str
    alt_phone_number: str
    sex: str
    profile: str

class Note(BaseModel):
    application_id: str
    order_no: str
    order_date: str
    last_date: str
    description: str
    sent_from: str
    sent_to: str
    actions_taken: str

class Report(BaseModel):
    application_id: str
    order_no: str
    report_no: str
    report_date: str
    description: str
    actions_taken: str
    sent_from: str
    sent_to: str

class Dcr(BaseModel):
    application_id: str
    dcr_date: str
    signature_by: str

class Application(BaseModel):
    vpcase: str
    leasee: str
    nid_number: str
    application_date: str
    leasee_type: str
    applicant_type: str
    representative_name: str
    rep_phone_number: str
    user: str
    user_by: str
    application_status: str
    applied_for: str
    fee: int
    application_for: str

class LandUpdate(BaseModel):
    land_id: int
    vpcase: str
    mutation_number_past: str
    plot_number_past: str
    mutation_number_new: str
    plot_number_new:str
    land_area: float
    land_class: str
    shop_sqf: float
    renewed_upto: int

class PostCreate(PostBase):

    pass

class UserOut(BaseModel):

    username: str


class Post(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : Post                     # Post is a submodel
    votes : int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role : str

class SentTo(BaseModel):
    application_id: str
    sent_to: str

class UpdatePW(BaseModel):
    oldpassword: str
    newpassword: str


class UserLogin(BaseModel):
    username: EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None



''' # A "schema" is a definition or description of something.
    # pydentic for schema ((P4S)
    # in pyCharm install pydantic plugin
    # path + query parameters + Request body 
    # keyword arguments (key-value pairs)
    
    
    # QP- 
             item_id: str                               >> required
             item_id: UUID
             q: str | None = None                       >> optional                                         
             short: bool = False                        >> default value
             skip: int = 0
             price: float
             q: list = ["foo", "bar"]/[]                >> list                 
             q: list[str] = ["foo", "bar"]/[]           >> items validated      
             q: set[str] = set()                        >> set of strings, each of them is identical
             q: list[Image] | None = None               >> list of sub-model, and it can be continued (sub to sub)
             q: datetime | None = Body(default=None)
             q: datetime | None = Body(default=None)
             q: time | None = Body(default=None)
             q: timedelta | None = Body(default=None)
    
    # q: str | None = Query(default=None)               >> same as q: str | None = None
                      Query(min_length=3, 
                            max_length=50)              >> FastAPI.Query
                      Query(regex="^fixedquery$")       >> Regular Expression
                      Query(default=...)                >> required                 >> ... is Ellipsis
                      Query()                           >> required
                      Query(default=Required)           >> required                 >> from pydantic
                      Query(title="", 
                            description="")             >> these are as per wish for readability in front end
                      Query(alias="item-query")         >> item-query is not a valid Python variable name but item_Query
                      Query(deprecated=True)            >> you don't like this parameter anymore
                      Query(include_in_schema=False)    >> To exclude from OpenAPI schema
                      
                      Cookie(default=None)
                      Header(default=None)
                      Header(convert_underscores=False) >> to disable automatic conversion of underscores to hyphens
    q: list[str] =    Header()                          >> list of Headers
    
    
    # PP2QP  
    # @app.get("/items/{item_id}") >>  item_id: int
    # item_id: int = Path(title="The ID of the item to get")        >> Path from FastAPI
                     Path(ge=1, le=1000)                            >> greater than or equal to
                     
    # size: float =  Query(gt=0, lt=10.5)    
    # item_id: int, item: Item, user: User                          >> Mix Schemas
                                                                    >> more than one body parameters                    
    # item_id: int, item: Item, user: User, importance: int = Body()  >> PP2QP, model1, model2, 
                                                                    >> importance is single entry incorporated into body
    # item_id: int, item: Item = Body(embed=True)                     >> although single model, incorporated into body
    # price: float = Field(gt=0, description="g zero")                >> Field from pydantic no need FastAPI
        
    # pydantic 
            email: EmailStr
            url: HttpUrl
            dir: conint(le=1)
    
    
    # JSON array (a Python list) is a python list.
    # JSON only supports str as keys. But Pydantic has automatic data conversion.
    # JSON to dict
                    >> q: dict[int, float]
    # pip install email-validator or pip install pydantic[email].
    # def create_user(user: UserIn) -> BaseUser:       >> -> is the return type
    # async def read_items() -> Any:                    >> -> Any will pass all data to response model
    # from fastapi.responses import JSONResponse, RedirectResponse          >> JSONResponse, RedirectResponse
        
        async def get_portal(teleport: bool = False) -> Response:           >> Response Model
    # @app.get("/portal", response_model=None)                              >> Don't want FastAPI validation rather mypy/ect.
    # response_model=Union[PlaneItem, CarItem]                              >> 1st go First
    # response_model=list[Item]                                             >> list of Item will be sent
    # response_model=dict[str, float]                                       >> list without PM
    
    # response_model_exclude_unset=True                                     >> to return only the values explicitly set
    # response_model_exclude_defaults=True
    # response_model_exclude_none=True
    # response_model_include={"name", "description"}                        >> to include an Item in response Model
    # response_model_exclude={"tax"}                                        >> to exclude an Item from response model
    # JSON(dict) >>(FastAPI) >> **dict(kv-arg) >> (PM)   >> PM_Data         >> **dict is kv-arg
                                                                            >> only kv-arg can pass through PM(Pydantic Model)
    # PM_Data.dict() = JSON(dict)
    # UserInDB(**user_in.dict())                                            >> 1PM2AnotherPM
    # UserInDB(**user_in.dict(), hashed_password = hashed_password)         >> add extra kv-arg
                        
    
    >>>> Dependency >>>>>
    # def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100): 
            
            return {"q": q, "skip": skip, "limit": limit}                                       >>> whole model as like function , these are for common parameter (CP)
            
    
    # def read_items(commons: dict = Depends(common_parameters)):
                
            return commons                                                                      >>> Depending on other for schema (PM)
    # info >> go to depends to be rectified >> come into my function                            >> Dependency Injection (DI)
    # Other common terms for this same idea of "DI" are: resources, providers, services, injectables, components
    # commons: CommonQueryParams = Depends()
'''

