{ pkgs ? import <nixpkgs> { }, lib ? pkgs.lib, stdenv ? pkgs.stdenv }:

self: super:

{
  drf-access-policy = super.drf-access-policy.overridePythonAttrs
    (old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ]; });
}
