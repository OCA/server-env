# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.data_encryption.tests.common import CommonDataEncrypted
from pathlib import Path


class TestServerEnvDataEncrypted(CommonDataEncrypted):

    def test_dynamic_view_current_env(self):
        self.maxDiff = None
        self.set_new_key_env("prod")
        self.set_new_key_env("preprod")
        mixin_obj = self.env["server.env.mixin"]
        base_path = Path(__file__).parent / "fixtures" / "base.xml"
        xml = base_path.read_text()
        res_xml = mixin_obj._update_form_view_from_env(xml, "form")
        expected_xml_path = Path(__file__).parent / "fixtures" / "res1.xml"
        expected_xml = expected_xml_path.read_text()
        self.assertEqual(res_xml, expected_xml)

    def test_dynamic_view_other_env(self):
        self.set_new_key_env("prod")
        self.set_new_key_env("preprod")
        mixin_obj = self.env["server.env.mixin"]
        base_path = Path(__file__).parent / "fixtures" / "base.xml"
        xml = base_path.read_text()
        res_xml = mixin_obj.with_context(
            environment="prod"
        )._update_form_view_from_env(xml, "form")
        expected_xml_path = Path(__file__).parent / "fixtures" / "res2.xml"
        expected_xml = expected_xml_path.read_text()
        self.assertEqual(res_xml, expected_xml)
