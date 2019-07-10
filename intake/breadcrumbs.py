class Breadcrumbs:
    def __init__(self):
        self.crumbs = []
        self.active = None
    def __str__(self):
        list_items = []
        list_items.append('<nav aria-label="breadcrumb">')
        list_items.append('<ol class="breadcrumb">')
        print('SC', self.crumbs)
        if self.crumbs:
            for model, field in self.crumbs:
                print(model)
                list_items.append('<li class="breadcrumb-item"><a href="{% url "' + model.__class__.__name__ + ':detail" ' + str(model.id) + ' %}">' + eval('model.%s' % field) + '</a></li>')
                # list_items.append('<li class="breadcrumb-item"><a href="{% url "%(url)s:detail" %(id)d %}">%(model)s</a></li>' % {
                #     'url': model.__class__.__name__,
                #     'model': model.name,
                #     'id': model.id,
                # })
            list_items.insert(0, '<li class="breadcrumb-item"><a href="{% url "home" %}">Home</a></li>')
        if self.active:
            list_items.append('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {'model': self.active})
        list_items.append('</ol>')
        list_items.append('</nav>')
        return '\n'.join(list_items)
