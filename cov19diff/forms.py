from django import forms

CHOICE = [
    ('C', '累計感染者数'),
    ('D', '死亡数'),
    ('R', '回復数'),
    ('A', '現在数'),
    ('DR', '死亡率'),
    ('RR', '回復率'),
    ('AR', '現在率')
]

class DailyStatusForm(forms.Form):
    day = forms.CharField(label='対象日', max_length=10)
    order = forms.ChoiceField(label='ソート順', choices=CHOICE)

    day.widget.attrs.update(size='12')
