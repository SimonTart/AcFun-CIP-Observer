from .content import Base as ContentBase
from .comment import Base as CommentBase
target_metadata = [ContentBase.metadata, CommentBase.metadata]