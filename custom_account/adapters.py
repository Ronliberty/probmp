from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Overrides the default save_user method to save additional fields (phone_number, country).
        """
        user = super().save_user(request, user, form, commit=False)  # Save user without commit

        # Save additional fields from the signup form
        user.phone_number = form.cleaned_data.get('phone_number', '')
        user.country = form.cleaned_data.get('country', '')

        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Overrides the social login save process to store additional fields.
        """
        user = super().save_user(request, sociallogin, form)

        # Extract social account data (Google, etc.)
        extra_data = sociallogin.account.extra_data
        user.country = extra_data.get('locale', '')  # Google provides locale info
        user.phone_number = ''  # Google does not provide phone number

        user.save()
        return user
