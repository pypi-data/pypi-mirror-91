from __future__ import unicode_literals

from django.db import transaction
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django_anysign import api as django_anysign

from django_adobesign.exceptions import AdobeSignException


class SignerReturnView(SingleObjectMixin, RedirectView):
    """Handle return of signer on project after document signing/reject.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """Route request to signer return view depending on status.
        Trigger events for latest signer: calls
        ``signer_{status}`` methods.

        Adobe signer status:
        - COMPLETED: everybody has signed
        - WAITING_FOR_OTHERS: the signer has already signed
        - NOT_YET_VISIBLE: the signer signing url is not generated yet,
                           it is not his turn to sign
        - WAITING_FOR_MY_SIGNATURE: the user signing url is generated, it is
                                    his turn to sign
        - CANCELLED: the user has refused to sign
        -  WAITING_FOR_AUTHORING, WAITING_FOR_MY_DELEGATION
            WAITING_FOR_MY_ACCEPTANCE, WAITING_FOR_MY_ACKNOWLEDGEMENT
            WAITING_FOR_MY_APPROVAL, WAITING_FOR_MY_FORM_FILLING
        """

        signer = self.get_current_signer()
        if not signer:
            return self.get_signer_error_url('No more signer')
        agreement_id = self.signature.signature_backend_id
        adobe_signer_id = signer.signature_backend_id
        status = self.backend.get_signer_status(agreement_id, adobe_signer_id)
        if status == 'WAITING_FOR_MY_SIGNATURE':
            return self.get_signer_error_url('User mismatch')
        if status == 'CANCELLED':
            self.signer_cancelled(signer, status)
            return self.get_signer_canceled_url(status)

        if status == 'COMPLETED':
            if not self.backend.is_last_signer(signer):
                raise AdobeSignException('Consistency issue, agreement {} '
                                         'is complete, remaining signers have '
                                         'been found'.format(agreement_id))
            self.signer_signed(status, signer)
            self.update_signature(status)
            return self.get_signer_signed_url(status)
        if status == 'WAITING_FOR_OTHERS':
            self.signer_signed(status, signer)
            return self.get_signer_signed_url(status)

        self.update_signer(signer, status)
        return self.get_signer_error_url()

    def get_current_signer(self):
        for signer in self.signature.signers.all().order_by('signing_order'):
            if not self.has_already_signed(signer):
                return signer

    def get_queryset(self):
        model = django_anysign.get_signature_model()
        return model.objects.all()

    def get_signed_document(self):
        # In our model, there is only one doc.
        return next(
            self.backend.get_documents(self.signature.signature_backend_id))

    def signer_cancelled(self, signer,  status):
        """Handle 'Cancel' status for signer."""
        self.update_signer(signer=signer, status=status)
        self.update_signature(status=status)

    def signer_signed(self, status, signer):
        """ Update signer status after he sign
        """
        # download signed document out of the atomic block
        signed_document = self.get_signed_document()
        with transaction.atomic():
            self.replace_document(signed_document)
            self.update_signer(signer, status)

    @property
    def signature(self):
        """Signature model instance.

        This is a shortcut property using a cache.
        If you want to adapt the implementation, consider overriding
        :meth:`get_signature`.

        """
        try:
            return self._signature
        except AttributeError:
            self._signature = self.get_object()
            return self._signature

    @property
    def backend(self):
        try:
            return self._backend
        except AttributeError:
            self._backend = self.signature.signature_backend
            return self._backend

    def has_already_signed(self, signer):
        raise NotImplementedError()

    def get_signer_canceled_url(self, status):
        """Url redirect when signer canceled signature."""
        raise NotImplementedError()

    def get_signer_error_url(self, message=''):
        """Url redirect when failure."""
        raise NotImplementedError()

    def get_signer_signed_url(self, status):
        """Url redirect when signer signed signature."""
        raise NotImplementedError()

    def update_signature(self, status):
        """ Update signature with ``status``."""
        raise NotImplementedError()

    def update_signer(self, signer, status, message=''):
        """Update ``signer`` with ``status``."""
        raise NotImplementedError()

    def replace_document(self, signed_document):
        """Replace original document by signed one."""
        raise NotImplementedError()
