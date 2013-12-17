from django.template import Library

register = Library()

@register.filter_function
def order_by(queryset, args):
    #Trim whitespace from each argument in args, a list of comma-separated arguments
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)