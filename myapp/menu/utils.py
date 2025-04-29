def build_menu_tree(items, active_url):
    if not items: 
        return []

    tree = []
    lookup = {}

    for item in items:
        if not hasattr(item, 'id'):  
            continue
            
        item.children_items = []  
        item.url_resolved = getattr(item, 'get_absolute_url', lambda: '#')() 
        item.active = str(item.url_resolved) == str(active_url) 
        item.open = False
        lookup[item.id] = item

    for item in items:
        if not hasattr(item, 'parent_id'):
            continue
            
        if item.parent_id and item.parent_id in lookup:
            parent = lookup[item.parent_id]
            parent.children_items.append(item)
        elif item.parent_id is None:  
            tree.append(item)

    def mark_active(item):
        if getattr(item, 'active', False):
            return True
            
        for child in getattr(item, 'children_items', []):
            if mark_active(child):
                item.open = True
                return True
        return False

    for item in tree:
        mark_active(item)

    return tree