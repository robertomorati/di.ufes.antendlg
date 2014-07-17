# -*- coding: utf-8 -*-
'''
Created on 18/09/2013

@author: Roberto
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from editor_objetos.models import TipoObjeto,Autor


class AutorInline(admin.TabularInline):
    model = Autor

class UserAdmin(DjangoUserAdmin):
    inlines = (AutorInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
''''
class Calc(DjangoUserAdmin):
    inlines = (AutorInline,)

admin.site.unregister(CalcClass)
admin.site.register(CalcClass, Calc)
'''

class TipoObjetoAdmin(admin.ModelAdmin):
    pass

admin.site.register(TipoObjeto, TipoObjetoAdmin)



'''
Código Antigo
'''
'''
class TipoObjetoAdmin(admin.ModelAdmin):
    pass

admin.site.register(TipoObjeto, TipoObjetoAdmin)

class ObjetoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Objeto, ObjetoAdmin)

'''
'''
class TipoObjetoAdmin(admin.ModelAdmin):
    pass

admin.site.register(TipoObjeto, TipoObjetoAdmin)

class TipoObjetoAdmin(admin.ModelAdmin):
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(TipoObjetoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 photoblog entry was"
        else:
            message_bit = "%s photoblog entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"

admin.site.register(TipoObjeto, TipoObjetoAdmin)
'''