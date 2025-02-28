{ domain, https, pkgs, dataDir }:
let
  proxyConf = {
    extraConfig = ''
      proxy_connect_timeout       600;
      proxy_send_timeout          600;
      proxy_read_timeout          600;
      send_timeout                600;
      proxy_set_header Host     $host;
      proxy_set_header      X-Forwarded-Proto $scheme;
      proxy_set_header      X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_redirect        off;
    '';
    proxyPass = "http://localhost:7000/";
  };
in {
  enable = true;
  statusPage = true;

  virtualHosts = {
    "${domain}" = {
      enableACME = https;
      forceSSL = https;
      locations = {
        "/" = proxyConf;
        "/static/" = { alias = "${dataDir}/static/"; };
      };
    };
  };
}
