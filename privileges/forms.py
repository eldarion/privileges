from django import forms

from privileges.models import Grant, grants


class GrantForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(GrantForm, self).__init__(*args, **kwargs)
        self.fields["grantee"].choices = [
            (x.pk, x)
            for x in grants.grantee_list(grantor=self.user)
        ]
        self.fields["privilege"].choices = [
            (x.pk, x.verbose_name)
            for x in grants.privilege_list(grantor=self.user)
        ]
    
    class Meta:
        model = Grant
        fields = [
            "grantee",
            "start",
            "end",
            "privilege"
        ]
    
    def save(self, commit=True):
        self.instance.grantor = self.user
        super(GrantForm, self).save(commit=commit)
