from rest_framework import serializers
import getch.models as m


class FollowSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='profile.pix.url')

    class Meta:
        model = m.Boo
        fields = ['id', 'profile']
        read_only_fields = fields


class BooSerializer(serializers.ModelSerializer):
# class IntlibSerializer(serializers.HyperlinkedModelSerializer):
    # followers = FollowerSerializer(source='followers', many=True)
    followers = FollowSerializer(many=True)
    followees = FollowSerializer(many=True)
    profile = serializers.CharField(source='profile.pix.url')

    class Meta:
        model = m.Boo
        fields = ['id', 'nick', 'text', 'followers', 'followees', 'profile'] #'__all__'
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    boos = BooSerializer(source='boo_set', many=True)

    class Meta:
        model = m.User
        fields = ['id', 'email', 'boo_selected', 'boos']
        read_only_fields = fields
