import os
import importlib

def middleware(app, middleware_dir = "middleware"):
    if not os.path.exists("./" + middleware_dir):
        return
    middlewares = os.listdir("./" + middleware_dir)
    for middleware_path in middlewares:
        if not middleware_path.endswith(".py"):
            continue
        middleware_module_name = middleware_path.replace(".py", "")
        middleware_module_prefix = middleware_dir.replace("/", ".")
        middleware_module_path = f"{middleware_module_prefix}.{middleware_module_name}"
        middleware_module = importlib.import_module(middleware_module_path)

        middleware_class_name = middleware_module_name.replace("middleware", "Middleware")
        middleware_class_name = middleware_class_name[0].upper() + "".join(middleware_class_name[1:])

        middleware_class = getattr(middleware_module, middleware_class_name)
        app.add_middleware(middleware_class)

def router(app, router_dir = "router", router_instance_name="router"):
    if not os.path.exists("./" + router_dir):
        return
    router_files = os.listdir("./" + router_dir)
    for router_file in router_files:
        if not router_file.endswith(".py"):
            continue
        router_module_name = router_file.replace(".py", "")
        router_module_prefix = router_dir.replace("/", ".")
        router_module_path = f"{router_module_prefix}.{router_module_name}"
        router_module = importlib.import_module(router_module_path)        
        
        router_instance = getattr(router_module, router_instance_name)
        app.include_router(router_instance)

def import_keyfa(app):
    #import key core
    middleware(app, "keyfa/middleware")
    router(app, router_dir="keyfa/router")

    # import user modules
    middleware(app)    
    router(app)

