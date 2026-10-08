def global_context(request):
    """
    Global context processor for UNISSU:
    Provides cart badge count and safe user profile defaults.
    """
    cart_items_count = 0
    raw_cart = request.session.get('cart', {})
    if isinstance(raw_cart, dict):
        for item in raw_cart.values():
            if isinstance(item, dict):
                cart_items_count += item.get('quantity', 1)
            elif isinstance(item, int):
                cart_items_count += item
            else:
                cart_items_count += 1

    user = request.user
    if getattr(user, 'is_authenticated', False):
        try:
            profile = getattr(user, 'profile', None)
            if profile:
                user.full_name = profile.display_name
                user.phone_number = profile.phone_number or ''
                user.address = profile.address or ''
            else:
                user.full_name = user.get_full_name() or user.username
                user.phone_number = ''
                user.address = ''
        except Exception:
            user.full_name = getattr(user, 'username', '')
            user.phone_number = ''
            user.address = ''

    return {
        'cart_items_count': cart_items_count,
        'portal_name': 'UNISSU',
        'portal_institution': 'DMMMSU NLUC',
    }
