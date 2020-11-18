from typing import Optional,List

class EncryptionOptions:
    def __init__(
        self,
        *,
        share_with_users: Optional[List[str]] = None,
        share_with_groups: Optional[List[str]] = None,
        share_with_self: bool = True,
        ):
        self.share_with_users = []
        self.share_with_groups = []
        self.share_with_self = True

    def add_user_public_key(self,public_key):
        self.share_with_users.append(public_key)

