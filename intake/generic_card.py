class GCBody:
    def __init__(self):
        self.title = None
        self.subtitle = None
        self.text = None
        self.badge_groups = None
        self.buttons = None
        self.card_link = None
    def __str__(self):
        body = ['<div class="card-body">']
        if self.title:
            body.append('<h1 class="card-title">%(title)s</h1>' % {'title': self.title})
        if self.subtitle:
            body.append('<h6 class="card-subtitle mb-2 text-muted">%(subtitle)s</h6>' % {'subtitle': self.subtitle})
        if self.text:
            body.append('<p class="card-text">%(text)s</p>' % {'text': self.text})
        if self.badge_groups:
            for badge_type, badges in self.badge_groups:
                for badge in badges:
                    body.append('<span class="badge badge-pill badge-%(badge_type)s">%(badge_text)s</span>' % {'badge_type': badge_type, 'badge_text': badge})
        if self.buttons:
            button_type, buttons = self.buttons
            for button in buttons:
                body.append('<button type="button" class="btn btn-%(button_type)s">%(button_text)s</button>' % {'button_type': button_type, 'button_text': button})
        if self.card_link:
            body.append('<a href="%(url)s" class="card-link">%(link_text)s</a>' % {'url': self.card_link[0], 'link_text': self.card_link[-1]})
        body.append('</div>')
        return '\n'.join(body)

class GCFooter:
    def __init__(self):
        self.badge_groups = None
        self.buttons = None
        self.card_link = None
        self.see_more = None
    def __str__(self):
        footer = ['<div class="card-footer">']
        if self.badge_groups:
            for badge_type, badges in self.badge_groups:
                for badge in badges:
                    footer.append('<span class="badge badge-pill badge-%(badge_type)s">%(badge_text)s</span>' % {'badge_type': badge_type, 'badge_text': badge})
        if self.buttons:
            button_type, buttons = self.buttons
            for button in buttons:
                footer.append('<button type="button" class="btn btn-%(button_type)s">%(button_text)s</button>' % {'button_type': button_type, 'button_text': button})
        if self.card_link:
            footer.append('<a href="%(url)s" class="card-link">%(link_text)s</a>' % {'url': self.card_link[0], 'link_text': self.footer.card_link[-1]})
        if self.see_more:
            footer.append('<a href="' + self.see_more + '" class="card-link">See more</a>')
            print(footer[-1])
        footer.append('</div>')
        return '\n'.join(footer)

class GenericCard:
    def __init__(self):
        self.body = GCBody()
        self.footer = GCFooter()
    def __str__(self):
        card = ['<div class="card">']
        card.append(str(self.body))
        card.append(str(self.footer))
        card.append('</div>')
        return '\n'.join(card)
