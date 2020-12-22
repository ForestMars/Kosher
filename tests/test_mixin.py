import mixin


def test_mixin():
    kpm = mixin.KosherPickleMixin()

    assert isinstance(kpm, mixin.KosherPickleMixin), "Class instantiation test."


def test_encrypted_obj_type():
    payload = "I heard you liked writing tests."
    secret = 'supersecret'

    kpm = mixin.KosherPickleMixin()
    encrypted = kpm.encrypt(payload, secret, 'AES')
    assert isinstance(encrypted, bytes), "Check encrypted object type"

    kpm = mixin.KosherPickleMixin()
    encrypted = kpm.encrypt(payload, secret, 'Fernet')
    assert isinstance(encrypted, bytes), "Check encrypted object type"


def test_decrypted_obj_type():
    payload = "I heard you liked writing tests."
    secret = 'supersecret'

    kpm = mixin.KosherPickleMixin()
    encrypted = kpm.encrypt(payload, secret, 'AES')
    decrypted = kpm.decrypt(encrypted, secret, 'AES')
    assert type(payload) == type(decrypted)

    kpm = mixin.KosherPickleMixin()
    encrypted = kpm.encrypt(payload, secret, 'Fernet')
    decrypted = kpm.decrypt(encrypted, secret, 'Fernet')
    assert type(payload) == type(decrypted)


def test_decrypted_obj_value():
    payload = "I heard you liked writing tests."
    secret = 'supersecret'

    kpm = mixin.KosherPickleMixin()
    encrypted = kpm.encrypt(payload, secret, 'AES')
    decrypted = kpm.decrypt(encrypted, secret, 'AES')
    assert payload == decrypted

    kpm = mixin.KosherPickleMixin()
    encrypted = kpm.encrypt(payload, secret, 'Fernet')
    decrypted = kpm.decrypt(encrypted, secret, 'Fernet')
    assert payload == decrypted
