# Copyright 2017 Chi-kwan Chan
# Copyright 2017 Harvard-Smithsonian Center for Astrophysics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from lict import Lict

class Metainer(Lict):
    """Metainer

    `Metainer` is a metadatabase based on `Lict`.

    """
    __slots__ = ('namekey', 'mountkey', 'hiddenkey')

    def __init__(self, *args, namekey='name', mountkey='mounts', hiddenkey='hidden', **kwargs):
        self.namekey   = namekey
        self.mountkey  = mountkey
        self.hiddenkey = hiddenkey
        super().__init__(*args, **kwargs)

    def set(self, name, value, **kwargs):
        self.append(Lict(value, **{self.namekey:name}, **kwargs))

    def mount(self, i, setback):
        getvalue = lambda s: s[i][0]
        getmeta  = lambda s: s[i][1:]

        # Special keys that metainer uses
        value = getvalue(self)
        meta  = {k:v for k, v in getmeta(self)}
        keys  = self.group(self.namekey).get(self.mountkey, [[self.namekey]])[-1][0]

        # Cache value to `__dict__` according to their metadata
        for k in keys:
            if k in meta:
                if not k == self.namekey or not meta.get(self.hiddenkey, False):
                    setback(meta[k], value)
