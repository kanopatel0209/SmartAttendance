from django.contrib.admin.utils import get_fields_from_path
from django.db import models
from django.contrib.admin.filters import (
  RelatedFieldListFilter,
  BooleanFieldListFilter,
  ChoicesFieldListFilter,
  DateFieldListFilter,
  AllValuesFieldListFilter
)



class RelatedGroupFilter(RelatedFieldListFilter):
  # template = 'listfilter/related_group_filter.html'
  pass


class ToggleBooleanFilter(BooleanFieldListFilter):
  # template = 'listfilter/toggle_boolean_filter.html'
  pass


class DropdownChoiceFilter(ChoicesFieldListFilter):
  template = 'listfilter/dropdown_choice_filter.html'


class DatePickerFilter(DateFieldListFilter):
  # template = 'listfilter/date_picker_filter.html'
  pass


class AllValuesFilter(AllValuesFieldListFilter):
  # template = 'listfilter/all_values_filter.html'
  pass




def check_filter_field(model, list_filter):
  new_list_filter = []

  field_list_filters = [
    (lambda f: f.remote_field, RelatedGroupFilter),
    (lambda f: isinstance(f, models.BooleanField), ToggleBooleanFilter),
    (lambda f: bool(f.choices), DropdownChoiceFilter),
    (lambda f: isinstance(f, models.DateField), DatePickerFilter),
    (lambda f: True, AllValuesFilter),
  ]

  for field in list_filter:
    if not (callable(field) or isinstance(field, (tuple, list))):
      model_field = get_fields_from_path(model, field)[-1]
      for test, list_filter_class in field_list_filters:
        if test(model_field):
          field = field, list_filter_class
          break
    new_list_filter.append(field)

  return new_list_filter

