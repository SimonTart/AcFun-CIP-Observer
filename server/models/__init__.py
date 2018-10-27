from .content import Base as ContentBase
from .comment import Base as CommentBase
from .spiderRecord import Base as SpiderBase
target_metadata = [ContentBase.metadata, CommentBase.metadata, SpiderBase.metadata]
