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

from  abc  import ABCMeta
from .core import Metainer

class MetainerMixin(metaclass=ABCMeta):
    """MetainerMixin

    `MetainerMixin` provides a metainer-based mixin for building
    interpolatable python classes.

    """
    __slots__ = ('_metainer')

    @property
    def metainer(self):
        try:
            m = super().__getattribute__('_metainer')
        except AttributeError:
            m = Metainer() # initialization is done lazily in this property
            super().__setattr__('_metainer', m)
        return m

    #--------------------------------------------------------------------------
    # The actual attribute getter and setter
    #
    # After putting `value` to the metainer, we perform a `setattr()`
    # so that `value` is accessible efficiently.  However, we should
    # always use super().__[set/get]attr__() here to avoid infinite
    # recursion.

    def set(self, name, value, **kwargs):
        self.metainer.set(name, value, **kwargs)
        self.metainer.mount(-1, super().__setattr__)

    def get(self, name, *args):
        try:
            return super().__getattribute__(name)
        except AttributeError as e:
            if args:
                return args[0] if len(args) == 1 else args
            else:
                raise e

    #--------------------------------------------------------------------------
    # Pass the getter and setter to a more pythonic interface

    def __setattr__(self, name, value):
        self.set(name, value)

    def __getattr__(self, name):
        return self.get(name)
