# Copyright 2019 Kemal Kurniawan
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

from collections import defaultdict
from random import Random
from typing import Any, Callable, Iterable, Iterator, Optional, Sequence, Sized
import statistics as stat

from . import Batch, Sample


class BatchIterator(Iterable[Batch], Sized):
    """Iterator that produces batches of samples.

    Example:

        >>> from text2array import BatchIterator
        >>> samples = [
        ...   {'ws': ['a']},
        ...   {'ws': ['a', 'b']},
        ...   {'ws': ['b', 'b']},
        ... ]
        >>> iter_ = BatchIterator(samples, batch_size=2)
        >>> for b in iter_:
        ...   print(list(b))
        ...
        [{'ws': ['a']}, {'ws': ['a', 'b']}]
        [{'ws': ['b', 'b']}]

    Args:
        samples (~typing.Iterable[Sample]): Iterable of samples to batch.
        batch_size: Maximum number of samples in each batch.

    Note:
        When ``samples`` is an instance of `~typing.Sized`, this iterator can
        be passed to `len` to get the number of batches. Otherwise, a `TypeError`
        is raised.
    """

    def __init__(self, samples: Iterable[Sample], batch_size: int = 1) -> None:
        if batch_size <= 0:
            raise ValueError("batch size must be greater than 0")

        self._samples = samples
        self._bsz = batch_size

    @property
    def batch_size(self) -> int:
        return self._bsz

    def __len__(self) -> int:
        n = len(self._samples)  # type: ignore
        b = self._bsz
        return n // b + (1 if n % b != 0 else 0)

    def __iter__(self) -> Iterator[Batch]:
        it, exhausted = iter(self._samples), False
        while not exhausted:
            batch = Batch()
            while not exhausted and len(batch) < self._bsz:
                try:
                    batch.append(next(it))
                except StopIteration:
                    exhausted = True
            if batch:
                yield batch


class ShuffleIterator(Iterable[Any], Sized):
    r"""Iterator that shuffles a sequence of items before iterating.

    When ``key`` is not given, this iterator performs ordinary shuffling using
    `random.shuffle`. Otherwise, a noisy sorting is performed. The items are
    sorted ascending by the value of the given key, plus some random noise
    :math:`\epsilon \sim` Uniform :math:`(-z, z)`, where :math:`z` equals ``scale``
    times the standard deviation of key values. This formulation means that ``scale``
    regulates how noisy the sorting is. The larger it is, the more noisy the sorting
    becomes, i.e. it resembles random shuffling more closely. In an extreme case
    where ``scale=0``, this method just sorts the items by ``key``. This method is
    useful when working with text data, where we want to shuffle the dataset and also
    minimize padding by ensuring that sentences of similar lengths are not too far apart.

    Example:

        >>> from random import Random
        >>> from text2array import ShuffleIterator
        >>> samples = [
        ...   {'ws': ['a', 'b', 'b']},
        ...   {'ws': ['a']},
        ...   {'ws': ['a', 'a', 'b', 'b', 'b', 'b']},
        ... ]
        >>> iter_ = ShuffleIterator(samples, key=lambda s: len(s['ws']), rng=Random(1234))
        >>> for s in iter_:
        ...   print(s)
        ...
        {'ws': ['a']}
        {'ws': ['a', 'a', 'b', 'b', 'b', 'b']}
        {'ws': ['a', 'b', 'b']}

    Args:
        items (~typing.Sequence[Any]): Sequence of items to shuffle and iterate over.
        key (typing.Callable[[Any], int]): Callable to get the key value of an item.
        scale: Value to regulate the noise of the sorting. Must not be negative.
        rng: Random number generator to use for shuffling. Set this to ensure reproducibility.
            If not given, an instance of `~random.Random` with the default seed is used.
    """

    def __init__(
        self,
        items: Sequence[Any],
        key: Optional[Callable[[Any], int]] = None,
        scale: float = 1.0,
        rng: Optional[Random] = None,
    ) -> None:
        if scale < 0:
            raise ValueError("scale cannot be less than 0")
        if rng is None:  # pragma: no cover
            rng = Random()

        self._items = items
        self._key = key
        self._scale = scale
        self._rng = rng

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Sample]:
        if self._key is None:
            self._shuffle()
        else:
            self._shuffle_by_key()
        return iter(self._items)

    def _shuffle(self) -> None:
        self._items = list(self._items)
        self._rng.shuffle(self._items)

    def _shuffle_by_key(self) -> None:
        assert self._key is not None

        std = stat.stdev(self._key(s) for s in self._items)
        z = self._scale * std

        noises = [self._rng.uniform(-z, z) for _ in range(len(self._items))]
        indices = list(range(len(self._items)))
        indices.sort(key=lambda i: self._key(self._items[i]) + noises[i])  # type: ignore
        shuf_items = [self._items[i] for i in indices]

        self._items = shuf_items


class BucketIterator(Iterable[Batch], Sized):
    """Iterator that batches together samples from the same bucket.

    Example:

        >>> from text2array import BucketIterator
        >>> samples = [
        ...   {'ws': ['a']},
        ...   {'ws': ['a', 'b']},
        ...   {'ws': ['b']},
        ...   {'ws': ['c']},
        ...   {'ws': ['b', 'b']},
        ... ]
        >>> iter_ = BucketIterator(samples, key=lambda s: len(s['ws']), batch_size=2)
        >>> for b in iter_:
        ...   print(list(b))
        ...
        [{'ws': ['a']}, {'ws': ['b']}]
        [{'ws': ['c']}]
        [{'ws': ['a', 'b']}, {'ws': ['b', 'b']}]

    Args:
        samples (~typing.Iterable[Sample]): Iterable of samples to batch.
        key (typing.Callable[[Sample], Any]): Callable to get the bucket key of a sample.
        batch_size: Maximum number of samples in each batch.
        shuffle_bucket: Whether to shuffle every bucket before batching.
        rng: Random number generator to use for shuffling. Set this to ensure reproducibility.
            If not given, an instance of `~random.Random` with the default seed is used.

    Note:
        When ``samples`` is an instance of `~typing.Sized`, this iterator can
        be passed to `len` to get the number of batches. Otherwise, a `TypeError`
        is raised.
    """

    def __init__(
        self,
        samples: Iterable[Sample],
        key: Callable[[Sample], Any],
        batch_size: int = 1,
        shuffle_bucket: bool = False,
        rng: Optional[Random] = None,
    ) -> None:
        if rng is None:  # pragma: no cover
            rng = Random()

        self._bsz = batch_size
        self._shuf = shuffle_bucket
        self._rng = rng

        bucket_dict = defaultdict(list)
        for s in samples:
            bucket_dict[key(s)].append(s)
        self._buckets = bucket_dict.values()

    @property
    def batch_size(self):
        return self._bsz

    def __len__(self):
        return sum(len(BatchIterator(ss, self._bsz)) for ss in self._buckets)

    def __iter__(self):
        for ss in self._buckets:
            if self._shuf:
                self._rng.shuffle(ss)
            yield from BatchIterator(ss, self._bsz)
