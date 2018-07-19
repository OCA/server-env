# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from functools import partialmethod

from lxml import etree

from odoo import api, fields, models
from ..serv_config import serv_config

_logger = logging.getLogger(__name__)


class ServerEnvMixin(models.AbstractModel):
    """Mixin to add server environment in existing models

    Usage::

        class StorageBackend(models.Model):
            _name = "storage.backend"
            _inherit = ["storage.backend", "server.env.mixin"]

            @property
            def _server_env_fields(self):
                return {"directory_path": {'getter': 'get'}}

    With the snippet above, the "storage.backend" model now uses a server
    environment configuration for the field ``directory_path``.

    Under the hood, this mixin automatically replaces the original field
    by an env-computed field that reads from the configuration files.

    By default, it looks for the configuration in a section named
    ``[model_name.Record Name]`` where ``model_name`` is the ``_name`` of the
    model with ``.`` replaced by ``_``. Then in a global section which is only
    the name of the model. They can be customized by overriding the method
    :meth:`~_server_env_section_name` and
    :meth:`~_server_env_global_section_name`.

    For each field transformed to an env-computed field, a companion field
    ``<field>_env_default`` is automatically created. When it's value is set
    and the configuration files do not contain a key, the env-computed field
    uses the default value stored in database. If a key is empty, the
    env-computed field has an empty value.

    Env-computed fields are conditionally editable, based on the absence
    of their key in environment configuration files. When edited, their
    value is stored in the database.
    """
    _name = 'server.env.mixin'

    server_env_defaults = fields.Serialized()

    @property
    def _server_env_fields(self):
        """Dict of fields to replace by fields computed from env

        To override in models. The dictionary is:
        {'name_of_the_field': options}

        Where ``options`` is a dictionary::

            options = {
                "getter": "getint",
            }

        The configparser getter can be one of: get, getbool, getint.
        If options is an empty dict, "get" is used.

        Example::

            @property
            def _server_env_fields(self):
                base_fields = super()._server_env_fields
                sftp_fields = {
                    "sftp_server": {
                        "getter": "get",
                    },
                    "sftp_port": {
                        "getter": "getint",
                    },,
                    "sftp_login": {},
                    "sftp_password": {},
                }
                sftp_fields.update(base_fields)
                return sftp_fields
        """
        return {}

    @api.multi
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        self.ensure_one()
        return self._name.replace(".", "_")

    @api.multi
    def _server_env_section_name(self):
        """Name of the section in the configuration files

        Can be customized in your model
        """
        self.ensure_one()
        return ".".join(
            (self._name.replace(".", "_"), self.name)
        )

    @api.multi
    def _server_env_read_from_config(self, field_name, config_getter):
        self.ensure_one()
        global_section_name = self._server_env_global_section_name()
        section_name = self._server_env_section_name()
        try:
            # at this point we should have checked that we have a key with
            # _server_env_has_key_defined so we are sure that the value is
            # either in the global or the record config
            getter = getattr(serv_config, config_getter)
            if (section_name in serv_config
                    and field_name in serv_config[section_name]):
                value = getter(section_name, field_name)
            else:
                value = getter(global_section_name, field_name)
        except:
            _logger.exception(
                "error trying to read field %s in section %s",
                field_name,
                section_name,
            )
            return False
        return value

    @api.multi
    def _server_env_has_key_defined(self, field_name):
        self.ensure_one()
        global_section_name = self._server_env_global_section_name()
        section_name = self._server_env_section_name()
        has_global_config = (
            global_section_name in serv_config
            and field_name in serv_config[global_section_name]
        )
        has_config = (
            section_name in serv_config
            and field_name in serv_config[section_name]
        )
        return has_global_config or has_config

    @api.multi
    def _compute_server_env(self):
        """Read values from environment configuration files

        If an env-computed field has no key in configuration files,
        read from the ``<field>_env_default`` field from database.
        """
        for record in self:
            for field_name, options in self._server_env_fields.items():
                if record._server_env_has_key_defined(field_name):
                    getter_name = options.get('getter', 'get')
                    value = record._server_env_read_from_config(
                        field_name, getter_name
                    )

                else:
                    default_field = record._server_env_default_fieldname(
                        field_name
                    )
                    value = record[default_field]

                record[field_name] = value

    def _inverse_server_env(self, field_name):
        default_field = self._server_env_default_fieldname(field_name)
        is_editable_field = self._server_env_is_editable_fieldname(field_name)
        for record in self:
            # when we write in an env-computed field, if it is editable
            # we update the default value in database

            if record[is_editable_field]:
                record[default_field] = record[field_name]

    @api.multi
    def _compute_server_env_is_editable(self):
        """Compute <field>_is_editable values

        We can edit an env-computed filed only if there is no key
        in any environment configuration file. If there is an empty
        key, it's an empty value so we can't edit the env-computed field.
        """
        # we can't group it with _compute_server_env otherwise when called
        # in ``_inverse_server_env`` it would reset the value of the field
        for record in self:
            for field_name in self._server_env_fields:
                is_editable_field = self._server_env_is_editable_fieldname(
                    field_name
                )
                is_editable = not record._server_env_has_key_defined(
                    field_name
                )
                record[is_editable_field] = is_editable

    def _server_env_view_set_readonly(self, view_arch):
        field_xpath = './/field[@name="%s"]'
        for field in self._server_env_fields:
            is_editable_field = self._server_env_is_editable_fieldname(field)
            for elem in view_arch.findall(field_xpath % field):
                # set env-computed fields to readonly if the configuration
                # files have a key
                elem.set('attrs',
                         str({'readonly': [(is_editable_field, '=', False)]}))
            if not view_arch.findall(field_xpath % is_editable_field):
                # add the _is_editable fields in the view for the 'attrs'
                # domain
                view_arch.append(
                    etree.Element(
                        'field',
                        name=is_editable_field,
                        invisible="1"
                    )
                )
        return view_arch

    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                         submenu=False):
        view_data = super()._fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu
        )
        view_arch = etree.fromstring(view_data['arch'].encode('utf-8'))
        view_arch = self._server_env_view_set_readonly(view_arch)
        view_data['arch'] = etree.tostring(view_arch, encoding='unicode')
        return view_data

    def _server_env_default_fieldname(self, base_field_name):
        """Return the name of the field with default value"""
        return '%s_env_default' % (base_field_name,)

    def _server_env_is_editable_fieldname(self, base_field_name):
        """Return the name of the field for "is editable

        This is the field used to tell if the env-computed field can
        be edited.
        """
        return '%s_env_is_editable' % (base_field_name,)

    def _server_env_transform_field_to_read_from_env(self, field):
        """Transform the original field in a computed field"""
        field.compute = '_compute_server_env'
        inverse_method_name = '_inverse_server_env_%s' % field.name
        inverse_method = partialmethod(
            ServerEnvMixin._inverse_server_env, field.name
        )
        setattr(ServerEnvMixin, inverse_method_name, inverse_method)
        field.inverse = inverse_method_name
        field.store = False
        field.required = False
        field.copy = False
        field.sparse = None
        field.prefetch = False

    def _server_env_add_is_editable_field(self, base_field):
        """Add a field indicating if we can edit the env-computed fields

        It is used in the inverse function of the env-computed field
        and in the views to add 'readonly' on the fields.
        """
        fieldname = self._server_env_is_editable_fieldname(base_field.name)
        if fieldname not in self._fields:
            field = fields.Boolean(
                compute='_compute_server_env_is_editable',
                automatic=True,
            )
            self._add_field(fieldname, field)

    def _server_env_add_default_field(self, base_field):
        """Add a field storing the default value

        The default value is used when there is no key for an env-computed
        field in the configuration files.

        The field is stored in the serialized field ``server_env_defaults``.
        """
        fieldname = self._server_env_default_fieldname(base_field.name)
        if fieldname not in self._fields:
            base_field_cls = base_field.__class__
            field_args = base_field.args.copy()
            field_args.pop('_sequence', None)
            field_args.update({
                'sparse': 'server_env_defaults',
                'automatic': True,
            })

            if hasattr(base_field, 'selection'):
                field_args['selection'] = base_field.selection
            field = base_field_cls(**field_args)
            self._add_field(fieldname, field)

    @api.model
    def _setup_base(self):
        super()._setup_base()
        for fieldname in self._server_env_fields:
            field = self._fields[fieldname]
            self._server_env_add_default_field(field)
            self._server_env_transform_field_to_read_from_env(field)
            self._server_env_add_is_editable_field(field)
