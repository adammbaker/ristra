from django import forms

# from intake.models import Families
#
# class FamilyForm(forms.ModelForm):
#     LANGUAGE_CHOICES = [
#         ('Latin', (
#                 ('portuguese', 'Brazilian/Portuguese'),
#                 ('spanish', 'Spanish'),
#             )
#         ),
#         ('Maya', (
#                 ('achi', 'Achi'),
#                 ('awakatek', 'Awakatek'),
#                 ('chorti', "Ch\'orti\'"),
#                 ('chuj', 'Chuj'),
#                 ('itza', "Itza\'"),
#                 ('ixil', 'Ixil'),
#                 ('jakaltek', 'Jakaltek'),
#                 ('kiche', "K\'iche\'"),
#                 ('kaqchiquel', 'Kaqchiquel'),
#                 ('mam', 'Mam'),
#                 ('mopan', 'Mopan'),
#                 ('poqomam', 'Poqomam'),
#                 ('poqomchi', "Poqomchi\'"),
#                 ('qanjobal', 'Q\'anjob\'al'),
#                 ('qeqchi', 'Q\'eqchi\''),
#                 ('sakapultek', 'Sakapultek'),
#                 ('sipakapense', 'Sipakapense'),
#                 ('tektitek', 'Tektitek'),
#                 ('tzutujil', 'Tz\'utujil'),
#                 ('upsantek', 'Upsantek'),
#                 ('other', 'Other'),
#             )
#         ),
#         ('other', 'Other'),
#     ]
#     language_spoken = forms.MultipleChoiceField(
#         help_text="Languages spoken",
#         choices=LANGUAGE_CHOICES,
#     )
#     class Meta:
#         model = Families
#         exclude = ['id']
