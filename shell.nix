with import <nixpkgs> { };

let
  sources = import ./nix/sources.nix;
  scripts = import ./nix/scripts.nix { };
  overrides = sources.poetry2nix.overrides.withDefaults
    (import ./nix/overrides.nix { inherit pkgs lib; });
  pythonEnv = sources.poetry2nix.mkPoetryEnv {
    python = python311;
    pyproject = ./pyproject.toml;
    poetrylock = ./poetry.lock;
    overrides = overrides;
    preferWheels = true;
    groups = [ ];
    checkGroups = [ ];
  };
in mkShell {
  buildInputs = [ poetry  ] ++ scripts; # pythonEnv

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ]}
  '';
}
