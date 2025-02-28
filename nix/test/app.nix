{ config, pkgs, lib, ... }:
let
  domain = "djangobook.local";
  secrets = import ./secrets.nix;
in {
  imports = [ ../service.nix ];

  services.djangoService = {
    enable = true;
    https = false;
    environment = secrets.environment;
    inherit domain;
  };

  networking.hosts = { "127.0.0.1" = [ domain ]; };
}
