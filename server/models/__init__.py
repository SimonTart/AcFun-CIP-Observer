from .content import Base as ContentBase
from .comment import Base as CommentBase
from .sectionLatestContent import Base as SectionLatestContent
target_metadata = [ContentBase.metadata, CommentBase.metadata, SectionLatestContent.metadata]
