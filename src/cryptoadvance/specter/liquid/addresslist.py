from ..addresslist import *
from embit.liquid.addresses import addr_decode, address


class LAddressList(AddressList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # scriptpubkey dict for lookups of unconf addresses
        self._scripts = {}
        self._update_scripts()

    def _update_scripts(self):
        for addr in self:
            sc, _ = addr_decode(addr)
            if sc and sc not in self._scripts:
                self._scripts[sc] = self[addr]

    def add(self, *args, **kwargs):
        res = super().add(*args, **kwargs)
        # update scriptpubkey dict for lookups of unconf addresses
        self._update_scripts()
        return res

    def __contains__(self, addr):
        """finds address by confidential or unconfidential address by converting to scriptpubkey"""
        sc, _ = addr_decode(addr)
        if sc and self._scripts.__contains__(sc):
            return True
        return super().__contains__(addr)

    def __getitem__(self, addr):
        """finds address by confidential or unconfidential address by converting to scriptpubkey"""
        sc, _ = addr_decode(addr)
        if sc in self._scripts:
            return self._scripts[sc]
        return super().__getitem__(addr)
