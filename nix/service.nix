{ config, lib, pkgs, project ? "application", ... }:
with lib;
let
  project = "application";
  user = project;
  group = project;
  cfg = config.services.djangoService;
  backend = import ../default.nix { };

  dataDir = "/var/lib/${project}";

  nginxConf = import ./nginx {
    domain = cfg.domain;
    https = cfg.https;
    pkgs = pkgs;
    dataDir = dataDir;
  };

in {

  options = {
    services.djangoService = {
      enable = mkOption {
        default = false;
        type = types.bool;
        description = ''
          Enable ${project} web service.
        '';
      };

      https = mkOption {
        default = false;
        description = ''
          Enable https.
        '';
      };

      domain = mkOption {
        type = types.str;
        description = "Domain";
      };

      environment = mkOption {
        type = types.attrs;
        default = { };
        description = ''
          Add environment to systemd
        '';
      };
    };
  };

  config = mkIf cfg.enable {

    services.nginx = nginxConf;

    networking.firewall.allowedTCPPorts = [
      80 # HTTP
      443 # HTTPs
    ];

    systemd.tmpfiles.rules =
      [ "d '${dataDir}' - ${user} ${config.users.users.${user}.group} - -" ];

    systemd.services.djangoService = {
      description = "Running ${project} service";
      wantedBy = [ "multi-user.target" ];
      after = [ "postgresql.service" ];
      environment = {
        DATA_DIR = dataDir;
        ALLOWED_HOSTS = cfg.domain;
        CSRF_TRUSTED_ORIGINS = "https://${cfg.domain}";

      } // cfg.environment;

      preStart = ''
        ${backend}/bin/python ${backend}/lib/python3.11/site-packages/library/manage.py migrate
        ${backend}/bin/python ${backend}/lib/python3.11/site-packages/library/manage.py collectstatic -c --no-input
      '';

      script = ''
        ${backend}/bin/gunicorn --chdir ${backend}/lib/python3.11/site-packages/library/ --bind 127.0.0.1:7000 library.wsgi
      '';

      serviceConfig = {
        User = user;
        Group = group;
      };
    };

    users.groups.${group} = { };
    users.users.${user} = {
      group = group;
      isSystemUser = true;
      home = dataDir;
    };
  };
}
