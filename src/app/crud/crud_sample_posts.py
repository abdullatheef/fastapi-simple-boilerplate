from fastcrud import FastCRUD

from ..models.sample_post import SamplePost
# from ..schemas.post import PostCreateInternal, PostDelete, PostUpdate, PostUpdateInternal

# CRUDPost = FastCRUD[Post, PostCreateInternal, PostUpdate, PostUpdateInternal, PostDelete, None]
crud_sample_post = FastCRUD(SamplePost)
