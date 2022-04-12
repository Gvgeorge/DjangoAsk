from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    '''
    Adds new get parameters to the url
    input context of an url with existing get parameters and a number of kwargs
    example input:
    url - /new/?search=and
    kwargs - {'page': 2}
    example output:
    /new/?search=and&page=2
    '''
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
