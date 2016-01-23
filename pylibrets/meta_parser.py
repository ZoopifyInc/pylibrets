"""
Metadata Parser classes - .
"""
from xml.etree import ElementTree

from .models import (
	RetsResource, RetsClass, RetsField, RetsLookup,
	RetsLookupType, RetsObject
)

class MetaParser(object):
	def get_all_resource(self):
		pass

	def get_resource(self, resource_id):
		pass

	def get_all_class(self, resource_id):
		pass

	def get_class(self, resource_id, class_name):
		pass

	def get_all_field(self, resource_id, class_name):
		pass

	def get_field(self, resource_id, class_name, field_system_name):
		pass

	def get_all_lookup(self, resource_id, class_name, field_system_name):
		pass

	def get_lookup(self, resource_id, class_name, field_system_name, lookup_name):
		pass

	def get_all_lookup_type(self, resource_id, lookup_name):
		pass


class StandardXmlMetaParser(MetaParser):
	def __init__(self, xml_str):
		self.meta_xml = ElementTree.fromstring(xml_str)

	def get_all_resource(self):
		resource_list = []
		resource_xml_list = self._get_all_resource_xml()
		for resource_xml in resource_xml_list:
			resource = RetsResource()
			resource.resource_id = resource_xml.find('ResourceID').text
			resource.standard_name = resource_xml.find('StandardName').text
			resource.key_field = resource_xml.find('KeyField').text
			resource_list.append(resource)
		return resource_list

	def get_resource(self, resource_id):
		resource_list = self.get_all_resource()
		for resource in resource_list:
			if resource.resource_id == resource_id:
				return resource

	def get_all_class(self, resource_id):
		class_list = []
		class_xml_list = self._get_all_class_xml(resource_id)
		for class_xml in class_xml_list:
			rets_class = RetsClass()
			rets_class.class_name = class_xml.find('ClassName').text
			rets_class.standard_name = class_xml.find('StandardName').text
			rets_class.description = class_xml.find('Description').text
			class_list.append(rets_class)
		return class_list

	def get_class(self, resource_id, class_name):
		rets_class_list = self.get_all_class(resource_id)
		for rets_class in rets_class_list:
			if rets_class.class_name == class_name:
				return rets_class

	def get_all_field(self, resource_id, class_name):
		field_list = []
		field_xml_list = self._get_all_field_xml(resource_id, class_name)
		for field_xml in field_xml_list:
			rets_field = RetsField()
			rets_field.system_name = field_xml.find('SystemName').text
			rets_field.standard_name = field_xml.find('StandardName').text
			rets_field.long_name = field_xml.find('LongName').text
			rets_field.db_name = field_xml.find('DBName').text
			rets_field.max_length = field_xml.find('MaximumLength').text
			rets_field.data_type = field_xml.find('DataType').text
			rets_field.precision = field_xml.find('Precision').text
			rets_field.is_searchable = field_xml.find('Searchable').text
			rets_field.required = field_xml.find('Required').text
			rets_field.interpretation = field_xml.find('Interpretation').text
			rets_field.units = field_xml.find('Units').text
			rets_field.is_unique = field_xml.find('Unique').text
			rets_field.lookup_name = field_xml.find('LookupName').text
			field_list.append(rets_field)
		return field_list

	def get_field(self, resource_id, class_name, field_system_name):
		field_list = self.get_all_field(resource_id, class_name)
		for field in field_list:
			if field.system_name == field_system_name:
				return field

	def get_all_lookup(self, resource_id):
		lookup_list = []
		lookup_xml_list = self._get_all_lookup_xml(resource_id)
		if lookup_xml_list is not None:
			for lookup_xml in lookup_xml_list:
				lookup = RetsLookup()
				lookup.lookup_name = lookup_xml.find('LookupName').text
				lookup.visible_name = lookup_xml.find('VisibleName').text
				lookup_list.append(lookup)
		return lookup_list

	def get_lookup(self, resource_id, lookup_name):
		lookup_list = self.get_all_lookup(resource_id)
		for lookup in lookup_list:
			if lookup.lookup_name == lookup_name:
				return lookup

	def get_all_lookup_type(self, resource_id, lookup_name):
		lookup_list = []
		lookup_type_xml_list = self._get_all_lookup_type_xml(resource_id, lookup_name)
		for lookup_type_xml in lookup_type_xml_list:
			lookup_type = RetsLookupType()
			lookup_type.value = lookup_type_xml.find('Value').text
			lookup_type.long_value = lookup_type_xml.find('LongValue').text
			lookup_type.short_value = lookup_type_xml.find('ShortValue').text
			lookup_list.append(lookup_type)
		return lookup_list

	def get_all_object(self, resource_id):
		object_list = []
		object_xml_list = self._get_all_object_xml(resource_id)
		if object_xml_list is not None:
			for object_xml in object_xml_list:
				obj = RetsObject()
				obj.object_type = object_xml.find('ObjectType').text
				obj.standard_name = object_xml.find('StandardName').text
				obj.mime_type = object_xml.find('MimeType').text
				obj.description = object_xml.find('Description').text
				object_list.append(obj)
		return object_list

	def _get_resource_xml(self, resource_id):
		resource_xml_list = self._get_all_resource_xml()
		for resource_xml in resource_xml_list:
			if resource_id == resource_xml.find('ResourceID').text:
				return resource_xml

	def _get_all_resource_xml(self):
		resource_xml_list = self.meta_xml.find('METADATA').find('METADATA-SYSTEM').find('System').find('METADATA-RESOURCE').findall('Resource')
		return resource_xml_list

	def _get_all_class_xml(self, resource_id):
		resource_xml = self._get_resource_xml(resource_id)
		return resource_xml.find('METADATA-CLASS').findall('Class')

	def _get_class_xml(self, resource_id, class_name):
		class_xml_list = self._get_all_class_xml(resource_id)
		for class_xml in class_xml_list:
			if class_name == class_xml.find('ClassName').text:
				return class_xml

	def _get_all_field_xml(self, resource_id, class_name):
		class_xml = self._get_class_xml(resource_id, class_name)
		return class_xml.find('METADATA-TABLE').findall('Field')

	def _get_field_xml(self, resource_id, class_name, field_system_name):
		field_xml_list = self._get_all_field_xml(resource_id, class_name)
		for field_xml in field_xml_list:
			if field_system_name == field_xml.find('SystemName').text:
				return field_xml

	def _get_all_lookup_xml(self, resource_id):
		resource_xml = self._get_resource_xml(resource_id)
		try:
			return resource_xml.find('METADATA-LOOKUP').findall('LookupType')
		except:
			return None

	def _get_lookup_xml(self, resource_id, lookup_name):
		lookup_xml_list = self._get_all_lookup_xml(resource_id)
		for lookup_xml in lookup_xml_list:
			if lookup_name == lookup_xml.find('LookupName').text:
				return lookup_xml

	def _get_all_lookup_type_xml(self, resource_id, lookup_name):
		lookup_xml = self._get_lookup_xml(resource_id, lookup_name)
		return lookup_xml.find('METADATA-LOOKUP_TYPE').findall('Lookup')

	def _get_all_object_xml(self, resource_id):
		resource_xml = self._get_resource_xml(resource_id)
		try:
			return resource_xml.find('METADATA-OBJECT').findall('Object')
		except:
			return None