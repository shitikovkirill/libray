{ pkgs ? import <nixpkgs> { } }:

let
  sources = import ./nix/sources.nix;
  overrides = sources.poetry2nix.overrides.withDefaults
    (import ./nix/overrides.nix {
      pkgs = pkgs;
      lib = pkgs.lib;
    });
    app = sources.poetry2nix.mkPoetryApplication {
      python = pkgs.python311;
      src = pkgs.lib.cleanSource ./.;
      pyproject = ./pyproject.toml;
      poetrylock = ./poetry.lock;
      overrides = overrides;
      preferWheels = true;
      groups = [ ];
      checkGroups = [ ];
    };
in app.dependencyEnv
