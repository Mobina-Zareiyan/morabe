# Third Party Packages
from unfold.widgets import (
    UnfoldAdminTextInputWidget,
    UnfoldAdminFileFieldWidget,
)


class NumberInput(UnfoldAdminTextInputWidget):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        try:
            # Try to remove commas and convert to int
            return int(value.replace(',', '')) if ',' in value else int(value)
        except (TypeError, ValueError):
            return value

    def render(self, name, value, attrs=None, renderer=None):
        try:
            value = int(value)
        except (TypeError, ValueError):
            pass  # Keep the original value if conversion fails
        try:
            return super().render(name, '{:,}'.format(value) if value is not None else '', attrs, renderer)
        except Exception:
            return super().render(name, value, attrs=attrs, renderer=renderer)


class ImagePreviewFileInput(UnfoldAdminFileFieldWidget):
    template_name = 'unfold_admin/widgets/image_preview_file_input.html'

    class Media:
        js = ('unfold_admin/widgets/js/image_widget.js',)
