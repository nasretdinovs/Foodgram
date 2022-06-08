from rest_framework import serializers


def check_value(value, klass=None):
    if not str(value).isdecimal():
        raise serializers.ValidationError(
            f'{value} должен содержать цифру'
        )
    if klass:
        obj = klass.objects.filter(id=value)
        if not obj:
            raise serializers.ValidationError(
                f'{value} не существует'
            )
        return obj[0]
