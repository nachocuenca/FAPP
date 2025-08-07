import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def export_csv(queryset, fields, filename="export.csv"):
    """Generate a CSV HttpResponse for the given queryset.

    Args:
        queryset (Iterable): Django queryset or list of objects.
        fields (Iterable): Field names or (attribute, header) tuples.
        filename (str): Name for the downloaded file.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=\"{filename}\""
    writer = csv.writer(response)
    headers = [field[1] if isinstance(field, (tuple, list)) else field for field in fields]
    writer.writerow(headers)
    for obj in queryset:
        row = []
        for field in fields:
            attr = field[0] if isinstance(field, (tuple, list)) else field
            value = getattr(obj, attr)
            row.append(value)
        writer.writerow(row)
    return response


def export_pdf(template_path, context, filename="export.pdf"):
    """Render a template to PDF using xhtml2pdf."""
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=\"{filename}\""
    pisa.CreatePDF(html, dest=response)
    return response


def render_html(template_path, context):
    """Render a template for HTML printing."""
    template = get_template(template_path)
    return HttpResponse(template.render(context))
