import qonversion.api_resources as api_resources

OBJECT_MAP = {
    api_resources.User.OBJECT_NAME: api_resources.user.User,
    api_resources.Entitlement.OBJECT_NAME: api_resources.entitlement.Entitlement,
    api_resources.Purchase.OBJECT_NAME: api_resources.purchase.Purchase,
    api_resources.Product.OBJECT_NAME: api_resources.product.Product,
    api_resources.Subscription.OBJECT_NAME: api_resources.subscription.Subscription,
    api_resources.Identity.OBJECT_NAME: api_resources.identity.Identity,
}
