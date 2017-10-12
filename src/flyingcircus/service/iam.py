from .._raw.iam import *

__all__ = [
    "Policy",
    "PolicyDocument",
    "PolicyStatement",
    "PrincipalSet",
    "Role",
]


class PrincipalSet(BaseAWSObject):
    """Represents a set of principals for use in an IAM policy Statement (either as a Principal or NotPrincipal element).

    See http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Principal
    """

    def __init__(self, aws=None, services=None, federated=None, canonicalusers=None, everyone=False):
        BaseAWSObject.__init__(self)

        # We can have several of some types of principal
        self.AWS.extend(self._list_or_item(aws))
        self.CanonicalUser.extend(self._list_or_item(canonicalusers))
        self.Service.extend(self._list_or_item(services))

        # We can only have one federation source (I think)
        if federated:
            assert isinstance(federated, str)
            self._data["Federated"] = federated

        # Or you could just allow everyone!
        self._allow_everyone = everyone

        assert self._data  # TODO cleanup

    @property
    def AWS(self):
        return self._data.setdefault('AWS', [])

    @property
    def CanonicalUser(self):
        return self._data.setdefault('CanonicalUser', [])

    @property
    def Service(self):
        return self._data.setdefault('Service', [])

    def as_yaml_node(self, dumper):
        if self._allow_everyone:
            assert not self._has_specific_principals()
            return dumper.represent_str("*")
        else:
            assert self._has_specific_principals()
        return super(PrincipalSet, self).as_yaml_node(dumper)

    def _has_specific_principals(self):
        return self.AWS or self.CanonicalUser or self.Service or self._data["Federated"]

    def _list_or_item(item=None):
        if item is None:
            return []
        if isinstance(item, (set, list)):
            return item
        return [item]
