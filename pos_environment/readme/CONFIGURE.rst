* Open your module ``server_environment_files``

* In each environment folder, create a new file named ``pos_environment.conf``
  (for exemple)

* In each file, write a section like this one, depending on your environment

::

    [pos_environment_header]
    line_1 = ===============================
    line_2 = TICKET EDITED ON A TEST
    line_3 = ENVIRONMENT
    line_4 = ===============================

    [pos_environment_footer]
    line_1 = ===============================
    line_2 = THIS TICKET HAS BEEN EDITED
    line_3 = ON A TEST ENVIRONMENT
    line_4 = -------------------------------
    line_5 = IT CAN NOT BE CONSIDERED
    line_6 = AS A PROOF OF PURCHASE
    line_7 = ===============================
