from fastcrud import FastCRUD

from ..models.sample_user import SampleUser
from ..schemas.sample_user import SampleUserDelete, SampleUserUpdate

# CRUDUser = FastCRUD[SampleUser, SampleUserUpdate, SampleUserDelete, None]
crud_sample_user = FastCRUD(SampleUser)
