{
  poetry2nix = import (fetchGit {
    url = "https://github.com/nix-community/poetry2nix.git";
    ref = "master";
    rev = "a0cbe913ce184bef7cd739f75ba5d123e1f41ef2";
  }) { };
}
