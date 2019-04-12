In order to use this module properly, each environment should have their own encryption key
and the production environment should have the keys of all environments. 

Example : 
Development environment ::

  [options]
  running_env=dev
  encryption_key_dev=XXX

Pre-production environment ::

  [options]
  running_env=preprod
  encryption_key_preprod=YYY

Production environment ::

  [options]
  running_env=prod
  encryption_key_dev=XXX
  encryption_key_preprod=YYY
  encryption_key_prod=ZZZ

