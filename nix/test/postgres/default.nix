{ config, pkgs, lib, ... }:
let
  secrets = import ../../secrets/common/third-party/postgres;
  package = builtins.fetchGit {
    url = "https://git.webwave.work/Nix/postgres.git";
    rev = "2f5f6e5fc2e63c79bf4638ea053ac202d961a2bf";
  };
in with secrets; {
  imports = [ "${package}" ];

  services.devPostgres = {
    enable = true;
    users = [{
      user = "application";
      database = "application";
      password = "Qwerty123";
    }];
  };

  networking.hosts = { "127.0.0.1" = [ "db.local" ]; };
}
