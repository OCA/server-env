# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pathlib import Path

from lxml import etree

from odoo.addons.data_encryption.tests.common import CommonDataEncrypted


class TestServerEnvDataEncrypted(CommonDataEncrypted):
    def test_dynamic_view_current_env(self):
        self.maxDiff = None
        self.set_new_key_env("prod")
        self.set_new_key_env("preprod")
        mixin_obj = self.env["server.env.mixin"]
        base_path = Path(__file__).parent / "fixtures" / "base.xml"
        xml_str = base_path.read_text()
        xml = etree.XML(xml_str)
        res_xml = mixin_obj._update_form_view_from_env(xml, "form")
        expected_xml_path = Path(__file__).parent / "fixtures" / "res1.xml"
        expected_xml = expected_xml_path.read_text()
        # convert both to xml with parser removing space then convert to string to
        # compare
        parser = etree.XMLParser(remove_blank_text=True)
        res_xml_str = etree.tostring(etree.XML(etree.tostring(res_xml), parser=parser))
        expected_xml_str = etree.tostring(etree.XML(expected_xml, parser=parser))
        self.assertEqual(res_xml_str, expected_xml_str)

    def test_dynamic_view_other_env(self):
        self.maxDiff = None
        self.set_new_key_env("prod")
        self.set_new_key_env("preprod")
        mixin_obj = self.env["server.env.mixin"]
        base_path = Path(__file__).parent / "fixtures" / "base.xml"
        xml_str = base_path.read_text()
        xml = etree.XML(xml_str)
        res_xml = mixin_obj.with_context(environment="prod")._update_form_view_from_env(
            xml, "form"
        )
        expected_xml_path = Path(__file__).parent / "fixtures" / "res2.xml"
        expected_xml = expected_xml_path.read_text()
        # convert both to xml with parser removing space then convert to string to
        # compare
        parser = etree.XMLParser(remove_blank_text=True)
        res_xml_str = etree.tostring(etree.XML(etree.tostring(res_xml), parser=parser))
        expected_xml_str = etree.tostring(etree.XML(expected_xml, parser=parser))
        self.assertEqual(res_xml_str, expected_xml_str)
