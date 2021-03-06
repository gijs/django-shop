# -*- coding: utf-8 -*-
from shop.backend_base import BaseBackendAPI, BaseBackend
from shop.models.ordermodel import ExtraOrderPriceField
from django.shortcuts import redirect

class ShippingBackendAPI(BaseBackendAPI):
    '''
    This object's purpose is to expose an API to the shop system.
    Ideally, shops (Django shop or others) should implement this API, so that
    shipping plugins are interchangeable between systems.
    
    This implementation is the interface reference for Django Shop
    
    Methods defined in BaseBackendAPI:
    getOrder(request): Return the Order object for the current shopper
    '''

    def add_shipping_costs(self, order, label, value):
        '''
        Add shipping costs to the given order, with the given label (text), and
        for the given value. 
        Please not that the value *should* be negative (it's a cost).
        '''
        ExtraOrderPriceField.objects.create(order=order, 
                                            label=label, 
                                            value=value,
                                            is_shipping=True)
        order.order_total = order.order_total + value
        order.save()
        

class BaseShippingBackend(BaseBackend):
    '''
    This is the base class for all shipping backends to implement.
    
    Class members:
    
    url_namespace 
    backend_name
    shop
    '''
    
    def __init__(self, shop=ShippingBackendAPI()):
        '''
        Make sure the shop helper is of the right type (shipping), then call 
        super
        '''
        self.shop = shop
        super(BaseShippingBackend, self).__init__()
        
    def finished(self):
        '''
        A helper for subclasses, so that they can call this when their job
        is finished i.e. shipping costs are added to the order.
        This will redirect to the "select a payment method" page.
        '''
        return redirect('checkout_payment')
