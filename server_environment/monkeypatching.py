# Copyright 2025 Dynapps - Eric Lembregts
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.orm import model_classes

add_to_registry_original = model_classes.add_to_registry


def add_to_registry(registry, model_def):
    model_cls = add_to_registry_original(registry, model_def)
    if hasattr(model_cls, "_build_model"):
        model_cls._build_model()
    return model_cls


# Monkey-patching of the method
model_classes.add_to_registry = add_to_registry
