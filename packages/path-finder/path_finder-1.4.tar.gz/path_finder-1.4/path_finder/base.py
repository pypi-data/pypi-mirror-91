from pathlib import Path
from typing import List

import logging


logger = logging.getLogger(__name__)


class Finder:

    DEPTH_MAPPER = {
        0: "*",  # search only start_dir
        1: "*/*",  # search start_dir + its subdirs
        2: "*/*/*",  # etc..
        3: "*/*/*/*",
        4: "*/*/*/*/*",
        5: "*/*/*/*/*/*",
        6: "*/*/*/*/*/*/*",
    }

    def __init__(
        self,
        single_start_dir: Path = None,
        multi_start_dir: List[Path] = None,
        limit_depth: bool = True,
        depth: int = 0,
    ):
        """
        :param single_start_dir: Path:      One single path (=directory) from where the search starts.
        :param multi_start_dir: List[Path]: You can start your search from multiple paths directories.
        :param limit_depth: bool:           if False, then search all subdirs. If True then limit search to 'depth'.
        :param depth: int:                  nr of directories deep (recursively). E.g. depth=1? then only search in
                                            dir, all subdirs of dir
        Either choose single_start_dir or multi_start_dir
        """
        self.single_start_dir = single_start_dir
        self.multi_start_dir = multi_start_dir
        self.limit_depth = limit_depth
        self.depth = depth
        self.validate_finder_constructor()

    def validate_finder_constructor(self):
        # validate single_start_dir + multi_start_dir
        if (self.single_start_dir and self.multi_start_dir) or (
            not self.single_start_dir and not self.multi_start_dir
        ):
            raise AssertionError(f"use either single_start_dir or multi_start_dir")
        if self.single_start_dir:
            assert isinstance(
                self.single_start_dir, Path
            ), "single_start_dir must be a pathlib.Path"
            assert (
                self.single_start_dir.is_dir()
            ), f"single_start_dir {self.single_start_dir} does not exist"
        elif self.multi_start_dir:
            assert isinstance(
                self.multi_start_dir, list
            ), "multi_start_dir must be a list (with pathlib.Path)"
            none_path_objects = [
                x for x in self.multi_start_dir if not isinstance(x, Path)
            ]
            if none_path_objects:
                msg = "not all elements in multi_start_dir are of type pathlib.Path"
                if (
                    len(none_path_objects) < 4
                ):  # 4 is a bit random (just do not return too many paths..)
                    raise AssertionError(f"{msg} : {none_path_objects}")
                raise AssertionError(msg)
            none_existing_dirs = [x for x in self.multi_start_dir if not x.is_dir()]
            if none_existing_dirs:
                msg = "not all elements in multi_start_dir are existing directories"
                if (
                    len(none_existing_dirs) < 4
                ):  # 4 is a bit random (just do not return too many paths..)
                    raise AssertionError(f"{msg}: {none_existing_dirs}")
                raise AssertionError(msg)

        # validate depth + limit_depth
        assert isinstance(self.limit_depth, bool), f"limit_depth must be a bool"
        if self.depth and not self.limit_depth:
            raise AssertionError(
                f"depth={self.depth} is only possible with limit_depth=True"
            )
        if not self.limit_depth:
            return
        max_allowed_depth = max(self.DEPTH_MAPPER.keys())
        if not isinstance(self.depth, int) or not 0 <= self.depth <= max_allowed_depth:
            raise AssertionError(
                f"depth {self.depth} must be a int and in range: 0 <= depth <= {max_allowed_depth}"
            )
        logger.debug(
            f"search recursively with limit_depth=True with depth={self.depth}"
        )

    def _depth_to_startdir(self, path: Path, start_dir: Path) -> int:
        """Calculate the nr of parts (between slashes) in a relative path to start_dir.
        Returns 0 if path == start_dir,
        Returns 1 if path is a subdir of start_dir,
        etc..
        """
        try:
            parts = path.relative_to(start_dir).parts
            return len(parts) - 1
        except TypeError as err:
            raise AssertionError(
                f"path {path} could not related to start_dir {start_dir}, err={err}"
            )
